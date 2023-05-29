from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QDialog,
    QVBoxLayout
)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Titlebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("titlebar")
        self.setStyleSheet("""
            QFrame#titlebar {
                background-color: #1f1f1f;
            }
        """)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.title_layout = QHBoxLayout()
        self.title_label = QLabel("딥러닝 프로젝트 1조")
        self.title_label.setFont(QFont("Arial", pointSize=30, weight=QFont.Bold))
        self.title_layout.addWidget(self.title_label)

        self.right_layout = QHBoxLayout()
        self.btn_option = QPushButton("설명")
        self.btn_option.setFont(QFont("Arial", pointSize=15, weight=QFont.Bold))
        self.right_layout.addWidget(self.btn_option)
        self.right_layout.setAlignment(Qt.AlignRight)
        self.title_layout.addLayout(self.right_layout)

        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(QHLine())
        self.btn_option.clicked.connect(self.explain)
        self.setLayout(self.main_layout)

    def explain(self) -> None:
        dialog = QDialog()
        main_layout = QVBoxLayout()
        title = QLabel("프로그램 설명")
        title.setFont(QFont("Arial", pointSize=40, weight=QFont.Bold))
        label1 = QLabel("1. 왼쪽에 피팅할 사람의 이미지를 넣으세요.")
        label1.setFont(QFont("Arial", pointSize=20, weight=QFont.Bold))
        label2 = QLabel("2. 가운데에 피팅할 옷의 이미지를 넣으세요.")
        label2.setFont(QFont("Arial", pointSize=20, weight=QFont.Bold))
        label3 = QLabel("3. 버튼 클릭 후 오른쪽에서 결과를 확인하세요.")
        label3.setFont(QFont("Arial", pointSize=20, weight=QFont.Bold))

        main_layout.addWidget(title)
        main_layout.addWidget(label1)
        main_layout.addWidget(label2)
        main_layout.addWidget(label3)
        dialog.setLayout(main_layout)
        dialog.exec_()