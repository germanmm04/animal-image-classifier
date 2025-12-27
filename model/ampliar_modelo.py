import tensorflow as tf
from tensorflow.keras import layers, Model, optimizers
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import image_dataset_from_directory

# CONFIGURACIÓN
OLD_MODEL_PATH = "pokedex_modelv1.keras"
NEW_DATASET_DIR = "./dataset_nuevo"  #Nuevo dataset
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42
VALIDATION_SPLIT = 0.2
FINE_TUNE_EPOCHS = 10
LEARNING_RATE = 1e-4

# CARGAR NUEVO DATASET
train_ds_new = image_dataset_from_directory(
    NEW_DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

val_ds_new = image_dataset_from_directory(
    NEW_DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

# OPTIMIZACIÓN PIPELINE
AUTOTUNE = tf.data.AUTOTUNE
train_ds_new = train_ds_new.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds_new = val_ds_new.cache().prefetch(buffer_size=AUTOTUNE)

# CARGAR MODELO ANTIGUO
model_old = load_model(OLD_MODEL_PATH)

# Extraer el backbone y la capa anterior a la salida
base_model = model_old.layers[2]  # MobileNetV3Small
x = model_old.layers[3](base_model.output)  # GlobalAveragePooling2D
x = model_old.layers[4](x)  # BatchNormalization
x = model_old.layers[5](x)  # Dense(128)
x = model_old.layers[6](x)  # Dropout


# NUEVA CANTIDAD DE CLASES
NUM_CLASSES_NEW = len(train_ds_new.class_names)  # si solo entrenas nuevas clases

# NUEVA CAPA FINAL
outputs = layers.Dense(NUM_CLASSES_NEW, activation="softmax")(x)
model_new = Model(inputs=base_model.input, outputs=outputs)

# FINE-TUNING PARCIAL

# Congelar todo menos las últimas 30 capas
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Compilar
model_new.compile(
    optimizer=optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ENTRENAMIENTO
history_fine = model_new.fit(
    train_ds_new,
    validation_data=val_ds_new,
    epochs=FINE_TUNE_EPOCHS
)

# GUARDAR MODELO FINAL
MODEL_FINAL_PATH = "mobilenetv3_animales_ampliado.keras"
model_new.save(MODEL_FINAL_PATH)
print("Modelo ampliado y fine-tuned guardado en:", MODEL_FINAL_PATH)
