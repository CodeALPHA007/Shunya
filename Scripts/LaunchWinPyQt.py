import subprocess
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5 import QtCore
from pyqt_slideshow import SlideShow
from PyQt5.uic import loadUi
import sys
import numpy as np
import cv2
import webbrowser

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(r"C:\Users\Atreyee\Desktop\Python scripts\Assets\Back.mp4")
        frame_counter = 0
        while self._run_flag:
            ret, cv_img = cap.read()
            cv_img = cv2.resize(cv_img, (1080, 572), interpolation = cv2.INTER_LINEAR)
            frame_counter += 1
            #If the last frame is reached, reset the capture and the frame_counter
            if frame_counter == (cap.get(cv2.CAP_PROP_FRAME_COUNT)-1):
                frame_counter = 0 #Or whatever as long as it is the same as next line
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.try_now(self)
        self.dlg=loadUi(r"..\Assets\dial_1.ui")

    def try_now(self,checked = None):
        loadUi(r"..\Assets\\untitled.ui",self)
        self.setWindowTitle("Project Shunya")
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon("..\\Assets\\Solar-system.ico"))
       #
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        
        self.button1.clicked.connect(self.show_new)
        self.button2.clicked.connect(self.show_about)
        self.button3.clicked.connect(self.show_web)
        
        self.settings_button.setIcon(QIcon("..\\Assets\\settings.png"))
        self.settings_button.clicked.connect(self.show_dialog)

        self.textBox.setText("hi")

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        #print(rgb_image.shape)
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(1080, 572, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def show_web(self):
        webbrowser.open('https://yashprogrammer.wordpress.com/', new= 2)
    
    def show_about(self):
        dialog = QDialog(self)
        dialog.resize(650,350)
        dialog.exec_()
    
    def show_dialog(self):
        #dlg = QDialog(self)
        
        #dlg.resize(650,350)
        self.dlg.color_btn.clicked.connect(self.on_click)
        #self.dlg.color_btn.clicked.connect(self.dlg.close)
        #dlg.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))


        self.dlg.slider_btn.clicked.connect(self.slide)
        #self.dlg.slider_btn.clicked.connect(self.dlg.close)

        self.dlg.change_btn.clicked.connect(self.change)
        #self.dlg.change_btn.clicked.connect(self.dlg.close)
        self.dlg.exec_()
    
    def change(self):
        fname=QFileDialog.getOpenFileName(self, "Open file", "..\Assets", 'Images (*.png *.xmp *.jpg)')
        if fname[0] != "":
            print(fname[0])
            self.image_label.hide()
            self._label.setPixmap(QPixmap(r'{}'.format(fname[0])))
        #self.filename.setText(fname[0])
    
    def slide(self):
        slider = QSlider(Qt.Horizontal,self.dlg)
        self.dlg.move(470,170)
        self.dlg.resize(500,300) 
        slider.setGeometry(250, 100, 160, 16)
        slider.show()
        # After each value change, slot "scaletext" will get invoked. 
        slider.valueChanged.connect(self.scale)
        #slider.valueChanged.connect(slider.hide)

    def scale(self,value):
        self.setWindowOpacity(1-value/250)
        self.dlg.setWindowOpacity(1-value/250)

    @pyqtSlot()
    def on_click(self):
        color1 = QColorDialog.getColor().getRgb()
        #print(color1)
        color2 = QColorDialog.getColor().getRgb()
        #print(color2)
        
        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        self.dlg.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        return (color1,color2)      

    def show_new(self):
        subprocess.Popen(r".\SolarSystem_Final.exe",shell=True)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
