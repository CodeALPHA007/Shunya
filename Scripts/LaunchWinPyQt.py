import subprocess
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from pyqt_slideshow import SlideShow
import os
import sys
import numpy as np
import cv2

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\Back.mp4")
        frame_counter = 0
        while self._run_flag:
            ret, cv_img = cap.read()
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

class Show_NewWin(QWidget):
    def __init__(self):
        super().__init__()
        self.s = SlideShow()
        self.s.setGeometry(150, 150, 600, 400)
        pixmap1 = QtGui.QPixmap("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\Space1.png")
        pixmap2 = QtGui.QPixmap("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\Space2.png")
        pixmap3 = QtGui.QPixmap("C:\\Users\\Atreyee\\Desktop\Python scripts\\Assets\\Space3.png")
        img1 = pixmap1.scaled(600, 400)
        img2 = pixmap2.scaled(600, 400)
        img3 = pixmap3.scaled(600, 400)
        self.s.setFilenames([img1,img2 ,img3 ])

        self.s.setNavigationButtonVisible(False) # to not show the navigation button

        self.s.setBottomButtonVisible(False) # to not show the bottom button
        
        #s.setGradientEnabled(False)
        
        self.s.setInterval(2000)
        self.new(self.s)

        self.s.show()
    
    def button(self, str, s, t):
       pybutton = QPushButton(str, s)
       pybutton.setGeometry(t[0], t[1], t[2], t[3])
       pybutton.setStyleSheet("color: white;"
                             "background-color: rgb(0,20,20);"
                             "border: 0.5px solid black;"
                             "border-radius: 20px;")
       return pybutton

    def new(self, s):
        s.setWindowTitle("Main")
        #s.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(20, 34, 195), stop: 1 rgb(0, 100, 25) );")
        #self.setWindowOpacity(1.0)        
        s.setGeometry(150, 150, 800, 500)
  
        self.button('Mercury', s, (100, 150, 100, 50)).clicked.connect(self.show_message)
        self.button('Venus', s, (200, 150, 100, 50)).clicked.connect(self.show_message)
        self.button('Earth', s, (300, 150, 100, 50)).clicked.connect(lambda: self.show_Earth("LaunchWinPyQt.py", "Planet.py"))
        self.button('Mars', s, (400, 150, 100, 50)).clicked.connect(self.show_message)
        self.button('Jupiter', s, (100, 250, 100, 50)).clicked.connect(self.show_message)
        self.button('Saturn', s, (200, 250, 100, 50)).clicked.connect(self.show_message)
        self.button('Uranus', s, (300, 250, 100, 50)).clicked.connect(self.show_message)
        self.button('Neptune', s, (400, 250, 100, 50)).clicked.connect(self.show_message)

        self.button('Credits', s, ((10,60,100,50))).clicked.connect(self.show_dia)

        settings_button = self.button("Setting", s, ((10,10,100,50)))
        settings_button.setIcon(QIcon("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\settings.png"))
        settings_button.clicked.connect(lambda: self.show_on_click(s))
        #settings_button.clicked.connect(s.close)

    def show_dia(self):
        d=QDialog()
        label = QLabel("NASA, ESA, and The Hubble Heritage Team (STScI/AURA). Acknowledgment: \nJ. Gallagher (University of Wisconsin), M. Mountain (STScI) and P. Puxley (NSF).", d)
        d.setGeometry(80,350, 400,100)
        d.exec_()
    
    def show_on_click(self, s):
        self.x = NewWin()
        self.x.show()
        s.close()
        
    def show_Earth(self, calling_file_name, path_relative):
        cwd = os.path.abspath(__file__)
        cwd = cwd.replace(calling_file_name,"")
        abs_path = os.path.join(cwd,path_relative)
        subprocess.Popen(["python", abs_path])

    def show_message(self):
        msg = QMessageBox(self)
        msg.setIcon( QMessageBox.Warning)
        msg.setText("In pipeline")
        msg.setWindowTitle("Soon")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

