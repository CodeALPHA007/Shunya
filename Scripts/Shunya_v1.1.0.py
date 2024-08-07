
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.uic import loadUi

import numpy as np
import cv2
import webbrowser

#import for ursina simulation
import spiceypy
from ursina import *
import datetime
import numpy
from collections import deque
import xarray as xr
import cftime
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.shaders import lit_with_shadows_shader
from direct.filter.CommonFilters import CommonFilters

from panda3d.core import TextureStage

import time as Time
import calendar
import json

import os

ursina_start=False

avl_new_version=False

version='v1.1.0'

try:
    with open("version.txt",'r') as cur_ver:
        temp=cur_ver.read().strip()
        if version!=temp:
            avl_new_version=True

    os.system(r'start "" /d "%cd%"  "%cd%\version_control.exe"')
except:
    pass

my_credits=["  TEXTURES :  https://www.solarsystemscope.com/textures/",
            "  https://planetpixelemporium.com/",
            "  https://visibleearth.nasa.gov/",
            "  PHOBOS AND DEIMOS OBJECTS:  https://science.nasa.gov/solar-system/resources/?types=3d",
            "  Kernels:  https://naif.jpl.nasa.gov/pub/naif/generic_kernels/"
            ]
#MAIN WINDOW
screen_size=(1412,716)
qt_scale=1

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    change_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        global my_credits
        self._run_flag = True
        self._credit_index=0
        self._scroll_text=my_credits[self._credit_index]
        self._scroll_text_size=len(self._scroll_text)
        self._scroll_text_deque=deque([' ' for i in range(500)],maxlen=500)


    def run(self):
        global my_credits
        cap = cv2.VideoCapture(r"../Assets/Earth_Back.mp4")
        frame_counter = 0
        frame_rate = 18
        prev=0
        i=0
        while self._run_flag:
            time_p = Time.time()-prev
            if time_p > 1./frame_rate:
                prev = Time.time()
                frame_counter += 1
                ret, cv_img = cap.read()
                if i<len(self._scroll_text):
                    self._scroll_text_deque.append(self._scroll_text[i])
                else:
                    if (self._scroll_text_deque[0] != self._scroll_text[-1]) and i<=len(self._scroll_text)+max(50,(self._scroll_text_deque.maxlen)//10):
                        self._scroll_text_deque.append(" ")
                    else:
                        self._scroll_text_deque.append(" ")
                        i=0
                        self._credit_index = (self._credit_index+1)%len(my_credits)
                        self._scroll_text=my_credits[self._credit_index]
                i+=1
                temp="".join([e for e in self._scroll_text_deque])
                #If the last frame is reached, reset the capture and the frame_counter
                if frame_counter == (cap.get(cv2.CAP_PROP_FRAME_COUNT)-5):
                     frame_counter = 0 
                     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                if ret:
                    self.change_pixmap_signal.emit(cv_img)
                    self.change_text.emit(temp)
        cap.release()

    def stop(self):
        #Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        global screen_size
        self.screen_size=screen_size
        self.custom_scale=(self.screen_size[0]/1412,self.screen_size[1]/716)
        self.try_now(self)
        self.setWindowFlags( QtCore.Qt.WindowFlags() | QtCore.Qt.FramelessWindowHint)
        
        self.dlg=loadUi(r"..\Assets\dial_1.ui")
        self.dialog=loadUi(r"..\Assets\dial_2.ui")
        self.dial=loadUi(r"..\Assets\dial_3.ui")
        self.dlg.slider = QSlider(Qt.Horizontal,self.dlg)
        self.dlg.slider.hide()
        self.label.parent=self
        self.label_2.parent=self
        self.resizing()
        self.move(0,0)


    def custom_scaling(self,custom_size,scale):  
        try:
            temp_size=(int(custom_size[0]*scale[0]),int(custom_size[1]*scale[1]))
            if 0 in temp_size :
                return custom_size
            return temp_size
        except:
            return custom_size     

    def resizing(self):
        custom_widgets = {
                         "main window":[self,(1412,716),(0,0)],
                         "_label":[self._label,(1451,756),(0,0)],
                         "button1":[self.button1,(181,51),(585,350)],
                         "button2":[self.button2,(101,41),(900,20)],
                         "button3":[self.button3,(101,41),(1010,20)],
                         "button4":[self.button4,(131,41),(1120,20)],
                         "close button":[self.close_btn,(41,41),(1280,20)],
                         "dt":[self.dt,(1271,16),(60,680)],
                         "image_label":[self.image_label,(1451,750),(0,0)],
                         "instagram":[self.insta_btn,(41,41),(620,630)],
                         "label":[self.label,(201,91),(577,240)],
                         "label_2":[self.label_2,(61,20),(640,600)],
                         "linkedin":[self.ln_btn,(41,41),(670,630)],
                         "settings button":[self.settings_button,(41,41),(30,20)],
                         "version button":[self.version_btn,(361,171),(90,160)],
                         "version label":[self.version_label,(161,20),(190,290)],
                         "change button":[self.dlg.change_btn,(121,41),(40,190)],
                         "colorbin":[self.dlg.colorbin,(121,41),(40,90)],
                         "reset button":[self.dlg.reset_button,(41,41),(170,230)],
                         "slider button":[self.dlg.slider_btn,(121,41),(40,140)],
                         "theme":[self.dlg.theme_btn,(121,41),(40,40)],
                         "slider":[self.dlg.slider,(160,16),(250,100)],
                         "dialog":[self.dialog,(931,560),(190,50)],
                         "text":[self.dialog.textBrowser,(900,551),(20,10)],
                         "guide":[self.dial,(620,529),(420,50)],
                         "table":[self.dial.tableWidget,(600,301),(40,60)],
                         "text1":[self.dial.textBrowser,(600,45),(30,20)],
                         "text2":[self.dial.textBrowser_2,(600,131),(40,410)]
                          }
        for i in custom_widgets.keys():
            temp_size=self.custom_scaling(custom_widgets[i][1],self.custom_scale)
            temp_pos = self.custom_scaling(custom_widgets[i][2],self.custom_scale)
            custom_widgets[i][0].setFixedSize(temp_size[0],temp_size[1])
            custom_widgets[i][0].move(temp_pos[0],temp_pos[1])
        
        dial1_size=self.custom_scaling((230,300),self.custom_scale)
        dial1_pos = self.custom_scaling((532,210),self.custom_scale)
        self.dlg.setMinimumSize(dial1_size[0],dial1_size[1])
        self.dlg.move(dial1_pos[0],dial1_pos[1])
        for i in[0,2]:
            self.dial.tableWidget.resizeColumnToContents(i)
        #self.dial.tableWidget.resizeColumnToContents(2)

    def try_now(self,checked = None):
        global avl_new_version
        #loadUi(r"../Assets/untitled.ui",self)
        loadUi(r"../Assets/untitled.ui",self)
        self.setWindowTitle("Shunya")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setWindowIcon(QIcon("..\\Assets\\Shunya.ico"))

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.change_text.connect(self.update_txt)
        # start the thread
        self.thread.start()
        self.button1.parent=self  
        self.button1.clicked.connect(self.show_new)
        self.button2.parent=self
        self.button2.clicked.connect(self.show_about)
        self.button3.parent=self
        self.button3.clicked.connect(lambda: self.show_web('https://shunyathespaceapp.onrender.com'))
        self.settings_button.parent=self
        self.settings_button.setIcon(QIcon("..\\Assets\\settings.png"))
        self.settings_button.clicked.connect(self.show_dialog)

        self.version_btn.parent=self
        self.version_btn.hide()
        self.version_label.parent=self
        self.version_label.hide()
        if avl_new_version:
            self.version_label.show()
            self.version_btn.show()
            self.version_btn.clicked.connect(self.ver_new)

        self.close_btn.parent=self
        self.close_btn.setIcon(QIcon("..\\Assets\\close.png"))
        self.close_btn.clicked.connect(self.call)

        self.insta_btn.parent=self
        self.insta_btn.setIcon(QIcon("..\\Assets\\insta.png"))
        self.insta_btn.clicked.connect(lambda: self.show_web('https://www.instagram.com/teamshunya1114/?hl=en'))

        self.ln_btn.parent=self
        self.ln_btn.setIcon(QIcon("..\\Assets\\linkedin.png"))
        self.ln_btn.clicked.connect(lambda: self.show_web('https://www.linkedin.com/in/team-shunya-95b6a4304/'))
        
        self.button4.parent=self
        self.button4.clicked.connect(self.show_credits)

        self.image_label.parent=self
        
        temp_x=max(self.image_label.width(),screen_size[0])
        temp_y=max(self.image_label.height(),screen_size[1])
        self.image_label.showNormal()
        self.image_label.resize(temp_x,temp_y)

       
    def ver_new(self):
        webbrowser.open('https://shunyathespaceapp.onrender.com/', new= 2)    
        
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        qt_img = qt_img.scaled(screen_size[0],screen_size[1],Qt.IgnoreAspectRatio)
        self.image_label.setPixmap(qt_img)
        
        #self.image_label.resize(1450,self.height())

    def call(self):
        self.close()    

    def update_txt(self,t):
        self.dt.parent=self
        self.dt.setText(t)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        #print(rgb_image.shape)
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(screen_size[0],screen_size[1],Qt.IgnoreAspectRatio)
        return QPixmap.fromImage(p)
    
    def show_web(self,str):
        webbrowser.open(str, new= 2)
    
    def show_credits(self):
        self.dial.tableWidget.parent = self.dial
        self.dial.textBrowser.parent = self.dial
        self.dial.textBrowser_2.parent = self.dial
        self.dial.exec_()
    
    def show_about(self):
        #self.dialog.Coffee.clicked.connect(lambda: self.show_web('https://shunyathespaceapp.onrender.com/'))
        self.dialog.exec_()
    
    def change(self):
        self._label.parent=self
        self._label.show()
        fname=QFileDialog.getOpenFileName(self, "Open file", r"..\Assets", 'Images (*.png *.xmp *.jpg)')
        if fname[0] != "":
            #print(fname[0])
            self.image_label.hide()
            self._label.setPixmap(QtGui.QPixmap(r'{}'.format(fname[0])).scaled(screen_size[0],screen_size[1],Qt.IgnoreAspectRatio))
            #self._label.resize(1450, 770)
    
    def donotshow(self):
        self.image_label.hide()
        self._label.hide()
    
    def colr(self):
        color1 = QColorDialog.getColor().getRgb()
        color2 = QColorDialog.getColor().getRgb()
        
        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        self.dlg.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        self.dialog.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        self.dial.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb({}, {}, {}), stop: 1 rgb({}, {}, {}) );".format(color1[0],color1[1],color1[2],color2[0],color2[1],color2[2]))
        
    def show_dialog(self):
        #self.dlg.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        
        self.dlg.theme_btn.parent=self.dlg
        self.dlg.colorbin.parent=self.dlg
        self.dlg.slider_btn.parent=self.dlg
        self.dlg.change_btn.parent=self.dlg
        self.dlg.reset_button.parent=self.dlg

        self.dlg.theme_btn.clicked.connect(self.donotshow)
        self.dlg.colorbin.clicked.connect(self.colr)

        self.dlg.slider_btn.clicked.connect(self.slide)

        self.dlg.change_btn.clicked.connect(self.change)

        self.dlg.reset_button.clicked.connect(self.back)
        self.dlg.reset_button.setIcon(QIcon("..\\Assets\\reset.png"))

        self.dlg.exec_()
        self.dlg.change_btn.clicked.disconnect(self.change)
        self.dlg.colorbin.clicked.disconnect(self.colr)
        self.dlg.move(570,170)
        self.dlg.resize(230,300)
  
    
    def back(self):
        self.image_label.show()
        self._label.hide()

        self.setWindowOpacity(1)
        self.dlg.setWindowOpacity(1)
        self.dialog.setWindowOpacity(1)
        self.dial.setWindowOpacity(1)
        self.dlg.slider.setValue(0)

        self.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(114, 4, 85), stop: 1 rgb(3, 6, 55) );")
        self.dlg.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(114, 4, 85), stop: 1 rgb(3, 6, 55) );")
        self.dialog.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(114, 4, 85), stop: 1 rgb(3, 6, 55) );")
        self.dial.setStyleSheet("background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgb(114, 4, 85), stop: 1 rgb(3, 6, 55) );")

    def slide(self):
        dial1_size=self.custom_scaling((500,300),self.custom_scale)
        dial1_pos = self.custom_scaling((470,170),self.custom_scale)
        self.dlg.move(dial1_pos[0],dial1_pos[1])
        self.dlg.resize(dial1_size[0],dial1_size[1]) 
        #self.dlg.slider.setGeometry(250, 100, 160, 16)
        self.dlg.slider.parent=self.dlg
        self.dlg.slider.show()
        # After each value change, slot "scaletext" will get invoked. 
        self.dlg.slider.valueChanged.connect(self.scale)

    def scale(self,value):
        self.setWindowOpacity(1-value/250)
        self.dlg.setWindowOpacity(1-value/250)
        self.dialog.setWindowOpacity(1-value/250)
        self.dial.setWindowOpacity(1-value/250)

    def show_new(self):
        global ursina_start
        ursina_start=True
        self.close()


