import splitfolders

# Carpeta donde tienes actualmente tus subcarpetas 'brotes' y 'suelo_carbonizado'
carpeta_origen = "dataset_rover" 
carpeta_destino = "dataset_yolo"

print("Dividiendo imágenes en conjuntos de entrenamiento y validación...")

# Separa el 80% para entrenar y el 20% para validar
splitfolders.ratio(
    carpeta_origen, 
    output=carpeta_destino, 
    seed=42, 
    ratio=(0.8, 0.2)
)

print(f"¡Listo! Dataset organizado en la carpeta '{carpeta_destino}'")