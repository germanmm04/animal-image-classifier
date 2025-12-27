from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pathlib import Path
import json

# Diccionario de colores para cada tipo
TYPE_COLORS = {
    "Normal": "#C0C0C0",  # gris clarito
    "Fuego": "#FF6B35",  # naranja fuego
    "Agua": "#4FC3F7",  # azul agua celeste
    "Planta": "#66BB6A",  # verde planta
    "Eléctrico": "#FFEB3B",  # amarillo eléctrico
    "Hielo": "#B3E5FC",  # azul muy claro
    "Lucha": "#E53935",  # rojo
    "Veneno": "#9C27B0",  # morado
    "Tierra": "#8D6E63",  # marrón tierra
    "Volador": "#E1F5FE",  # azul aún más claro que el hielo
    "Psíquico": "#EC407A",  # rosa
    "Bicho": "#CDDC39",  # verde lima
    "Roca": "#D7CCC8",  # marrón muy claro
    "Fantasma": "#BA68C8",  # lila
    "Dragón": "#2196F3",  # azul
    "Siniestro": "#424242",  # gris muy oscuro
    "Acero": "#90A4AE",  # color metálico
    "Hada": "#F8BBD0",  # rosa claro
    # Variantes con diferentes capitalizaciones
    "normal": "#C0C0C0",
    "fuego": "#FF6B35",
    "agua": "#4FC3F7",
    "planta": "#66BB6A",
    "eléctrico": "#FFEB3B",
    "hielo": "#B3E5FC",
    "lucha": "#E53935",
    "veneno": "#9C27B0",
    "tierra": "#8D6E63",
    "volador": "#E1F5FE",
    "psíquico": "#EC407A",
    "bicho": "#CDDC39",
    "roca": "#D7CCC8",
    "fantasma": "#BA68C8",
    "dragón": "#2196F3",
    "siniestro": "#424242",
    "acero": "#90A4AE",
    "hada": "#F8BBD0",
    "Insecto": "#CDDC39",  # Variante de Bicho
    "insecto": "#CDDC39",
}


