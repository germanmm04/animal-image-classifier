import json
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QDateTime


class AppSettings:
    """Gestor simple para idioma y hora global."""

    def __init__(self) -> None:
        self.settings_path = Path(__file__).resolve().parent.parent / "data\\settings.json"
        self._data = {
            "language": "es",
            "custom_time": None,
        }
        self._load()

    def _load(self) -> None:
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                if isinstance(saved, dict):
                    self._data.update(saved)
            except Exception as exc:  # pragma: no cover - lectura simple
                print(f"Error al cargar settings: {exc}")

    def _save(self) -> None:
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as exc:  # pragma: no cover - escritura simple
            print(f"Error al guardar settings: {exc}")

    def get_language(self) -> str:
        return self._data.get("language", "es")

    def set_language(self, language: str) -> None:
        self._data["language"] = language
        self._save()

    def get_custom_time(self) -> Optional[str]:
        value = self._data.get("custom_time")
        return value if value else None

    def set_custom_time(self, time_str: Optional[str]) -> None:
        self._data["custom_time"] = time_str
        self._save()

    def clear_custom_time(self) -> None:
        self.set_custom_time(None)

    def get_time_string(self) -> str:
        """Devuelve la hora a mostrar (personalizada o la actual)."""
        custom = self.get_custom_time()
        if custom:
            return custom
        current_time = QDateTime.currentDateTime()
        return current_time.toString("hh:mm")

