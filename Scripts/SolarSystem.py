import spiceypy
from ursina import *
import datetime
import numpy
from collections import deque
import xarray as xr
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import time as Time

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
import pandas as pd
dates=[]
start_date = '{}-01-04'         #change
end_date = '{}-12-31'
year=1900                  #change
toggle_trail=False

multiplier=1000
def km2au(dist_in_km: float):
    global multiplier
    return (spiceypy.convrt(dist_in_km,'km','au'))*multiplier

def gen_pos(target: int, cur_et,obs:int):   #change
    global multiplier
    planet_state_wrt_sun,earth_sun_light_time=spiceypy.spkgeo(targ=target,et=cur_et
                                                        ,ref="ECLIPJ2000",obs=obs)  #change
    x,y,z=planet_state_wrt_sun[:3]
    #earth_vel_x,earth_vel_y,earth_vel_z=earth_state_wrt_sun[3:]
    x=spiceypy.convrt(x,'km','au')*multiplier
    y=spiceypy.convrt(y,'km','au')*multiplier
    z=spiceypy.convrt(z,'km','au')*multiplier
    return Vec3(x,y,z)


def gen_dates(start_date,end_date):
    global dates
    dates.clear()
    dates=list(xr.cftime_range(start_date, end_date, freq='D'))
    #dates = list(pd.date_range(start_date, end_date, freq='M'))

gen_dates(start_date.format(year),end_date.format(year))
    
i=0

app=Ursina()

window.color=color.black
year_text='<red>YEAR</red>\n<green>{}</green><red>\nZoom</red>\n<green>{}</green>'
cur_year_txt = Text(scale=1,position=(-0.85,0.45,0))


sun=Entity(name='Sun', model='sphere',scale=km2au(696000),texture=r"..\Assets\8k_sun.png",collider='box')
sun.position=Vec3(0,0,0)

mercury=Entity(name='Mercury', model='sphere',texture=r"..\Assets\mercury.png", scale = km2au(2439),collider='box')
venus=Entity(name='Venus', model='sphere', scale = km2au(6052), texture=r"..\Assets\venus_atmosphere.png", collider='box')
earth=Entity(name='Earth',model='sphere', scale = km2au(6387),texture=r"..\Assets\earth_daymap.png", collider='box')
moon=Entity(name='Moon', model='sphere', scale = km2au(1738), texture=r"..\Assets\moon.png" ,collider='box')
mars=Entity(name=' Mars', model='sphere', scale = km2au(3393),collider='box', texture="..\Assets\mars.png")
phobos=Entity(name=' Phobos', model='sphere', scale = km2au(11.2),collider='box', texture="..\Assets\phobos.png")
deimos=Entity(name=' Deimos', model='sphere', scale = km2au(6.3),collider='box', texture="..\Assets\deimos.png")
jupiter=Entity(name='Jupiter',model='sphere', scale = km2au(71398), texture="..\Assets\jupiter.png", collider='box')
ganymede=Entity( name='Ganymede',model='sphere', scale = km2au(2634.1), texture="..\Assets\ganymede.jpg", collider='box')   #change
callisto=Entity( name='Callisto',model='sphere', scale = km2au(2410.3), texture="..\Assets\callisto.png", collider='box')   #change
io=Entity( name='Io',model='sphere', scale = km2au(1821.6), texture="..\Assets\io.png", collider='box')                     #change
europa=Entity( name='Europa',model='sphere', scale = km2au(1560.8), texture="..\Assets\europa.png", collider='box')         #change
saturn=Entity(name='Saturn', model='sphere', scale = km2au(60000), texture="..\Assets\saturn.png", collider='box')
titan=Entity( name='Titan',model='sphere', scale = km2au(2574.8), texture="..\Assets\\titan.png", collider='box')           #change
rhea=Entity( name='Rhea',model='sphere', scale = km2au(763.8), texture="..\Assets\\rhea.png", collider='box')               #change
uranus=Entity(name='Uranus', model='sphere', scale = km2au(25559), texture=r"..\Assets\uranus.png", collider='box')
titania=Entity( name='Titania',model='sphere', scale = km2au(789), texture="..\Assets\\titania.png", collider='box')        #change
neptune=Entity(name='Neptune', model='sphere', scale = km2au(24800), texture=r"..\Assets\neptune.png", collider='box')
triton=Entity(name='Triton', model='sphere', scale = km2au(1355), texture=r"..\Assets\triton.png", collider='box')          #change
pluto=Entity(name='Pluto', model='sphere', scale = km2au(1140), texture="..\Assets\pluto.png", collider='box')
ceres=Entity(name='Ceres', model='sphere', scale = km2au(476), texture="..\Assets\ceres_fictional.png", collider='box')     #change