################################URSINA######################################

class SolarSystem:
    def __init__(self,myapp):
        self.__set_date_year()
        self.__set_kernels()
        self.__set_constants()
        self.__create_planet_dict()
        self.__gen_dates(forced=True)
        pivot=Entity(unlit=True)
        pivot.world_position=Vec3(0,0,0)
        PointLight(parent=pivot, x=0,y=0, z=0, color=color.white,shadows=False)._light.setColorTemperature(5772)
        self._ambient_light=AmbientLight(color= color.dark_gray)
        try:
            self.filters = CommonFilters(myapp.win, myapp.cam)
            self.filters.setBloom(blend=(0.3,0.1,0,0.5),mintrigger=0.7,maxtrigger=1.0,desat=0,intensity=5,size='medium' )
        except:
            pass
        


    def __set_date_year(self):    
        self._start_year=0
        self._end_year=0
        temp_current_time=datetime.datetime.now(datetime.timezone.utc).strftime('%Y %m %d %H %M %S').split(' ')
        self._year=int(temp_current_time[0])
        self._month , self._day=temp_current_time[1:3]
        self._hour, self._minute, self._second=temp_current_time[3:6]
        
        
        self._date_frequency='Daily'
        self._start_date=cftime.datetime
        self._end_date=cftime.datetime
        self._end_arr=[]
        self._start_arr=[]

    def __check_leap_year(self,year):
        if year%100==0:
            year=year//100
        if year%4==0:
            return True
        else:
            return False    

    def __set_start_end_date(self,forced=False):
        temp_calendar='365_day'
        if self.__check_leap_year(self._year):
            temp_calendar='366_day'

        if forced:
            self._start_date=cftime.datetime(year=self._year,
                                                    month=int(self._month),
                                                    day=int(self._day),
                                                    hour=int(self._hour),
                                                    minute=int(self._minute),
                                                    second=int(self._second),
                                                    calendar=temp_calendar
                                            )
        else:    
            if self._year!=self._start_year:
                self._start_date=cftime.datetime(year=self._year,
                                                month=1,
                                                day=1,
                                                hour=int(self._hour),
                                                minute=int(self._minute),
                                                second=int(self._second),
                                                calendar=temp_calendar
                                            )    
            else:
                self._start_date=cftime.datetime(year=self._year,
                                                month=self._start_arr[1],
                                                day=self._start_arr[2]+1,
                                                hour=0,
                                                minute=0,
                                                second=0,
                                                calendar=temp_calendar
                                            )


        if self._year!=self._end_year:
            self._end_date=cftime.datetime(year=self._year,
                                            month=12,
                                            day=31,
                                            hour=int(self._hour),
                                            minute=int(self._minute),
                                            second=int(self._second),
                                            calendar=temp_calendar
                                        )
        else:
            self._end_date=cftime.datetime(year=self._year,
                                            month=self._end_arr[1],
                                            day=self._end_arr[2]-1,
                                            hour=0,
                                            minute=0,
                                            second=0,
                                            calendar=temp_calendar
                                        )

    def __set_kernels(self):  
        with open("../Kernels/kernel_info.json",'r') as json_file:
            kernel_info=json.load(json_file)
        #print(kernel_info)    
        temp_start_dt_arr=[]
        temp_end_dt_arr=[]
        for kernel in kernel_info.keys():
            spiceypy.furnsh(kernel_info[kernel]['path'])
            temp_start_dt_arr.append(kernel_info[kernel]['start_date'])
            temp_end_dt_arr.append(kernel_info[kernel]['end_date'])
        temp_start=str(max(temp_start_dt_arr))
        temp_end=str(min(temp_end_dt_arr)) 
        
        self._start_year=int(temp_start[:4])
        
        self._start_arr=[int(temp_start[:4]),
                       int(temp_start[4:6]),
                       int(temp_start[6:])
                       ]
        
        self._end_arr=[int(temp_end[:4]),
                       int(temp_end[4:6]),
                       int(temp_end[6:])
                       ]
        self._end_year=self._end_arr[0]
        if self._year>=self._end_year:
            self._year=self._start_year
            
            

    def __set_constants(self):
        self._toggle_trail=False
        self._multiplier=1000
        self._cur_year_dict_index=0
        self._year_text='<red>CURRENT DATE</red>\n<green>{}-{}-{}</green><red>\n\nCURRENT TIME</red>\n<green>{}:{}:{}  (UTC)</green><red>\n\nZoom</red>\n<green>{}</green><red>\n\nACTIVE ACTIONS</red><green>{}</green>'
        self._cur_year_txt = Text(scale=1,position=(-0.85,0.45,0))
        self._sensi=0.005
        self._current_focus='Sun'
        self._toggle_free=False
        
        self._dates=[]
        

        camera.parent=scene
        self._default_zoom=-20
        camera.z=self._default_zoom
        self._max_far_zoom=300000
        camera.clip_plane_far_setter(self._max_far_zoom*2)
        self._collider_ray = raycast(origin= camera.position+camera.forward*5,
                                     ignore=(camera,), 
                                     direction= camera.forward,
                                     distance= 10, 
                                     debug= False
                                     )         
            

        self._drop_down_text='Focus on: {}'

        self._mouse_enabled_movement=False

       

        self._mouse_drag=False
        self._mouse_drag_initial=None

        self._delay_counter=0

        self._drop_menu=Entity(visible=False)
        self._slider=Entity(visible=False)

        self._thick=0.05
        self._curve_mode='line'
        
        self._info = Entity(visible=False)    
        self._info_text="<red>INFO BOARD</red>\n<white>NAME: </white><green>{}</green>\n<white>PLANET ID: </white><green>{}</green>\n<white>RADIUS: </white><green>{} km</green>\n<white>AXIAL ROTATION: </white><green>{}⁰/sec</green>\n<white>TILT: </white><green>{}⁰</green>"
        
        self._temp_position=Vec2(0,0)

        self._pause_menu_enabled=False

        self._month_drop=Entity(visible=False)
        
        self._pause=False

        self._update_frequency=1.0

        self._date_frequency_options_dict={'Hourly':'h',
                                           'Daily': 'D',
                                           'Monthly': 'ME'
                                           }
        
        self._axial_rotation_multiplier={'Hourly':3600,
                                         'Daily': 86400,
                                        'Monthly': 2629845}
        
        self._ursina_color={'violet':color.violet,
                           'cyan':color.cyan,
                           'blue':color.blue,
                           'green':color.green,
                           'yellow':color.yellow,
                           'orange':color.orange,
                           'red':color.red,
                           'pink':color.pink,
                           'white':color.white
                        }
        
        self._active_action_list=['SIMULATION NOT STARTED']

        self._pause_menu_return_val=[self._year,self._month,self._day,
                                     self._hour,self._minute,self._second]  

        self._start=False
        
    def __km2au(self,val_km: float):
        return (spiceypy.convrt(val_km,'km','au'))*self._multiplier

    def __gen_pos(self,target: int, cur_et , obs:int):   #change
        temp_planet_state_wrt_sun,temp_earth_sun_light_time=spiceypy.spkgeo(targ=target,
                                                                  et=cur_et,
                                                                  ref="ECLIPJ2000",
                                                                  obs=obs
                                                                  )  #change
        x,y,z=temp_planet_state_wrt_sun[:3]
        
        x=spiceypy.convrt(x,'km','au')*self._multiplier
        y=spiceypy.convrt(y,'km','au')*self._multiplier
        z=spiceypy.convrt(z,'km','au')*self._multiplier
        return Vec3(y,z,-x)
        '''
            URSINA ----- > SPICE
                X -------->  Y
                Y --------> Z
                Z --------> -X
        '''


    def __gen_dates(self,forced=False):
        self._dates.clear()
        
        self.__set_start_end_date(forced)
        _, temp_number_of_days = calendar.monthrange(self._year, int(self._month))

        if self._date_frequency_options_dict[self._date_frequency]=='ME' and int(self._day)<temp_number_of_days:
            self._dates.clear()
            for m in range (int(self._month),13):
                
                if self._year==self._end_year and m==self._end_arr[1]:
                    if int(self._day)>self._end_arr[2]:
                        self._day=self._end_arr[2]-1
                cf_time_object=cftime.datetime(year=self._year,
                                               month=m,
                                               day=int(self._day),
                                               hour=int(self._hour),
                                               minute=int(self._minute),
                                               second=int(self._second)
                                               )
                self._dates.append(cf_time_object)
        else:
            self._dates=list(xr.cftime_range(self._start_date, self._end_date, freq=self._date_frequency_options_dict[self._date_frequency]))
            if self._year==self._end_year and len(self._dates) < (self._end_arr[1]-int(self._month)+1):
                cf_time_object=cftime.datetime(year=self._year,
                                               month=self._end_arr[1],
                                               day=self._end_arr[2]-1,
                                               hour=int(self._hour),
                                               minute=int(self._minute),
                                               second=int(self._second)
                                               )
                self._dates.append(cf_time_object)
                
        
        

    
    def __create_planet_dict(self):
        with open(r"..\Assets\Planets_info.json",'r') as planet_json_file:
            self.planets_info=json.load(planet_json_file)
            
        
        self._master_planet_dict={}
        temp_planet_details_dict={
                                  'entity': None,
                                  'planet_id': 0,
                                  'axial_rotation': 0,
                                  "sibling_entity": None,
                                  'obs_planet_id' : 0,
                                  "text_tag_entity": None,
                                  "trail_deque": None,
                                  "curve_renderer": None,
                                  'follow': False,
                                  'trail_color': None 
                                  }
        for planet in self.planets_info.keys():
            self._master_planet_dict[planet]=temp_planet_details_dict.copy()
            temp_scale=''
            if self.planets_info[planet]["scale"]=="km2au":
                temp_scale=self.__km2au(self.planets_info[planet]['radius_km'])*2
            else:
                temp_scale=self.planets_info[planet]["scale"]*self._multiplier
                
            
            if self.planets_info[planet]['texture']=='None':
                self._master_planet_dict[planet]['entity']=Entity(name=planet, model=self.planets_info[planet]['model'],collider='box',
                                                                rotation_x = self.planets_info[planet]['rotation_x'],
                                                                rotation_z= self.planets_info[planet]['rotation_z'],
                                                                scale=temp_scale
                                                            )

            else:    
                self._master_planet_dict[planet]['entity']=Entity(name=planet, model=self.planets_info[planet]['model'],collider='box',
                                                                    rotation_z= self.planets_info[planet]['rotation_z'],
                                                                    scale=temp_scale,
                                                                    texture=self.planets_info[planet]['texture']
                                                                )
                self._master_planet_dict[planet]['entity'].setTexScale(TextureStage.getDefault(),-1,1)
           
            self._master_planet_dict[planet]['entity'].model_getter().setTwoSided(True)
            self._master_planet_dict[planet]['planet_id']=self.planets_info[planet]['id']
            self._master_planet_dict[planet]['axial_rotation']=self.planets_info[planet]['rotation_y']
            self._master_planet_dict[planet]['sibling_entity']=Entity(name=planet, visible=True, collider='box',
                                                                      scale=self.__km2au(self.planets_info[planet]['radius_km'])*2
        
                                                                     )
            self._master_planet_dict[planet]['obs_planet_id']=self.planets_info[planet]['obs_planet_id']
            
            temp_textfield_text=planet
            if self._master_planet_dict[planet]['obs_planet_id']!=10 or planet in ['moon','Saturn_ring']:
                temp_textfield_text=''

            self._master_planet_dict[planet]['text_tag_entity']=Text(parent=self._master_planet_dict[planet]['sibling_entity'],
                                                                     text=temp_textfield_text, 
                                                                     text_color=color.white,
                                                                     unlit=True,
                                                                     scale=camera.z * 0.4
                                                                     )
            self._master_planet_dict[planet]['text_tag_entity'].billboard_setter(True)
            self._master_planet_dict[planet]['text_tag_entity'].unlit=True
            self._master_planet_dict[planet]['text_tag_entity'].alpha=1

            if planet=='Sun':
                self._master_planet_dict[planet]['entity'].shader=lit_with_shadows_shader
                self._master_planet_dict[planet]['entity'].unlit=True
                

            if planet!='Sun':
                self._master_planet_dict[planet]['trail_deque']=deque([],maxlen=80)
                self._master_planet_dict[planet]['curve_renderer']=Entity(unlit=True)
                self._master_planet_dict[planet]['trail_color']=self._ursina_color[self.planets_info[planet]['color']]
    def __set_all_follow_false(self):
        for i in self._master_planet_dict.keys():
            self._master_planet_dict[i]['follow']=False  
            self._master_planet_dict[i]['text_tag_entity'].visible=False 

    def __set_follow(self,planet_name: str):
        self.__set_all_follow_false()
        if planet_name=='free':
            self._toggle_free=True
            camera.parent=scene
            camera.world_position=Vec3(0,0,self._default_zoom)
            camera.world_rotation=Vec3(0,0,0)
            camera.look_at(self._master_planet_dict['Sun']['entity'])
            self._current_focus=None
            for i in self._master_planet_dict.keys():
                self._master_planet_dict[i]['text_tag_entity'].visible=True
            
        else:
            self._toggle_free=False
            self._master_planet_dict[planet_name]['follow']=True
            self._current_focus=planet_name
            self.__focus(planet_name)    

    def __scale_sensitivity(self):
        self._sensi = self._slider.value/1000


    def __focus(self,planet_name: str):
        if planet_name==None:
                self._mouse_enabled_movement=False
                camera.look_at(self._master_planet_dict['Sun']['entity'])
                camera.parent=scene
                camera.world_rotation=Vec3(0,0,0)
                camera.world_position=Vec3(0,0,self._default_zoom)
                camera.look_at(self._master_planet_dict['Sun']['entity'])
                
                self._master_planet_dict['Sun']['follow']=False
                self._info._visible=False
                

        elif self._master_planet_dict[planet_name]['follow']:
            self._master_planet_dict[planet_name]['follow']=False
            self._mouse_enabled_movement=False
            self.__update_active_action_list(text='Following mouse',append=False)
            camera.position=Vec3(0,0,self._default_zoom)
            camera.rotation=Vec3(0,0,0)
            camera.parent=self._master_planet_dict[planet_name]['sibling_entity']
            camera.position=Vec3(0,0,0)
            camera.z=self._default_zoom
            
            camera._always_on_top=True
            self._info.enable()
            self._info._visible=True
            self._info.text=self._info_text.format( planet_name, 
                                                    self._master_planet_dict[planet_name]['planet_id'],
                                                    self.planets_info[planet_name]['radius_km'],
                                                    self._master_planet_dict[planet_name]['axial_rotation'],
                                                    self.planets_info[planet_name]['rotation_z']
                                                    )
                    

    def load_widgets(self):
        self._start_text=Text(scale =3, y = 0.2, x=-0.2,z=999,text="<red>Press 'SPACE' key\n       to\nstart the simulation</red>")
        
        Text(scale =0.7, y = -0.46, x=0.5,text="<white>Press 'tab' to open/close controls guide</white>")
        def __set_inputfield_inactive(inputfield):
            inputfield.active=False
        
    

        #Focus drop down list
        button_list=[
                    DropdownMenuButton('Free rotation',on_click=Func(self.__set_follow,'free')),
                    DropdownMenuButton('Sun',on_click=Func(self.__set_follow,'Sun')),
                    DropdownMenuButton('Mercury',on_click=Func(self.__set_follow,'Mercury')),
                    DropdownMenuButton('Venus',on_click=Func(self.__set_follow,'Venus')),
                    DropdownMenu(text='Earth and Moon',buttons=[DropdownMenuButton('Earth',on_click=Func(self.__set_follow,'Earth')),
                                                                DropdownMenuButton('Moon',on_click=Func(self.__set_follow,'Moon'))],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Mars and moons',buttons=[DropdownMenuButton('Mars',on_click=Func(self.__set_follow,'Mars')),
                                                                DropdownMenuButton('Phobos',on_click=Func(self.__set_follow,'Phobos')),
                                                                DropdownMenuButton('Deimos',on_click=Func(self.__set_follow,'Deimos'))],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Jupiter and moons',buttons=[DropdownMenuButton('Jupiter',on_click=Func(self.__set_follow,'Jupiter')),
                                                                    DropdownMenuButton('Ganymede',on_click=Func(self.__set_follow,'Ganymede')),
                                                                    DropdownMenuButton('Callisto',on_click=Func(self.__set_follow,'Callisto')),
                                                                    DropdownMenuButton('Io',on_click=Func(self.__set_follow,'Io')),
                                                                    DropdownMenuButton('Europa',on_click=Func(self.__set_follow,'Europa'))],       #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Saturn and moons',buttons=[DropdownMenuButton('Saturn',on_click=Func(self.__set_follow,'Saturn')),
                                                                    DropdownMenuButton('Titan',on_click=Func(self.__set_follow,'Titan')),
                                                                    DropdownMenuButton('Rhea',on_click=Func(self.__set_follow,'Rhea'))],           #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Uranus and Titania',buttons=[DropdownMenuButton('Uranus',on_click=Func(self.__set_follow,'Uranus')),
                                                                    DropdownMenuButton('Titania',on_click=Func(self.__set_follow,'Titania')),],    #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Neptune and Triton',buttons=[DropdownMenuButton('Neptune',on_click=Func(self.__set_follow,'Neptune')),
                                                                    DropdownMenuButton('Triton',on_click=Func(self.__set_follow,'Triton'))],      #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Pluto and Charon',buttons=[DropdownMenuButton('Pluto',on_click=Func(self.__set_follow,'Pluto')),
                                                                    DropdownMenuButton('Charon',on_click=Func(self.__set_follow,'Charon'))],      #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenuButton('Ceres',on_click=Func(self.__set_follow,'Ceres'))                          #change
                    ]


        destroy(self._drop_menu)
        self._drop_menu=DropdownMenu(x=-.60,y=0.45,text=self._drop_down_text.format(self._current_focus), 
                    buttons=button_list,color=color.white,text_color=color.red,highlight_color=color.green,
                    scale=(0.3,0.03,0.0))
        self._drop_menu.disable()

    
        #Pause menu
        
        def __cal(x: int):
            self._year_selector.active=False      
            temp_month=str(x)
            if int(temp_month)%10==int(temp_month):
                temp_month="0{}".format(int(temp_month))
            self._pause_menu_return_val[1]=temp_month
            
            self._month_drop.text='Month: '+self._pause_menu_return_val[1]

            temp_input_year=int(self._year_selector.text)
            temp_days=calendar.month(temp_input_year,x).split()[9:]
            
            
            if temp_input_year==self._end_year:
                if int(self._pause_menu_return_val[1])==self._end_arr[1]:
                    temp_days=temp_days[:self._end_arr[2]-1]
            
            elif temp_input_year==self._start_year:
                if int(self._pause_menu_return_val[1])==self._start_arr[1]:
                    temp_days=temp_days[self._start_arr[2]-1:]
            
            self._pause_menu_return_val[2]='0'*(2-len(temp_days[0])) +temp_days[0]
            self._day_selector.options=temp_days
            self._day_selector.enable()
        
            def on_value_changed():
                try:
                    temp=str(self._day_selector.value)
                    if int(temp)%10==int(temp):
                        temp="0{}".format(int(temp))
                        self._year_selector.active=False
                    self._pause_menu_return_val[2]=temp
                except:
                    pass    
            self._day_selector.on_value_changed = on_value_changed


        self._month_button_list=[
                            DropdownMenuButton('January: 01',on_click=Func(__cal,1), ignore_paused=True),
                            DropdownMenuButton('February: 02',on_click=Func(__cal,2), ignore_paused=True),
                            DropdownMenuButton('March: 03',on_click=Func(__cal,3), ignore_paused=True),
                            DropdownMenuButton('April: 04',on_click=Func(__cal,4), ignore_paused=True),
                            DropdownMenuButton('May: 05',on_click=Func(__cal,5), ignore_paused=True),
                            DropdownMenuButton('June: 06',on_click=Func(__cal,6), ignore_paused=True),
                            DropdownMenuButton('July: 07',on_click=Func(__cal,7), ignore_paused=True),
                            DropdownMenuButton('August: 08',on_click=Func(__cal,8), ignore_paused=True),
                            DropdownMenuButton('September: 09',on_click=Func(__cal,9), ignore_paused=True),
                            DropdownMenuButton('October: 10',on_click=Func(__cal,10), ignore_paused=True),
                            DropdownMenuButton('November: 11',on_click=Func(__cal,11), ignore_paused=True),
                            DropdownMenuButton('December: 12',on_click=Func(__cal,12), ignore_paused=True)
                          ]
        self._wp = WindowPanel(
                        title='Pause Menu',
                        content=(
                                Text('Adjust Sensitivity'),
                                temp_slider := Slider(1, 50, default=5,
                                                    height=Text.size, 
                                                    y=-0.4, x=-0.8, 
                                                    step=1, dynamic= True, 
                                                    on_value_changed=self.__scale_sensitivity, 
                                                    vertical=False,
                                                    bar_color = color.yellow),
                                temp_y_t:= Text('Set Year [range {} to {}]'.format(self._start_year,self._end_year)),
                                temp_year_field := InputField( limit_content_to='0123456789', active=False),                 
                                temp_day_selector:= ButtonGroup(['Day'],max_selection=1,
                                                                min_selection=1,
                                                                spacing=(0.05,0.05,0)),
                                temp_t_t:= Text('Set Time HH:MM:SS'),
                                temp_time_field := InputField( limit_content_to=':0123456789', active=False),
                                temp_d_f_t:= Text('Set Date Change Frequency'),
                                temp_date_frequency_button := ButtonGroup(self._date_frequency_options_dict.keys(),
                                                                          max_selection=1,min_selection=1,
                                                                          default=self._date_frequency,
                                                                          spacing=(0.1,0,0)
                                                                          ),
                                temp_u_f_t:= Text('Set Update Frequency: \n  (in seconds)'),
                                temp_update_frequency_field := InputField( limit_content_to='.0123456789', active=False),                 
                                                                                                             
                                ),
                        popup=True
                        )
        
        self._slider=temp_slider
        self._slider.knob.ignore_paused= True
        self._slider.ignore_paused=True
        
        self._year_selector=temp_year_field
        self._year_selector.world_position=temp_y_t.world_position+Vec3(4.5,-1.5,0)
        self._year_selector.text=str(self._pause_menu_return_val[0])
        self._year_selector.submit_on=['enter',]
        self._year_selector.on_submit=Func(__set_inputfield_inactive,self._year_selector)
        
        self._month_drop=DropdownMenu()
    
        self._day_selector=temp_day_selector
        self._day_selector.disable()
        
        self._month_drop.parent=self._wp
        self._month_drop.world_position=self._year_selector.world_position+Vec3(-7.5,-1,0)
        self._month_drop.scale=0.5
        self._month_drop.text='Select Month'
        
        self.__set_month_drop_buttons(self._month_button_list[:self._start_arr[1]-1],initial=True)
        self.__set_month_drop_buttons(self._month_button_list[self._start_arr[1]-1:])
        self._month_drop.buttons=self._month_button_list
        
        self._month_drop.disable()
               
        temp_t_t.position=self._month_drop.position+Vec3(-0.1,-7,0) 
        
        self._time_selector_field=temp_time_field
        self._time_selector_field.world_position=temp_t_t.world_position+Vec3(4.5,-1.5,0) 
        self._time_selector_field.submit_on=['enter',]
        self._time_selector_field.on_submit=Func(__set_inputfield_inactive,self._time_selector_field)
        self._time_selector_field.text=''.join(e for e in self._pause_menu_return_val[3:6])

        temp_d_f_t.position=temp_t_t.position+Vec3(1.125,0,0)
        
        self._date_frequency_button=temp_date_frequency_button
        def _date_frequency_button_on_value_changed():
                temp=str(self._date_frequency_button.value)
                if temp in self._date_frequency_options_dict.keys():
                    self._date_frequency=temp
                    
        self._date_frequency_button.on_value_changed = _date_frequency_button_on_value_changed

        self._date_frequency_button.world_position=temp_d_f_t.world_position+Vec3(-0.5,-1,0) 

        temp_u_f_t.position=temp_t_t.position+Vec3(0,-3.5,0) 
        
        self._update_frequency_field=temp_update_frequency_field
        self._update_frequency_field.world_position=temp_u_f_t.world_position+temp_u_f_t.right*0.50 
        self._update_frequency_field.text=str(self._update_frequency)
        self._update_frequency_field.submit_on=['enter',]
        self._update_frequency_field.on_submit=Func(__set_inputfield_inactive,self._update_frequency_field)
        self._wp._always_on_top=True
        self._wp.x=0.2
        self._wp.y=0.475
        self._wp.disable()
        
        self._wp.bg.on_click=None
        self._wp.panel.world_scale=Vec3(20,25,0)
        try:
            self._wp.panel.texture=r'..\Assets\flipped_vertical_gradient'
        except:
            self._wp.panel.texture='vertical_gradient'
        self._wp.panel.color=color.hsv(200,0.6,0.1,1)
        
        self._info = Text(scale =1, y = -0.10, x=-0.85, wordwrap=30, color=color.tint(color.white,0.9))
        self._info.current_color=color.red
        self._info._visible=False

        control_text='''
<red>Zoom in  : </red><green>Scroll up / w</green>
<red>Zoom out :</red><green> Scroll down / s</green>
<red>Camera move left  :</red><green> a</green>
<red>Camera move right :</red><green> d</green>
<red>Camera move up    :</red><green> z</green>
<red>Camera move down  :</red><green> x</green>

<red>Rotate camera up    :</red><green> Up arrow</green>
<red>Rotate camera down  :</red><green> Down arrow</green>
<red>Rotate camera left  :</red><green> left arrow</green>
<red>Rotate camera right :</red><green> Right arrow</green>
<red>Rotate camera around axis :</red><green> c / v</green>

<red>Pause / unpause simulation :</red><green> P / p</green>
<red>Toggle pause menu  :</red><green> Esc</green>
<red>Toggle full screen :</red><green> F / f</green>
<red>Toggle trail :</red><green> T / t</green>
<red>Enable mouse associated camera movement :</red><green> M / m</green>
<white>(*Available only in focus: None)</white>

<red>Deletes trail :</red><green> Backspace</green>
<red>Ambient light off/on :</red><green> L / l</green>

<red>Start stimulation :</red><green> Spacebar</green>

<red>Toggle Controls guide :</red><green> tab</green>

<white>  **While mouse associated movement enabled.. **</white>
<red>Rotate camera left and right :</red><green> Left click / Right click</green>
<red>Rotate camera up and down    :</red><green> Ctrl + Left / Right click</green>
<red>Rotate camera around axis    :</red><green> Alt + Left / Right click</green>'''

        self._control_window=WindowPanel(
                                        title='<white>Controls Guide</white>',
                                        content=(
                                                Text(text=control_text),
                                                ),
                                        popup=True
                                        ) 
        self._control_window.x=0.2
        self._control_window.y=0.475
        self._control_window.disable()
        self._control_window._always_on_top=True
        self._control_window.bg.on_click=None
        self._control_window.panel.world_scale=Vec3(20,25,0)
        try:
            self._control_window.panel.texture=r'..\Assets\flipped_vertical_gradient'
        except:
            self._control_window.panel.texture='vertical_gradient'
        self._control_window.panel.color=color.hsv(200,0.6,0.1,1)
               

    def __set_month_drop_buttons(self,temp_button_list,initial=False):
            if initial:
                height=Vec3(9999,9999,9999)
            else:    
                height=self._month_drop.down*2
            for i in temp_button_list:
                i.parent=self._month_drop
                i.scale=1
                i.position=height
                height+=i.down*2
        

    def __year_selector_enable(self,status: bool):
            if status:
                self._month_drop.disable()
                self._year_selector.text_color=color.green
                temp_input_year=int(self._year_selector.text)
                                
                if temp_input_year==self._start_year:
                    temp_buttons=self._month_button_list[self._start_arr[1]-1:]
                elif temp_input_year==self._end_year:
                    temp_buttons=self._month_button_list[:self._end_arr[1]]
                else:
                    temp_buttons=self._month_button_list
                self.__set_month_drop_buttons(temp_button_list=temp_buttons)   
                
                self._month_drop.buttons=temp_buttons
                
                self._month_drop.enable()    
                
            else:
                self._year_selector.text_color=color.red
                self._month_drop.disable()
                try:
                    self._day_selector.disable()
                    
                except:
                    pass
    
    
    def __camera_control(self):

        if not self._start:
            return
       
        if self._mouse_drag and self._mouse_drag_initial!=None:
            temp_x=mouse.x - self._mouse_drag_initial[0]
            temp_y=mouse.y - self._mouse_drag_initial[1]

            camera.position+=abs(camera.z) * (camera.up*abs(min(0,temp_y))+camera.down*abs(max(0,temp_y))) * time.dt * self._sensi * 100
            camera.position+=abs(camera.z) * (camera.right*abs(min(0,temp_x))+camera.left*abs(max(0,temp_x))) * time.dt * self._sensi *100
    
            
        if self._collider_ray.entity==None:
            camera.position +=camera.forward *100 * held_keys['w'] * time.dt * max(1,abs(camera.z)) * 0.005
        camera.position +=camera.back * 100 * held_keys['s'] * time.dt * max(1,abs(camera.z)) * 0.005

        
        camera.position +=camera.left * 20 * held_keys['a'] * time.dt * max(10,abs(camera.z)) * 0.005
        camera.position +=camera.right * 20 * held_keys['d'] * time.dt * max(10,abs(camera.z)) * 0.005
        camera.position +=camera.up * 20 * held_keys['z'] * time.dt  * max(10,abs(camera.z)) * 0.005
        camera.position +=camera.down  * 20 * held_keys['x'] * time.dt * max(10,abs(camera.z)) * 0.005
        
        camera.rotate(Vec3(20 *held_keys['down arrow'] * time.dt* max(1000,abs(camera.z)%5000) * 0.0005 , 
                              20 *held_keys['right arrow'] * time.dt * max(1000,abs(camera.z)%5000) * 0.0005,
                              20 *held_keys['c'] * time.dt))

        camera.rotate(Vec3(-20 *held_keys['up arrow'] * time.dt* max(1000,abs(camera.z)%5000) * 0.0005 ,
                              -20 *held_keys['left arrow'] * time.dt* max(1000,abs(camera.z)%5000) * 0.0005 ,
                              -20 *held_keys['v'] * time.dt))

        if self._mouse_enabled_movement and self._toggle_free:            
            self._mouse_drag=False
            self._mouse_drag_initial=None
             
            camera.position+= (camera.right*mouse.x + camera.up*mouse.y) *self._sensi * max(abs(camera.z),10) * 10

            temp_multiplier= (held_keys['right mouse'] or held_keys['left mouse']) *time.dt * self._sensi * 10000

            camera.rotate(Vec3(held_keys['right mouse'] * int(bool(held_keys['control'] * temp_multiplier)),
                                held_keys['right mouse'] * int(not(held_keys['control'] or held_keys['alt'] * temp_multiplier)) ,
                                held_keys['right mouse'] * int(bool(held_keys['alt'] * temp_multiplier))
                               )
                         )
            camera.rotate(Vec3(-held_keys['left mouse'] * int(bool(held_keys['control'] * temp_multiplier)),
                                -held_keys['left mouse'] * int(not(held_keys['control'] or held_keys['alt'] * temp_multiplier)) ,
                                -held_keys['left mouse'] * int(bool(held_keys['alt'] * temp_multiplier))
                               )
                         )
    

    def __update_active_action_list(self,text: str,append: bool):
        if append:
            if text not in self._active_action_list:
                self._active_action_list.append(text)
                self.__update_active_action_list(text='None',append=False)
        else:   
            if text in self._active_action_list:
                self._active_action_list.remove(text)
                if self._active_action_list==[]:
                    self._active_action_list=['None']


    def custom_input(self,key):
        
        if key=='space':
            if not self._start:
                destroy(self._start_text)
                self._active_action_list=['Ambient Lights On']
                self._drop_menu.enable()
            self._start=True
            

        if not self._start:        
            return
        
        if key=='scroll up':
            if self._collider_ray.entity==None:
                camera.world_position +=camera.forward*abs(camera.z)*self._sensi
        
        elif key=='scroll down':
            camera.world_position +=camera.back*abs(camera.z)*self._sensi
        
        elif key=='left mouse down' and not self._mouse_enabled_movement:
            self._mouse_drag=True
            if self._pause_menu_enabled:
                self._mouse_drag=False
            if self._mouse_drag_initial==None and self._mouse_drag:
                self._mouse_drag_initial=mouse.position
                self.__update_active_action_list(text='Mouse Drag',append=True)
        
        elif key=='left mouse up' and not self._mouse_enabled_movement:
            self._mouse_drag=False
            self._mouse_drag_initial=None
            self.__update_active_action_list(text='Mouse Drag',append=False)
        
        elif key in ['m','M']:
            if self._toggle_free and not self._pause_menu_enabled:
                self._mouse_enabled_movement = not self._mouse_enabled_movement
            else:
                pass
            if self._mouse_enabled_movement:
                self.__focus('Sun')
                self.__update_active_action_list(text='Following mouse',append=True)
            else:   
                self.__update_active_action_list(text='Following mouse',append=False)

        elif key in ['t','T']:
            if self._toggle_trail:
                try:
                    for planet in self._master_planet_dict.keys():
                        destroy(self._master_planet_dict[planet]['curve_renderer'])
                except:
                    pass    
            self._toggle_trail = not self._toggle_trail

            if self._toggle_trail:
                self.__update_active_action_list(text='Showing Trails',append=True)
            else:   
                self.__update_active_action_list(text='Showing Trails',append=False)

        elif key in ['f','F']:
            if window.size!=window.fullscreen_size:
                self._temp_position=window.position
                window.size=window.fullscreen_size
                window.position=Vec2(0,0)
            else:
                window.position=(window.size-Vec2(1164,582))/2
                window.size=Vec2(1164,582)

        elif key == 'backspace':
            for planet in self._master_planet_dict.keys():
                if planet=='Sun':
                    continue
                try:
                    destroy(self._master_planet_dict[planet]['curve_renderer'])
                except:
                    pass
                try:
                    self._master_planet_dict[planet]['trail_deque'].clear()     
                except:
                    pass

        elif key=='escape':
            self._pause_menu_enabled= not self._pause_menu_enabled
            if self._pause_menu_enabled:
                self._mouse_enabled_movement=False
                self.__update_active_action_list(text='Following mouse',append=False)

                self._drop_menu.disable()

                self._pause_menu_return_val=[self._year,self._month,self._day,
                                    self._hour,self._minute,self._second] 
                
                self.__update_active_action_list(text='Showing Controls',append=False)
                self._control_window.disable()
                self._wp.enable()
                self._year_selector.text=str(self._year)
                self._time_selector_field.text=''.join(e for e in self._pause_menu_return_val[3:6])
                self._month_drop.close()
                
                self.__update_active_action_list(text='Pause Menu Opened',append=True)

            else:                
                self._drop_menu.enable()
                self._wp.disable()
                self.__update_active_action_list(text='Showing Controls',append=False)
                self._control_window.disable()
                self._year, self._month, self._day = self._pause_menu_return_val[0:3]
                self._hour, self._minute, self._second = self._pause_menu_return_val[3:6]
                self.__gen_dates(forced=True)
                self._cur_year_dict_index=0
                self.__update_active_action_list(text='Pause Menu Opened',append=False)

        elif key in ['p','P']:
            self._pause= not self._pause
            
            if self._pause:
                self.__update_active_action_list(text='Simulation Paused',append=True)
            else:   
                self.__update_active_action_list(text='Simulation Paused',append=False)

        elif key in ['l','L']:
            if self._ambient_light.color==color.dark_gray:
                self._ambient_light.color=color.black
                self._master_planet_dict['Sun']['entity'].unlit=False
                self.__update_active_action_list(text='Ambient Lights On',append=False)
                self.__update_active_action_list(text='Ambient Lights Off',append=True)
            elif self._ambient_light.color==color.black:
                self._ambient_light.color=color.dark_gray
                self._master_planet_dict['Sun']['entity'].unlit=True
                self.__update_active_action_list(text='Ambient Lights On',append=True)
                self.__update_active_action_list(text='Ambient Lights Off',append=False)

        elif key=='tab':
            if self._control_window.enabled==False:
                self._mouse_enabled_movement=False
                self.__update_active_action_list(text='Following mouse',append=False)

                self._drop_menu.disable()
                self._wp.disable()
                self._control_window.enable()
        
                self.__update_active_action_list(text='Showing Controls',append=True)

            else:                
                self._drop_menu.enable()
                self._control_window.disable()
                self.__update_active_action_list(text='Showing Controls',append=False)
        
                if self._pause_menu_enabled:
                    self._pause_menu_enabled=False
                    self.custom_input('escape')
                
                
           
        

    def custom_update(self):
        if self._pause_menu_enabled:
            self._sensi = self._slider.value/1000
            if self._year_selector.active:
                if self._year_selector.text!='':
                    if int(self._year_selector.text) in range(self._start_year,self._end_year+1):
                        self.__year_selector_enable(True)
                    else:
                        self.__year_selector_enable(False)
            if not self._year_selector.active:
                if self._year_selector.text=="":
                    self.__year_selector_enable(False)
                elif self._month_drop.enabled==True:
                    self._pause_menu_return_val[0]=int(self._year_selector.text)
            else:
                pass
            if self._time_selector_field.active:
                temp=self._time_selector_field.text.replace(':','')
                self._time_selector_field.text=temp
                if len(temp)>0:
                    temp=temp+'0'*(6-len(temp))
                if len(self._time_selector_field.text) in range (1,7) and int(temp[:2])<24 and int (temp[2:4])<60 and int (temp[4:])<60:
                    self._time_selector_field.text_color=color.green    
                else :
                    self._time_selector_field.text_color=color.red
                    self._time_selector_field.text=self._time_selector_field.text[:7]
            else:
                temp=self._time_selector_field.text
                temp=temp.replace(":",'')
                if len(temp) in range (1,7):
                    temp+='0'*(6-len(temp))
                    if int(temp[0:2])<24 and int(temp[2:4])<60 and int(temp[4:6])<60 :
                        self._pause_menu_return_val[3]=temp[0:2]
                        self._pause_menu_return_val[4]=temp[2:4]
                        self._pause_menu_return_val[5]=temp[4:6]
                           
                self._time_selector_field.text=(''.join(e+':' for e in self._pause_menu_return_val[3:6]))[:8]
                self._time_selector_field.text_color=color.green
                
            try:
                if self._day_selector.value!='Day':
                    #self._pause_menu_return_val[2]='0'*(2-len(self._day_selector.value))+self._day_selector.value
                    pass
            except:
                pass
            
            if self._update_frequency_field.active:
                temp=self._update_frequency_field.text
                if temp.count('.')==2:
                    self._update_frequency_field.text=temp[:len(temp)-1]
            else:
                temp=self._update_frequency_field.text
                if temp in ['0','0.0','']:
                    self._update_frequency_field.text=str(self._update_frequency)
                else:
                    self._update_frequency=float(temp)
            
        if not self._pause_menu_enabled:
            self.__camera_control()
        if int(window.fps_counter.text)<20:
            self._curve_mode='point'
        else:
            self._curve_mode='line'    
        
        if abs(camera.z)>self._max_far_zoom:
            camera.z=-self._max_far_zoom
        
        self._collider_ray = raycast(origin= camera.world_position,
                                    ignore=(camera,),
                                    direction= camera.forward,
                                    distance= 0.3, 
                                    debug= False
                                    )
        self._drop_menu.text=self._drop_down_text.format(self._current_focus)
        
        self._cur_year_txt.text = self._year_text.format(self._year,self._month,self._day,
                                                         self._hour,self._minute,self._second,
                                                         camera.z,
                                                         ''.join('\n'+e for e in self._active_action_list)) 

        if self._toggle_free:
            self._info.disable()
            self._info._visible=False

        if self._pause:
            if self._toggle_trail :
                        for planet in self._master_planet_dict.keys():
                            if planet=='Sun':
                                continue
                            destroy(self._master_planet_dict[planet]['curve_renderer'])
                            try:
                                self._master_planet_dict[planet]['curve_renderer']= Entity(model=Mesh(
                                                                                                    vertices=self._master_planet_dict[planet]['trail_deque'],
                                                                                                    mode=self._curve_mode,
                                                                                                    thickness=self._thick
                                                                                                    ),
                                                                                        color=self._master_planet_dict[planet]['trail_color'] 
                                                                                        )  
                            except:
                                pass    
        
        else:        
            self._delay_counter+=time.dt
            
            temp_cur_utc=str(self._dates[self._cur_year_dict_index])
            temp_cur_utc=temp_cur_utc.replace(" ",'T')
            self._year=int(temp_cur_utc[:4])
            self._month=temp_cur_utc[5:7]
            T_index=temp_cur_utc.index("T")
            self._day=temp_cur_utc[8:T_index]
            self._hour=temp_cur_utc[T_index+1:T_index+3]
            self._minute=temp_cur_utc[T_index+4:T_index+6]
            self._second=temp_cur_utc[T_index+7:T_index+9]

            if self._delay_counter>=self._update_frequency:
                if self._start:
                    self._cur_year_dict_index += 1
                self._delay_counter=0

            if self._cur_year_dict_index==len(self._dates):
                self._year +=1
                self._month='01'
                if self._year>self._end_year:  
                    self._year=self._start_year
                    if self._date_frequency_options_dict[self._date_frequency]=='ME' and int(self._day)==self._end_arr[2]-1:
                        self._day='31'     
                self.__gen_dates()
                self._cur_year_dict_index=0
            temp_cur_et=spiceypy.utc2et(temp_cur_utc)
            
            if self._delay_counter==0:
                for planet in self._master_planet_dict.keys():                    
                    if planet!='Sun':
                        temp_obs_planet_id=self._master_planet_dict[planet]['obs_planet_id']
                        if temp_obs_planet_id!=10:
                            self._master_planet_dict[planet]['entity'].position= self.__gen_pos(self._master_planet_dict[planet]['planet_id'],temp_cur_et,temp_obs_planet_id) + self.__gen_pos(temp_obs_planet_id,temp_cur_et,10)
                        else:
                            self._master_planet_dict[planet]['entity'].position=self.__gen_pos(self._master_planet_dict[planet]['planet_id'],temp_cur_et,temp_obs_planet_id)           
                    self._master_planet_dict[planet]['sibling_entity'].position=self._master_planet_dict[planet]['entity'].position
                    self._master_planet_dict[planet]['text_tag_entity'].world_position=self._master_planet_dict[planet]['sibling_entity'].position
                    self._master_planet_dict[planet]['text_tag_entity'].world_scale=abs(camera.z) * 0.50
                    if self._start:
                        self._master_planet_dict[planet]['entity'].rotate(Vec3(0,
                                                                               self._master_planet_dict[planet]['axial_rotation']*self._axial_rotation_multiplier[self._date_frequency],
                                                                               0 )
                                                                         )       
                    if planet!='Sun':
                        if self._delay_counter==0 :
                            self._master_planet_dict[planet]['trail_deque'].append(self._master_planet_dict[planet]['entity'].position)
                        
                        if self._toggle_trail :
                            destroy(self._master_planet_dict[planet]['curve_renderer'])
                        
                            try:
                                self._master_planet_dict[planet]['curve_renderer']= Entity(model=Mesh(
                                                                                                    vertices=self._master_planet_dict[planet]['trail_deque'],
                                                                                                    mode=self._curve_mode,
                                                                                                    thickness=self._thick
                                                                                                    ),
                                                                                        unlit=True,
                                                                                        color=self._master_planet_dict[planet]['trail_color'] 
                                                                                        )  
                            except:
                                pass


