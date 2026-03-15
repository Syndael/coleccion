# 0. Configuración necesaria en config.txt

Antes de usar el endpoint de importación de Steam, debes añadir la **clave de la Steam Web API** al archivo de configuración.

Archivo:

```
ApiRest/config.txt
```

Contenido mínimo requerido:

```ini
[config]
host = 127.0.0.1
user = root
password = root
db = coleccion
log_file = api.log
path_files = /tmp/coleccion_files
steam_api_key = TU_STEAM_API_KEY
```

La clave se obtiene en:

```
https://steamcommunity.com/dev/apikey
```

Durante el registro puedes usar como dominio:

```
localhost
```

---
# 1. Endpoint para importar juegos de Steam

**Endpoint**

POST /api/steam/import

**Body JSON**

```json
{
  "steam_user": "STEAM_ID_O_URL"
}
```

`steam_user` puede ser:

- SteamID64  
- URL del perfil  
- Vanity URL (nombre de usuario)

**Ejemplos válidos**

```
76561197999249388
https://steamcommunity.com/profiles/71561197999249387
https://steamcommunity.com/id/usuario
```

---

# 2. Ejemplo de llamada con curl

## Linux / Mac / Git Bash

```bash
curl -X POST http://localhost:5000/api/steam/import \
-H "Content-Type: application/json" \
-d '{"steam_user":"71561197999249387"}'
```

## PowerShell

```powershell
curl -Method POST http://localhost:5000/api/steam/import `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"steam_user":"71561197999249387"}'
```

---

# 3. Respuesta esperada

Ejemplo de respuesta:

```json
{
  "steam_id": "71561197999249387",
  "total_encontrados": 120,
  "importados": [
    {
      "appid": 620,
      "name": "Portal 2",
      "coleccion_id": 345
    }
  ],
  "omitidos_duplicado": [],
  "omitidos_dudosos": [],
  "errores": [],
  "resumen": {
    "importados": 20,
    "omitidos_duplicado": 5,
    "omitidos_dudosos": 1,
    "errores": 0
  }
}
```

---

# 4. Comprobación en base de datos

Para verificar los juegos importados:

```sql
SELECT 
    b.nombre,
    p.nombre AS plataforma,
    t.nombre AS tienda
FROM COLECCION c
JOIN BASE b ON b.id = c.base_id
JOIN PLATAFORMA p ON p.id = c.plataforma_id
LEFT JOIN TIENDA t ON t.id = c.tienda_id
ORDER BY c.id DESC
LIMIT 20;
```

Los juegos importados aparecerán con:

```
PLATAFORMA = PC
TIENDA = Steam
```

---

# 5. Requisitos en Steam

El perfil debe tener **biblioteca pública**:

```
Profile
→ Edit Profile
→ Privacy Settings
→ Game details = Public
```