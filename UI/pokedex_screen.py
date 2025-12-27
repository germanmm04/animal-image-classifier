from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pathlib import Path
import json
from core.constants import CLASS_NAMES


def PokedexScreen(main_window) -> None:
    """Crea y muestra la pantalla de Pokédex"""
    container = QWidget(main_window)
    container.setObjectName("backgroundContainer")
    outer_layout = QVBoxLayout()
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.setSpacing(0)

    # Barra superior
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

    # Botón Atrás
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
    back_button.clicked.connect(main_window.show_main_screen)
    top_bar_layout.addWidget(back_button)
    outer_layout.addWidget(top_bar)

    # Contenedor principal dividido en dos mitades
    main_content = QWidget()
    main_layout = QVBoxLayout(main_content)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    # ========== MITAD SUPERIOR: Detalle del animal ==========
    detail_container = QWidget()
    detail_container.setFixedHeight(400)
    detail_layout = QVBoxLayout(detail_container)
    detail_layout.setAlignment(Qt.AlignCenter)
    detail_layout.setSpacing(20)
    detail_layout.setContentsMargins(20, 20, 20, 20)
    detail_container.setStyleSheet(
        """
        QWidget {
            background-color: #1a1a1a;
            border-bottom: 3px solid #545252;
        }
        """
    )

    # Imagen del animal
    main_window.pokedex_detail_image = QLabel()
    main_window.pokedex_detail_image.setFixedSize(200, 200)
    main_window.pokedex_detail_image.setAlignment(Qt.AlignCenter)
    main_window.pokedex_detail_image.setStyleSheet(
        """
        QLabel {
            background-color: #292929;
            border: 3px solid #545252;
            border-radius: 8px;
        }
        """
    )
    main_window.pokedex_detail_image.setText(main_window.tr("Sin imagen"))
    detail_layout.addWidget(main_window.pokedex_detail_image, 0, Qt.AlignCenter)

    # Nombre del animal
    main_window.pokedex_detail_name = QLabel(main_window.tr("Selecciona un animal"))
    main_window.pokedex_detail_name.setAlignment(Qt.AlignCenter)
    main_window.pokedex_detail_name.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 24px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    detail_layout.addWidget(main_window.pokedex_detail_name, 0, Qt.AlignCenter)

    # Botón "Ver ficha"
    view_button = QPushButton(main_window.tr("Ver ficha"))
    view_button.setFixedSize(150, 40)
    view_button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #ED5647;
            color: white;
            border: 2px solid #545252;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    view_button.clicked.connect(main_window.show_animal_detail_screen)
    detail_layout.addWidget(view_button, 0, Qt.AlignCenter)
    main_window.pokedex_view_button = view_button

    # Estado vacío cuando no hay registro
    main_window.pokedex_empty_label = QLabel(main_window.tr("Sin información almacenada"))
    main_window.pokedex_empty_label.setAlignment(Qt.AlignCenter)
    main_window.pokedex_empty_label.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 15px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    main_window.pokedex_empty_label.hide()
    detail_layout.addWidget(main_window.pokedex_empty_label, 0, Qt.AlignCenter)

    main_layout.addWidget(detail_container)

    # ========== MITAD INFERIOR: Lista de animales ==========
    list_container = QWidget()
    list_layout = QVBoxLayout(list_container)
    list_layout.setContentsMargins(10, 10, 10, 10)
    list_layout.setSpacing(5)

    # ScrollArea para la lista
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet(
        """
        QScrollArea {
            border: none;
            background-color: #1a1a1a;
        }
        QScrollBar:vertical {
            background-color: #292929;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #545252;
            border-radius: 5px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #ED5647;
        }
        """
    )

    # Widget contenedor de los elementos de la lista
    list_widget = QWidget()
    list_widget_layout = QVBoxLayout(list_widget)
    list_widget_layout.setContentsMargins(0, 0, 0, 0)
    list_widget_layout.setSpacing(5)

    # Cargar datos desde JSON (siempre leer del archivo, no de memoria)
    animals_data = _load_animals_from_json(main_window)
    
    # Crear los elementos de la lista
    main_window.pokedex_list_items = []
    for animal in animals_data:
        item = _create_list_item(main_window, animal)
        main_window.pokedex_list_items.append(item)
        list_widget_layout.addWidget(item)
    
    # Guardar referencia a los datos cargados
    main_window.animals_data = animals_data

    list_widget_layout.addStretch()
    scroll_area.setWidget(list_widget)
    list_layout.addWidget(scroll_area)
    main_layout.addWidget(list_container, 1)

    outer_layout.addWidget(main_content, 1)

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

    # Seleccionar el animal registrado si existe, sino el primero
    if (
            hasattr(main_window, 'registered_animal_idx')
            and main_window.registered_animal_idx is not None
            and main_window.registered_animal_idx < len(main_window.pokedex_list_items)
    ):
        animal_idx = main_window.registered_animal_idx
        _select_animal(
            main_window,
            main_window.animals_data[animal_idx],
            main_window.pokedex_list_items[animal_idx]
        )
        delattr(main_window, 'registered_animal_idx')

    elif main_window.pokedex_list_items:
        _select_animal(
            main_window,
            main_window.animals_data[0],
            main_window.pokedex_list_items[0]
        )