app=Ursina(title='Shunya', icon=r'../Assets/Shunya.ico',render_mode='onscreen', development_mode=False)
window.windowed_position=Vec2(137,77)
window.color=color.black
camera.overlay.color=color.black
logo = Sprite(name='ursina_splash', parent=camera.ui, texture=r'../Assets/Shunya.png', world_z=camera.overlay.z-1, scale=0.25, color=color.clear)
logo.animate_color(color.white, duration=4, delay=2, curve=curve.out_quint_boomerang)
camera.overlay.animate_color(color.clear, duration=2, delay=7)
destroy(logo, delay=11)

my_exit_button=Button(texture='../Assets/close.png', eternal=True, ignore_paused=True, origin=(.5, .5), enabled=True,
            position=window.top_right-Vec2(0.02,0.02), z=-999, scale=0.05, color=color.red.tint(-.2), on_click=application.quit, name='exit_button',unlit=True) 

screen_size=(int(window.fullscreen_size[0]),int(window.fullscreen_size[1]))
window.size=Vec2(2,1)
app.step()
window._icon=r'../Assets/Shunya.ico'
window._title='Shunya'

while True:
    ursina_start=False
    myapp = QApplication([])
    w = MainWindow()    
    print('HELLO')
    w.show()
    myapp.exec()
    del myapp

    if ursina_start==True:
        window.position=Vec2(0,0)
        window.size=window.fullscreen_size      
        scene.clear()
        camera.overlay.color=color.black
        logo = Sprite(name='ursina_splash', parent=camera.ui, texture=r'../Assets/Shunya.png', world_z=camera.overlay.z-1, scale=0.25, color=color.clear)
        logo.animate_color(color.white, duration=4, delay=2, curve=curve.out_quint_boomerang)
        camera.overlay.animate_color(color.clear, duration=2, delay=7)
        destroy(logo, delay=9)
        solarsystem=SolarSystem(app)
        solarsystem.load_widgets()

        def ursina_my_window_exit():
            global ursina_start,app
            ursina_start=False
            camera.parent=scene
            camera.world_position=Vec3(0,0,0)
            camera.world_rotation=Vec3(0,0,0)            
            solarsystem.filters.del_bloom()
            app.render.clearLight()
            
        my_exit_button.on_click=ursina_my_window_exit  
        i=0

        def input(key):
            solarsystem.custom_input(key)

        def update():
            global ursina_start,app,i

            if not ursina_start:
                scene.clear()
                window.size=Vec2(2,1)
                i+=1
                if i>=2:
                    raise Exception()
                
            else:
                try:   
                    solarsystem.custom_update()
                except Exception as e :
                    print(e)

        try:
            app.run()
        except :
            pass    
            
    else:
        break






















