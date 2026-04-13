import requests
import os

# Configuración
plataforma = "Switch"
tipo_base_id = 1
base_url = "http://192.168.1.55:9501"
output_dir = "."  # Carpeta raíz donde se crean subdirectorios

# Paso 1: Obtener colecciones
colecciones_url = f"{base_url}/api/colecciones"
params = {"plataforma": plataforma, "tipo_base_id": tipo_base_id}
response = requests.get(colecciones_url, params=params)

if response.status_code == 200:
    colecciones = response.json()

    for item in colecciones:
        id_ = item.get("id")
        codigo = item.get("codigo")
        print(f"\nID: {id_} - Código: {codigo}")

        # Paso 2: Obtener ficheros
        ficheros_url = f"{base_url}/api/datos_ficheros_coleccion/{id_}"
        ficheros_resp = requests.get(ficheros_url)

        if ficheros_resp.status_code == 200:
            ficheros = ficheros_resp.json()

            if ficheros:
                carpeta = os.path.join(output_dir, codigo)
                os.makedirs(carpeta, exist_ok=True)
                print(f"  📁 Carpeta creada: {carpeta}")

                for fichero in ficheros:
                    fichero_id = fichero["id"]
                    nombre_original = fichero["nombre_original"]

                    # Paso 3: Descargar fichero
                    fichero_url = f"{base_url}/api/fichero/id/{fichero_id}"
                    fichero_resp = requests.get(fichero_url)

                    if fichero_resp.status_code == 200:
                        ruta_fichero = os.path.join(carpeta, nombre_original)
                        with open(ruta_fichero, "wb") as f:
                            f.write(fichero_resp.content)
                        print(f"    📥 {nombre_original} descargado.")
                    else:
                        print(f"    ❌ Error al descargar fichero {fichero_id}")
            else:
                print("  No hay ficheros.")
        else:
            print(f"  ❌ Error al obtener ficheros (código {ficheros_resp.status_code})")
else:
    print(f"❌ Error al obtener colecciones: {response.status_code}")