class Show_Main(QWidget):
    def __init__(self):
        super().__init__()
        self.s = SlideShow()
        self.s.setGeometry(150, 150, 600, 400)
        pixmap1 = QtGui.QPixmap("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\Space1.png")
        pixmap2 = QtGui.QPixmap("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\Space2.png")
        pixmap3 = QtGui.QPixmap("C:\\Users\\Atreyee\\Desktop\Python scripts\\Assets\\Space3.png")
        img1 = pixmap1.scaled(600, 400)
        img2 = pixmap2.scaled(600, 400)
        img3 = pixmap3.scaled(600, 400)
        self.s.setFilenames([img1,img2 ,img3 ])
        
        self.s.setNavigationButtonVisible(False) # to not show the navigation button

        self.s.setBottomButtonVisible(False) # to not show the bottom button
        
        #s.setGradientEnabled(False)
        
        self.s.setInterval(2000)
        self.new(self.s)

        self.s.show()
    
    def button(self, str, s, t):
       pybutton = QPushButton(str, s)
       pybutton.setGeometry(t[0], t[1], t[2], t[3])
       pybutton.setStyleSheet("color: white;"
                             "background-color: rgb(0,20,20);"
                             "border: 0.5px solid black;"
                             "border-radius: 20px;")
       return pybutton

    def new(self, s):
        s.setWindowTitle("Main")
        #s.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(20, 34, 195), stop: 1 rgb(0, 100, 25) );")
        #self.setWindowOpacity(1.0)        
        s.setGeometry(150, 150, 800, 500)
  
        str_planets = 'Planets'
        self.button(str_planets, s, ((200,150,100,50))).clicked.connect(self.show_new_window)

        str_system = 'Revolution'
        #s="C:\\Users\\Atreyee\\Desktop\\Python scripts\\Scripts\\Trail.py"
        self.button(str_system, s, ((300, 150, 100, 50))).clicked.connect(self.show_new)

        label = QLabel("Welcome", s)
        label.setStyleSheet("color: white;"
                            "background-color: none;"
                            "border: rgb(0,0,55);")
        label.setGeometry(220, 100, 75, 45)

        self.button('Credits', s, ((10,60,100,50))).clicked.connect(self.show_dia)

        settings_button = self.button("Setting", s, ((10,10,100,50)))
        settings_button.setIcon(QIcon("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\settings.png"))
        settings_button.clicked.connect(lambda: self.show_on_click(s))
        #settings_button.clicked.connect(s.close)

    def show_dia(self):
        d=QDialog()
        label = QLabel("NASA, ESA, and The Hubble Heritage Team (STScI/AURA). Acknowledgment: \nJ. Gallagher (University of Wisconsin), M. Mountain (STScI) and P. Puxley (NSF).", d)
        d.setGeometry(80,350, 400,100)
        d.exec_()
    
    def show_on_click(self, s):
        self.x = MainWindow()
        self.x.show()
        s.close()
     
    def show_new_window(self):
        self.w=NewWin()
        self.w.show()

    def show_new(self, path_relative, calling_file_name):
        cwd = os.path.abspath(__file__)
        cwd = cwd.replace(calling_file_name,"")
        abs_path = os.path.join(cwd,path_relative)
        subprocess.Popen(["python", abs_path])