sun_text=Text(parent=sun,text='Sun', scale=camera.z*0.4)
mercury_text=Text(parent=mercury , text='Mercury', scale=camera.z*0.4)
venus_text=Text(parent=venus , text='Venus', scale=camera.z*0.4)
earth_text=Text(parent=earth , text='Earth', scale=camera.z*0.4)
moon_text=Text(parent=moon , text='Moon', scale=camera.z*0.4)
mars_text=Text(parent=mars , text='Mars', scale=camera.z*0.4)
phobos_text=Text(parent=phobos , text='Phobos', scale=camera.z*0.4)
deimos_text=Text(parent=deimos , text='Deimos', scale=camera.z*0.4)
jupiter_text=Text(parent=jupiter , text='Jupiter', scale=camera.z*0.4)
ganymede_text=Text(parent=ganymede , text='Ganymede', scale=camera.z*0.4)   #change
callisto_text=Text(parent=callisto , text='Callisto', scale=camera.z*0.4)   #change
io_text=Text(parent=io , text='Io', scale=camera.z*0.4)                     #change
europa_text=Text(parent=europa , text='Europa', scale=camera.z*0.4)         #change
saturn_text=Text(parent=saturn , text='Saturn', scale=camera.z*0.4)
titan_text=Text(parent=titan , text='Titan', scale=camera.z*0.4)            #change
rhea_text=Text(parent=rhea , text='Rhea', scale=camera.z*0.4)               #change
uranus_text=Text(parent=uranus , text='Uranus', scale=camera.z*0.4)
titania_text=Text(parent=titania , text='Titania', scale=camera.z*0.4)      #change
neptune_text=Text(parent=neptune , text='Neptune', scale=camera.z*0.4)
triton_text=Text(parent=triton , text='Triton', scale=camera.z*0.4)         #change
pluto_text=Text(parent=pluto , text='Pluto', scale=camera.z*0.4)
ceres_text=Text(parent=ceres , text='Ceres', scale=camera.z*0.4)            #change


trail_mercury=deque([],maxlen=100)
trail_venus=deque([],maxlen=100)
trail_earth=deque([],maxlen=100)
trail_moon=deque([],maxlen=100)
trail_mars=deque([],maxlen=100)
trail_phobos=deque([],maxlen=100)
trail_deimos=deque([],maxlen=100)
trail_jupiter=deque([],maxlen=100)
trail_ganymede=deque([],maxlen=100) #change
trail_callisto=deque([],maxlen=100) #change
trail_io=deque([],maxlen=100)       #change
trail_europa=deque([],maxlen=100)   #change
trail_saturn=deque([],maxlen=100)
trail_titan=deque([],maxlen=100)    #change
trail_rhea=deque([],maxlen=100)     #change
trail_uranus=deque([],maxlen=100)
trail_titania=deque([],maxlen=100)  #change
trail_neptune=deque([],maxlen=100)
trail_triton=deque([],maxlen=100)   #change
trail_pluto=deque([],maxlen=100)
trail_ceres=deque([],maxlen=100)    #change


curve_renderer_mercury=Entity()
curve_renderer_venus=Entity()
curve_renderer_earth=Entity()
curve_renderer_moon=Entity()
curve_renderer_mars=Entity()
curve_renderer_phobos=Entity()
curve_renderer_deimos=Entity()
curve_renderer_jupiter=Entity()
curve_renderer_ganymede=Entity()    #change
curve_renderer_callisto=Entity()    #change
curve_renderer_io=Entity()          #change
curve_renderer_europa=Entity()      #change
curve_renderer_saturn=Entity()
curve_renderer_titan=Entity()       #change
curve_renderer_rhea=Entity()        #change
curve_renderer_uranus=Entity()
curve_renderer_titania=Entity()     #change
curve_renderer_neptune=Entity()
curve_renderer_triton=Entity()      #change
curve_renderer_pluto=Entity()
curve_renderer_ceres=Entity()       #change


