import os
import glob
from ultralytics import YOLO

# Cargar el modelo usando la ruta exacta
modelo = YOLO(r'C:\Users\USER\Desktop\ROVER\classify\rover_ai\modelo_v1\weights\best.pt')

# Carpeta de validación que queremos probar
carpeta_prueba = r'dataset_yolo\val\brotes' # Puedes cambiarlo a 'dataset_yolo\val\suelo_carbonizado'

# Buscar automáticamente todas las imágenes .jpg en la carpeta
imagenes = glob.glob(os.path.join(carpeta_prueba, '*.jpeg'))

if not imagenes:
    print(f"No se encontraron imágenes en la ruta: {carpeta_prueba}")
else:
    print(f"Se encontraron {len(imagenes)} imágenes. Evaluando las primeras 5...\n")
    
    # Iterar sobre las primeras 5 fotos que encuentre
    for ruta_imagen in imagenes[:5]:
        nombre_archivo = os.path.basename(ruta_imagen)
        
        # Realizar la predicción (verbose=False oculta el texto extra de YOLO en consola)
        resultados = modelo(ruta_imagen, verbose=False)
        
        diccionario_nombres = resultados[0].names
        clase_ganadora_id = resultados[0].probs.top1
        confianza = resultados[0].probs.top1conf.item() * 100
        
        print(f"Archivo: {nombre_archivo}")
        print(f" -> Predicción: {diccionario_nombres[clase_ganadora_id]}")
        print(f" -> Seguridad: {confianza:.2f}%\n")