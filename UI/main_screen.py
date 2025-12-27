from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect,
    QLabel,
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon
from pathlib import Path


def MainScreen(main_window) -> None:
    """Crea y muestra la pantalla principal del menú"""
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
    top_bar_layout.setContentsMargins(0, 0, 0, 0)
    top_bar_layout.setSpacing(0)

    font_family = main_window.font().family()

    # Label para la hora actual
    main_window.time_label = QLabel()
    main_window.time_label.setAlignment(Qt.AlignLeft)
    main_window.time_label.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    main_window._update_time()
    top_bar_layout.addWidget(main_window.time_label)

    # Espaciador para empujar el título a la derecha
    top_bar_layout.addStretch()

    title_label = QLabel(main_window.tr("Pokédex"))
    title_label.setAlignment(Qt.AlignRight)
    title_label.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 24px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    top_bar_layout.addWidget(title_label)
    outer_layout.addWidget(top_bar)

    # Timer para actualizar la hora cada minuto
    main_window.time_timer = QTimer(main_window)
    main_window.time_timer.timeout.connect(main_window._update_time)
    main_window.time_timer.start(60000)  # Actualizar cada 60000ms (1 minuto)

    grid = QGridLayout()
    grid.setAlignment(Qt.AlignCenter)
    grid.setHorizontalSpacing(30)
    grid.setVerticalSpacing(30)
    button_texts = [
        main_window.tr("Escanear"),
        main_window.tr("Pokédex"),
        main_window.tr("Opciones"),
        main_window.tr("Amigos"),
        main_window.tr("Registros"),
        main_window.tr("Perfil"),
        main_window.tr("Logros"),
        main_window.tr("Actualizar"),
        main_window.tr("Salir"),
    ]

    icon_camera_path = (
        Path(__file__).resolve().parent / "assets" / "icono_camara.png"
    ).as_posix()
    icon_pokedex_path = (
        Path(__file__).resolve().parent / "assets" / "icono_pokedex.png"
    ).as_posix()
    icon_settings_path = (
        Path(__file__).resolve().parent / "assets" / "icono_ajustes.png"
    ).as_posix()
    icon_friends_path = (
        Path(__file__).resolve().parent / "assets" / "icono_amigos.png"
    ).as_posix()
    icon_register_path = (
        Path(__file__).resolve().parent / "assets" / "icono_registro.png"
    ).as_posix()
    icon_logros_path = (
        Path(__file__).resolve().parent / "assets" / "icono_logros.png"
    ).as_posix()
    icon_update_path = (
        Path(__file__).resolve().parent / "assets" / "icono_actualizar.png"
    ).as_posix()
    icon_exit_path = (
        Path(__file__).resolve().parent / "assets" / "icono_salir.png"
    ).as_posix()
    icon_profile_path = (
        Path(__file__).resolve().parent / "assets" / "icono_perfil.png"
    ).as_posix()

    # Usamos la familia de fuente cargada (o la actual si falló)
    font_family = main_window.font().family()

    for row in range(3):
        for col in range(3):
            index = row * 3 + col
            label_text = button_texts[index]
            button = QPushButton("")
            button.setFixedSize(120, 120)
            if index == 0:
                rounded_icon = main_window._rounded_icon(
                    icon_camera_path, QSize(88, 88), 44
                )
                button.setIcon(QIcon(rounded_icon))
                button.setIconSize(QSize(88, 88))
                # Conectar el botón Escanear a la pantalla de escaneo
                button.clicked.connect(main_window.show_scan_screen)
            if index == 1:
                rounded_icon = main_window._rounded_icon(
                    icon_pokedex_path, QSize(88, 88), 44
                )
                button.setIcon(QIcon(rounded_icon))
                button.setIconSize(QSize(88, 88))
                # Conectar el botón Pokédex a la pantalla de Pokédex
                button.clicked.connect(main_window.show_pokedex_screen)
            if index == 2:
                button.setIcon(QIcon(icon_settings_path))
                button.setIconSize(QSize(110, 110))
                button.clicked.connect(main_window.show_settings_screen)
            if index == 3:
                button.setIcon(QIcon(icon_friends_path))
                button.setIconSize(QSize(88, 88))
            if index == 4:
                button.setIcon(QIcon(icon_register_path))
                button.setIconSize(QSize(100, 100))
            if index == 5:
                button.setIcon(QIcon(icon_logros_path))
                button.setIconSize(QSize(88, 88))
            if index == 6:
                button.setIcon(QIcon(icon_update_path))
                button.setIconSize(QSize(100, 100))
            if index == 7:
                button.setIcon(QIcon(icon_exit_path))
                button.setIconSize(QSize(88, 88))
            if index == 8:
                rounded_icon = main_window._rounded_icon(
                    icon_profile_path, QSize(88, 88), 25
                )
                button.setIcon(QIcon(rounded_icon))
                button.setIconSize(QSize(88, 88))
            shadow = QGraphicsDropShadowEffect(main_window)
            shadow.setBlurRadius(16)
            shadow.setXOffset(4)
            shadow.setYOffset(4)
            shadow.setColor(Qt.black)
            button.setGraphicsEffect(shadow)
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #292929;
                    background-image: none;
                    color: white;
                    border: 3.5px solid #545252;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: "{font_family}";
                }}
                QPushButton:pressed {{
                    background-color: #545252;
                }}
                """
            )

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                f"""
                QLabel {{
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: "{font_family}";
                }}
                """
            )

            cell = QWidget()
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(15)
            cell_layout.addWidget(button, 0, Qt.AlignCenter)
            cell_layout.addWidget(label, 0, Qt.AlignCenter)

            grid.addWidget(cell, row, col)

    # Contenedor centrado para el grid
    grid_container = QWidget()
    grid_container_layout = QVBoxLayout(grid_container)
    grid_container_layout.setAlignment(Qt.AlignCenter)
    grid_container_layout.setSpacing(30)
    grid_container_layout.addLayout(grid)
    grid_container.setStyleSheet("background: transparent;")
    
    outer_layout.addWidget(grid_container, 1)
    container.setLayout(outer_layout)
    # Aplica fondo estático desde assets/fondo.jpg sólo al contenedor principal
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
    main_window.main_container = container
    main_window.setCentralWidget(container)

