from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect,
    QLabel,
    QProgressBar,
)
from PySide6.QtCore import Qt
from pathlib import Path


def ScanScreen(main_window) -> None:
    """Crea y muestra la pantalla de escaneo"""
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

    # Label "Escanear" a la izquierda
    scan_label = QLabel(main_window.tr("Escanear"))
    scan_label.setAlignment(Qt.AlignLeft)
    scan_label.setStyleSheet(
        f"""
        QLabel {{
            color: #01FF88;
            font-size: 24px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    top_bar_layout.addWidget(scan_label)

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

    # Contenedor principal con el cuadrado y el botón
    content_layout = QVBoxLayout()
    content_layout.setAlignment(Qt.AlignCenter)
    content_layout.setSpacing(20)
    content_layout.setContentsMargins(20, 10, 20, 30)

    # Cuadrado para la vista previa (simulado con un QLabel)
    main_window.preview_square = QLabel()
    main_window.preview_square.setFixedSize(440, 440)
    main_window.preview_square.setAlignment(Qt.AlignCenter)
    main_window.preview_square.setText(main_window.tr("Vista Previa"))
    main_window.preview_square.setStyleSheet(
        f"""
        QLabel {{
            background-color: #292929;
            border: 3.5px solid #545252;
            border-radius: 8px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    content_layout.addWidget(main_window.preview_square, 0, Qt.AlignCenter)

    # Botón para cargar imagen de prueba
    load_image_button = QPushButton(main_window.tr("Cargar Imagen de Prueba"))
    load_image_button.setFixedSize(200, 35)
    load_image_button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #292929;
            color: white;
            border: 2px solid #545252;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
            font-family: "{font_family}";
            padding: 5px;
        }}
        QPushButton:pressed {{
            background-color: #545252;
        }}
        """
    )
    load_image_button.clicked.connect(main_window.load_test_image)
    content_layout.addWidget(load_image_button, 0, Qt.AlignCenter)

    # Rectángulo informativo
    main_window.initial_info_text = main_window.tr("Mantén una buena iluminación y encuadre para mejorar la identificación")
    main_window.info_rectangle = QLabel(main_window.initial_info_text)
    main_window.info_rectangle.setWordWrap(True)
    main_window.info_rectangle.setFixedSize(440, 60)
    main_window.info_rectangle.setAlignment(Qt.AlignLeft)
    main_window.info_rectangle.setStyleSheet(
        f"""
        QLabel {{
            background-color: #292929;
            border: 2px solid #545252;
            border-radius: 8px;
            color: white;
            font-size: 10px;
            font-family: "{font_family}";
            padding: 10px;
        }}
        """
    )
    content_layout.addWidget(main_window.info_rectangle, 0, Qt.AlignCenter)

    # Barra de progreso (inicialmente oculta)
    main_window.progress_bar = QProgressBar()
    main_window.progress_bar.setFixedSize(440, 60)
    main_window.progress_bar.setRange(0, 0)  # Modo indeterminado
    main_window.progress_bar.setStyleSheet(
        f"""
        QProgressBar {{
            background-color: #292929;
            border: 2px solid #545252;
            border-radius: 8px;
            color: white;
            font-size: 12px;
            font-weight: bold;
            font-family: "{font_family}";
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: #01FF88;
            border-radius: 6px;
        }}
        """
    )
    main_window.progress_bar.hide()  # Oculto inicialmente
    content_layout.addWidget(main_window.progress_bar, 0, Qt.AlignCenter)

    # Botón Capturar
    main_window.capture_button = QPushButton(main_window.tr("¡Capturar!"))
    main_window.capture_button.setFixedSize(240, 60)
    shadow = QGraphicsDropShadowEffect(main_window)
    shadow.setBlurRadius(16)
    shadow.setXOffset(4)
    shadow.setYOffset(4)
    shadow.setColor(Qt.black)
    main_window.capture_button.setGraphicsEffect(shadow)
    main_window.capture_button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #01FF88;
            color: white;
            border: 2px solid #545252;
            border-radius: 30px;
            font-size: 22px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        QPushButton:pressed {{
            background-color: #545252;
        }}
        """
    )
    main_window.capture_button.clicked.connect(main_window.on_capture_clicked)
    content_layout.addWidget(main_window.capture_button, 0, Qt.AlignCenter)

    # Contenedor para los botones Registrar y Repetir (inicialmente oculto)
    buttons_container = QWidget()
    buttons_layout = QHBoxLayout(buttons_container)
    buttons_layout.setSpacing(20)
    buttons_layout.setContentsMargins(0, 0, 0, 0)

    # Botón Registrar
    register_button = QPushButton(main_window.tr("Registrar"))
    register_button.setFixedSize(200, 60)
    register_shadow = QGraphicsDropShadowEffect(main_window)
    register_shadow.setBlurRadius(16)
    register_shadow.setXOffset(4)
    register_shadow.setYOffset(4)
    register_shadow.setColor(Qt.black)
    register_button.setGraphicsEffect(register_shadow)
    register_button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #01FF88;
            color: white;
            border: 2px solid #545252;
            border-radius: 30px;
            font-size: 15px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        QPushButton:pressed {{
            background-color: #545252;
        }}
        """
    )
    register_button.clicked.connect(main_window.register_animal)
    buttons_layout.addWidget(register_button)

    # Botón Repetir
    repeat_button = QPushButton(main_window.tr("Repetir"))
    repeat_button.setFixedSize(200, 60)
    repeat_shadow = QGraphicsDropShadowEffect(main_window)
    repeat_shadow.setBlurRadius(16)
    repeat_shadow.setXOffset(4)
    repeat_shadow.setYOffset(4)
    repeat_shadow.setColor(Qt.black)
    repeat_button.setGraphicsEffect(repeat_shadow)
    repeat_button.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #292929;
            color: white;
            border: 2px solid #545252;
            border-radius: 30px;
            font-size: 15px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        QPushButton:pressed {{
            background-color: #545252;
        }}
        """
    )
    repeat_button.clicked.connect(main_window.on_repeat_clicked)
    buttons_layout.addWidget(repeat_button)

    main_window.buttons_container = buttons_container
    main_window.buttons_container.hide()  # Oculto inicialmente
    content_layout.addWidget(main_window.buttons_container, 0, Qt.AlignCenter)

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

