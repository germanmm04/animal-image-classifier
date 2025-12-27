"""Estilos CSS reutilizables para la UI."""

from typing import Callable


def get_font_family(main_window) -> str:
    """Obtiene la familia de fuente del main_window."""
    return main_window.font().family()


def top_bar_style() -> str:
    """Estilo para la barra superior."""
    return """
    QWidget {
        background-color: #1a1a1a;
        border-bottom: 6px solid #545252;
        padding: 20px 10px 10px 10px;
    }
    """


def title_label_style(font_family: str, color: str = "#ED5647", size: int = 24) -> str:
    """Estilo para labels de título."""
    return f"""
    QLabel {{
        color: {color};
        font-size: {size}px;
        font-weight: bold;
        font-family: "{font_family}";
    }}
    """


def back_button_style(font_family: str) -> str:
    """Estilo para botón Volver."""
    return f"""
    QPushButton {{
        background-color: #292929;
        color: white;
        border: 2px solid #545252;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
        font-family: "{font_family}";
        padding: 8px 16px;
    }}
    QPushButton:pressed {{
        background-color: #545252;
    }}
    """


def section_container_style() -> str:
    """Estilo para contenedores de sección."""
    return """
    QWidget {
        background-color: #1a1a1a;
        border: 2px solid #545252;
        border-radius: 10px;
    }
    """


def info_label_style(font_family: str, size: int = 12) -> str:
    """Estilo para labels informativos."""
    return f"""
    QLabel {{
        color: white;
        font-size: {size}px;
        font-family: "{font_family}";
    }}
    """


def input_field_style(font_family: str, min_width: int = 120) -> str:
    """Estilo para campos de entrada."""
    return f"""
    QTimeEdit, QComboBox {{
        background-color: #292929;
        color: white;
        border: 2px solid #545252;
        border-radius: 8px;
        font-size: 16px;
        font-family: "{font_family}";
        padding: 6px 10px;
        min-width: {min_width}px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #292929;
        color: white;
        border: 2px solid #545252;
        selection-background-color: #ED5647;
    }}
    """


def primary_button_style(font_family: str) -> str:
    """Estilo para botón primario (rojo)."""
    return f"""
    QPushButton {{
        background-color: #ED5647;
        color: white;
        border: 2px solid #545252;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        font-family: "{font_family}";
        padding: 8px 16px;
    }}
    QPushButton:pressed {{
        background-color: #545252;
    }}
    """


def secondary_button_style(font_family: str) -> str:
    """Estilo para botón secundario (gris)."""
    return f"""
    QPushButton {{
        background-color: #292929;
        color: white;
        border: 2px solid #545252;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        font-family: "{font_family}";
        padding: 8px 16px;
    }}
    QPushButton:pressed {{
        background-color: #545252;
    }}
    """


def info_rectangle_style(font_family: str, size: int = 10) -> str:
    """Estilo para rectángulo informativo."""
    return f"""
    QLabel {{
        background-color: #292929;
        border: 2px solid #545252;
        border-radius: 8px;
        color: white;
        font-size: {size}px;
        font-family: "{font_family}";
        padding: 10px;
    }}
    """


def background_container_style(background_path: str) -> str:
    """Estilo para contenedor con fondo."""
    return f"""
    #backgroundContainer {{
        background-image: url("{background_path}");
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    """

