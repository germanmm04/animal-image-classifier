import json
from pathlib import Path
from typing import List, Dict, Optional


class AnimalsRepository:
    """Gestor de persistencia para los animales de la Pokédex."""

    def __init__(self, class_names: List[str], data_file: Path) -> None:
        self._class_names = class_names
        self._data_file = data_file
        self._animals: List[Dict] = []
        self._init_base()
        self._load_from_disk()

    @property
    def animals(self) -> List[Dict]:
        return self._animals

    def get(self, index: int) -> Optional[Dict]:
        if 0 <= index < len(self._animals):
            return self._animals[index]
        return None

    def mark_registered(self, index: int, image_path: Optional[str] = None) -> None:
        animal = self.get(index)
        if animal is None:
            return
        animal["registrado"] = True
        if image_path:
            animal["imagen"] = image_path
        self._save_to_disk()

    def _init_base(self) -> None:
        self._animals = []
        for idx, name in enumerate(self._class_names):
            self._animals.append(
                {
                    "id": idx + 1,
                    "nombre": name,
                    "imagen": None,
                    "registrado": False,
                }
            )

    def _load_from_disk(self) -> None:
        if not self._data_file.exists():
            return
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
            saved_dict = {entry["nombre"]: entry for entry in saved}
            for i, animal in enumerate(self._animals):
                if animal["nombre"] in saved_dict:
                    saved_animal = saved_dict[animal["nombre"]]
                    self._animals[i]["registrado"] = saved_animal.get("registrado", False)
                    self._animals[i]["imagen"] = saved_animal.get("imagen")
        except Exception as exc:  # pragma: no cover - lectura simple
            print(f"Error al cargar datos desde JSON: {exc}")

    def _save_to_disk(self) -> None:
        try:
            data_to_save = []
            for animal in self._animals:
                data_to_save.append(
                    {
                        "id": animal["id"],
                        "nombre": animal["nombre"],
                        "imagen": animal.get("imagen"),
                        "registrado": animal.get("registrado", False),
                    }
                )
            with open(self._data_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        except Exception as exc:  # pragma: no cover - escritura simple
            print(f"Error al guardar datos en JSON: {exc}")

