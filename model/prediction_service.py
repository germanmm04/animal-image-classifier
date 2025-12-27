from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from PIL import Image
from PySide6.QtGui import QPixmap
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image


class PredictionService:
    """Encapsula la carga del modelo y la predicción."""

    def __init__(self, model_path: Path, class_names: list[str], threshold: float) -> None:
        self._model_path = model_path
        self._class_names = class_names
        self._threshold = threshold
        self._model = None

    def ensure_model_loaded(self) -> None:
        if self._model is None:
            self._model = load_model(str(self._model_path))

    def predict(self, image_path: Optional[str], fallback_pixmap: Optional[QPixmap]) -> Tuple[Optional[int], float]:
        """Devuelve (idx, confidence). idx es None si no se identifica."""
        self.ensure_model_loaded()
        if image_path:
            img = keras_image.load_img(image_path, target_size=(224, 224))
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
        elif fallback_pixmap is not None:
            img_array = self._pixmap_to_array(fallback_pixmap)
        else:
            raise ValueError("No hay imagen para predecir")

        predictions = self._model.predict(img_array, verbose=0)
        idx = int(np.argmax(predictions))
        confidence = float(predictions[0][idx])
        if confidence < self._threshold:
            return None, confidence
        return idx, confidence

    def class_name(self, idx: int) -> str:
        if 0 <= idx < len(self._class_names):
            return self._class_names[idx]
        return ""

    def _pixmap_to_array(self, pixmap: QPixmap) -> np.ndarray:
        image = pixmap.toImage()
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        arr = arr[:, :, :3]
        pil_image = Image.fromarray(arr.astype("uint8"), "RGB")
        pil_image = pil_image.resize((224, 224))
        img_array = np.array(pil_image).astype("float32")
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array

