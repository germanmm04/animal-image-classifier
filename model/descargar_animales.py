import fiftyone as fo
import fiftyone.zoo as foz
import os

DIRECTORIO_RAIZ = "Dataset"
CONJUNTO_DESTINO = "train"

CLASES_A_DESCARGAR = [
    ("Polar bear", 1000),

]

for clase, num_imagenes in CLASES_A_DESCARGAR:

    nombre_carpeta_animal = clase.replace(" ", "_")

    carpeta_final = os.path.join(
        DIRECTORIO_RAIZ,
        CONJUNTO_DESTINO,
        nombre_carpeta_animal
    )

    os.makedirs(carpeta_final, exist_ok=True)

    print(f"\n--- Iniciando descarga de {num_imagenes} imágenes de: {clase} ---")
    print(f"-> Exportando a: {carpeta_final}")

    try:
        dataset = foz.load_zoo_dataset(
            "open-images-v7",
            split=CONJUNTO_DESTINO,
            label_types=["detections"],
            classes=[clase],
            max_samples=num_imagenes,
            shuffle=True,
        )

        dataset.export(
            export_dir=carpeta_final,
            dataset_type=fo.types.ImageDirectory,
        )

        print(f"✅ Descarga de {clase} completada.")

        dataset.delete()  # <-- EVITA QUE LA SIGUIENTE ITERACIÓN REUTILICE IMÁGENES

    except Exception as e:
        print(f"❌ ERROR en clase {clase}: {e}")
        continue

print("\n--- ¡Proceso de descarga completado! ---")
