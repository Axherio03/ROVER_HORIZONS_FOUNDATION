from ultralytics import YOLO

# 1. Cargar el modelo base de clasificación (Nano: el más rápido y ligero)
model = YOLO('yolov8n-cls.pt')

if __name__ == '__main__':
    print("Iniciando el entrenamiento del modelo del Rover...")
    
    # 2. Entrenar el modelo
    resultados = model.train(
        data='dataset_yolo', # La carpeta generada en el paso anterior
        epochs=30,           # Número de veces que el modelo estudiará el dataset
        imgsz=224,           # Resolución a la que se redimensionarán las imágenes
        batch=16,            # Cantidad de imágenes procesadas a la vez
        device='cpu',        # Cambia a '0' si tienes una tarjeta gráfica NVIDIA configurada
        project='rover_ai',  # Carpeta donde se guardarán los resultados
        name='modelo_v1'     # Nombre de esta versión del entrenamiento
    )
    
    print("Entrenamiento finalizado. El modelo guardado está en: rover_ai/modelo_v1/weights/best.pt")