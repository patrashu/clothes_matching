import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
)

from .titlebar import Titlebar
from .content import Content
from .footer import Footer


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initial_window()

    def initial_window(self) -> None:
        self.setFixedSize(1440, 780)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.titlebar = Titlebar()
        self.content = Content()
        self.footer = Footer()
        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addWidget(self.content)
        self.main_layout.addWidget(self.footer)

        self.setCentralWidget(self.main_widget)

        