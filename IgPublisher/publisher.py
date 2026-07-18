#!/usr/bin/env python3
"""
IG Publisher — Publica en Instagram via instagrapi (API privada).
Sube imágenes directamente, sin necesidad de URLs HTTPS públicas.
Notifica por Telegram solo si hay novedades.
"""

import configparser
import json
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
from datetime import datetime, timezone

import requests
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.types import StoryLink
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.txt')
SESSION_FILE = os.path.join(BASE_DIR, 'ig_session.json')
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


# ── Instagram (instagrapi) ─────────────────────────────────────────
_ig_client = None


def get_ig_client(cfg):
    global _ig_client
    if _ig_client is not None:
        return _ig_client

    cl = Client()
    cl.delay_range = [2, 5]

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(cfg.get('config', 'ig_username'),
                     cfg.get('config', 'ig_password'))
            cl.get_timeline_feed()
            log.info("Sesión de IG restaurada")
            _ig_client = cl
            return cl
        except LoginRequired:
            log.warning("Sesión expirada, re-login...")
        except Exception as e:
            log.warning(f"Error cargando sesión: {e}")

    # Login fresco
    cl.login(cfg.get('config', 'ig_username'),
             cfg.get('config', 'ig_password'))
    cl.dump_settings(SESSION_FILE)
    log.info("Login en IG correcto, sesión guardada")
    _ig_client = cl
    return cl


def publish_instagram(cfg, image_paths, caption):
    """Publica foto(s) en Instagram. Retorna (code, media_pk, None) o (None, None, error)."""
    cl = get_ig_client(cfg)
    try:
        if len(image_paths) == 1:
            media = cl.photo_upload(image_paths[0], caption=caption)
        else:
            media = cl.album_upload(image_paths[:10], caption=caption)
        code = media.code if hasattr(media, 'code') else str(media.pk)
        return code, str(media.pk), None
    except Exception as e:
        return None, None, str(e)


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


def _compute_overlay_pos(overlay_path):
    """Calcula posicion y tamano del overlay proporcional a su aspecto real.
    Todo en coordenadas 540x960 (se escala a 1080x1920 en FFmpeg)."""
    W, H = 540, 960
    MARGIN = 20
    try:
        ovl = Image.open(overlay_path)
        w, h = ovl.size
    except Exception:
        return None, None, None, None

    target_ratio = random.uniform(0.15, 0.20)
    ov_area = W * H * target_ratio
    aspect = w / h if h > 0 else 1.0
    ow = int((ov_area * aspect) ** 0.5)
    oh = max(int(ow / aspect), 1)

    max_x = max(W - ow - MARGIN, MARGIN)
    max_y = max(H - oh - MARGIN, MARGIN)
    ox = random.randint(MARGIN, max(max_x, MARGIN))
    oy = random.randint(MARGIN, max(max_y, MARGIN))

    return ox, oy, ow, oh


def share_to_story(cfg, image_path, permalink, game_name, platform):
    """Sube la story con frame Pillow + overlay + musica.
    Retorna (True, None) si OK, o (False, video_path) si falla la subida
    (el video_path sobrevive para enviarse por Telegram como fallback)."""
    cl = get_ig_client(cfg)

    video_path, frame_path = _create_story_video(cfg, image_path, game_name, platform)
    if not video_path:
        log.warning("  No se genero el video de story, se omite.")
        if frame_path:
            try:
                os.unlink(frame_path)
            except Exception:
                pass
        return False, None

    try:
        links = []
        if permalink:
            links = [StoryLink(webUri=permalink)]
            log.info(f"  Link sticker (default pos): {permalink}")
        log.info("  Subiendo story con video...")
        result = cl.video_upload_to_story(video_path, thumbnail=frame_path, links=links)
        log.info(f"  [OK] Story subida. pk={result.pk if hasattr(result,'pk') else '?'}  links_en_respuesta={bool(result.links)}")
        os.unlink(video_path)
        os.unlink(frame_path)
        return True, None
    except Exception as e:
        log.warning(f"  Story video fallo: {e}")
        if frame_path:
            try:
                os.unlink(frame_path)
            except Exception:
                pass
        return False, video_path


