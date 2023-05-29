import os
from selenium import webdriver
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By

from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QFont, Qt, QPixmap
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QGridLayout, QProgressBar, QFileDialog
)
from .common import Label, PushButton


class Content(QFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.main_layout = QGridLayout()
        # left layout
        self.label_title1 = QLabel("피팅할 모델")
        self.label_title1.setStyleSheet(" font-size: 30px; text-align: center; ")
        self.frame_image1 = Label()
        self.btn_search_file1 = PushButton("파일 탐색하기")
        self.main_layout.addWidget(self.label_title1, 0, 0)
        self.main_layout.addWidget(self.frame_image1, 1, 0)
        self.main_layout.addWidget(self.btn_search_file1, 2, 0, 2, 1)

        # center layout
        self.label_title2 = QLabel("피팅할 옷")
        self.label_title2.setStyleSheet(" font-size: 30px; text-align: center; ")
        self.frame_image2 = Label()
        self.btn_search_file2 = PushButton("파일 탐색하기")
        self.url_layout = QHBoxLayout()
        self.url = QTextEdit()
        self.url.setFixedSize(390, 50)
        self.btn_url_search = QPushButton("탐색")
        self.btn_url_search.setFixedSize(50, 50)
        self.url_layout.addWidget(self.url)
        self.url_layout.addWidget(self.btn_url_search)

        self.main_layout.addWidget(self.label_title2, 0, 1)
        self.main_layout.addWidget(self.frame_image2, 1, 1)
        self.main_layout.addLayout(self.url_layout, 2, 1)
        self.main_layout.addWidget(self.btn_search_file2, 3, 1)

        # right layout
        self.label_title3 = QLabel("결과")
        self.label_title3.setStyleSheet(" font-size: 30px; text-align: center; ")
        self.frame_image3 = Label()
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(450, 50)
        self.btn_search_file3 = PushButton("결과보기")

        self.main_layout.addWidget(self.label_title3, 0, 2)
        self.main_layout.addWidget(self.frame_image3, 1, 2)
        self.main_layout.addWidget(self.progress_bar, 2, 2)
        self.main_layout.addWidget(self.btn_search_file3, 3, 2)
        self.setLayout(self.main_layout)

        # events
        self.btn_search_file1.clicked.connect(self.search_model)
        self.btn_search_file2.clicked.connect(self.search_cloth)
        self.btn_search_file3.clicked.connect(self.inference)
        self.btn_url_search.clicked.connect(self.web_crawl)

    def search_model(self) -> None:
        file = QFileDialog.getOpenFileName(self, "Choose File", "", "All FIles(*) ;; Images(*.jpeg)")
        if file[0]:
            pixmap = QPixmap(file[0])
            self.frame_image1.setPixmap(pixmap.scaled(QSize(450, 450)))   
    
    def search_cloth(self) -> None:
        file = QFileDialog.getOpenFileName(self, "Choose File", "", "All FIles(*) ;; Images(*.jpeg)")
        if file[0]:
            pixmap = QPixmap(file[0])
            self.frame_image2.setPixmap(pixmap.scaled(QSize(450, 450)))

    def inference(self) -> None:
        pass

    def web_crawl(self) -> None:
        # download
        url = self.url.toPlainText()
        driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
        driver.get(url)

        image = driver.find_element(By.CSS_SELECTOR, "#detail_bigimg > div > img")
        image_url = image.get_attribute('src')
        driver.quit()
        # save
        print(image_url)
        urlretrieve(image_url, "tmp.jpg")
        # load
        pixmap = QPixmap("tmp.jpg")
        self.frame_image2.setPixmap(pixmap.scaled(QSize(450, 450)))
        os.remove("tmp.jpg")
        
    @Slot(int)
    def progressChange(self, value):
        pass
        tmp = (value / self.total_frame) * 100
        self.progress_bar.setValue(tmp)
        self.progress_bar.setFormat("%.02f %%" % tmp)
        self.ax.cla()
        self.is_minimap = True