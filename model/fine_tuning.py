# FINE-TUNING RE-COMPILADO Y OPTIMIZADO CON KERAS

from tensorflow.keras.models import load_model
from tensorflow import keras
from tensorflow.keras.optimizers import Adam

# --- PARÁMETROS ---
FINE_TUNE_EPOCHS = 10
NEW_LEARNING_RATE = 1e-5
NUM_LAYERS_TO_UNFREEZE = 30 # Número de capas finales a descongelar

DATASET_DIR = "../Dataset/train"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42
EPOCHS = 20
VALIDATION_SPLIT = 0.2

train_ds = keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

val_ds = keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

#1. Cargar el modelo entrenado y la base
try:
    model = load_model("pokedex_modelv0.keras")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    exit()

# Suponiendo que la base MobileNetV3Small es la capa en el índice 2:
base_model = model.layers[2]

#2. Preparación de la Base para Fine-Tuning

#Establece TODA la base como entrenable
base_model.trainable = True

#Congela todas las capas EXCEPTO las últimas N capas
for layer in base_model.layers[:-NUM_LAYERS_TO_UNFREEZE]:
    layer.trainable = False

#Re-compilar el modelo con nuevo Learning Rate

print(f"Capas entrenables en el modelo base: {len([l for l in base_model.layers if l.trainable])}")
print(f"Tasa de Aprendizaje: {NEW_LEARNING_RATE}")

#La re-compilación es OBLIGATORIA después de cambiar 'trainable'
model.compile(
    optimizer=Adam(learning_rate=NEW_LEARNING_RATE), # Tasa MÁS BAJA
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

#4. Entrenar nuevamente (Fine-Tuning)

print("Comenzando la fase de Fine-Tuning...")

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS
)

#5. Guardar el modelo final ajustado
model.save("pokedex_modelv1.keras")
print("Fine-tuning completado y modelo guardado correctamente.")