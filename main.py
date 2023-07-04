import qdarktheme
from components.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import os
import shutil


if __name__ == "__main__":
    shutil.rmtree('./Data_preprocessing/test_color')
    shutil.rmtree('./Data_preprocessing/test_colormask')
    shutil.rmtree('./Data_preprocessing/test_edge')
    shutil.rmtree('./Data_preprocessing/test_img')
    shutil.rmtree('./Data_preprocessing/test_label')
    shutil.rmtree('./Data_preprocessing/test_mask')
    shutil.rmtree('./Data_preprocessing/test_pose')
    shutil.rmtree('./results')
    os.mkdir('./results')
    os.mkdir('./results/test')
    os.mkdir('./Data_preprocessing/test_color')
    os.mkdir('./Data_preprocessing/test_colormask')
    os.mkdir('./Data_preprocessing/test_edge')
    os.mkdir('./Data_preprocessing/test_img')
    os.mkdir('./Data_preprocessing/test_label')
    os.mkdir('./Data_preprocessing/test_mask')
    os.mkdir('./Data_preprocessing/test_pose')
    os.mkdir('./results/swinir_real_sr_x4_large')
    os.mkdir('./results/test/refined_cloth')
    os.mkdir('./results/test/try-on')
    os.mkdir('./results/test/warped_cloth')
    app = QApplication()
    qdarktheme.setup_theme()
    main_window = MainWindow()
    main_window.show()
    app.exec()