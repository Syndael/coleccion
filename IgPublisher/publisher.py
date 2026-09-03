#!/usr/bin/env python3
"""
IG Publisher — Publica en Instagram via Graph API oficial.
Sube imágenes a Cloudflare R2 para obtener URLs públicas.
Notifica por Telegram solo si hay novedades.
"""

import configparser
import logging
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

import boto3
import requests
from botocore.exceptions import ClientError
from PIL import Image, ImageDraw, ImageFilter, ImageOps

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.txt')
FONT_FILE = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

log = logging.getLogger('ig-publisher')
log.setLevel(logging.INFO)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
log.addHandler(h)


def load_cfg():
    cfg = configparser.RawConfigParser()
    if not os.path.exists(CONFIG_FILE):
        log.error("No se encontró config.txt")
        sys.exit(1)
    cfg.read(CONFIG_FILE)
    return cfg


def _fix_orientation(image_path):
    """Aplica la rotacion EXIF si existe y reescribe el archivo corregido."""
    try:
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        img.save(image_path, quality=95, subsampling=0)
        log.info(f"  Orientacion EXIF corregida: {os.path.basename(image_path)}")
        return True
    except Exception as e:
        log.warning(f"  No se pudo corregir orientacion EXIF: {e}")
        return False


# ── API helpers ────────────────────────────────────────────────────
def api_get(cfg, path):
    url = cfg.get('config', 'api_url').rstrip('/') + path
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log.error(f"GET {path}: {e}")
        return None


def api_post(cfg, path, data=None):
    url = cfg.get('config', 'api_url').rstrip('/') + path
    try:
        r = requests.post(url, json=data, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log.error(f"POST {path}: {e}")
        return None


def api_put(cfg, path, data=None):
    url = cfg.get('config', 'api_url').rstrip('/') + path
    try:
        r = requests.put(url, json=data, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log.error(f"PUT {path}: {e}")
        return None


def get_image_from_api(cfg, fichero_id):
    url = cfg.get('config', 'api_url').rstrip('/') + f'/api/fichero/id/{fichero_id}'
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        return r.content
    except Exception as e:
        log.error(f"  Descargando fichero {fichero_id}: {e}")
        return None


# ── Cloudflare R2 Storage ──────────────────────────────────────────
class R2Storage:
    def __init__(self, cfg):
        self.endpoint = cfg.get('config', 'r2_endpoint')
        self.bucket_name = cfg.get('config', 'r2_bucket')
        self.access_key = cfg.get('config', 'r2_access_key')
        self.secret_key = cfg.get('config', 'r2_secret_key')
        self.public_url = cfg.get('config', 'r2_public_url').rstrip('/')
        
        self.client = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='auto'
        )
    
    def upload_image(self, local_path, content_type='image/jpeg'):
        """Sube una imagen a R2 y retorna la URL pública."""
        filename = os.path.basename(local_path)
        key = f"ig-temp/{int(time.time())}_{filename}"
        
        try:
            with open(local_path, 'rb') as f:
                self.client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=f.read(),
                    ContentType=content_type
                )
            
            public_url = f"{self.public_url}/{key}"
            log.info(f"  Imagen subida a R2: {key}")
            return public_url, key
        except Exception as e:
            log.error(f"  Error subiendo a R2: {e}")
            return None, None
    
    def delete_object(self, key):
        """Elimina un objeto de R2."""
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            log.info(f"  Objeto eliminado de R2: {key}")
            return True
        except ClientError as e:
            log.warning(f"  Error eliminando de R2: {e}")
            return False


