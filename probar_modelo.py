import os
import glob
import random
from ultralytics import YOLO

# 1. Cargar el modelo entrenado
# OJO: Verifica si tu nuevo entrenamiento se guardó en modelo_v2 o similar. 
# Si es así, actualiza esta ruta.
modelo = YOLO(r'C:\Users\USER\Desktop\ROVER\classify\rover_ai\modelo_v1\weights\best.pt')

# 2. Buscar dinámicamente en TODAS las carpetas de validación (.jpg, .jpeg, .png)
ruta_base = r'dataset_yolo\val\*\*'
imagenes = glob.glob(f"{ruta_base}.jpg") + glob.glob(f"{ruta_base}.jpeg") + glob.glob(f"{ruta_base}.png")

print("Analizando imágenes con lógica de decisión del Rover...\n")

if not imagenes:
    print("⚠️ ERROR: No se encontraron imágenes en la carpeta 'dataset_yolo/val/'.")
    print("Verifica que preparaste los datos correctamente y que las rutas existen.")
else:
    # Mezclar las imágenes para probar casos de las 3 carpetas (brotes, suelo_carbonizado, ceniza_blanca)
    random.shuffle(imagenes)
    
    # Evaluar las primeras 5 imágenes aleatorias
    for ruta_imagen in imagenes[:5]:
        nombre_archivo = os.path.basename(ruta_imagen)
        
        # Realizar la predicción
        resultados = modelo(ruta_imagen, verbose=False)
        
        # Extraer datos de YOLO
        nombres_clases = resultados[0].names
        clase_id = resultados[0].probs.top1
        clase_detectada = nombres_clases[clase_id]
        confianza = resultados[0].probs.top1conf.item() * 100
        
        # 3. LÓGICA DE DECISIÓN DEL ROVER
        diagnostico = ""
        accion_rover = ""

        # Umbral de duda general: Si la IA está insegura, forzar muestreo
        if confianza < 55.0:
            diagnostico = "⚠️ Imagen confusa o mezclada."
            accion_rover = "MECANISMO ACTIVADO: Tomar muestra de tierra para análisis por sensores."
            
        # Decisiones basadas en la clase detectada
        elif clase_detectada == "brotes":
            diagnostico = "🟢 Viable: Regeneración natural detectada."
            accion_rover = "AVANZAR: No requiere muestreo. Suelo apto para reforestar."
            
        elif clase_detectada == "ceniza_blanca": # Actualizado al nombre real de tu carpeta
            diagnostico = "🔴 Inviable: Daño extremo. Suelo estéril superficialmente."
            accion_rover = "AVANZAR: No requiere muestreo. Marcar zona en el mapa."
            
        elif clase_detectada == "suelo_carbonizado":
            diagnostico = "🟡 Zona en Transición: Superficie cubierta de hollín."
            accion_rover = "MECANISMO ACTIVADO: Tomar muestra de tierra para evaluar pH y humedad."

        # 4. Mostrar resultados en consola
        print(f"--- Archivo: {nombre_archivo} ---")
        print(f"Visión: {clase_detectada.upper()} (Seguridad: {confianza:.1f}%)")
        print(f"Veredicto: {diagnostico}")
        print(f"Comando al Rover: {accion_rover}\n")