zoom_on=True
def goto():
    global follow_earth,zoom_field,camera
    x=zoom_field.text
    print(x)
    if x=='earth':  
        follow_earth=True

planets_info={"sun":{'entity':sun,'planet_id': 10, 'text_tag_entity':sun_text ,'follow': False },
              "mercury":{'entity':mercury,'planet_id': 1, 'text_tag_entity':mercury_text ,'follow': False },
              "venus":{'entity':venus,'planet_id': 2, 'text_tag_entity':venus_text ,'follow': False },
              "earth":{'entity':earth,'planet_id': 399, 'text_tag_entity':earth_text ,'follow': False },
              "moon":{'entity':moon,'planet_id': 301, 'text_tag_entity':moon_text ,'follow': False },
              "phobos":{'entity':phobos,'planet_id': 401, 'text_tag_entity':phobos_text ,'follow': False },
              "deimos":{'entity':deimos,'planet_id': 402, 'text_tag_entity':deimos_text ,'follow': False },
              "mars":{'entity':mars,'planet_id': 4, 'text_tag_entity':mars_text ,'follow': False },
              "jupiter":{'entity':jupiter,'planet_id': 5, 'text_tag_entity':jupiter_text ,'follow': False },
              "ganymede":{'entity':ganymede,'planet_id': 503, 'text_tag_entity':ganymede_text ,'follow': False },   #change
              "callisto":{'entity':callisto,'planet_id': 504, 'text_tag_entity':callisto_text ,'follow': False },   #change
              "io":{'entity':io,'planet_id': 501, 'text_tag_entity':io_text ,'follow': False },                     #change
              "europa":{'entity':europa,'planet_id': 502, 'text_tag_entity':europa_text ,'follow': False },         #change
              "saturn":{'entity':saturn,'planet_id': 6, 'text_tag_entity':saturn_text ,'follow': False },
              "titan":{'entity':titan,'planet_id': 606, 'text_tag_entity':titan_text ,'follow': False },            #change
              "rhea":{'entity':rhea,'planet_id': 605, 'text_tag_entity':rhea_text ,'follow': False },               #change
              "uranus":{'entity':uranus,'planet_id': 7, 'text_tag_entity':uranus_text ,'follow': False },
              "titania":{'entity':titania,'planet_id': 703, 'text_tag_entity':titania_text ,'follow': False },      #change
              "neptune":{'entity':neptune,'planet_id': 8, 'text_tag_entity':neptune_text ,'follow': False },
              "triton":{'entity':triton,'planet_id': 801, 'text_tag_entity':triton_text ,'follow': False },         #change
              "pluto":{'entity':pluto,'planet_id': 9, 'text_tag_entity':pluto_text ,'follow': False },
              "ceres":{'entity':ceres,'planet_id': 2000001, 'text_tag_entity':ceres_text ,'follow': False }         #change
              }
def set_all_follow_false():
    global planets_info
    for i in planets_info.keys():
        planets_info[i]['follow']=False
        #planets_info[i]['text_tag_entity'].visible=False

current_focus='sun'
toggle_free=False

camera.parent=scene
default_zoom=-20
camera.z=default_zoom
camera.collider=BoxCollider(camera,center=Vec3(0,0,5),size=(5,5,20))
camera.collider.visible=False
max_far_zoom=300000
camera.clip_plane_far_setter(max_far_zoom*2)            

drop_down_text='Focus on: {}'

def set_follow(planet_name: str):
    global planets_info,current_focus,toggle_free
    set_all_follow_false()
    if planet_name=='free':
        toggle_free=True
        camera.parent=scene
        camera.position=Vec3(0,0,-20)
        current_focus=None
        for i in planets_info.keys():
            planets_info[i]['text_tag_entity'].visible=True
    else:
        toggle_free=False
        planets_info[planet_name]['follow']=True
        current_focus=planet_name    



