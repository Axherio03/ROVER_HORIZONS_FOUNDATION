import os
import requests
from ultralytics import YOLO

# 1. Cargar el modelo entrenado
modelo = YOLO(r'C:\Users\USER\Desktop\ROVER\classify\rover_ai\modelo_v1\weights\best.pt')

# 2. Configurar la URL de la cámara del Rover
# En modo AP, el ESP32 suele tener la IP 192.168.4.1. Si tu monitor serie muestra otra, cámbiala aquí.
url_captura = "http://192.168.4.1/capture"
ruta_imagen_temporal = "captura_actual.jpg"

print("📸 Solicitando fotografía al Rover...")

try:
    # 3. Descargar la foto del ESP32-CAM
    respuesta = requests.get(url_captura, timeout=10)
    
    if respuesta.status_code == 200:
        # Guardar la imagen en la PC
        with open(ruta_imagen_temporal, 'wb') as archivo:
            archivo.write(respuesta.content)
        print("✅ Fotografía recibida. Iniciando análisis de suelo...\n")
        
        # 4. Pasar la foto al modelo YOLO
        resultados = modelo(ruta_imagen_temporal, verbose=False)
        
        # Extraer datos
        nombres_clases = resultados[0].names
        clase_id = resultados[0].probs.top1
        clase_detectada = nombres_clases[clase_id]
        confianza = resultados[0].probs.top1conf.item() * 100
        
        # 5. LÓGICA DE DECISIÓN DEL ROVER
        diagnostico = ""
        accion_rover = ""

        if confianza < 55.0:
            diagnostico = "⚠️ Imagen confusa o mezclada."
            accion_rover = "MECANISMO ACTIVADO: Tomar muestra de tierra para análisis por sensores."
        elif clase_detectada == "brotes":
            diagnostico = "🟢 Viable: Regeneración natural detectada."
            accion_rover = "AVANZAR: No requiere muestreo. Suelo apto para reforestar."
        elif clase_detectada == "ceniza_blanca": 
            diagnostico = "🔴 Inviable: Daño extremo. Suelo estéril superficialmente."
            accion_rover = "AVANZAR: No requiere muestreo. Marcar zona en el mapa."
        elif clase_detectada == "suelo_carbonizado":
            diagnostico = "🟡 Zona en Transición: Superficie cubierta de hollín."
            accion_rover = "MECANISMO ACTIVADO: Tomar muestra de tierra para evaluar pH y humedad."

        # 6. Mostrar resultados
        print(f"--- ANÁLISIS EN TIEMPO REAL ---")
        print(f"Visión: {clase_detectada.upper()} (Seguridad: {confianza:.1f}%)")
        print(f"Veredicto: {diagnostico}")
        print(f"Comando a enviar al Rover: {accion_rover}\n")
        
    else:
        print(f"❌ Error del servidor de la cámara. Código: {respuesta.status_code}")

except requests.exceptions.RequestException as e:
    print("❌ No se pudo conectar con el Rover.")
    print("Asegúrate de que la laptop esté conectada al WiFi 'ESP32-CAM Robot' y que el rover esté encendido.")