def AnimalDetailScreen(main_window, animal: dict) -> None:
    """Crea y muestra la pantalla de detalles del animal"""
    container = QWidget(main_window)
    container.setObjectName("backgroundContainer")
    outer_layout = QVBoxLayout()
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.setSpacing(0)

    # Barra superior (idéntica a la de Pokédex)
    top_bar = QWidget()
    top_bar.setFixedHeight(60)
    top_bar.setStyleSheet(
        """
        QWidget {
            background-color: #1a1a1a;
            border-bottom: 6px solid #545252;
            padding: 20px 10px 10px 10px;
        }
        """
    )
    top_bar_layout = QHBoxLayout(top_bar)
    top_bar_layout.setContentsMargins(0, 0, 10, 0)
    top_bar_layout.setSpacing(0)

    font_family = main_window.font().family()

    # Label "Pokédex" a la izquierda
    pokedex_label = QLabel(main_window.tr("Pokédex"))
    pokedex_label.setAlignment(Qt.AlignLeft)
    pokedex_label.setStyleSheet(
        f"""
        QLabel {{
            color: #ED5647;
            font-size: 24px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    top_bar_layout.addWidget(pokedex_label)

    # Espaciador para empujar el botón atrás a la derecha
    top_bar_layout.addStretch()

    # Botón Volver
    back_button = QPushButton(main_window.tr("Volver"))
    back_button.setStyleSheet(
        f"""
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
    )
    back_button.clicked.connect(main_window.show_pokedex_screen)
    top_bar_layout.addWidget(back_button)
    outer_layout.addWidget(top_bar)

    # Contenedor principal con el contenido
    content_layout = QVBoxLayout()
    content_layout.setAlignment(Qt.AlignTop)
    content_layout.setSpacing(20)
    content_layout.setContentsMargins(20, 20, 20, 20)

    # Cargar información del animal desde JSON
    animal_info = _load_animal_info(main_window, animal['nombre'])

    # Nombre del animal (centrado)
    name_label = QLabel(main_window.tr(animal['nombre']))
    name_label.setAlignment(Qt.AlignCenter)
    name_label.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    content_layout.addWidget(name_label, 0, Qt.AlignCenter)

    # Contenedor para imagen y tipos
    image_types_container = QWidget()
    image_types_layout = QHBoxLayout(image_types_container)
    image_types_layout.setContentsMargins(0, 0, 0, 0)
    image_types_layout.setSpacing(20)
    image_types_layout.setAlignment(Qt.AlignCenter)

    # Imagen del animal
    animal_image = QLabel()
    animal_image.setFixedSize(200, 200)
    animal_image.setAlignment(Qt.AlignCenter)
    animal_image.setStyleSheet(
        f"""
        QLabel {{
            background-color: #292929;
            border: 3px solid #545252;
            border-radius: 8px;
        }}
        """
    )
    
    # Cargar imagen si está disponible
    if animal.get('imagen'):
        image_path = Path(animal['imagen'])
        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    200, 200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                animal_image.setPixmap(scaled_pixmap)
            else:
                animal_image.setText(main_window.tr("Sin imagen"))
        else:
            animal_image.setText(main_window.tr("Sin imagen"))

    image_types_layout.addWidget(animal_image, 0, Qt.AlignCenter)

    # Tipos del animal (a la derecha de la imagen)
    types_container = QWidget()
    types_layout = QVBoxLayout(types_container)
    types_layout.setContentsMargins(0, 0, 0, 0)
    types_layout.setSpacing(10)
    types_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    # Label "Tipo" arriba de los tipos
    tipo_label = QLabel(main_window.tr("Tipo"))
    tipo_label.setAlignment(Qt.AlignLeft)
    tipo_label.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 16px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    types_layout.addWidget(tipo_label)

    if animal_info and 'tipos' in animal_info:
        tipos = animal_info['tipos']
        for tipo in tipos:
            # Obtener el color del tipo, o usar un color por defecto si no existe
            tipo_color = TYPE_COLORS.get(tipo, TYPE_COLORS.get(tipo.capitalize(), "#888888"))
            # Determinar el color del texto según el fondo (claro u oscuro)
            # Colores oscuros que necesitan texto blanco
            dark_colors = ["#424242", "#8D6E63", "#9C27B0", "#E53935", "#2196F3"]
            text_color = "#FFFFFF" if tipo_color in dark_colors else "#1a1a1a"
            
            type_label = QLabel(tipo)
            type_label.setAlignment(Qt.AlignCenter)
            type_label.setStyleSheet(
                f"""
                QLabel {{
                    background-color: {tipo_color};
                    color: {text_color};
                    border: 2px solid #545252;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: "{font_family}";
                    padding: 8px 16px;
                    min-width: 100px;
                }}
                """
            )
            types_layout.addWidget(type_label)

    image_types_layout.addWidget(types_container, 0, Qt.AlignTop | Qt.AlignLeft)
    content_layout.addWidget(image_types_container, 0, Qt.AlignCenter)

    # Cuadro de texto con la información del animal
    info_text = animal_info.get('informacion', main_window.tr('No hay información disponible sobre este animal.')) if animal_info else main_window.tr('No hay información disponible sobre este animal.')
    info_label = QLabel(info_text)
    info_label.setWordWrap(True)
    info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    info_label.setStyleSheet(
        f"""
        QLabel {{
            background-color: #292929;
            border: 2px solid #545252;
            border-radius: 8px;
            color: white;
            font-size: 20px;
            font-family: "{font_family}";
            padding: 15px;
        }}
        """
    )
    content_layout.addWidget(info_label, 1)

    # Widget contenedor del contenido
    content_widget = QWidget()
    content_widget.setLayout(content_layout)
    content_widget.setStyleSheet("background: transparent;")
    outer_layout.addWidget(content_widget, 1)

    container.setLayout(outer_layout)
    # Aplica fondo estático desde assets/fondo.jpg
    background_path = (
        Path(__file__).resolve().parent / "assets" / "fondo.jpg"
    ).as_posix()
    container.setStyleSheet(
        f"""
        #backgroundContainer {{
            background-image: url("{background_path}");
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        """
    )
    main_window.setCentralWidget(container)


def _load_animal_info(main_window, animal_name: str) -> dict:
    """Carga la información del animal desde el archivo JSON"""
    info_file = Path(__file__).resolve().parent.parent / "data\\animals_info.json"
    
    if info_file.exists():
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                animals_info = json.load(f)
            
            # Buscar el animal por nombre
            for animal_info in animals_info:
                if animal_info.get('nombre') == animal_name:
                    return animal_info
        except Exception as e:
            print(f"Error al cargar información del animal desde JSON: {e}")
    
    return None

