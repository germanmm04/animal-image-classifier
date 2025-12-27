"""Ventana principal de la aplicación Pokédex."""

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize, Qt, QTranslator
from PySide6.QtGui import QFont, QFontDatabase, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

# Añadir raíz del proyecto al path para imports absolutos
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root))

from core.constants import CLASS_NAMES, CONFIDENCE_THRESHOLD, WINDOW_HEIGHT, WINDOW_WIDTH
from model.prediction_service import PredictionService
from storage.animals_repository import AnimalsRepository
from storage.app_settings import AppSettings

# Imports relativos dentro de UI
from animal_detail_screen import AnimalDetailScreen
from main_screen import MainScreen
from pokedex_screen import PokedexScreen
from scan_screen import ScanScreen
from settings_screen import SettingsScreen
from ui_styles import info_rectangle_style


class MainMenu(QMainWindow):
    """Ventana principal de la aplicación."""

    def __init__(self) -> None:
        super().__init__()
        self.settings = AppSettings()
        self._installed_translator: Optional[QTranslator] = None
        self.current_language = self.settings.get_language()
        self.main_container = None
        self.current_image_path: Optional[str] = None
        self.current_screen = "main"
        self.detected_animal_idx: Optional[int] = None
        self.detected_animal_confidence: float = 0.0
        self.registered_animal_idx: Optional[int] = None

        # Rutas de archivos
        project_root = Path(__file__).resolve().parent.parent
        self.data_file = project_root / "data\\pokedex_data.json"
        self.model_path = project_root / "model" / "pokedex_modelv1.keras"

        # Inicialización
        self._load_custom_font()
        self._apply_language(self.current_language)
        self.setWindowTitle(self.tr("Pokedex"))
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))

        # Servicios
        self.animals_repo = AnimalsRepository(CLASS_NAMES, self.data_file)
        self.animals_data = self.animals_repo.animals
        self.predictor = PredictionService(self.model_path, CLASS_NAMES, CONFIDENCE_THRESHOLD)
        self.MainScreen()

    def MainScreen(self) -> None:
        """Muestra la pantalla principal"""
        self.current_screen = "main"
        MainScreen(self)

    def show_scan_screen(self) -> None:
        """Muestra la pantalla de escaneo"""
        self.current_screen = "scan"
        ScanScreen(self)

    def show_pokedex_screen(self) -> None:
        """Muestra la pantalla de Pokédex"""
        self.current_screen = "pokedex"
        PokedexScreen(self)

    def show_settings_screen(self) -> None:
        """Muestra la pantalla de opciones"""
        self.current_screen = "settings"
        SettingsScreen(self)

    def show_animal_detail_screen(self) -> None:
        """Muestra la pantalla de detalles del animal"""
        if hasattr(self, 'selected_animal'):
            self.current_screen = "detail"
            AnimalDetailScreen(self, self.selected_animal)
        else:
            print("No hay animal seleccionado")

    def load_test_image(self) -> None:
        """Carga una imagen de prueba en el cuadro de vista previa"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Seleccionar Imagen de Prueba"),
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.current_image_path = file_path
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Escalar la imagen para que quepa en el cuadro manteniendo la proporción
                scaled_pixmap = pixmap.scaled(
                    440, 440,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.preview_square.setPixmap(scaled_pixmap)
                self.preview_square.setAlignment(Qt.AlignCenter)

    def on_capture_clicked(self) -> None:
        """Realiza la predicción del modelo y muestra el resultado."""
        if not hasattr(self, 'preview_square') or self.preview_square.pixmap() is None:
            if hasattr(self, 'info_rectangle'):
                self.info_rectangle.setText(self.tr("Por favor, carga una imagen primero"))
            return

        if self.preview_square.pixmap().isNull():
            if hasattr(self, 'info_rectangle'):
                self.info_rectangle.setText(self.tr("Por favor, carga una imagen primero"))
            return

        # Mostrar progreso
        if hasattr(self, 'info_rectangle'):
            self.info_rectangle.hide()
        if hasattr(self, 'progress_bar'):
            self.progress_bar.show()
        QApplication.processEvents()

        try:
            pixmap = self.preview_square.pixmap()
            idx, confidence = self.predictor.predict(self.current_image_path, pixmap)

            self.detected_animal_idx = idx
            self.detected_animal_confidence = confidence

            # Formatear resultado
            if idx is None or confidence < CONFIDENCE_THRESHOLD:
                result_text = self.tr("No hemos podido identificar ningún animal")
            else:
                animal_name = self.predictor.class_name(idx)
                result_text = self.tr("¿Quieres registrar este %1?").replace("%1", animal_name)

            # Ocultar progreso y mostrar resultado
            if hasattr(self, 'progress_bar'):
                self.progress_bar.hide()
            if hasattr(self, 'info_rectangle'):
                font_family = self.font().family()
                self.info_rectangle.setStyleSheet(info_rectangle_style(font_family, size=14))
                self.info_rectangle.setText(result_text)
                self.info_rectangle.show()

            # Cambiar botones
            if hasattr(self, 'capture_button'):
                self.capture_button.hide()
            if hasattr(self, 'buttons_container'):
                self.buttons_container.show()

        except Exception as e:
            if hasattr(self, 'progress_bar'):
                self.progress_bar.hide()
            if hasattr(self, 'info_rectangle'):
                error_msg = self.tr("Error al procesar la imagen: %1").replace("%1", str(e))
                self.info_rectangle.setText(error_msg)
                self.info_rectangle.show()
            print(f"Error en predicción: {e}")

    def on_repeat_clicked(self) -> None:
        """Restaura el estado inicial de la pantalla de escaneo."""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.hide()

        if hasattr(self, 'buttons_container'):
            self.buttons_container.hide()
        if hasattr(self, 'capture_button'):
            self.capture_button.show()

        if hasattr(self, 'info_rectangle') and hasattr(self, 'initial_info_text'):
            self.info_rectangle.setText(self.initial_info_text)
            font_family = self.font().family()
            self.info_rectangle.setStyleSheet(info_rectangle_style(font_family, size=10))
            self.info_rectangle.show()

        if hasattr(self, 'preview_square'):
            self.preview_square.clear()
            self.preview_square.setText(self.tr("Vista Previa"))

    def register_animal(self) -> None:
        """Registra el animal detectado y navega a la Pokédex."""
        if self.detected_animal_idx is None:
            if hasattr(self, 'info_rectangle'):
                self.info_rectangle.setText(self.tr("Error: No hay animal detectado"))
            return

        if self.detected_animal_confidence < CONFIDENCE_THRESHOLD:
            return

        if self.detected_animal_idx >= len(self.animals_data):
            return

        # Registrar animal
        self.animals_repo.mark_registered(self.detected_animal_idx, self.current_image_path)
        self.registered_animal_idx = self.detected_animal_idx

        # Navegar a Pokédex
        self.show_pokedex_screen()
    
    def _update_pokedex_list(self) -> None:
        """Actualiza la lista de Pokédex con los estados actualizados."""
        if not (hasattr(self, 'pokedex_list_items') and hasattr(self, 'animals_data')):
            return

        font_family = self.font().family()
        for i, item in enumerate(self.pokedex_list_items):
            if i >= len(self.animals_data):
                continue

            animal = self.animals_data[i]
            layout = item.layout()
            if not layout:
                continue

            # El label de estado es el último widget
            status_label = layout.itemAt(layout.count() - 1).widget()
            if status_label:
                status_text = self.tr("Registrado") if animal['registrado'] else self.tr("No registrado")
                status_color = "#01FF88" if animal['registrado'] else "#888888"
                status_label.setText(status_text)
                status_label.setStyleSheet(
                    f"""
                    QLabel {{
                        color: {status_color};
                        font-size: 14px;
                        font-weight: bold;
                        font-family: "{font_family}";
                    }}
                    """
                )

    def show_main_screen(self) -> None:
        """Vuelve a la pantalla principal"""
        self.MainScreen()

    def _update_time(self) -> None:
        """Actualiza el label de la hora con la hora actual"""
        time_string = self.settings.get_time_string()
        if hasattr(self, 'time_label'):
            self.time_label.setText(time_string)

    def set_language(self, language: str) -> None:
        """Cambia el idioma de la aplicación y recarga la pantalla actual."""
        if language == self.current_language:
            return
        self.settings.set_language(language)
        self._apply_language(language)
        self._reload_current_screen()

    def _apply_language(self, language: str) -> None:
        """Instala el traductor global."""
        app = QApplication.instance()
        if app is None:
            return

        project_root = Path(__file__).resolve().parent.parent
        translator_path = project_root / "translations" / f"app_{language}.qm"

        # Retirar traductor previo
        if self._installed_translator:
            app.removeTranslator(self._installed_translator)
            self._installed_translator = None

        # Cargar nuevo traductor
        translator = QTranslator()
        if translator.load(str(translator_path)):
            app.installTranslator(translator)
            self._installed_translator = translator
        else:
            print(f"No se pudo cargar la traducción: {translator_path}")

        self.current_language = language

    def _reload_current_screen(self) -> None:
        """Reconstruye la pantalla activa para aplicar cambios de idioma."""
        screen = getattr(self, "current_screen", "main")
        if screen == "scan":
            self.show_scan_screen()
        elif screen == "pokedex":
            self.show_pokedex_screen()
        elif screen == "detail" and hasattr(self, "selected_animal"):
            self.show_animal_detail_screen()
        elif screen == "settings":
            self.show_settings_screen()
        else:
            self.show_main_screen()

    def _load_custom_font(self) -> None:
        """Carga la fuente personalizada."""
        font_path = Path(__file__).resolve().parent / "assets" / "fuente.TTF"
        if not font_path.exists():
            return

        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                self.setFont(QFont(families[0], 11))

    def _rounded_icon(self, path: str, size: QSize, radius: int) -> QPixmap:
        """Crea un icono redondeado a partir de una imagen"""
        base = QPixmap(path)
        if base.isNull():
            return QPixmap()

        target_w, target_h = size.width(), size.height()

        # Escalar manteniendo proporción, centrado en el lienzo solicitado
        scaled = base.scaled(
            target_w, target_h, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        x = (target_w - scaled.width()) // 2
        y = (target_h - scaled.height()) // 2

        result = QPixmap(target_w, target_h)
        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        path_clip = QPainterPath()
        path_clip.addRoundedRect(0, 0, target_w, target_h, radius, radius)
        painter.setClipPath(path_clip)
        painter.drawPixmap(x, y, scaled)
        painter.end()
        return result


def main() -> None:
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