button_list=[DropdownMenuButton('Free rotation',on_click=Func(set_follow,'free')),
             DropdownMenuButton('Sun',on_click=Func(set_follow,'sun')),
             DropdownMenuButton('Mercury',on_click=Func(set_follow,'mercury')),
             DropdownMenuButton('Venus',on_click=Func(set_follow,'venus')),
             DropdownMenu(text='Earth and Moon',buttons=[DropdownMenuButton('Earth',on_click=Func(set_follow,'earth')),
                                                DropdownMenuButton('Moon',on_click=Func(set_follow,'moon'))],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenu(text='Mars and moons',buttons=[DropdownMenuButton('Mars',on_click=Func(set_follow,'mars')),
                                                DropdownMenuButton('Phobos',on_click=Func(set_follow,'phobos')),
                                                DropdownMenuButton('Deimos',on_click=Func(set_follow,'deimos'))],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenu(text='Jupiter and moons',buttons=[DropdownMenuButton('Jupiter',on_click=Func(set_follow,'jupiter')),
                                                DropdownMenuButton('Ganymede',on_click=Func(set_follow,'ganymede')),
                                                DropdownMenuButton('Callisto',on_click=Func(set_follow,'callisto')),
                                                DropdownMenuButton('Io',on_click=Func(set_follow,'io')),
                                                DropdownMenuButton('Europa',on_click=Func(set_follow,'europa'))],       #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenu(text='Saturn and moons',buttons=[DropdownMenuButton('Saturn',on_click=Func(set_follow,'saturn')),
                                                DropdownMenuButton('Titan',on_click=Func(set_follow,'titan')),
                                                DropdownMenuButton('Rhea',on_click=Func(set_follow,'rhea'))],           #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenu(text='Uranus and Titania',buttons=[DropdownMenuButton('Uranus',on_click=Func(set_follow,'uranus')),
                                                DropdownMenuButton('Titania',on_click=Func(set_follow,'titania')),],    #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenu(text='Neptune and Triton',buttons=[DropdownMenuButton('Neptune',on_click=Func(set_follow,'neptune')),
                                                DropdownMenuButton('Triton',on_click=Func(set_follow,'triton')),],      #change
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenuButton('Pluto',on_click=Func(set_follow,'pluto')),
             DropdownMenuButton('Ceres',on_click=Func(set_follow,'ceres'))                          #change
             ]



drop_menu=DropdownMenu(x=-.60,y=0.45,text=drop_down_text.format(current_focus), 
                       buttons=button_list,color=color.white,text_color=color.red,highlight_color=color.green,
                       scale=(0.3,0.03,0.0))

mouse_enabled_movement=False
last_time_mouse_button_clicked=0
def mouse_enabled_movement_function():
    global mouse_enabled_movement,toggle_free,last_time_mouse_button_clicked
    if (Time.time()-last_time_mouse_button_clicked)<2:
        return 0
    if not mouse_enabled_movement:
        if toggle_free:
            mouse_enabled_movement=True
            last_time_mouse_button_clicked=Time.time()
    else:
        mouse_enabled_movement=False
        last_time_mouse_button_clicked=Time.time()
   

mouse_text="Mouse control: {}"
mouse_button=Button(parent=window,name='mouse_button',scale=1,text=mouse_text.format(mouse_enabled_movement),text_color=color.black,
                    color=color.red,highlight_color=color.white, disabled=False,collider='box')
mouse_button.world_position=(0,8.5,0)
mouse_button.fit_to_text()
mouse_button._eternal=True
mouse_button.on_click=mouse_enabled_movement_function
mouse_button.on_mouse_enter= mouse_button.enable
mouse.unhover_everything_not_hit()
mouse.double_click=False


#camera.position=Vec3(0,10,-100)
#camera.look_at(sun)
def magnitude(vector):
    return numpy.linalg.norm(vector)

def focus(planet_name: str, cur_et):
    global planets_info,default_zoom,mouse_enabled_movement
    
    if planets_info[planet_name]['follow']:
        if planet_name=='sun':
            mouse_enabled_movement=False
            camera.parent=sun
            #camera.collider=BoxCollider(camera,center=Vec3(0,0,0),size=(10,10,10))
            
            camera.look_at(sun)
            camera.position=(0,10,default_zoom)
            camera.look_at(sun)
            planets_info['sun']['follow']=False
        
        else:
            mouse_enabled_movement=False
            camera.position=Vec3(0,0,default_zoom)
            camera.rotation=Vec3(0,0,0)
            camera.parent=planets_info[planet_name]['entity']
            
            #camera.set_position=planets_info[planet_name]['entity'].position.up*2
            #camera.collider=BoxCollider(camera,center=Vec3(0,0,10),size=(3,3,3))
            #camera.collider.visible=True
            #camera.z=default_zoom
            camera.position=Vec3(0,0,0)
            camera.z=default_zoom
            planets_info[planet_name]['follow']=False
            camera._always_on_top=True
            
        #focus_camera.rotate=Vec3(0,0,0)
        

            
