import spiceypy
from ursina import *
import datetime
import numpy
from collections import deque
import xarray as xr
import cftime
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import time as Time
import pandas as pd
import calendar
import json

class SolarSystem():
    def __init__(self):
        self.__set_date_year()
        self.__set_kernels()
        self.__set_constants()
        self.__create_planet_dict()
        #self.__gen_dates(self._start_date.format(self._year),self._end_date.format(self._year))
        self.__gen_dates()


    def __set_date_year(self):    
        #self._start_date = "{}-01-04"
        #self._end_date = "{}-12-31" 
        self._start_year=0
        self._end_year=0
        self._year=self._start_year
        self._month="01"
        self._day="01"
        self._hour="00"
        self._minute='00'
        self._second='00'
        self._date_frequency='Daily'
        self._start_date=cftime.datetime
        self._end_date=cftime.datetime
        self._end_arr=[]
        self._start_arr=[]

        
    def __set_start_end_date(self,forced=False):
        if forced:
            self._start_date=cftime.datetime(year=self._year,
                                                    month=int(self._month),
                                                    day=int(self._day),
                                                    hour=int(self._hour),
                                                    minute=int(self._minute),
                                                    second=int(self._second)
                                            )
        else:    
            if self._year!=self._start_year:
                self._start_date=cftime.datetime(year=self._year,
                                                month=1,
                                                day=1,
                                                hour=int(self._hour),
                                                minute=int(self._minute),
                                                second=int(self._second)
                                            )    
            else:
                self._start_date=cftime.datetime(year=self._year,
                                                month=self._start_arr[1],
                                                day=self._start_arr[2]+1,
                                                hour=0,
                                                minute=0,
                                                second=0
                                            )


        if self._year!=self._end_year:
            self._end_date=cftime.datetime(year=self._year,
                                            month=12,
                                            day=31,
                                            hour=int(self._hour),
                                            minute=int(self._minute),
                                            second=int(self._second)
                                        )
        else:
            self._end_date=cftime.datetime(year=self._year,
                                            month=self._end_arr[1],
                                            day=self._end_arr[2]-1,
                                            hour=0,
                                            minute=0,
                                            second=0
                                        )

    def __set_kernels(self):  
        """ spiceypy.furnsh("../Kernels/lsk/naif0012.tls")
        spiceypy.furnsh("../Kernels/spk/de430.bsp")
        spiceypy.furnsh("../Kernels/spk/jup365.bsp")    #change
        spiceypy.furnsh("../Kernels/spk/sat441.bsp")    #change
        spiceypy.furnsh("../Kernels/spk/nep097.bsp")    #change
        spiceypy.furnsh("../Kernels/spk/ura111l.bsp")   #change
        spiceypy.furnsh("../Kernels/spk/mar097.bsp")    #change
        #spiceypy.furnsh("../Kernels/spk/codes_300ast_20100725.bsp")    #change
        #spiceypy.furnsh("../Kernels/spk/ceres-2003-2016.bsp")    #change
        spiceypy.furnsh("../Kernels/spk/ceres_1900_2100.bsp")    #change
        spiceypy.furnsh("../Kernels/spk/plu058.bsp")    #change
        """
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
        self._year=self._start_year
        self._month=temp_start[4:6]
        self._day=temp_start[6:] 
        self._start_arr=[int(temp_start[:4]),
                       int(temp_start[4:6]),
                       int(temp_start[6:])
                       ]
        
        self._end_arr=[int(temp_end[:4]),
                       int(temp_end[4:6]),
                       int(temp_end[6:])
                       ]
        self._end_year=self._end_arr[0]
            
            

    def __set_constants(self):
        self._toggle_trail=False
        self._multiplier=1000
        self._cur_year_dict_index=0
        self._year_text='<red>CURRENT DATE</red>\n<green>{}-{}-{}</green><red>\nCURRENT TIME</red>\n<green>{}:{}:{}</green><red>\nZoom</red>\n<green>{}</green><red>\nACTIVE ACTIONS</red><green>{}</green>'
        self._cur_year_txt = Text(scale=1,position=(-0.85,0.45,0))
        self._sensi=0.005
        self._current_focus='sun'
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
                                     debug= True
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
        
        self._active_action_list=['None']

        self._pause_menu_return_val=[self._year,self._month,self._day,
                                     self._hour,self._minute,self._second]  

        
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
        return Vec3(x,y,z)


    def __gen_dates(self,forced=False):
        self._dates.clear()
        
        self.__set_start_end_date(forced)
        _, temp_number_of_days = calendar.monthrange(self._year, int(self._month))

        if self._date_frequency_options_dict[self._date_frequency]=='ME' and int(self._day)<temp_number_of_days:
            #print([self._year,self._month,self._day,temp_number_of_days])
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
                
        
        #print(self._start_date)
        #print(self._end_date)
        #print(self._dates)
        

    
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
            if planet in ["saturn_ring"]:
                self._master_planet_dict[planet]['entity']=Entity(name=planet, model=self.planets_info[planet]['model'],collider='box',
                                                                rotation_x = self.planets_info[planet]['rotation_x'],
                                                                rotation_z= self.planets_info[planet]['rotation_z'],
                                                                scale=6.68459e-9*10000,
                                                                texture=self.planets_info[planet]['texture']
                                                            )


            else:
                if self.planets_info[planet]['texture']=='None':
                    self._master_planet_dict[planet]['entity']=Entity(name=planet, model=self.planets_info[planet]['model'],collider='box',
                                                                    rotation_x = self.planets_info[planet]['rotation_x'],
                                                                    rotation_z= self.planets_info[planet]['rotation_z'],
                                                                    scale=self.__km2au(self.planets_info[planet]['radius_km'])*2
                                                                    
                                                                    
                                                                )

                else:    
                    self._master_planet_dict[planet]['entity']=Entity(name=planet, model=self.planets_info[planet]['model'],collider='box',
                                                                        rotation_x = self.planets_info[planet]['rotation_x'],
                                                                        rotation_z= self.planets_info[planet]['rotation_z'],
                                                                        scale=self.__km2au(self.planets_info[planet]['radius_km'])*2,
                                                                        texture=self.planets_info[planet]['texture']
                                                                    )
                    


            
            self._master_planet_dict[planet]['planet_id']=self.planets_info[planet]['id']
            self._master_planet_dict[planet]['axial_rotation']=self.planets_info[planet]['rotation_y']
            self._master_planet_dict[planet]['sibling_entity']=Entity(name=planet, visible=True, collider='box',
                                                                      scale=self.__km2au(self.planets_info[planet]['radius_km'])*2,
                                                                     )
            self._master_planet_dict[planet]['obs_planet_id']=self.planets_info[planet]['obs_planet_id']
            
            self._master_planet_dict[planet]['text_tag_entity']=Text(parent=self._master_planet_dict[planet]['sibling_entity'],
                                                                     text=planet, 
                                                                     scale=camera.z * 0.4
                                                                     )

            if planet!='sun':
                self._master_planet_dict[planet]['trail_deque']=deque([],maxlen=80)
                self._master_planet_dict[planet]['curve_renderer']=Entity()
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
            camera.position=Vec3(0,0,self._default_zoom)
            self._current_focus=None
            for i in self._master_planet_dict.keys():
                self._master_planet_dict[i]['text_tag_entity'].visible=True
            #self.__focus('None')

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
                camera.parent=scene
                camera.look_at(self._master_planet_dict['sun']['sibling_entity'])
                camera.position=(0,10,self._default_zoom)
                camera.look_at(self._master_planet_dict['sun']['sibling_entity'])
                self._master_planet_dict['sun']['follow']=False
                self._info._visible=False

        elif self._master_planet_dict[planet_name]['follow']:
            self._mouse_enabled_movement=False
            self.__update_active_action_list(text='Following mouse',append=False)
            camera.position=Vec3(0,0,self._default_zoom)
            camera.rotation=Vec3(0,0,0)
            camera.parent=self._master_planet_dict[planet_name]['sibling_entity']
            camera.position=Vec3(0,0,0)
            camera.z=self._default_zoom
            self._master_planet_dict[planet_name]['follow']=False
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
        
        def __set_inputfield_inactive(inputfield):
            inputfield.active=False

        #Focus drop down list
        button_list=[
                    DropdownMenuButton('Free rotation',on_click=Func(self.__set_follow,'free')),
                    DropdownMenuButton('Sun',on_click=Func(self.__set_follow,'sun')),
                    DropdownMenuButton('Mercury',on_click=Func(self.__set_follow,'mercury')),
                    DropdownMenuButton('Venus',on_click=Func(self.__set_follow,'venus')),
                    DropdownMenu(text='Earth and Moon',buttons=[DropdownMenuButton('Earth',on_click=Func(self.__set_follow,'earth')),
                                                                DropdownMenuButton('Moon',on_click=Func(self.__set_follow,'moon'))],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Mars and moons',buttons=[DropdownMenuButton('Mars',on_click=Func(self.__set_follow,'mars')),
                                                                DropdownMenuButton('Phobos',on_click=Func(self.__set_follow,'phobos')),
                                                                DropdownMenuButton('Deimos',on_click=Func(self.__set_follow,'deimos'))],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Jupiter and moons',buttons=[DropdownMenuButton('Jupiter',on_click=Func(self.__set_follow,'jupiter')),
                                                                    DropdownMenuButton('Ganymede',on_click=Func(self.__set_follow,'ganymede')),
                                                                    DropdownMenuButton('Callisto',on_click=Func(self.__set_follow,'callisto')),
                                                                    DropdownMenuButton('Io',on_click=Func(self.__set_follow,'io')),
                                                                    DropdownMenuButton('Europa',on_click=Func(self.__set_follow,'europa'))],       #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Saturn and moons',buttons=[DropdownMenuButton('Saturn',on_click=Func(self.__set_follow,'saturn')),
                                                                    DropdownMenuButton('Titan',on_click=Func(self.__set_follow,'titan')),
                                                                    DropdownMenuButton('Rhea',on_click=Func(self.__set_follow,'rhea'))],           #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Uranus and Titania',buttons=[DropdownMenuButton('Uranus',on_click=Func(self.__set_follow,'uranus')),
                                                                    DropdownMenuButton('Titania',on_click=Func(self.__set_follow,'titania')),],    #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Neptune and Triton',buttons=[DropdownMenuButton('Neptune',on_click=Func(self.__set_follow,'neptune')),
                                                                    DropdownMenuButton('Triton',on_click=Func(self.__set_follow,'triton'))],      #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenu(text='Pluto and Charon',buttons=[DropdownMenuButton('Pluto',on_click=Func(self.__set_follow,'pluto')),
                                                                    DropdownMenuButton('Charon',on_click=Func(self.__set_follow,'charon'))],      #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
                    DropdownMenuButton('Ceres',on_click=Func(self.__set_follow,'ceres'))                          #change
                    ]


        destroy(self._drop_menu)
        self._drop_menu=DropdownMenu(x=-.60,y=0.45,text=self._drop_down_text.format(self._current_focus), 
                    buttons=button_list,color=color.white,text_color=color.red,highlight_color=color.green,
                    scale=(0.3,0.03,0.0))

    
        #Pause menu
        
        def __cal(x: int):
                     
            temp_month=str(x)
            if int(temp_month)%10==int(temp_month):
                temp_month="0{}".format(int(temp_month))
            self._pause_menu_return_val[1]=temp_month
            
            self._month_drop.text='Month: '+self._pause_menu_return_val[1]
        
            temp_days=calendar.month(self._pause_menu_return_val[0],x).split()[9:]
            temp_input_year=self._pause_menu_return_val[0]
            
            if temp_input_year==self._end_year:
                if int(self._pause_menu_return_val[1])==self._end_arr[1]:
                    temp_days=temp_days[:self._end_arr[2]-1]
            
            elif temp_input_year==self._start_year:
                if int(self._pause_menu_return_val[1])==self._start_arr[1]:
                    temp_days=temp_days[self._start_arr[2]-1:]
            

            self._pause_menu_return_val[2]='0'*(2-len(temp_days[0])) +temp_days[0]
            #print(self._pause_menu_return_val)
            self._day_selector.options=temp_days
            #self._day_selector.default_values=(self._pause_menu_return_val[2],)
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
                                temp_slider := Slider(0, 20, default=5,
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
                                temp_u_f_t:= Text('Set Update Frequency: '),
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
        
            #self._month_drop.buttons=self._month_button_list
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
                    #self.__gen_dates(forced=True)

        self._date_frequency_button.on_value_changed = _date_frequency_button_on_value_changed

        self._date_frequency_button.world_position=temp_d_f_t.world_position+Vec3(-0.5,-1,0) 

        temp_u_f_t.position=temp_t_t.position+Vec3(0,-3.5,0) 
        
        self._update_frequency_field=temp_update_frequency_field
        self._update_frequency_field.world_position=temp_u_f_t.world_position+temp_u_f_t.right*0.50 
        self._update_frequency_field.text=str(self._update_frequency)
        self._update_frequency_field.submit_on=['enter',]
        self._update_frequency_field.on_submit=Func(__set_inputfield_inactive,self._update_frequency_field)
        
        #self._wp.y = self._wp.panel.scale_y / 2 * self._wp.scale_y
        self._wp.y=0.475
        self._wp.disable()
        self._wp._always_on_top=True
        self._wp.bg.on_click=None
        self._wp.panel.world_scale=Vec3(20,25,0)
        try:
            self._wp.panel.texture=r'..\Assets\flipped_vertical_gradient'
        except:
            self._wp.panel.texture='vertical_gradient'
        self._wp.panel.color=color.hsv(200,0.6,0.1,1)

        #destroy(self._slider)
        

        

        self._info = Text(scale =1, y = 0.0, x=-0.85, wordwrap=30, color=color.tint(color.white,0.9))
        self._info.current_color=color.red
        self._info._visible=False
    
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
                #print(len(temp_buttons),' ',self._year,self._start_arr)
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
        if self._mouse_drag and self._mouse_drag_initial!=None:
            temp_x=mouse.x - self._mouse_drag_initial[0]
            temp_y=mouse.y - self._mouse_drag_initial[1]

            camera.position+=abs(camera.z) * (camera.up*abs(min(0,temp_y))+camera.down*abs(max(0,temp_y))) * time.dt * self._sensi * 100
            camera.position+=abs(camera.z) * (camera.right*abs(min(0,temp_x))+camera.left*abs(max(0,temp_x))) * time.dt * self._sensi *100
    
            
        if self._collider_ray.entity==None:
            camera.position +=camera.forward *100 * held_keys['w'] * time.dt * abs(camera.z) * 0.005
        camera.position +=camera.back * 100 * held_keys['s'] * time.dt * abs(camera.z) * 0.005

        
        camera.position +=camera.left * 10 * held_keys['a'] * time.dt
        camera.position +=camera.right * 10 * held_keys['d'] * time.dt
        camera.position +=camera.up * 10 * held_keys['z'] * time.dt
        camera.position +=camera.down  * 10 * held_keys['x'] * time.dt
        
        camera.rotate(Vec3(10 *held_keys['down arrow'] * time.dt ,
                              10 *held_keys['right arrow'] * time.dt ,
                              10 *held_keys['c'] * time.dt))

        camera.rotate(Vec3(-10 *held_keys['up arrow'] * time.dt ,
                              -10 *held_keys['left arrow'] * time.dt ,
                              -10 *held_keys['v'] * time.dt))


        if self._mouse_enabled_movement and self._toggle_free:
            
            self._mouse_drag=False
            self._mouse_drag_initial=None
             
            """ temp_pos=(camera.up*mouse.y + camera.right*mouse.x) *self._sensi * max(abs(camera.z),10) * 10
            camera.world_position+=Vec3(temp_pos[0] ,
                                 temp_pos[1] ,
                                 0)
             """
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
                self.__focus('sun')
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
                window.position=self._temp_position
                window.size=Vec2(1090,582)

        elif key == 'backspace':
            for planet in self._master_planet_dict.keys():
                if planet=='sun':
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
                #self._pause=True
                self._mouse_enabled_movement=False
                self.__update_active_action_list(text='Following mouse',append=False)

                self._drop_menu.disable()


                self._pause_menu_return_val=[self._year,self._month,self._day,
                                     self._hour,self._minute,self._second] 
                
                #print(self._pause_menu_return_val)

                self._wp.enable()
                self._year_selector.text=str(self._year)
                self._time_selector_field.text=''.join(e for e in self._pause_menu_return_val[3:6])
                self._month_drop.close()
                
                
                
                self.__update_active_action_list(text='Pause Menu Opened',append=True)

                
            else:
                #self._pause=False
                self._drop_menu.enable()
                self._wp.disable()
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
        
  


    def custom_update(self):
        
        #print(self._year,' ',self._month,' ',self._day)

        

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
                if len(self._time_selector_field.text) in range (1,7):
                    self._time_selector_field.text_color=color.green
                        
                elif len(self._time_selector_field.text)>=7:
                    self._time_selector_field.text_color=color.red
                    self._time_selector_field.text=self._time_selector_field.text[:7]
            else:
                
                temp=self._time_selector_field.text
                temp=temp.replace(":",'')
                if len(temp)<=6:
                    temp+='0'*(6-len(temp))
                    if int(temp[0:2])<24 and int(temp[2:4])<60 and int(temp[4:6])<60 :
                        self._pause_menu_return_val[3]=temp[0:2]
                        self._pause_menu_return_val[4]=temp[2:4]
                        self._pause_menu_return_val[5]=temp[4:6]
                        #self._hour=temp[0:2]
                        #self._minute=temp[2:4]
                        #self._second=temp[4:6]
                        
                    
                self._time_selector_field.text=(''.join(e+':' for e in self._pause_menu_return_val[3:6]))[:8]
                self._time_selector_field.text_color=color.green
                
            #self._date_frequency=self._date_frequency_button.value  
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
            
        
        
        self.__camera_control()
        
        if abs(camera.z)>self._max_far_zoom:
            camera.z=-self._max_far_zoom
        
        self._collider_ray = raycast(origin= camera.world_position,
                                     ignore=(camera,),
                                     direction= camera.forward,
                                     distance= 0.3, 
                                     debug= True
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
                            if planet=='sun':
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
            #print(temp_cur_utc)
            temp_cur_utc=temp_cur_utc.replace(" ",'T')
            self._year=int(temp_cur_utc[:4])
            self._month=temp_cur_utc[5:7]
            T_index=temp_cur_utc.index("T")
            self._day=temp_cur_utc[8:T_index]
            self._hour=temp_cur_utc[T_index+1:T_index+3]
            self._minute=temp_cur_utc[T_index+4:T_index+6]
            self._second=temp_cur_utc[T_index+7:T_index+9]

            
            if self._delay_counter>=self._update_frequency:
                self._cur_year_dict_index += 1
                self._delay_counter=0

            if self._cur_year_dict_index==len(self._dates):
                self._year +=1
                self._month='01'
                if self._year>self._end_year:  
                    self._year=self._start_year
                    #print([int(self._day),self._end_arr[2]-1])
                    if self._date_frequency_options_dict[self._date_frequency]=='ME' and int(self._day)==self._end_arr[2]-1:
                        self._day='31'     
                self.__gen_dates()
                self._cur_year_dict_index=0
            temp_cur_et=spiceypy.utc2et(temp_cur_utc)
            
            if self._delay_counter==0:
                for planet in self._master_planet_dict.keys():
                    
                    #self.__focus(planet,temp_cur_et)
                    if planet!='sun':
                        temp_obs_planet_id=self._master_planet_dict[planet]['obs_planet_id']
                        if temp_obs_planet_id!=10:
                            self._master_planet_dict[planet]['entity'].position= self.__gen_pos(self._master_planet_dict[planet]['planet_id'],temp_cur_et,temp_obs_planet_id) + self.__gen_pos(temp_obs_planet_id,temp_cur_et,10)
                        else:
                            self._master_planet_dict[planet]['entity'].position=self.__gen_pos(self._master_planet_dict[planet]['planet_id'],temp_cur_et,temp_obs_planet_id)           
                    self._master_planet_dict[planet]['sibling_entity'].position=self._master_planet_dict[planet]['entity'].position
                    self._master_planet_dict[planet]['text_tag_entity'].world_position=self._master_planet_dict[planet]['sibling_entity'].position
                    self._master_planet_dict[planet]['text_tag_entity'].world_scale=abs(camera.z) * 0.50
                    self._master_planet_dict[planet]['entity'].rotate(Vec3(0,
                                                                        self._master_planet_dict[planet]['axial_rotation']*self._axial_rotation_multiplier[self._date_frequency],
                                                                        0
                                                                        )
                                                                    )       
                    if planet!='sun':
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
                                                                                        color=self._master_planet_dict[planet]['trail_color'] 
                                                                                        )  
                            except:
                                pass

app=Ursina(title='Project Shunya', icon=r'../Assets/Solar-system.ico')
window.color=color.black
window._icon='../Assets/Solar-system.ico'
window._title='Project Shunya'
solarsystem=SolarSystem()
solarsystem.load_widgets()
def input(key):
    solarsystem.custom_input(key)
def update():
    solarsystem.custom_update()
app.run()


                        



                        
