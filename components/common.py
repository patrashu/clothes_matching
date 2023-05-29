from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel, QPushButton
)

class Label(QLabel):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.setFixedSize(450, 450)
        self.setStyleSheet("border-color: white;")
        self.setAlignment(Qt.AlignCenter)


class PushButton(QPushButton):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.setText(text)
        self.setFixedSize(150, 70)
        self.setStyleSheet(" font-size: 15px; ")