class NewWin(QWidget):
    def __init__(self):
        super().__init__()
        self.try_now(self)

    def button(self, str,t):
       pybutton = QPushButton(str, self)
       pybutton.setGeometry(t[0], t[1], t[2], t[3])
       pybutton.setStyleSheet("color: white;"
                             "border: 0.5px solid brown;"
                             "border-radius: 20px;")
       return pybutton
    
    def button_diag(self, dlg, str,t, col):
       pybutton = QPushButton(str, dlg)
       pybutton.setGeometry(t[0], t[1], t[2], t[3])
       pybutton.setStyleSheet("background-color: {};"
                             "color: white;"
                             "border: 0.5px solid black;".format(col))
       return pybutton

    def try_now(self, chceked = None):
        self.setWindowTitle("Planets")
        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(20, 34, 195), stop: 1 rgb(0, 100, 25) );")
        self.setWindowOpacity(1.0)        
        self.setGeometry(150, 150, 800, 500)

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 780,475)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

        #Planets
        self.button('Mercury', (100, 150, 100, 50)).clicked.connect(self.show_message)
        self.button('Venus', (200, 150, 100, 50)).clicked.connect(self.show_message)
        self.button('Earth', (300, 150, 100, 50)).clicked.connect(lambda: self.show_Earth("LaunchWinPyQt.py", "Planet.py"))
        self.button('Mars', (400, 150, 100, 50)).clicked.connect(self.show_message)
        self.button('Jupiter', (100, 250, 100, 50)).clicked.connect(self.show_message)
        self.button('Saturn', (200, 250, 100, 50)).clicked.connect(self.show_message)
        self.button('Uranus', (300, 250, 100, 50)).clicked.connect(self.show_message)
        self.button('Neptune', (400, 250, 100, 50)).clicked.connect(self.show_message)

        settings_button = self.button("Setting",((10,10,100,50)))
        settings_button.setIcon(QIcon("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\settings.png"))
        settings_button.clicked.connect(self.show_dialog)

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
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(900, 900, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def show_dialog(self):
        dlg = QDialog(self)
        dlg.move(650,350)
        self.button_diag(dlg, 'Open color dialog', ((10,50,90,40)), "transparent").clicked.connect(self.on_click)

        slider_button= self.button_diag(dlg, 'Open slider', ((10,90,90,40)), "transparent")
        slider_button.clicked.connect(self.slide)
        slider_button.clicked.connect(dlg.close)

        slide_show_button = self.button_diag(dlg, 'Slide Show', ((10,130,90,40)), "transparent")
        slide_show_button.clicked.connect(self.slide_show)
        slide_show_button.clicked.connect(dlg.close)
        slide_show_button.clicked.connect(self.close)
        dlg.exec_()
        
    def slide_show(self):
        Show_NewWin()
    
    def show_Earth(self, calling_file_name, path_relative):
        cwd = os.path.abspath(__file__)
        cwd = cwd.replace(calling_file_name,"")
        abs_path = os.path.join(cwd,path_relative)
        subprocess.Popen(["python", abs_path])

    def show_message(self):
        msg = QMessageBox(self)
        msg.setIcon( QMessageBox.Warning)
        msg.setText("In pipeline")
        msg.setWindowTitle("Soon")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def slide(self):
        slider = QSlider(Qt.Horizontal, self) 
        slider.setGeometry(190, 200, 160, 16)
        slider.show()
        # After each value change, slot "scaletext" will get invoked. 
        slider.valueChanged.connect(self.scale) 

    def scale(self,value):
        self.setWindowOpacity(1-value/500)
        
    @pyqtSlot()
    def on_click(self):
        color1 = QColorDialog.getColor().getRgb()
        #print(color1)
        color2 = QColorDialog.getColor().getRgb()
        #print(color2)
        
        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.try_now(self)

    def button(self, str,t):
       pybutton = QPushButton(str, self)
       pybutton.setGeometry(t[0], t[1], t[2], t[3])
       pybutton.setStyleSheet("color: black;"
                             "border: 0.5px solid black;"
                             "border-radius: 20px;")
       return pybutton
    
    def button_diag(self, dlg, str,t, col):
       pybutton = QPushButton(str, dlg)
       pybutton.setGeometry(t[0], t[1], t[2], t[3])
       pybutton.setStyleSheet("background-color: {};"
                             "color: white;"
                             "border: 0.5px solid brown;".format(col))
       return pybutton

    def try_now(self,checked = None):
        self.setWindowTitle("Main")
        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(20, 34, 195), stop: 1 rgb(0, 100, 25) );")
        self.setWindowOpacity(1.0)        
        self.setGeometry(150, 150, 800, 500)

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 780,475)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
  
        str_planets = 'Planets'
        self.button(str_planets, ((200,150,100,50))).clicked.connect(self.show_new_window)

        str_system = 'Revolution'
        #s="C:\\Users\\Atreyee\\Desktop\\Python scripts\\Scripts\\Trail.py"
        self.button(str_system, ((300, 150, 100, 50))).clicked.connect(lambda: self.show_new("Trail.py","LaunchWinPyQt.py"))

        label = QLabel("Welcome", self)
        label.setStyleSheet("color: white;"
                            "background-color: none;"
                            "border: rgb(0,0,55);")
        label.setGeometry(220, 100, 75, 45)

        settings_button = self.button("Setting",((10,10,100,50)))
        settings_button.setIcon(QIcon("C:\\Users\\Atreyee\\Desktop\\Python scripts\\Assets\\settings.png"))
        settings_button.clicked.connect(self.show_dialog)

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
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(900, 900, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def show_dialog(self):
        dlg = QDialog(self)
        dlg.move(650,350)
        self.button_diag(dlg, 'Open color dialog', ((10,50,90,40)), "transparent").clicked.connect(self.on_click)

        slider_button= self.button_diag(dlg, 'Open slider', ((10,90,90,40)), "transparent")
        slider_button.clicked.connect(self.slide)
        slider_button.clicked.connect(dlg.close)

        slide_show_button = self.button_diag(dlg, 'Slide Show', ((10,130,90,40)), "transparent")
        slide_show_button.clicked.connect(self.slide_show)
        slide_show_button.clicked.connect(dlg.close)
        slide_show_button.clicked.connect(self.close)
        dlg.exec_()
    
    def slide_show(self):
        Show_Main()
    
    def slide(self):
        slider = QSlider(Qt.Horizontal, self) 
        slider.setGeometry(190, 200, 160, 16)
        slider.show()
        # After each value change, slot "scaletext" will get invoked. 
        slider.valueChanged.connect(self.scale) 

    def scale(self,value):
        self.setWindowOpacity(1-value/500)

    @pyqtSlot()
    def on_click(self):
        color1 = QColorDialog.getColor().getRgb()
        #print(color1)
        color2 = QColorDialog.getColor().getRgb()
        #print(color2)
        
        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        

    def show_new_window(self, checked = None):
        self.w=NewWin()
        self.w.show()
        

    def show_new(self, path_relative, calling_file_name):
        cwd = os.path.abspath(__file__)
        cwd = cwd.replace(calling_file_name,"")
        abs_path = os.path.join(cwd,path_relative)
        subprocess.Popen(["python", abs_path])

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