mouse_drag=False
mouse_drag_initial=None

def input(key):
    global sun,toggle_trail,mouse_enabled_movement,mouse_drag,mouse_drag_initial
    if key=='scroll up':
        if not camera.intersects().hit:
            camera.world_position +=camera.forward*abs(camera.z)*0.05
    elif key=='scroll down':
        camera.world_position +=camera.back*abs(camera.z)*0.05
    
    elif key=='left mouse down' and not mouse_enabled_movement:
        mouse_drag=True
        if mouse_drag_initial==None:
            mouse_drag_initial=mouse.position
    
    elif key=='left mouse up' and not mouse_enabled_movement:
        mouse_drag=False
        mouse_drag_initial=None
    #button gived to simulate this
    #elif key=='m':
    #    mouse_enabled_movement=not(mouse_enabled_movement)  
    #
    elif key=='t':
        if toggle_trail==True:
            global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth,curve_renderer_moon,curve_renderer_deimos,curve_renderer_ceres
            global curve_renderer_mars,curve_renderer_jupiter,curve_renderer_ganymede,curve_renderer_callisto,curve_renderer_saturn #change
            global curve_renderer_uranus,curve_renderer_neptune,curve_renderer_pluto,curve_renderer_io,curve_renderer_europa        #change
            global curve_renderer_titan,curve_renderer_rhea,curve_renderer_titania,curve_renderer_triton,curve_renderer_phobos      #change
            try:
                destroy(curve_renderer_mercury)
                destroy(curve_renderer_venus)
                destroy(curve_renderer_earth)
                destroy(curve_renderer_moon)
                destroy(curve_renderer_mars)
                destroy(curve_renderer_phobos)
                destroy(curve_renderer_deimos)
                destroy(curve_renderer_jupiter)
                destroy(curve_renderer_ganymede)    #change
                destroy(curve_renderer_callisto)    #change
                destroy(curve_renderer_io)          #change
                destroy(curve_renderer_europa)      #change
                destroy(curve_renderer_saturn)
                destroy(curve_renderer_titan)       #change
                destroy(curve_renderer_rhea)        #change
                destroy(curve_renderer_uranus)
                destroy(curve_renderer_titania)     #change
                destroy(curve_renderer_neptune)
                destroy(curve_renderer_triton)      #change
                destroy(curve_renderer_pluto)
                destroy(curve_renderer_ceres)       #change
            except:
                pass    
        toggle_trail=not(toggle_trail)            
                

def camera_control():
    
    global toggle_free,current_focus,planets_info,mouse_enabled_movement,mouse_drag,mouse_drag_initial
    
    

    if mouse_drag and mouse_drag_initial!=None:
        camera.x-=abs(camera.z) * (mouse.x - mouse_drag_initial[0]) * time.dt
        camera.y-=abs(camera.z) * (mouse.y - mouse_drag_initial[1]) * time.dt
        

    if not camera.intersects().hit: 
        camera.position +=camera.forward *100 * held_keys['w'] * time.dt
    camera.position +=camera.back * 100 * held_keys['s'] * time.dt
    

    if toggle_free:

        camera.position +=camera.left * 100 * held_keys['a'] * time.dt
        camera.position +=camera.right * 100 * held_keys['d'] * time.dt
        camera.position +=camera.up * 100 * held_keys['z'] * time.dt
        camera.position +=camera.down * 100 * held_keys['x'] * time.dt
        
        camera.rotation_x-=10 *held_keys['up arrow'] * time.dt
        camera.rotation_x+=10 *held_keys['down arrow'] * time.dt
        camera.rotation_y-=10 *held_keys['left arrow'] * time.dt
        camera.rotation_y+=10 *held_keys['right arrow'] * time.dt
        camera.rotation_z+=10 *held_keys['c'] * time.dt
        camera.rotation_z-=10 *held_keys['v'] * time.dt


        if mouse_enabled_movement:
            
            mouse_drag=False
            mouse_drag_initial=None
            camera.x+=abs(camera.z) * mouse.x * time.dt
            camera.y+=abs(camera.z) * mouse.y * time.dt
        

        
