import spiceypy
from ursina import *
import datetime
import numpy
from collections import deque
import xarray as xr
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import time as Time
import pandas as pd

class SolarSystem():
    def __init__(self):
        self.__set_date_year()
        self.__set_kernels()
        self.__set_constants()
        self.__create_planet_dict()
        self.__gen_dates(self._start_date.format(self._year),self._end_date.format(self._year))


    def __set_date_year(self):    
        self._start_date = '{}-01-04'
        self._end_date = '{}-12-31' 
        self._start_year=1900
        self._end_year=2099

    def __set_kernels(self):  
        spiceypy.furnsh("../Kernels/lsk/naif0012.tls")
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
    
    def __set_constants(self):
        self._toggle_trail=False
        self._multiplier=1000
        self._cur_year_dict_index=0
        self._year_text='<red>YEAR</red>\n<green>{}</green><red>\nZoom</red>\n<green>{}</green>'
        self._cur_year_txt = Text(scale=1,position=(-0.85,0.45,0))
        self._sensi=0.005
        self._current_focus='sun'
        self._toggle_free=False
        
        self._dates=[]
        self._year=self._start_year

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

        self._pause_handler = Entity(ignore_paused=True)

        self._mouse_drag=False
        self._mouse_drag_initial=None

        self._delay_counter=0

        self._drop_menu=Entity(visible=False)
        self._slider=Entity(visible=False)

        self._thick=0.05
        self._curve_mode='line'
        
        self._info = Entity(visible=False)    
        self._info_text="<white>Name: </white>{}\n<white>Planet ID: </white>{}\n<white>Radius: </white>{} km\n<white>Axial Rotation: </white>{} degree/sec\n<white>Tilt: </white>{} degrees"
        

    
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


    def __gen_dates(self,start_date,end_date):
        self._dates.clear()
        self._dates=list(xr.cftime_range(start_date, end_date, freq='D'))
        

    
    def __create_planet_dict(self):
        self.planets_info={
                   "sun": {'id': 10 ,'radius_km':696340 , 'texture':r"..\Assets\8k_sun.png" , 'rotation_x': -90, 'rotation_y': -0.00015, 'rotation_z': 7.25, 'obs_planet_id': 10, 'color': None},
                   "mercury": {'id': 1 ,'radius_km':2439, 'texture':r"..\Assets\mercury.png" , 'rotation_x': -90, 'rotation_y': -0.00007, 'rotation_z': 0.03, 'obs_planet_id': 10, 'color': color.violet},
                   "venus": {'id': 2 ,'radius_km':6052 , 'texture':r"..\Assets\venus_atmosphere.png" , 'rotation_x': -90, 'rotation_y': -0.00104, 'rotation_z': 2.64, 'obs_planet_id': 10, 'color': color.cyan},
                   "earth": {'id': 399 ,'radius_km':6387 , 'texture':r"..\Assets\earth_daymap.png" , 'rotation_x': -90, 'rotation_y': -0.00417, 'rotation_z': 23.44, 'obs_planet_id': 10, 'color': color.blue},
                   "moon": {'id': 301 ,'radius_km':1738 , 'texture':r"..\Assets\moon.png" , 'rotation_x': -90, 'rotation_y': -0.00015, 'rotation_z': 6.68, 'obs_planet_id': 10, 'color': color.blue},
                   "mars": {'id': 4 ,'radius_km':3393 , 'texture':r"..\Assets\mars.png" , 'rotation_x': -90, 'rotation_y': -0.00401, 'rotation_z': 25.19, 'obs_planet_id': 10, 'color': color.green},
                   "phobos": {'id': 401 ,'radius_km':11.2 , 'texture':r"..\Assets\phobos.png" , 'rotation_x': -90, 'rotation_y': -0.01307, 'rotation_z': 0.0, 'obs_planet_id': 4, 'color': color.green},
                   "deimos": {'id': 402 ,'radius_km':6.3 , 'texture':r"..\Assets\deimos.png" , 'rotation_x': -90, 'rotation_y': -0.00330, 'rotation_z': 2, 'obs_planet_id': 4, 'color': color.green},
                   "jupiter": {'id': 5 ,'radius_km':69911 , 'texture':r"..\Assets\jupiter.png" , 'rotation_x': -90, 'rotation_y': -0.01001, 'rotation_z': 3.13, 'obs_planet_id': 10, 'color': color.yellow},
                   "io": {'id': 501 ,'radius_km':1821 , 'texture':r"..\Assets\io.png" , 'rotation_x': -90, 'rotation_y': -0.00236, 'rotation_z': 0, 'obs_planet_id': 5, 'color': color.yellow},
                   "europa": {'id': 502 ,'radius_km':1560.8 , 'texture':r"..\Assets\europa.png" , 'rotation_x': -90, 'rotation_y': -0.00118, 'rotation_z': 0.1, 'obs_planet_id': 5, 'color': color.yellow},
                   "ganymede": {'id': 503 ,'radius_km':2634.1 , 'texture':r"..\Assets\ganymede.jpg" , 'rotation_x': -90, 'rotation_y': -0.00058, 'rotation_z': 0.33, 'obs_planet_id': 5, 'color': color.yellow},
                   "callisto": {'id': 504 ,'radius_km':2410.3 , 'texture':r"..\Assets\callisto.png" , 'rotation_x': -90, 'rotation_y': -0.00025, 'rotation_z': 0.0, 'obs_planet_id': 5, 'color': color.yellow},
                   "saturn": {'id': 6 ,'radius_km':60268 , 'texture':r"..\Assets\saturn.png" , 'rotation_x': -90, 'rotation_y': -0.00946, 'rotation_z': 26.73, 'obs_planet_id': 10, 'color': color.orange},
                   "rhea": {'id': 605 ,'radius_km':763.8 , 'texture':r"..\Assets\rhea.png" , 'rotation_x': -90, 'rotation_y': -0.00092, 'rotation_z': 0.0, 'obs_planet_id': 6, 'color': color.orange},
                   "titan": {'id': 606 ,'radius_km':2574.8 , 'texture':r"..\Assets\titan.png" , 'rotation_x': -90, 'rotation_y': -0.00026, 'rotation_z': 27, 'obs_planet_id': 6, 'color': color.orange},
                   "uranus": {'id': 7 ,'radius_km':25559 , 'texture':r"..\Assets\uranus.png" , 'rotation_x': -90, 'rotation_y': -0.00580, 'rotation_z': 82.23, 'obs_planet_id': 10, 'color': color.red},
                   "titania": {'id': 703 ,'radius_km':789 , 'texture':r"..\Assets\titania.png" , 'rotation_x': -90, 'rotation_y': -0.00048, 'rotation_z': 0.0, 'obs_planet_id': 7, 'color': color.red},
                   "neptune": {'id': 8 ,'radius_km':24764 , 'texture':r"..\Assets\neptune.png" , 'rotation_x': -90, 'rotation_y': -0.00621, 'rotation_z': 28.32, 'obs_planet_id': 10, 'color': color.pink},
                   "triton": {'id': 801 ,'radius_km':1355 , 'texture':r"..\Assets\triton.png" , 'rotation_x': -90, 'rotation_y': -0.00071, 'rotation_z': 30, 'obs_planet_id': 8, 'color': color.pink},
                   "pluto": {'id': 9 ,'radius_km':1140 , 'texture':r"..\Assets\pluto.png" , 'rotation_x': -90, 'rotation_y': -0.00065, 'rotation_z': 120, 'obs_planet_id': 10, 'color': color.white},
                   "charon": {'id': 901 ,'radius_km':606 , 'texture':r"..\Assets\charon.png" , 'rotation_x': -90, 'rotation_y': -0.00065, 'rotation_z': 119.6, 'obs_planet_id': 9, 'color': color.white},
                   "ceres": {'id': 2000001 ,'radius_km':476 , 'texture':r"..\Assets\ceres_fictional.png" , 'rotation_x': -90, 'rotation_y': -0.000002, 'rotation_z': 4, 'obs_planet_id': 10, 'color': color.white}
                   }
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
            self._master_planet_dict[planet]['entity']=Entity(name=planet, model='sphere',collider='box',
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
                self._master_planet_dict[planet]['trail_deque']=deque([],maxlen=100)
                self._master_planet_dict[planet]['curve_renderer']=Entity()
                self._master_planet_dict[planet]['trail_color']=self.planets_info[planet]['color']
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
        else:
            self._toggle_free=False
            self._master_planet_dict[planet_name]['follow']=True
            self._current_focus=planet_name    

    def __scale_sensitivity(self):
        self._sensi = self._slider.value/1000

    def __pause_handler_input(self,key):
        if key == 'escape':

            application.paused = not application.paused # Pause/unpause the game.
            self._wp.enabled = not self._wp.enabled

    def __focus(self,planet_name: str, cur_et):
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
            camera.position=Vec3(0,0,self._default_zoom)
            camera.rotation=Vec3(0,0,0)
            camera.parent=self._master_planet_dict[planet_name]['sibling_entity']
            camera.position=Vec3(0,0,0)
            camera.z=self._default_zoom
            self._master_planet_dict[planet_name]['follow']=False
            camera._always_on_top=True
            self._info._visible=True
            self._info.text=self._info_text.format( planet_name, 
                                                    self._master_planet_dict[planet_name]['planet_id'],
                                                    self.planets_info[planet_name]['radius_km'],
                                                    self._master_planet_dict[planet_name]['axial_rotation'],
                                                    self.planets_info[planet_name]['rotation_z']
                                                    )
                    

    def load_widgets(self):
        
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
        self._wp = WindowPanel(
                        title='Pause Menu',
                        content=(
                                Text('adjust sensitivity'),
                                temp_slider := Slider(0, 20, default=5,
                                                       height=Text.size, 
                                                       y=-0.4, x=-0.8, 
                                                       step=1, dynamic= True, 
                                                       on_value_changed=self.__scale_sensitivity, 
                                                       vertical=False,
                                                       bar_color = color.yellow)
                                ),
                        popup=True
                        )
        self._slider=temp_slider
        self._wp.enabled = False
        self._slider.knob.ignore_paused= True
        self._slider.ignore_paused=True
        #destroy(self._slider)
        

        #Pause menu: Assign the input function to the pause handler.
        self._pause_handler.input = self.__pause_handler_input 

        self._info = Text(scale =1, y = -0.3, x=-0.8)
        self._info._visible=False
        
    def __camera_control(self):      
        if self._mouse_drag and self._mouse_drag_initial!=None:
            camera.x-=abs(camera.z) * (mouse.x - self._mouse_drag_initial[0]) * time.dt
            camera.y-=abs(camera.z) * (mouse.y - self._mouse_drag_initial[1]) * time.dt
            
        if self._collider_ray.entity==None:
            camera.position +=camera.forward *100 * held_keys['w'] * time.dt * abs(camera.z) * 0.005
        camera.position +=camera.back * 100 * held_keys['s'] * time.dt * abs(camera.z) * 0.005

        
        camera.position +=camera.left * 100 * held_keys['a'] * time.dt
        camera.position +=camera.right * 100 * held_keys['d'] * time.dt
        camera.position +=camera.up * 100 * held_keys['z'] * time.dt
        camera.position +=camera.down * 100 * held_keys['x'] * time.dt
        '''
        camera.rotation_x-=10 *held_keys['up arrow'] * time.dt
        camera.rotation_x+=10 *held_keys['down arrow'] * time.dt
        camera.rotation_y-=10 *held_keys['left arrow'] * time.dt
        camera.rotation_y+=10 *held_keys['right arrow'] * time.dt
        camera.rotation_z+=10 *held_keys['c'] * time.dt
        camera.rotation_z-=10 *held_keys['v'] * time.dt
        '''
        camera.rotate(Vec3(10 *held_keys['down arrow'] * time.dt ,
                              10 *held_keys['right arrow'] * time.dt ,
                              10 *held_keys['c'] * time.dt))

        camera.rotate(Vec3(-10 *held_keys['up arrow'] * time.dt ,
                              -10 *held_keys['left arrow'] * time.dt ,
                              -10 *held_keys['v'] * time.dt))


        if self._mouse_enabled_movement and self._toggle_free:
            
            self._mouse_drag=False
            self._mouse_drag_initial=None
            camera.x+=abs(camera.z) * mouse.x * time.dt
            camera.y+=abs(camera.z) * mouse.y * time.dt


    def custom_input(self,key):
        if key=='scroll up':
            if self._collider_ray.entity==None:
                camera.world_position +=camera.forward*abs(camera.z)*self._sensi
        
        elif key=='scroll down':
            camera.world_position +=camera.back*abs(camera.z)*self._sensi
        
        elif key=='left mouse down' and not self._mouse_enabled_movement:
            self._mouse_drag=True
            if self._mouse_drag_initial==None:
                self._mouse_drag_initial=mouse.position
        
        elif key=='left mouse up' and not self._mouse_enabled_movement:
            self._mouse_drag=False
            self._mouse_drag_initial=None
        
        elif key == 'm':
            self._mouse_enabled_movement = not self._mouse_enabled_movement
        
        elif key=='t':
            if self._toggle_trail:
                try:
                    for planet in self._master_planet_dict.keys():
                        destroy(self._master_planet_dict[planet]['curve_renderer'])
                except:
                    pass    
            self._toggle_trail = not self._toggle_trail  

    def custom_update(self):
        self.__camera_control()
        if abs(camera.z)>self._max_far_zoom:
            camera.z=-self._max_far_zoom
        self._sensi = self._slider.value/1000
        
        self._collider_ray = raycast(origin= camera.world_position,
                                     ignore=(camera,),
                                     direction= camera.forward,
                                     distance= 0.3, 
                                     debug= True
                                    )
        
        self._drop_menu.text=self._drop_down_text.format(self._current_focus)
        
        self._cur_year_txt.text = self._year_text.format(self._year,camera.z) 

        self._delay_counter+=time.dt
        
        temp_cur_utc=str(self._dates[self._cur_year_dict_index])
        temp_cur_utc=temp_cur_utc.replace(" ",'T')
        if self._delay_counter>=1:
            self._cur_year_dict_index += 1
            self._delay_counter=0

        if self._cur_year_dict_index==len(self._dates):
            self._year += 1
            if self._year>=self._end_year:  
                self._year=self._start_year 
            self.__gen_dates(self._start_date.format(self._year),self._end_date.format(self._year))
            self._cur_year_dict_index=0
        temp_cur_et=spiceypy.utc2et(temp_cur_utc)
        

        for planet in self._master_planet_dict.keys():
            #self._master_planet_dict[planet]['entity']
            self.__focus(planet,temp_cur_et)
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
                                                                   self._master_planet_dict[planet]['axial_rotation'],
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

app=Ursina()
window.color=color.black
solarsystem=SolarSystem()
solarsystem.load_widgets()
def input(key):
    solarsystem.custom_input(key)
def update():
    solarsystem.custom_update()
app.run()


                        
