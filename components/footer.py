from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QVBoxLayout
)

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Footer(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.copyright_layout = QHBoxLayout()
        self.copyright_layout.setAlignment(Qt.AlignRight)
        self.title = QLabel("Copyright By HnvLab")
        self.copyright_layout.addWidget(self.title)
        self.main_layout.addWidget(QHLine())
        self.main_layout.addLayout(self.copyright_layout)
        self.setLayout(self.main_layout)