delay_counter=0
                
def update():
    
    global max_far_zoom
    camera_control()
    if abs(camera.z)>max_far_zoom:
        camera.z=-max_far_zoom

    global follow_earth,zoom_on,delay_counter
    global last_time,cur_year_txt,year_text,curve_renderer,start_date,end_date,i,year,dates,trail_titan,trail_triton,trail_titania,trail_rhea   #change
    global trail_mercury,trail_venus,trail_earth,trail_moon,trail_mars,trail_jupiter,trail_saturn,trail_uranus,trail_neptune,trail_europa       #change
    global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth,curve_renderer_moon,trail_ganymede,trail_callisto,trail_io          #change
    global curve_renderer_mars,curve_renderer_jupiter,curve_renderer_ganymede,curve_renderer_callisto,curve_renderer_saturn                     #change
    global curve_renderer_uranus,curve_renderer_neptune,curve_renderer_pluto,curve_renderer_io,curve_renderer_europa,curve_renderer_ceres       #change
    global curve_renderer_titan,curve_renderer_rhea,curve_renderer_titania,curve_renderer_triton,curve_renderer_phobos,curve_renderer_deimos    #change

    global sun_text,mercury_text,venus_text,earth_text,moon_text,rhea_text,deimos_text      #change
    global mars_text,jupiter_text,ganymede_text,saturn_text,callisto_text,triton_text,ceres_text       #change
    global uranus_text,neptune_text,pluto_text,io_text,europa_text,titan_text,phobos_text   #change

    global planets_info,drop_menu,mouse_button,mouse_enabled_movement


    drop_menu.text=drop_down_text.format(current_focus)

    mouse_button.text=mouse_text.format(mouse_enabled_movement)
    
    if mouse_enabled_movement:
        mouse_button.color=color.green
    else:
        mouse_button.color=color.red

    cur_year_txt.text = year_text.format(year,camera.z) 

    delay_counter+=time.dt

    #print(camera.world_position)
    
    if mouse.collision!=None:
        if mouse.collision.entity=='mouse_button':
            mouse_button._enabled=True
    else:
        mouse_button._enabled=False    
    cur_utc=str(dates[i])
    cur_utc=cur_utc.replace(" ",'T')
    if delay_counter>=1:
        i=(i+1)
        delay_counter=0
    if i==len(dates):
        year+=1
        if year>=2100:  #change
            year=1900     #change
        gen_dates(start_date.format(year),end_date.format(year))
        i=0
        print(year)
    cur_et=spiceypy.utc2et(cur_utc)


    #cur_view_info = raycast(origin= camera.position,ignore=(focus_cam_entity,), direction= camera.forward, distance= 1000, debug= True)
    #print(cur_view_info.entity)
    
    focus('sun',cur_et)
    sun_text.world_position=sun.position
    sun_text.world_scale=abs(camera.z)*0.50

    focus('mercury',cur_et)   
    mercury.position=gen_pos(1,cur_et,10)           #change
    mercury_text.world_position=mercury.position
    mercury_text.world_scale=abs(camera.z)*0.40

    focus('venus',cur_et)   
    venus.position=gen_pos(2,cur_et,10)             #change
    venus_text.world_position=venus.position
    venus_text.world_scale=abs(camera.z)*0.40

    focus('earth',cur_et)
    earth.position=gen_pos(399,cur_et,10)           #change
    earth_text.world_position=earth.position
    earth_text.world_scale=abs(camera.z)*0.40
   
    
    focus('moon',cur_et)   
    moon.position=gen_pos(301,cur_et,10)            #change
    moon_text.world_position=moon.position
    moon_text.world_scale=abs(camera.z)*0.15
    
    focus('mars',cur_et)  
    mars.position=gen_pos(4,cur_et,10)              #change
    mars_text.world_position=mars.position
    mars_text.world_scale=abs(camera.z)*0.40
        #add_func
    focus('phobos',cur_et)   
    phobos.position= gen_pos(401,cur_et,4) + gen_pos(4,cur_et,10)
    phobos_text.world_position=phobos.position
    phobos_text.world_scale=abs(camera.z)*0.15
        #add_func
    focus('deimos',cur_et)   
    deimos.position= gen_pos(402,cur_et,4) + gen_pos(4,cur_et,10)
    deimos_text.world_position=deimos.position
    deimos_text.world_scale=abs(camera.z)*0.15
    
    focus('jupiter',cur_et)   
    jupiter.position=gen_pos(5,cur_et,10)           #change
    jupiter_text.world_position=jupiter.position
    jupiter_text.world_scale=abs(camera.z)*0.40
        #add_func
    focus('ganymede',cur_et)   
    ganymede.position= gen_pos(503,cur_et,5) + gen_pos(5,cur_et,10)
    ganymede_text.world_position=ganymede.position
    ganymede_text.world_scale=abs(camera.z)*0.15
        #add_func
    focus('callisto',cur_et)   
    callisto.position= gen_pos(504,cur_et,5) + gen_pos(5,cur_et,10)
    callisto_text.world_position=callisto.position
    callisto_text.world_scale=abs(camera.z)*0.15
        #add_func
    focus('io',cur_et)   
    io.position= gen_pos(501,cur_et,5) + gen_pos(5,cur_et,10)
    io_text.world_position=io.position
    io_text.world_scale=abs(camera.z)*0.15
        #add_func
    focus('europa',cur_et)   
    europa.position= gen_pos(502,cur_et,5) + gen_pos(5,cur_et,10)
    europa_text.world_position=europa.position
    europa_text.world_scale=abs(camera.z)*0.15

    focus('saturn',cur_et)   
    saturn.position=gen_pos(6,cur_et,10)            #change
    saturn_text.world_position=saturn.position
    saturn_text.world_scale=abs(camera.z)*0.40
        #add_func
    focus('titan',cur_et)   
    titan.position= gen_pos(606,cur_et,6) + gen_pos(6,cur_et,10)
    titan_text.world_position=titan.position
    titan_text.world_scale=abs(camera.z)*0.15
        #add_func
    focus('rhea',cur_et)   
    rhea.position= gen_pos(605,cur_et,6) + gen_pos(6,cur_et,10)
    rhea_text.world_position=rhea.position
    rhea_text.world_scale=abs(camera.z)*0.15
    
    focus('uranus',cur_et)   
    uranus.position=gen_pos(7,cur_et,10)            #change
    uranus_text.world_position=uranus.position
    uranus_text.world_scale=abs(camera.z)*0.40
        #add_func
    focus('titania',cur_et)   
    titania.position= gen_pos(703,cur_et,7) + gen_pos(7,cur_et,10)
    titania_text.world_position=titania.position
    titania_text.world_scale=abs(camera.z)*0.15
    
    focus('neptune',cur_et)   
    neptune.position=gen_pos(8,cur_et,10)           #change
    neptune_text.world_position=neptune.position
    neptune_text.world_scale=abs(camera.z)*0.40
        #add_func
    focus('triton',cur_et)   
    triton.position= gen_pos(801,cur_et,8) + gen_pos(8,cur_et,10)
    triton_text.world_position=triton.position
    triton_text.world_scale=abs(camera.z)*0.15

    focus('pluto',cur_et)   
    pluto.position=gen_pos(9,cur_et,10)             #change
    pluto_text.world_position=pluto.position
    pluto_text.world_scale=abs(camera.z)*0.30
        #add
    focus('ceres',cur_et)   
    ceres.position=gen_pos(2000001,cur_et,10)             
    ceres_text.world_position=ceres.position
    ceres_text.world_scale=abs(camera.z)*0.30


    if delay_counter==0:
        trail_mercury.append(mercury.position)
        trail_venus.append(venus.position)
        trail_earth.append(earth.position)
        trail_moon.append(moon.position)
        trail_mars.append(mars.position)
        trail_phobos.append(phobos.position)
        trail_deimos.append(deimos.position)
        trail_jupiter.append(jupiter.position)
        trail_ganymede.append(ganymede.position)    #change
        trail_callisto.append(callisto.position)    #change
        trail_io.append(io.position)                #change
        trail_europa.append(europa.position)        #change
        trail_saturn.append(saturn.position)
        trail_titan.append(titan.position)          #change
        trail_rhea.append(rhea.position)            #change
        trail_uranus.append(uranus.position)
        trail_titania.append(titania.position)      #change
        trail_neptune.append(neptune.position)
        trail_neptune.append(triton.position)       #change
        trail_pluto.append(pluto.position)
        trail_ceres.append(ceres.position)          #change
        
    
    if toggle_trail:
        destroy(curve_renderer_mercury)
        destroy(curve_renderer_venus)
        destroy(curve_renderer_earth)
        destroy(curve_renderer_moon)
        destroy(curve_renderer_mars)
        destroy(curve_renderer_phobos)
        destroy(curve_renderer_deimos)
        destroy(curve_renderer_jupiter)
        destroy(curve_renderer_ganymede)    #change
        destroy(curve_renderer_callisto)    #change
        destroy(curve_renderer_io)          #change
        destroy(curve_renderer_europa)      #change
        destroy(curve_renderer_saturn)
        destroy(curve_renderer_titan)       #change
        destroy(curve_renderer_rhea)        #change
        destroy(curve_renderer_uranus)
        destroy(curve_renderer_titania)     #change
        destroy(curve_renderer_neptune)
        destroy(curve_renderer_triton)      #change
        destroy(curve_renderer_pluto)
        destroy(curve_renderer_ceres)       #change
        
        try:
            thick=0.05
            curve_mode='line'
            curve_renderer_mercury= Entity(model=Mesh(vertices=trail_mercury, mode=curve_mode,thickness=thick),color=color.violet )
            curve_renderer_venus= Entity(model=Mesh(vertices=trail_venus, mode=curve_mode,thickness=thick),color=color.cyan )

            curve_renderer_earth= Entity(model=Mesh(vertices=trail_earth, mode=curve_mode,thickness=thick),color=color.blue )
            curve_renderer_moon= Entity(model=Mesh(vertices=trail_moon, mode=curve_mode,thickness=thick),color=color.blue )
            
            curve_renderer_mars= Entity(model=Mesh(vertices=trail_mars, mode=curve_mode,thickness=thick),color=color.green )
            curve_renderer_phobos= Entity(model=Mesh(vertices=trail_phobos, mode=curve_mode,thickness=thick),color=color.green )
            curve_renderer_deimos= Entity(model=Mesh(vertices=trail_deimos, mode=curve_mode,thickness=thick),color=color.green )

            curve_renderer_jupiter= Entity(model=Mesh(vertices=trail_jupiter, mode=curve_mode,thickness=thick),color=color.yellow )
            curve_renderer_ganymede= Entity(model=Mesh(vertices=trail_ganymede, mode=curve_mode,thickness=thick),color=color.yellow )   #change
            curve_renderer_callisto= Entity(model=Mesh(vertices=trail_callisto, mode=curve_mode,thickness=thick),color=color.yellow )   #change
            curve_renderer_io= Entity(model=Mesh(vertices=trail_io, mode=curve_mode,thickness=thick),color=color.yellow )               #change
            curve_renderer_europa= Entity(model=Mesh(vertices=trail_europa, mode=curve_mode,thickness=thick),color=color.yellow )       #change

            curve_renderer_saturn= Entity(model=Mesh(vertices=trail_saturn, mode=curve_mode,thickness=thick),color=color.orange )
            curve_renderer_titan= Entity(model=Mesh(vertices=trail_titan, mode=curve_mode,thickness=thick),color=color.orange )         #change
            curve_renderer_rhea= Entity(model=Mesh(vertices=trail_rhea, mode=curve_mode,thickness=thick),color=color.orange )           #change

            curve_renderer_uranus= Entity(model=Mesh(vertices=trail_uranus, mode=curve_mode,thickness=thick),color=color.red )
            curve_renderer_titania= Entity(model=Mesh(vertices=trail_titania, mode=curve_mode,thickness=thick),color=color.red )        #change

            curve_renderer_neptune= Entity(model=Mesh(vertices=trail_neptune, mode=curve_mode,thickness=thick),color=color.pink )
            curve_renderer_triton= Entity(model=Mesh(vertices=trail_triton, mode=curve_mode,thickness=thick),color=color.pink )         #change

            curve_renderer_pluto= Entity(model=Mesh(vertices=trail_pluto, mode=curve_mode,thickness=thick),color=color.white )
            curve_renderer_ceres= Entity(model=Mesh(vertices=trail_ceres, mode=curve_mode,thickness=thick),color=color.white )          #change
            
        except:
            pass

        #time.sleep(0.5)

app.run()