def _create_story_video(cfg, image_path, game_name, platform, output_path=None):
    """Crea video para story con frame Pillow (blur + bordes redondeados) +
    overlay adaptativo + musica usando FFmpeg.
    Retorna (video_path, frame_path) o (None, None)."""
    if not shutil.which('ffmpeg'):
        log.warning("  FFmpeg no encontrado")
        return None, None

    music_path = _pick_music(cfg, platform)
    overlay_path = _pick_overlay(cfg)
    safe_name = game_name.replace("'", "'\\''")[:40]

    overlay_pos = None
    if overlay_path:
        ox, oy, ow, oh = _compute_overlay_pos(overlay_path)
        if ox is not None:
            overlay_pos = (ox, oy, ow, oh)
            log.info(f"  Overlay pos=({ox},{oy}) size=({ow},{oh})")
        else:
            log.warning("  Overlay no valido, omitiendo")

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

        if overlay_path and overlay_pos:
            ox, oy, ow, oh = overlay_pos
            overlay_ext = os.path.splitext(overlay_path)[1].lower()
            if overlay_ext == '.gif':
                cmd += ['-loop', '1', '-i', frame_path, '-stream_loop', '-1', '-i', overlay_path]
            else:
                cmd += ['-loop', '1', '-i', frame_path, '-loop', '1', '-i', overlay_path]
        else:
            cmd += ['-loop', '1', '-i', frame_path]

        if music_path:
            cmd += ['-i', music_path]

        if overlay_path and overlay_pos:
            vf = (
                f"[1:v]scale={ow}:{oh},setsar=1[ov];"
                f"[0:v][ov]overlay={ox}:{oy},scale=1080:1920:flags=lanczos[outv]"
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
            music_map_idx = 2 if (overlay_path and overlay_pos) else 1
            cmd += ['-map', f'{music_map_idx}:a', '-shortest', '-c:a', 'aac', '-b:a', '128k']
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


def _pick_overlay(cfg):
    """Elige una imagen/gif aleatoria de la carpeta gif/ para superponer en la story."""
    gif_dir = os.path.join(BASE_DIR, 'gif')
    if not os.path.isdir(gif_dir):
        return None

    img_exts = ('.gif', '.png', '.jpg', '.jpeg', '.webp')
    candidates = [os.path.join(gif_dir, f) for f in os.listdir(gif_dir)
                  if f.lower().endswith(img_exts)]
    if not candidates:
        return None

    random.shuffle(candidates)
    for chosen in candidates:
        if chosen.lower().endswith('.gif'):
            try:
                result = subprocess.run(
                    ['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-i', chosen, '-t', '1', '-f', 'null', '-'],
                    capture_output=True, text=True, timeout=8)
                if result.returncode != 0:
                    log.warning(f"  Overlay descartado (inválido): {os.path.basename(chosen)}")
                    continue
            except Exception:
                log.warning(f"  Overlay descartado (timeout/inválido): {os.path.basename(chosen)}")
                continue
        log.info(f"  Overlay seleccionado: {os.path.basename(chosen)}")
        return chosen

    log.warning("  Ningún overlay válido encontrado")
    return None


# ── Notificaciones ─────────────────────────────────────────────────
def send_telegram(cfg, message):
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
    send_telegram(cfg, message)
    send_email(cfg, 'IG Publisher', message)


# ── Publicación ────────────────────────────────────────────────────
def process_publication(cfg, pub):
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

    log.info(f"  Publicando en IG ({len(tmp_files)} fotos)...")
    ig_code, media_pk, error = publish_instagram(cfg, tmp_files, caption)

    first_image = tmp_files[0] if tmp_files else None

    if ig_code:
        permalink = f'https://www.instagram.com/p/{ig_code}/'
        api_post(cfg, f'/api/ig/publicado/{coleccion_id}',
                 {'ig_post_id': str(ig_code), 'ig_permalink': permalink})
        log.info(f"  [OK] {nombre} — {permalink}")

        story_ok, story_video = share_to_story(cfg, first_image, permalink, nombre, plataforma)
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

        for f in tmp_files:
            try:
                os.unlink(f)
            except:
                pass

        if story_failed:
            return 'ok', permalink, 'story_fail'
        return 'ok', permalink
    else:
        for f in tmp_files:
            try:
                os.unlink(f)
            except:
                pass

        log.error(f"  [FAIL] {nombre}: {error}")
        api_post(cfg, f'/api/ig/error/{coleccion_id}', {'error': str(error)[:300]})
        return 'error'


# ── Main ───────────────────────────────────────────────────────────
def run():
    cfg = load_cfg()
    interval = int(cfg.get('config', 'check_interval', fallback='300'))
    dev_mode = cfg.get('config', 'dev_mode', fallback='').lower() in ('1', 'true', 'yes', 'si')

    if dev_mode:
        log.info("=== IG Publisher iniciado en MODO DEVELOP ===")
        log.info("Las publicaciones se guardarán en dev_output/ sin subir a IG")
    else:
        # Verificar login IG al iniciar
        try:
            get_ig_client(cfg)
            log.info("IG login OK")
        except Exception as e:
            log.error(f"IG login falló: {e}")
            notify(cfg, f"<b>❌ IG Publisher: login fallido</b>\n{str(e)[:300]}")
            sys.exit(1)

        log.info("=== IG Publisher iniciado ===")

    log.info(f"API: {cfg.get('config', 'api_url')}  |  Intervalo: {interval}s")

    while True:
        try:
            data = api_get(cfg, '/api/ig/pendientes')
            if not data:
                time.sleep(interval)
                continue

            publicaciones = data if isinstance(data, list) else data.get('items', [])
            if not publicaciones:
                time.sleep(interval)
                continue

            log.info(f"Pendientes: {len(publicaciones)}")

            ok_list, err_list, dev_list = [], [], []
            for pub in publicaciones:
                c = pub.get('coleccion', {})
                b = c.get('base', {})
                name = b.get('nombre', '?')
                coleccion_id = pub.get('coleccion_id', '?')
                plataforma = c.get('plataforma', {}).get('nombre', '')
                try:
                    res = process_publication(cfg, pub)
                    if isinstance(res, tuple) and res[0] == 'ok':
                        story_note = ' (sin story)' if len(res) > 2 and res[2] == 'story_fail' else ''
                        ok_list.append({'id': coleccion_id, 'nombre': name, 'plataforma': plataforma, 'url': res[1],
                                        'story_note': story_note})
                    elif isinstance(res, tuple) and res[0] == 'dev':
                        dev_list.append({'id': coleccion_id, 'nombre': name, 'plataforma': plataforma, 'dir': res[1]})
                    elif res in ('error', 'sin_imgs') or (isinstance(res, tuple) and res[0] == 'error'):
                        err_list.append(name)
                except LoginRequired:
                    if dev_mode:
                        err_list.append(f'{name}: login requerido en dev mode')
                    else:
                        log.warning("Sesión IG expirada, reintentando login...")
                        global _ig_client
                        _ig_client = None
                        if os.path.exists(SESSION_FILE):
                            os.remove(SESSION_FILE)
                        try:
                            get_ig_client(cfg)
                        except:
                            err_list.append(f'{name}: login IG fallido')
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
                notify(cfg, '\n\n'.join(msg))

            if dev_mode:
                log.info("Modo DEV: saliendo tras procesar lote.")
                break

        except Exception as e:
            log.error(f"Ciclo: {traceback.format_exc()}")

        time.sleep(interval)


if __name__ == '__main__':
    run()
