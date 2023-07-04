import os
from selenium import webdriver
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By

from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QGridLayout, QProgressBar, QFileDialog
)
from .common import Label, PushButton
from .acgpn_inference import infer
from .SwinIR.main_test_swinir import resolution

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

        self.btn3_layout = QHBoxLayout()
        self.btn_search_file3 = PushButton("결과보기")
        self.btn_resolution = PushButton("Resolution (x4)")
        self.btn3_layout.addWidget(self.btn_search_file3)
        self.btn3_layout.addWidget(self.btn_resolution)

        self.main_layout.addWidget(self.label_title3, 0, 2)
        self.main_layout.addWidget(self.frame_image3, 1, 2)
        self.main_layout.addWidget(self.progress_bar, 2, 2)
        self.main_layout.addLayout(self.btn3_layout, 3, 2)
        self.setLayout(self.main_layout)

        # events
        self.btn_search_file1.clicked.connect(self.search_model)
        self.btn_search_file2.clicked.connect(self.search_cloth)
        self.btn_search_file3.clicked.connect(self.inference)
        self.btn_resolution.clicked.connect(self.resolution_4x)
        self.btn_url_search.clicked.connect(self.web_crawl)

    def search_model(self) -> None:
        self.model_file = QFileDialog.getOpenFileName(self, "Choose File", "", "All FIles(*) ;; Images(*.jpeg)")
        if self.model_file[0]:
            pixmap = QPixmap(self.model_file[0])
            self.frame_image1.setPixmap(pixmap.scaled(QSize(450, 450)))   
    
    def search_cloth(self) -> None:
        self.cloth_file = QFileDialog.getOpenFileName(self, "Choose File", "", "All FIles(*) ;; Images(*.jpeg)")
        if self.cloth_file[0]:
            pixmap = QPixmap(self.cloth_file[0])
            self.frame_image2.setPixmap(pixmap.scaled(QSize(450, 450)))

    def inference(self) -> None:
        infer(self.model_file[0], self.cloth_file[0])
        pixmap = QPixmap('./results/test/try-on/model.png')
        self.frame_image3.setPixmap(pixmap.scaled(QSize(450, 450)))

    def web_crawl(self) -> None:
        # download
        url = self.url.toPlainText()
        driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
        driver.get(url)

        image = driver.find_element(By.CSS_SELECTOR, "#detail_bigimg > div > img")
        image_url = image.get_attribute('src')
        driver.quit()
        # save
        urlretrieve(image_url, "tmp.jpg")
        # load
        pixmap = QPixmap("tmp.jpg")
        # q_image = pixmap.toImage()
        # np_image = qimage2ndarray.recarray_view(q_image)
        # print(np_image)

        # mask = np_image
        # # mask = cv2.cvtColor(np_image, cv2.COLOR_BAYER_BG2GRAY)
        # mask[mask[:, :]==255] = 0
        # mask[mask[:, :]>0] = 255
        # bg_removed = cv2.bitwise_and(np_image, np_image, mask=mask)
        # q_image = qimage2ndarray.array2qimage(bg_removed)
        # pixmap = QPixmap.fromImage(q_image)
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
    
    def resolution_4x(self):
        resolution()
        pixmap = QPixmap('./results/swinir_real_sr_x4_large/model_SwinIR.png')
        self.frame_image3.setPixmap(pixmap.scaled(QSize(450, 450)))