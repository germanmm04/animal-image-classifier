from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QTimeEdit,
    QComboBox,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTime
from pathlib import Path


def SettingsScreen(main_window) -> None:
    """Crea y muestra la pantalla de opciones."""
    container = QWidget(main_window)
    container.setObjectName("backgroundContainer")
    outer_layout = QVBoxLayout()
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.setSpacing(0)

    # Barra superior (igual a Pokédex)
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

    settings_label = QLabel(main_window.tr("Opciones"))
    settings_label.setAlignment(Qt.AlignLeft)
    settings_label.setStyleSheet(
        f"""
        QLabel {{
            color: #00A2E8;
            font-size: 24px;
            font-weight: bold;
            font-family: "{font_family}";
        }}
        """
    )
    top_bar_layout.addWidget(settings_label)
    top_bar_layout.addStretch()

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

    # Contenido principal
    content_layout = QVBoxLayout()
    content_layout.setAlignment(Qt.AlignTop)
    content_layout.setSpacing(16)
    content_layout.setContentsMargins(10, 10, 10, 20)

    # ---- Sección hora ----
    time_section = QWidget()
    time_layout = QVBoxLayout(time_section)
    time_layout.setContentsMargins(26, 26, 26, 26)
    time_layout.setSpacing(14)
    time_section.setMinimumWidth(440)
    time_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    time_section.setStyleSheet(
        """
        QWidget {
            background-color: #1a1a1a;
            border: 2px solid #545252;
            border-radius: 10px;
        }
        """
    )

    time_title = QLabel(main_window.tr("Cambiar hora"))
    time_title.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: "{font_family}";
            padding: 4px 2px;
        }}
        """
    )
    time_layout.addWidget(time_title)

    time_hint = QLabel(main_window.tr("Establece la hora global de la aplicación."))
    time_hint.setWordWrap(True)
    time_hint.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 12px;
            font-family: "{font_family}";
            padding: 4px 6px;
        }}
        """
    )
    time_layout.addWidget(time_hint)

    time_edit = QTimeEdit()
    time_edit.setDisplayFormat("HH:mm")
    time_edit.setStyleSheet(
        f"""
        QTimeEdit {{
            background-color: #292929;
            color: white;
            border: 2px solid #545252;
            border-radius: 8px;
            font-size: 16px;
            font-family: "{font_family}";
            padding: 12px 16px;
            min-width: 280px;
        }}
        """
    )
    time_edit.setMinimumHeight(42)
    current_custom_time = main_window.settings.get_custom_time()
    if current_custom_time:
        time_edit.setTime(QTime.fromString(current_custom_time, "HH:mm"))
    else:
        time_edit.setTime(QTime.currentTime())
    time_layout.addWidget(time_edit, 0, Qt.AlignLeft)

    feedback_label = QLabel("")
    feedback_label.setStyleSheet(
        f"""
        QLabel {{
            color: #01FF88;
            font-size: 12px;
            font-family: "{font_family}";
        }}
        """
    )

    def save_time() -> None:
        custom_time = time_edit.time().toString("HH:mm")
        main_window.settings.set_custom_time(custom_time)
        main_window._update_time()
        feedback_label.setText(main_window.tr("Hora guardada"))

    def reset_time() -> None:
        main_window.settings.clear_custom_time()
        main_window._update_time()
        time_edit.setTime(QTime.currentTime())
        feedback_label.setText(main_window.tr("Hora restablecida a la del sistema"))

    actions_col = QVBoxLayout()
    actions_col.setSpacing(10)
    save_time_btn = QPushButton(main_window.tr("Guardar hora"))
    save_time_btn.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #ED5647;
            color: white;
            border: 2px solid #545252;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            font-family: "{font_family}";
            padding: 12px 22px;
        }}
        """
    )
    save_time_btn.setMinimumWidth(200)
    save_time_btn.clicked.connect(save_time)
    actions_col.addWidget(save_time_btn, 0, Qt.AlignLeft)

    reset_time_btn = QPushButton(main_window.tr("Usar hora del sistema"))
    reset_time_btn.setStyleSheet(
        f"""
        QPushButton {{
            background-color: #292929;
            color: white;
            border: 2px solid #545252;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            font-family: "{font_family}";
            padding: 12px 22px;
        }}
        QPushButton:pressed {{
            background-color: #545252;
        }}
        """
    )
    reset_time_btn.setMinimumWidth(200)
    reset_time_btn.clicked.connect(reset_time)
    actions_col.addWidget(reset_time_btn, 0, Qt.AlignLeft)

    time_layout.addLayout(actions_col)
    time_layout.addWidget(feedback_label)

    # ---- Sección idioma ----
    language_section = QWidget()
    language_layout = QVBoxLayout(language_section)
    language_layout.setContentsMargins(24, 24, 24, 24)
    language_layout.setSpacing(12)
    language_section.setMinimumWidth(440)
    language_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    language_section.setStyleSheet(
        """
        QWidget {
            background-color: #1a1a1a;
            border: 2px solid #545252;
            border-radius: 10px;
        }
        """
    )

    language_title = QLabel(main_window.tr("Seleccionar idioma"))
    language_title.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: "{font_family}";
            padding: 4px 2px;
        }}
        """
    )
    language_layout.addWidget(language_title)

    language_hint = QLabel(main_window.tr("Elige el idioma para toda la aplicación."))
    language_hint.setWordWrap(True)
    language_hint.setStyleSheet(
        f"""
        QLabel {{
            color: white;
            font-size: 12px;
            font-family: "{font_family}";
            padding: 4px 6px;
        }}
        """
    )
    language_layout.addWidget(language_hint)

    language_selector = QComboBox()
    language_selector.addItem(main_window.tr("Español"), "es")
    language_selector.addItem(main_window.tr("Inglés"), "en")
    language_selector.setStyleSheet(
        f"""
        QComboBox {{
            background-color: #292929;
            color: white;
            border: 2px solid #545252;
            border-radius: 8px;
            font-size: 14px;
            font-family: "{font_family}";
            padding: 10px 12px;
            min-width: 240px;
        }}
        QComboBox QAbstractItemView {{
            background-color: #292929;
            color: white;
            selection-background-color: #ED5647;
        }}
        """
    )
    # Seleccionar idioma actual
    current_lang = main_window.settings.get_language()
    index = language_selector.findData(current_lang)
    if index != -1:
        language_selector.setCurrentIndex(index)

    def on_language_changed(index: int) -> None:
        lang_code = language_selector.itemData(index)
        if lang_code:
            main_window.set_language(lang_code)

    language_selector.currentIndexChanged.connect(on_language_changed)
    language_layout.addWidget(language_selector, 0, Qt.AlignLeft)

    # Añadir secciones al contenido principal
    content_layout.addWidget(time_section)
    content_layout.addWidget(language_section)

    # Contenedor principal del contenido
    content_widget = QWidget()
    content_widget.setLayout(content_layout)
    content_widget.setStyleSheet("background: transparent;")
    outer_layout.addWidget(content_widget, 1)

    container.setLayout(outer_layout)
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