def _load_animals_from_json(main_window) -> list:
    """Carga los datos de animales desde el archivo JSON (siempre lee del disco)"""
    data_file = Path(__file__).resolve().parent.parent / "data\\pokedex_data.json"
    
    # Inicializar estructura base con todos los animales
    animals_data = []
    for idx, animal_name in enumerate(CLASS_NAMES):
        animals_data.append({
            'id': idx + 1,
            'nombre': animal_name,
            'imagen': None,
            'registrado': False
        })
    
    # Cargar datos guardados desde JSON si existe
    if data_file.exists():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            # Crear diccionario para búsqueda rápida por nombre
            saved_dict = {animal['nombre']: animal for animal in saved_data}
            
            # Actualizar los datos con los guardados
            for i, animal in enumerate(animals_data):
                if animal['nombre'] in saved_dict:
                    saved_animal = saved_dict[animal['nombre']]
                    animals_data[i]['registrado'] = saved_animal.get('registrado', False)
                    animals_data[i]['imagen'] = saved_animal.get('imagen', None)
        except Exception as e:
            print(f"Error al cargar datos desde JSON en Pokédex: {e}")
    
    return animals_data


def _create_list_item(main_window, animal: dict) -> QFrame:
    """Crea un elemento de la lista de animales"""
    font_family = main_window.font().family()
    
    item = QFrame()
    item.setFixedHeight(60)
    item.setStyleSheet(
        f"""
        QFrame {{
            background-color: #292929;
            border: 2px solid #545252;
            border-radius: 8px;
            padding: 5px;
        }}
        """
    )
    item.setObjectName(f"animal_{animal['id']}")
    
    layout = QHBoxLayout(item)
    layout.setContentsMargins(8, 5, 8, 5)
    layout.setSpacing(10)

    # Nombre del animal
    name_label = QLabel(main_window.tr(animal['nombre']))
    name_label.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 12px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    layout.addWidget(name_label, 1)

    # Estado (Registrado/No registrado)
    status_text = main_window.tr("Registrado") if animal['registrado'] else main_window.tr("No registrado")
    status_color = "#FFFFFF" if animal['registrado'] else "#888888"
    status_bg_color = "#ED5647" if animal['registrado'] else "transparent"
    status_label = QLabel(status_text)
    status_label.setAlignment(Qt.AlignCenter)
    status_label.setFixedSize(200, 30)  # Tamaño más grande para que quepa mejor el texto
    status_label.setStyleSheet(
        f"""
        QLabel {{
            background-color: {status_bg_color};
            color: {status_color};
            font-size: 13px;
            font-weight: bold;
            font-family: "{font_family}";
            padding: 0px;
            border-radius: 4px;
        }}
        """
    )
    layout.addWidget(status_label, 0, Qt.AlignRight | Qt.AlignVCenter)

    # Hacer el item clickeable
    item.mousePressEvent = lambda event: _select_animal(main_window, animal, item)
    
    return item


def _select_animal(main_window, animal: dict, item: QFrame) -> None:
    """Selecciona un animal y actualiza la vista de detalle"""
    font_family = main_window.font().family()
    
    # Deseleccionar todos los items
    for list_item in main_window.pokedex_list_items:
        list_item.setStyleSheet(
            f"""
            QFrame {{
                background-color: #292929;
                border: 2px solid #545252;
                border-radius: 8px;
                padding: 5px;
            }}
            """
        )
    
    # Seleccionar el item actual
    item.setStyleSheet(
        f"""
        QFrame {{
            background-color: #ED5647;
            border: 3px solid #545252;
            border-radius: 8px;
            padding: 5px;
        }}
        """
    )
    
    # Guardar el animal seleccionado actualmente
    main_window.selected_animal = animal

    # Mostrar u ocultar detalles según registro
    is_registered = animal.get('registrado', False)
    main_window.pokedex_detail_image.setVisible(is_registered)
    main_window.pokedex_detail_name.setVisible(is_registered)
    main_window.pokedex_view_button.setVisible(is_registered)
    main_window.pokedex_empty_label.setVisible(not is_registered)

    if not is_registered:
        # Limpiar detalles anteriores
        main_window.pokedex_detail_image.clear()
        main_window.pokedex_detail_image.setText("")
        main_window.pokedex_detail_name.setText("")
        return

    # Actualizar la vista de detalle
    main_window.pokedex_detail_name.setText(main_window.tr(animal['nombre']))
    
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
                main_window.pokedex_detail_image.setPixmap(scaled_pixmap)
            else:
                main_window.pokedex_detail_image.setText(main_window.tr("Sin imagen"))
        else:
            main_window.pokedex_detail_image.setText(main_window.tr("Sin imagen"))
    else:
        # Intentar cargar imagen desde assets si existe
        image_path = (
            Path(__file__).resolve().parent / "assets" / f"{animal['nombre'].lower()}.png"
        )
        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    200, 200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                main_window.pokedex_detail_image.setPixmap(scaled_pixmap)
            else:
                main_window.pokedex_detail_image.setText(main_window.tr("Sin imagen"))
        else:
            main_window.pokedex_detail_image.setText(main_window.tr("Sin imagen"))

