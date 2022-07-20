import os
import time

import cv2

from PySide2.QtCore import QPoint

from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QRubberBand, QVBoxLayout

from PySide2.QtGui import QPixmap, QMouseEvent

from PySide2.QtCore import QRect, QSize, Qt

from PySide2 import QtCore, QtGui, QtWidgets

from PySide2.QtWidgets import QFileDialog, QDialog, QHBoxLayout, QGridLayout, QGroupBox, QGraphicsView, QGraphicsScene,QLineEdit,QLabel

import sys

import params,model,funcs,create_data


current_dir = os.path.dirname(os.path.realpath(__file__))
point_filename = os.path.join(current_dir, "41uu2.png")


class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setScene(QGraphicsScene(parent))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


    def set_image(self, pixmap):
        self.pixmap = pixmap
        self.scene().addPixmap(pixmap)  # pixmap_item.setPixmap(pixmap)

class CropView(GraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.origin_point: QPoint = None
        self.current_rubber_band: QRubberBand = None
        self.pixmap = None
        self.point_items = []
        self.widg = None

    def set_image_view(self, widg):
        self.widg = widg

    def mousePressEvent(self, mouse_event: QMouseEvent):
        self.origin_point = mouse_event.pos()
        self.current_rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.current_rubber_band.setGeometry(QRect(self.origin_point, QSize()))
        self.current_rubber_band.show()


    def mouseMoveEvent(self, mouse_event: QMouseEvent):
        self.current_rubber_band.setGeometry(QRect(self.origin_point, mouse_event.pos()).normalized())

    def mouseReleaseEvent(self, mouse_event: QMouseEvent):
        self.current_rubber_band.hide()
        self.current_rect: QRect = self.current_rubber_band.geometry()
        self.current_rubber_band.deleteLater()
        crop_pixmap: QPixmap = self.pixmap.copy(self.current_rect)
        self.widg.scene().clear()
        self.widg.set_image(crop_pixmap)
        crop_pixmap.save('image_to_predict.png')

class MainWindow(QDialog):

    def __init__(self, parent=None, is_dl=False):
        super(MainWindow, self).__init__(parent)

        self._is_dl = is_dl
        self.setFixedSize(1250, 770)
        self.image = None
        self.original_image = None
        self.model = model.my_load_model()

        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        header_font = QtGui.QFont()
        header_font.setFamily("Microsoft YaHei UI")
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_font.setWeight(75)


        self.file_dialog_button = QPushButton('Browse Image')
        self.file_dialog_button.setStyleSheet("background-color: rgb(0, 214, 157);")
        self.file_dialog_button.setFixedSize(230, 60)
        self.file_dialog_button.setFont(font)
        self.file_dialog_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.file_dialog_button.clicked.connect(self.load_image)

        self.camera_button = QPushButton('take a picture 📷')
        self.camera_button.setStyleSheet("background-color: rgb(0, 214, 157);")
        self.camera_button.setFixedSize(230 ,60)
        self.camera_button.setFont(font)
        self.camera_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.camera_button.clicked.connect(self.my_cam)

        self.classify_button = QPushButton('predict')
        self.classify_button.setStyleSheet("background-color: rgb(0,  214, 157);")
        self.classify_button.setFixedSize(150, 60)
        self.classify_button.setFont(font)
        self.classify_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.classify_button.clicked.connect(self.classify_image)

        self.add_image = QPushButton('add to test')
        self.add_image.setStyleSheet("background-color: rgb(0,  214, 157);")
        self.add_image.setFixedSize(150, 60)
        self.add_image.setFont(font)
        self.add_image.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_image.clicked.connect(self.add_image_to_test)


        self.create_image_view()  # right
        self.create_crop_view()  # left

        self.title = QLabel("recognize the object app:)")
        # self.title.setStyleSheet("background-color: rgb(0,189, 15);")
        self.title.setFixedSize(380, 60)
        self.title.setFont(header_font)

        self.label = QLabel('upload a picture and choose a square area to recognize or tap to take the whole picture')
        # self.label.setStyleSheet("background-color: rgb(50,200, 200);")
        self.label.setFixedSize(900, 60)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(font)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.label)
        bottom_layout.addWidget(self.camera_button)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.file_dialog_button)
        top_layout.addWidget(self.title)
        top_layout.addWidget(self.classify_button)
        top_layout.addWidget(self.add_image)

        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 6)
        main_layout.addLayout(bottom_layout, 5, 0, 1, 6)
        main_layout.addWidget(self.left_group_box, 2, 0, 2, 3)
        main_layout.addWidget(self.right_group_box, 2, 3, 2, 3)

        self.setLayout(main_layout)

    def load_image(self):
        f_types = "Images (*.png; *.jpg;*.jfif)"
        self.image, _ = QFileDialog.getOpenFileName(self, filter=f_types)
        self.original_image = self.image
        img = cv2.imread(self.image, cv2.IMREAD_UNCHANGED)
        resized = cv2.resize(img, (577,572), interpolation=cv2.INTER_AREA)
        self.label.setStyleSheet("background-color: rgb(50,200, 200);")
        cv2.imwrite('resized.jpg', resized)
        self.image='resized.jpg'

        if self.image:
            self.crop_view.set_image(QPixmap(self.image))

    def classify_image(self):
        resized_image=funcs.resize_to_3x32x32('image_to_predict.png')
        cv2.imwrite('image_to_predict.png', resized_image)
        label=model.predict('image_to_predict.png',self.model)
        self.title=label
        params.label=label
        self.label.setStyleSheet("background-color: rgb(50,0, 200);")

        self.label.setText(f'class classified as {label}')
        print(label)
        #self.label.setStyleSheet("background-color: rgb(50,200, 200);")

    def add_image_to_test(self):
        create_data.add_one_image(self.original_image, params.our_images_directory)
        self.label.setText('image added successfully')

    def my_cam(self):
        print("my_cam")
        cam = cv2.VideoCapture(0)
        result, image=cam.read()
        if result:
            cv2.imshow("your_picture", image)
            self.label.setStyleSheet("background-color: rgb(255, 252, 2);")
            self.label.setText('press enter in order to classify your picture ')
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('image_to_predict.png', image)
        self.classify_image()

    def create_crop_view(self):
        self.left_group_box = QWidget(self)
        self.crop_view = CropView(self)
        self.crop_view.set_image_view(self.image_view)
        layout = QVBoxLayout()
        layout.addWidget(self.crop_view)
        self.left_group_box.setLayout(layout)

    def create_image_view(self):
        self.right_group_box = QWidget(self)
        self.image_view = GraphicsView(self)
        layout = QVBoxLayout()
        layout.addWidget(self.image_view)
        self.right_group_box.setLayout(layout)


class Run(object):

    def __init__(self, is_dl=False):
        self.app = QApplication(sys.argv)

        self.gallery = MainWindow(is_dl=is_dl)

        # self.gallery.setWindowState(Qt.WindowMaximized)

        self.gallery.setWindowFlags(self.gallery.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)

        self.gallery.setWindowTitle("faigyb2002's great app")

    def run(self):
        self.gallery.show()

        sys.exit(self.app.exec_())


if __name__ == "__main__":
    Run(True).run()