# ── Instagram Graph API ────────────────────────────────────────────
class InstagramGraphAPI:
    GRAPH_URL = "https://graph.facebook.com/v21.0"
    
    def __init__(self, cfg):
        self.access_token = cfg.get('config', 'ig_access_token')
        self.ig_user_id = cfg.get('config', 'ig_user_id')
        self.max_retries = 3
        self._token_valid = None
    
    def verify_token(self):
        """Verifica que el token de acceso es válido."""
        if self._token_valid is not None:
            return self._token_valid
        
        try:
            result = self._make_request(
                'me',
                params={'fields': 'id,name'},
                method='GET'
            )
            self._token_valid = True
            log.info(f"  Token IG válido para: {result.get('name', '?')}")
            return True
        except Exception as e:
            self._token_valid = False
            error_msg = str(e)
            if 'OAuthException' in error_msg or 'Invalid OAuth' in error_msg:
                log.error(f"  Token IG expirado o inválido: {error_msg}")
            else:
                log.error(f"  Error verificando token IG: {error_msg}")
            return False
    
    def _make_request(self, endpoint, params=None, method='POST'):
        """Realiza una petición a la Graph API con reintentos limitados."""
        url = f"{self.GRAPH_URL}/{endpoint}"
        
        if params is None:
            params = {}
        params['access_token'] = self.access_token
        
        for attempt in range(self.max_retries):
            try:
                if method == 'POST':
                    r = requests.post(url, data=params, timeout=60)
                else:
                    r = requests.get(url, params=params, timeout=60)
                
                r.raise_for_status()
                return r.json()
            except requests.exceptions.RequestException as e:
                log.warning(f"  Request falló (intento {attempt+1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                else:
                    raise
        
        return None
    
    def _wait_for_container(self, container_id, timeout=120):
        """Espera a que un container esté listo (FINISHED)."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                result = self._make_request(
                    container_id,
                    params={'fields': 'status_code,status'},
                    method='GET'
                )
                
                status = result.get('status_code', '')
                if status == 'FINISHED':
                    return True
                elif status == 'ERROR':
                    log.error(f"  Container error: {result.get('status', 'unknown')}")
                    return False
                
                time.sleep(2)
            except Exception as e:
                log.warning(f"  Error verificando container: {e}")
                time.sleep(2)
        
        log.error(f"  Timeout esperando container {container_id}")
        return False
    
    def _get_media_shortcode(self, media_id):
        """Obtiene el shortcode de un media publicado."""
        try:
            result = self._make_request(
                media_id,
                params={'fields': 'shortcode,permalink'},
                method='GET'
            )
            shortcode = result.get('shortcode', '')
            if not shortcode:
                permalink = result.get('permalink', '')
                if permalink:
                    import re
                    match = re.search(r'/p/([^/]+)/', permalink)
                    if match:
                        shortcode = match.group(1)
            return shortcode
        except Exception as e:
            log.warning(f"  Error obteniendo shortcode: {e}")
            return ''
    
    def publish_photo(self, image_url, caption=''):
        """Publica una foto simple."""
        try:
            # Paso 1: Crear container
            container = self._make_request(
                f"{self.ig_user_id}/media",
                params={
                    'image_url': image_url,
                    'caption': caption,
                    'media_type': 'IMAGE'
                }
            )
            
            container_id = container.get('id')
            if not container_id:
                return None, None, "No se recibió container_id"
            
            # Paso 2: Esperar a que esté listo
            if not self._wait_for_container(container_id):
                return None, None, "Container no finalizó"
            
            # Paso 3: Publicar
            result = self._make_request(
                f"{self.ig_user_id}/media_publish",
                params={'creation_id': container_id}
            )
            
            media_id = result.get('id')
            shortcode = result.get('shortcode', '')
            
            if not shortcode and media_id:
                shortcode = self._get_media_shortcode(media_id)
            
            log.info(f"  Foto publicada: media_id={media_id}, shortcode={shortcode}")
            return shortcode, media_id, None
            
        except Exception as e:
            return None, None, str(e)
    
    def publish_album(self, image_urls, caption=''):
        """Publica un álbum (carousel) con múltiples imágenes."""
        try:
            if len(image_urls) < 2:
                return self.publish_photo(image_urls[0], caption)
            
            # Paso 1: Crear containers hijos
            children_ids = []
            for image_url in image_urls[:10]:  # Máximo 10 imágenes
                container = self._make_request(
                    f"{self.ig_user_id}/media",
                    params={
                        'image_url': image_url,
                        'is_carousel_item': 'true'
                    }
                )
                
                child_id = container.get('id')
                if child_id:
                    children_ids.append(child_id)
            
            if not children_ids:
                return None, None, "No se pudieron crear containers hijos"
            
            # Paso 2: Esperar a que todos estén listos
            for child_id in children_ids:
                if not self._wait_for_container(child_id):
                    return None, None, f"Container hijo {child_id} no finalizó"
            
            # Paso 3: Crear container padre
            parent_container = self._make_request(
                f"{self.ig_user_id}/media",
                params={
                    'media_type': 'CAROUSEL',
                    'children': ','.join(children_ids),
                    'caption': caption
                }
            )
            
            parent_id = parent_container.get('id')
            if not parent_id:
                return None, None, "No se recibió parent_id"
            
            # Paso 4: Esperar a que el padre esté listo
            if not self._wait_for_container(parent_id):
                return None, None, "Container padre no finalizó"
            
            # Paso 5: Publicar
            result = self._make_request(
                f"{self.ig_user_id}/media_publish",
                params={'creation_id': parent_id}
            )
            
            media_id = result.get('id')
            shortcode = result.get('shortcode', '')
            
            if not shortcode and media_id:
                shortcode = self._get_media_shortcode(media_id)
            
            log.info(f"  Álbum publicado: media_id={media_id}, shortcode={shortcode}")
            return shortcode, media_id, None
            
        except Exception as e:
            return None, None, str(e)
    
    def publish_story(self, image_url=None, video_url=None):
        """Publica una story (imagen o video)."""
        try:
            params = {'media_type': 'STORIES'}
            
            if video_url:
                params['video_url'] = video_url
                if image_url:
                    params['thumb_offset'] = 0
            elif image_url:
                params['image_url'] = image_url
            else:
                return None, None, "Se requiere image_url o video_url"
            
            # Paso 1: Crear container
            container = self._make_request(
                f"{self.ig_user_id}/media",
                params=params
            )
            
            container_id = container.get('id')
            if not container_id:
                return None, None, "No se recibió container_id para story"
            
            # Paso 2: Esperar a que esté listo
            if not self._wait_for_container(container_id, timeout=180):
                return None, None, "Container de story no finalizó"
            
            # Paso 3: Publicar
            result = self._make_request(
                f"{self.ig_user_id}/media_publish",
                params={'creation_id': container_id}
            )
            
            media_id = result.get('id')
            shortcode = result.get('shortcode', '')
            
            if not shortcode and media_id:
                shortcode = self._get_media_shortcode(media_id)
            
            log.info(f"  Story publicada: media_id={media_id}, shortcode={shortcode}")
            return shortcode, media_id, None
            
        except Exception as e:
            return None, None, str(e)


# ── Token refresh ──────────────────────────────────────────────────
def refresh_ig_token(cfg):
    """Refresca el token de acceso de Instagram. Retorna (nuevo_token, expires_in) o (None, None)."""
    current_token = cfg.get('config', 'ig_access_token')
    
    try:
        url = "https://graph.instagram.com/refresh_access_token"
        params = {
            'grant_type': 'ig_refresh_token',
            'access_token': current_token
        }
        
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        
        new_token = data.get('access_token')
        expires_in = data.get('expires_in', 5184000)
        
        if new_token:
            log.info(f"  Token refrescado correctamente (válido {expires_in // 86400} días)")
            return new_token, expires_in
        else:
            log.error(f"  No se recibió nuevo token: {data}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        log.error(f"  Error refrescando token: {e}")
        return None, None


def update_token_in_config(new_token):
    """Actualiza el token en config.txt."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            content = f.read()
        
        import re
        content = re.sub(
            r'ig_access_token\s*=\s*[^\n]+',
            f'ig_access_token = {new_token}',
            content
        )
        
        with open(CONFIG_FILE, 'w') as f:
            f.write(content)
        
        log.info("  Token actualizado en config.txt")
        return True
    except Exception as e:
        log.error(f"  Error actualizando config.txt: {e}")
        return False


def try_refresh_token(cfg):
    """Intenta refrescar el token. Retorna True si tuvo éxito o no era necesario."""
    log.info("Verificando token de Instagram...")
    
    ig = InstagramGraphAPI(cfg)
    
    if ig.verify_token():
        log.info("  Token válido, no es necesario refrescar")
        return True
    
    log.warning("  Token inválido o expirado, intentando refrescar...")
    new_token, expires_in = refresh_ig_token(cfg)
    
    if new_token:
        if update_token_in_config(new_token):
            log.info("✓ Token refrescado y guardado")
            return True
        else:
            log.error("  Token refrescado pero no se pudo guardar en config.txt")
            return False
    else:
        log.error("  No se pudo refrescar el token")
        notify(cfg, "❌ Token de Instagram expirado y no se pudo refrescar.\n"
                    "Necesitas generar un nuevo token en Facebook Developers.")
        return False


# ── Instagram publishing functions ─────────────────────────────────
def publish_instagram(cfg, r2, image_paths, caption):
    """Publica foto(s) en Instagram. Retorna (code, media_pk, None) o (None, None, error)."""
    ig = InstagramGraphAPI(cfg)
    
    # Verificar token antes de publicar
    if not ig.verify_token():
        return None, None, "Token de Instagram expirado o inválido. Regenera el token en Facebook Developers."
    
    # Subir imágenes a R2
    image_urls = []
    r2_keys = []
    
    try:
        for image_path in image_paths:
            url, key = r2.upload_image(image_path)
            if url:
                image_urls.append(url)
                r2_keys.append(key)
            else:
                # Limpiar archivos subidos si falla alguno
                for k in r2_keys:
                    r2.delete_object(k)
                return None, None, "Error subiendo imágenes a R2"
        
        if len(image_urls) == 1:
            code, media_id, error = ig.publish_photo(image_urls[0], caption)
        else:
            code, media_id, error = ig.publish_album(image_urls, caption)
        
        return code, media_id, error
    except Exception as e:
        return None, None, str(e)
    finally:
        # Limpiar archivos de R2
        for key in r2_keys:
            r2.delete_object(key)


# ── Stories ────────────────────────────────────────────────────────

def _generate_thumbnail(video_path):
    """Genera un thumbnail del primer frame del vídeo usando FFmpeg."""
    if not shutil.which('ffmpeg'):
        return None
    try:
        fd, thumb_path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        result = subprocess.run([
            'ffmpeg', '-y',
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',
            thumb_path
        ], capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and os.path.getsize(thumb_path) > 0:
            return thumb_path
        try:
            os.unlink(thumb_path)
        except:
            pass
        return None
    except Exception as e:
        log.warning(f"  Thumbnail falló: {e}")
        return None


def _render_story_frame(image_path):
    """Pre-renderiza el frame de la story con Pillow: fondo blur + imagen con bordes redondeados.
    Trabaja a 540x960 (mitad de 1080x1920) para reducir carga de CPU en el NAS.
    Retorna el path del frame temporal."""
    W, H = 540, 960
    FG_W, FG_H = 405, 720
    RADIUS = 25

    img = Image.open(image_path).convert("RGBA")
    img.thumbnail((FG_W, FG_H), Image.LANCZOS)
    fg_w, fg_h = img.size
    fg_x = (W - fg_w) // 2
    fg_y = (H - fg_h) // 2

    blur_bg = img.copy()
    blur_bg = blur_bg.resize((W, H), Image.LANCZOS)
    blur_bg = blur_bg.filter(ImageFilter.GaussianBlur(radius=15))

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    canvas.paste(blur_bg, (0, 0))

    mask = Image.new("L", (fg_w, fg_h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([(0, 0), (fg_w, fg_h)], radius=RADIUS, fill=255)
    canvas.paste(img, (fg_x, fg_y), mask)

    fd, frame_path = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    canvas = canvas.convert("RGB")
    canvas.save(frame_path, "JPEG", quality=90)
    return frame_path


def _compute_overlay_pos(overlay_path, is_flecha=False):
    """Calcula posicion y tamano del overlay.
    Regulares: siempre arriba, max 10-15% solapado sobre la imagen.
    Flechas: esquina superior-izq apunta al centro con margen abajo-derecha.
    Todo en coordenadas 540x960 (se escala a 1080x1920 en FFmpeg)."""
    W, H = 540, 960
    MARGIN = 20
    FG_W, FG_H = 405, 720
    FG_X = (W - FG_W) // 2
    FG_Y = (H - FG_H) // 2

    try:
        ovl = Image.open(overlay_path)
        w, h = ovl.size
    except Exception:
        return None, None, None, None

    if is_flecha:
        target_ratio = 0.09
        ov_area = W * H * target_ratio
        aspect = w / h if h > 0 else 1.0
        ow = int((ov_area * aspect) ** 0.5)
        oh = max(int(ow / aspect), 1)

        max_width = int(W * 0.30)
        if ow > max_width:
            ow = max_width
            oh = max(int(ow / aspect), 1)

        center_x = W // 2
        center_y = H // 2
        margin_x = int(FG_W * 0.12)
        margin_y = int(FG_H * 0.10)
        ox = center_x + margin_x
        oy = center_y + margin_y
        ox = max(MARGIN, min(ox, W - ow - MARGIN))
        oy = max(MARGIN, min(oy, H - oh - MARGIN))
        return ox, oy, ow, oh

    target_ratio = random.uniform(0.15, 0.20)
    ov_area = W * H * target_ratio
    aspect = w / h if h > 0 else 1.0
    ow = int((ov_area * aspect) ** 0.5)
    oh = max(int(ow / aspect), 1)

    max_width = int(W * 0.90)
    if ow > max_width:
        ow = max_width
        oh = max(int(ow / aspect), 1)

    max_overlap_pct = random.uniform(0.10, 0.15)
    max_overlap_y = int(FG_Y + FG_H * max_overlap_pct)
    max_oy = max(max_overlap_y - oh, MARGIN)

    max_x = max(W - ow - MARGIN, MARGIN)
    ox = random.randint(MARGIN, max(max_x, MARGIN))
    oy = random.randint(MARGIN, max(max_oy, MARGIN))

    return ox, oy, ow, oh


def share_to_story(cfg, r2, image_path, game_name, platform,
                   video_path=None, frame_path=None):
    """Sube la story con frame Pillow + overlay + musica.
    Si video_path/frame_path no se pasan, los genera con FFmpeg.
    Retorna (True, None) si OK, o (False, video_path) si falla la subida
    (el video_path sobrevive para enviarse por Telegram como fallback)."""
    ig = InstagramGraphAPI(cfg)
    
    # Verificar token antes de publicar story
    if not ig.verify_token():
        log.error("  Token IG expirado, no se puede publicar story")
        if video_path:
            return False, video_path
        return False, None
    
    own_video = video_path is None
    if own_video:
        video_path, frame_path = _create_story_video(cfg, image_path, game_name, platform)
    if not video_path:
        log.warning("  No se genero el video de story, se omite.")
        if frame_path and own_video:
            try:
                os.unlink(frame_path)
            except Exception:
                pass
        return False, None

    # Subir video a R2
    video_url, video_key = r2.upload_image(video_path, content_type='video/mp4')
    if not video_url:
        log.error("  Error subiendo video de story a R2")
        if own_video:
            os.unlink(video_path)
            if frame_path:
                os.unlink(frame_path)
        return False, video_path

    try:
        log.info("  Publicando story via Graph API...")
        code, media_id, error = ig.publish_story(video_url=video_url)
        
        if code:
            log.info(f"  [OK] Story publicada. shortcode={code}")
            if own_video:
                os.unlink(video_path)
                if frame_path:
                    os.unlink(frame_path)
            return True, None
        else:
            log.error(f"  Error publicando story: {error}")
            if own_video and frame_path:
                try:
                    os.unlink(frame_path)
                except Exception:
                    pass
            return False, video_path
    finally:
        # Limpiar archivo de R2
        if video_key:
            r2.delete_object(video_key)


def _create_story_video(cfg, image_path, game_name, platform, output_path=None):
    """Crea video para story con frame Pillow (blur + bordes redondeados) +
    overlay adaptativo + musica usando FFmpeg.
    Retorna (video_path, frame_path) o (None, None)."""
    if not shutil.which('ffmpeg'):
        log.warning("  FFmpeg no encontrado")
        return None, None

    music_path = _pick_music(cfg, platform)
    regular_path, _ = _pick_overlays(cfg)
    safe_name = game_name.replace("'", "'\\''")[:40]

    regular_pos = None
    if regular_path:
        ox, oy, ow, oh = _compute_overlay_pos(regular_path, is_flecha=False)
        if ox is not None:
            regular_pos = (ox, oy, ow, oh)
            log.info(f"  Overlay [normal] pos=({ox},{oy}) size=({ow},{oh})")
        else:
            log.warning("  Overlay regular no valido, omitiendo")

    frame_path = None
    try:
        log.info("  Renderizando frame con Pillow...")
        frame_path = _render_story_frame(image_path)
        log.info(f"  Frame renderizado: {frame_path}")

        if output_path:
            video_path = output_path
        else:
            fd, video_path = tempfile.mkstemp(suffix='.mp4')
            os.close(fd)

        duration = 15
        cmd = ['ffmpeg', '-y']

        has_regular = regular_path is not None and regular_pos is not None

        cmd += ['-loop', '1', '-i', frame_path]

        if has_regular:
            rext = os.path.splitext(regular_path)[1].lower()
            if rext == '.gif':
                cmd += ['-stream_loop', '-1', '-i', regular_path]
            else:
                cmd += ['-loop', '1', '-i', regular_path]

        if music_path:
            cmd += ['-i', music_path]

        overlay_inputs = 1 if has_regular else 0
        any_overlay = has_regular

        if has_regular:
            rx, ry, rw, rh = regular_pos
            vf = (
                f"[1:v]scale={rw}:{rh},setsar=1[rv];"
                f"[0:v][rv]overlay={rx}:{ry},scale=1080:1920:flags=lanczos[outv]"
            )
            cmd += ['-filter_complex', vf, '-map', '[outv]']
        else:
            filter_chain = (
                f"[0:v]scale=1080:1920:flags=lanczos[bg];"
                f"[bg]"
                f"drawbox=x=0:y=ih*0.72:w=iw:h=ih*0.28:color=black@0.45:t=fill,"
                f"drawtext=fontfile='{FONT_FILE}':text='NUEVO POST':fontcolor=white:fontsize=72:"
                f"x=(w-text_w)/2:y=h*0.79:box=1:boxcolor=black@0.5:boxborderw=16:"
                f"shadowcolor=black:shadowx=3:shadowy=3,"
                f"drawtext=fontfile='{FONT_FILE}':text='{safe_name}':fontcolor=white:fontsize=38:"
                f"x=(w-text_w)/2:y=h*0.87:box=1:boxcolor=black@0.5:boxborderw=10:"
                f"shadowcolor=black:shadowx=2:shadowy=2"
                f"[v]"
            )
            cmd += ['-filter_complex', filter_chain, '-map', '[v]']

        cmd += ['-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'stillimage',
                '-pix_fmt', 'yuv420p', '-t', str(duration),
                '-movflags', '+faststart']

        if music_path:
            music_idx = 1 + overlay_inputs
            cmd += ['-map', f'{music_idx}:a', '-shortest', '-c:a', 'aac', '-b:a', '128k']
        else:
            cmd += ['-an']

        cmd += [video_path]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            log.warning(f"  FFmpeg error: {result.stderr[-500:]}")
            if not output_path:
                try:
                    os.unlink(video_path)
                except Exception:
                    pass
            os.unlink(frame_path)
            return None, None

        if os.path.getsize(video_path) > 0:
            log.info(f"  Video generado: {video_path}")
            return video_path, frame_path
        os.unlink(frame_path)
        return None, None
    except subprocess.TimeoutExpired:
        log.warning("  FFmpeg timeout")
        if frame_path:
            try:
                os.unlink(frame_path)
            except Exception:
                pass
        return None, None
    except Exception as e:
        log.warning(f"  FFmpeg excepcion: {e}")
        if frame_path:
            try:
                os.unlink(frame_path)
            except Exception:
                pass
        return None, None


def _pick_music(cfg, platform):
    """Elige una canción según la plataforma del juego."""
    music_dir = cfg.get('config', 'music_dir', fallback='')
    if not music_dir:
        return None
    if music_dir.startswith('./'):
        music_dir = os.path.join(BASE_DIR, music_dir[2:])
    if not os.path.isdir(music_dir):
        log.warning(f"  Directorio de música no encontrado: {music_dir}")
        return None

    platform_map = {
        'NES': 'nes', 'SNES': 'snes', 'Super Nintendo': 'snes',
        'N64': 'n64', 'Nintendo 64': 'n64',
        'GameCube': 'gamecube', 'Wii': 'wii', 'Wii U': 'wiiu',
        'Switch': 'switch', 'Nintendo Switch': 'switch',
        'Game Boy': 'gameboy', 'Game Boy Color': 'gameboy',
        'Game Boy Advance': 'gba', 'GBA': 'gba',
        'DS': 'ds', 'Nintendo DS': 'ds', '3DS': '3ds',
        'PS1': 'ps1', 'PlayStation': 'ps1',
        'PS2': 'ps2', 'PlayStation 2': 'ps2',
        'PS3': 'ps3', 'PlayStation 3': 'ps3',
        'PS4': 'ps4', 'PlayStation 4': 'ps4',
        'PS5': 'ps5', 'PlayStation 5': 'ps5',
        'PSP': 'psp', 'PS Vita': 'vita',
        'Xbox': 'xbox', 'Xbox 360': 'xbox360',
        'Xbox One': 'xbone', 'Xbox Series': 'xboxseries',
        'Mega Drive': 'megadrive', 'Genesis': 'megadrive',
        'Dreamcast': 'dreamcast', 'Saturn': 'saturn',
        'PC': 'pc', 'Steam': 'pc',
    }

    folder = platform_map.get(platform, 'default')
    search_dir = os.path.join(music_dir, folder)
    if not os.path.isdir(search_dir):
        log.info(f"  Sin carpeta '{folder}' para '{platform}', usando default")
        search_dir = os.path.join(music_dir, 'default')
    if not os.path.isdir(search_dir):
        search_dir = music_dir

    audio_exts = ('.mp3', '.m4a', '.aac', '.ogg', '.wav', '.flac')
    songs = [os.path.join(search_dir, f) for f in os.listdir(search_dir)
             if f.lower().endswith(audio_exts)]
    if not songs:
        log.warning(f"  Sin archivos de audio en: {search_dir}")
        return None

    random.shuffle(songs)
    for chosen in songs:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', chosen],
            capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            log.warning(f"  Audio descartado (inválido): {os.path.basename(chosen)}")
            continue
        log.info(f"  Música seleccionada: {os.path.basename(chosen)} [{folder}]")
        return chosen

    log.warning(f"  Ningún audio válido en: {search_dir}")
    return None


def _validate_gif(path):
    if not path.lower().endswith('.gif'):
        return True
    try:
        result = subprocess.run(
            ['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-i', path, '-t', '1', '-f', 'null', '-'],
            capture_output=True, text=True, timeout=8)
        return result.returncode == 0
    except Exception:
        return False


def _pick_overlays(cfg):
    """Elige un overlay regular de gif/.
    Retorna (regular_path, None)."""
    gif_dir = os.path.join(BASE_DIR, 'gif')
    if not os.path.isdir(gif_dir):
        return None, None

    img_exts = ('.gif', '.png', '.jpg', '.jpeg', '.webp')

    regular = [os.path.join(gif_dir, f) for f in os.listdir(gif_dir)
               if f.lower().endswith(img_exts) and os.path.isfile(os.path.join(gif_dir, f))]
    random.shuffle(regular)
    regular_path = None
    for r in regular:
        if not _validate_gif(r):
            log.warning(f"  Overlay regular descartado (inválido): {os.path.basename(r)}")
            continue
        log.info(f"  Overlay regular: {os.path.basename(r)}")
        regular_path = r
        break
    if not regular_path:
        log.warning("  Ningun overlay regular valido")

    return regular_path, None


# ── Notificaciones ─────────────────────────────────────────────────
def send_telegram(cfg, message):
    dev_mode = cfg.get('config', 'dev_mode', fallback='').lower() in ('1', 'true', 'yes', 'si')
    if dev_mode:
        return
    token = cfg.get('config', 'telegram_token', fallback='')
    chat_id = cfg.get('config', 'telegram_chat_id', fallback='')
    if not token or not chat_id:
        return
    try:
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message[:4096]}).encode()
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        urllib.request.urlopen(urllib.request.Request(url, data=data,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'}), timeout=10)
    except Exception as e:
        log.error(f"Telegram: {e}")


def send_email(cfg, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    host = cfg.get('config', 'smtp_host', fallback='')
    if not host:
        return
    port = int(cfg.get('config', 'smtp_port', fallback='587'))
    user = cfg.get('config', 'smtp_user', fallback='')
    pwd = cfg.get('config', 'smtp_pass', fallback='')
    to = cfg.get('config', 'notification_email', fallback=user)
    try:
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = to
        with smtplib.SMTP(host, port, timeout=10) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
    except Exception as e:
        log.error(f"Email: {e}")


def send_telegram_video(cfg, video_path, caption=""):
    """Envia un video por Telegram como fallback si la story falla."""
    dev_mode = cfg.get('config', 'dev_mode', fallback='').lower() in ('1', 'true', 'yes', 'si')
    if dev_mode:
        log.info(f"  [DEV] Video Telegram suprimido: {caption[:80]}")
        return
    token = cfg.get('config', 'telegram_token', fallback='')
    chat_id = cfg.get('config', 'telegram_chat_id', fallback='')
    if not token or not chat_id:
        return
    try:
        boundary = "boundary" + str(int(time.time()))
        with open(video_path, "rb") as fh:
            video_data = fh.read()
        filename = os.path.basename(video_path)
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="video"; filename="{filename}"\r\n'
            f"Content-Type: video/mp4\r\n\r\n"
        ).encode("utf-8") + video_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        url = f"https://api.telegram.org/bot{token}/sendVideo"
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        with urllib.request.urlopen(req, timeout=120):
            pass
        log.info(f"  [NOTIFY telegram] Video enviado a {chat_id}")
    except Exception as e:
        log.error(f"  [NOTIFY telegram] error envio video: {e}")


def notify(cfg, message):
    dev_mode = cfg.get('config', 'dev_mode', fallback='').lower() in ('1', 'true', 'yes', 'si')
    if dev_mode:
        log.info(f"[DEV] Notificacion suprimida: {message[:120]}")
        return
    send_telegram(cfg, message)
    send_email(cfg, 'IG Publisher', message)


# ── Publicación ────────────────────────────────────────────────────
def process_publication(cfg, r2, pub):
    coleccion_id = pub.get('coleccion_id')
    coleccion = pub.get('coleccion', {})
    base = coleccion.get('base', {})
    nombre = base.get('nombre', 'Desconocido')
    texto = pub.get('texto_publicacion', '') or ''
    fotos = pub.get('fotos_seleccionadas', [])
    dev_mode = cfg.get('config', 'dev_mode', fallback='').lower() in ('1', 'true', 'yes', 'si')

    if not fotos:
        log.warning(f"«{nombre}» sin fotos seleccionadas, se omite.")
        return 'sin_fotos'

    log.info(f"\n{'='*50}\n«{nombre}» — {len(fotos)} foto(s){' [DEV]' if dev_mode else ''}\n{'='*50}")

    tmp_files = []
    for foto in fotos:
        fid = foto.get('fichero_id')
        if not fid:
            continue
        log.info(f"  Descargando fichero {fid}...")
        img_data = get_image_from_api(cfg, fid)
        if not img_data:
            continue
        _, ext = os.path.splitext(str(fid))
        tmp = tempfile.NamedTemporaryFile(suffix=ext or '.jpg', delete=False)
        tmp.write(img_data)
        tmp.close()
        _fix_orientation(tmp.name)
        tmp_files.append(tmp.name)

    if not tmp_files:
        log.error("  No se pudieron descargar las imágenes.")
        api_post(cfg, f'/api/ig/error/{coleccion_id}', {'error': 'No se pudieron descargar las imágenes'})
        return 'sin_imgs'

    caption = texto
    ig_url = coleccion.get('ig', '')
    if ig_url and ig_url not in caption:
        caption = f'{caption}\n\n{ig_url}' if caption else ig_url

    plataforma = coleccion.get('plataforma', {}).get('nombre', '')

    if dev_mode:
        safe_name = "".join(c if c.isalnum() or c in '._- ' else '_' for c in nombre).strip()
        output_dir = os.path.join(BASE_DIR, 'dev_output', safe_name)
        os.makedirs(output_dir, exist_ok=True)

        for i, f in enumerate(tmp_files):
            ext = os.path.splitext(f)[1] or '.jpg'
            dest = os.path.join(output_dir, f'foto_{i+1}{ext}')
            shutil.copy2(f, dest)
            log.info(f"  [DEV] Copiada: {dest}")

        caption_file = os.path.join(output_dir, 'caption.txt')
        with open(caption_file, 'w', encoding='utf-8') as cf:
            cf.write(caption)
        log.info(f"  [DEV] Caption guardada en: {caption_file}")

        story_path, frame_path = _create_story_video(cfg, tmp_files[0], nombre, plataforma,
                                                       output_path=os.path.join(output_dir, 'story.mp4'))
        if story_path:
            log.info(f"  [DEV] Story guardada en: {story_path}")
        else:
            log.warning(f"  [DEV] No se pudo generar el video de story")
        if frame_path and frame_path != story_path:
            try:
                os.unlink(frame_path)
            except Exception:
                pass

        for f in tmp_files:
            try:
                os.unlink(f)
            except:
                pass

        return 'dev', output_dir

    first_image = tmp_files[0] if tmp_files else None

    # Generar video de story offline ANTES de subir a R2
    story_video_path, story_frame_path = None, None
    if first_image:
        story_video_path, story_frame_path = _create_story_video(
            cfg, first_image, nombre, plataforma)

    log.info(f"  Publicando en IG ({len(tmp_files)} fotos)...")
    ig_code, media_pk, error = publish_instagram(cfg, r2, tmp_files, caption)

    if ig_code:
        permalink = f'https://www.instagram.com/p/{ig_code}/'
        api_post(cfg, f'/api/ig/publicado/{coleccion_id}',
                 {'ig_post_id': str(ig_code), 'ig_permalink': permalink})
        log.info(f"  [OK] {nombre} — {permalink}")

        story_ok, story_video = share_to_story(
            cfg, r2, first_image, nombre, plataforma,
            video_path=story_video_path, frame_path=story_frame_path)
        story_failed = not story_ok
        if story_failed:
            log.warning("  Publicacion en IG correcta pero la story fallo")
            if story_video:
                send_telegram_video(cfg, story_video,
                                    f"Story fallida para: {nombre}")
                try:
                    os.unlink(story_video)
                except Exception:
                    pass
        elif story_video_path:
            try:
                os.unlink(story_video_path)
            except Exception:
                pass

        if story_frame_path:
            try:
                os.unlink(story_frame_path)
            except Exception:
                pass

        for f in tmp_files:
            try:
                os.unlink(f)
            except:
                pass

        if story_failed:
            return 'ok', permalink, 'story_fail'
        return 'ok', permalink
    else:
        if story_video_path:
            try:
                os.unlink(story_video_path)
            except Exception:
                pass
        if story_frame_path:
            try:
                os.unlink(story_frame_path)
            except Exception:
                pass

        for f in tmp_files:
            try:
                os.unlink(f)
            except:
                pass

        log.error(f"  [FAIL] {nombre}: {error}")
        api_post(cfg, f'/api/ig/error/{coleccion_id}', {'error': str(error)[:300]})
        return 'error'


# ── Main ───────────────────────────────────────────────────────────
def next_run_at():
    now = datetime.now()
    targets = [now.replace(minute=m, second=0, microsecond=0) for m in (5, 35)]
    future = [t for t in targets if t > now]
    if future:
        return min(future)
    return now.replace(minute=5, second=0, microsecond=0) + timedelta(hours=1)


def wait_until_next_slot():
    target = next_run_at()
    seconds = (target - datetime.now()).total_seconds()
    if seconds > 0:
        log.info(f"Próxima ejecución: {target.strftime('%H:%M')} (en {int(seconds)}s)")
        time.sleep(seconds)


def run():
    cfg = load_cfg()
    dev_mode = cfg.get('config', 'dev_mode', fallback='').lower() in ('1', 'true', 'yes', 'si')
    
    log.info("=== IG Publisher iniciado%s ===" % (" en MODO DEVELOP" if dev_mode else ""))
    if dev_mode:
        log.info("Las publicaciones se guardarán en dev_output/ sin subir a IG")
    log.info(f"API: {cfg.get('config', 'api_url')}  |  Slots: minuto 5 y 35 de cada hora")

    # Inicializar R2
    r2 = None
    if not dev_mode:
        try:
            r2 = R2Storage(cfg)
            log.info("R2 inicializado correctamente")
        except Exception as e:
            log.error(f"Error inicializando R2: {e}")
            notify(cfg, f"<b>❌ IG Publisher: Error inicializando R2</b>\n{str(e)[:300]}")
            return
        
        # Verificar/refrescar token al inicio
        if not try_refresh_token(cfg):
            log.error("No se pudo verificar/refrescar el token de Instagram")
            # No salimos, seguimos intentando en cada ciclo
        
        # Recargar config por si el token fue actualizado
        cfg = load_cfg()

    while True:
        try:
            log.info("Verificando publicaciones pendientes...")
            data = api_get(cfg, '/api/ig/pendientes')
            if not data:
                log.info("No se pudo obtener la lista de pendientes, esperando siguiente slot")
                wait_until_next_slot()
                continue

            publicaciones = data if isinstance(data, list) else data.get('items', [])
            if not publicaciones:
                log.info("No hay publicaciones pendientes, esperando siguiente slot")
                wait_until_next_slot()
                continue

            log.info(f"✓ Hay {len(publicaciones)} publicación(es) pendiente(s), procesando...")

            ok_list, err_list, dev_list = [], [], []
            for pub in publicaciones:
                c = pub.get('coleccion', {})
                b = c.get('base', {})
                name = b.get('nombre', '?')
                coleccion_id = pub.get('coleccion_id', '?')
                plataforma = c.get('plataforma', {}).get('nombre', '')
                try:
                    res = process_publication(cfg, r2, pub)
                    if isinstance(res, tuple) and res[0] == 'ok':
                        story_note = ' (sin story)' if len(res) > 2 and res[2] == 'story_fail' else ''
                        ok_list.append({'id': coleccion_id, 'nombre': name, 'plataforma': plataforma, 'url': res[1],
                                        'story_note': story_note})
                    elif isinstance(res, tuple) and res[0] == 'dev':
                        dev_list.append({'id': coleccion_id, 'nombre': name, 'plataforma': plataforma, 'dir': res[1]})
                    elif res in ('error', 'sin_imgs') or (isinstance(res, tuple) and res[0] == 'error'):
                        err_list.append(name)
                except Exception as e:
                    err_list.append(f'{name}: {str(e)[:200]}')
                    log.error(f"Excepción: {traceback.format_exc()}")

            if ok_list or err_list or dev_list:
                msg = []
                for item in ok_list:
                    extra = item.get('story_note', '')
                    msg.append(f"Publicación #{item['id']} completada!{extra}\n{item['plataforma']} {item['nombre']}\n{item['url']}")
                for item in dev_list:
                    msg.append(f"[DEV] #{item['id']} {item['plataforma']} {item['nombre']}\nGuardado en: {item['dir']}")
                if err_list:
                    msg.append(f"❌ Errores ({len(err_list)}):\n" + '\n'.join(f'• {n}' for n in err_list))
                
                log.info(f"Enviando notificaciones (Telegram + Email)...")
                if not dev_mode:
                    notify(cfg, '\n\n'.join(msg))
                    log.info("✓ Notificaciones enviadas")
                else:
                    log.info("[DEV] Notificaciones suprimidas")

            if dev_mode:
                log.info("Modo DEV: saliendo tras procesar lote.")
                break

        except Exception as e:
            log.error(f"Ciclo: {traceback.format_exc()}")

        wait_until_next_slot()


if __name__ == '__main__':
    run()
