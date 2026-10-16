import os
import requests
from duckduckgo_search import DDGS

# Define las clases/términos que quieres buscar
terminos_de_busqueda = [
    "burned eucalyptus forest floor",
    "post fire grassland soil",
    "cenizas incendio forestal pasto",
    "green shoots burned soil"
]

directorio_base = 'dataset_rover'

# Iniciamos el buscador de DuckDuckGo
with DDGS() as ddgs:
    for termino in terminos_de_busqueda:
        print(f"\n--- Buscando imágenes para: {termino} ---")
        
        carpeta_destino = os.path.join(directorio_base, termino)
        os.makedirs(carpeta_destino, exist_ok=True)
        
        # Obtenemos hasta 150 resultados de DuckDuckGo
        resultados = ddgs.images(termino, max_results=150)
        
        # Contador para nombrar los archivos
        contador = 1
        
        for resultado in resultados:
            url_imagen = resultado.get('image')
            if url_imagen:
                try:
                    # Intentamos descargar la imagen con un tiempo límite de 10 segundos
                    respuesta = requests.get(url_imagen, timeout=10)
                    if respuesta.status_code == 200:
                        # Guardamos con nombres como 001.jpg, 002.jpg, etc.
                        nombre_archivo = f"{contador:03d}.jpg"
                        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
                        
                        with open(ruta_archivo, 'wb') as archivo:
                            archivo.write(respuesta.content)
                        
                        print(f"[{contador}] Descargada: {nombre_archivo}")
                        contador += 1
                except Exception as e:
                    # Si un enlace está roto o la página web original bloquea la descarga, lo ignoramos
                    print(f"[X] Error al descargar de: {url_imagen[:50]}...")
                    continue

print("\n¡Descarga completada con DuckDuckGo!")