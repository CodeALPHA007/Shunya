import spiceypy
from ursina import *
import datetime
import numpy
from collections import deque
import xarray as xr
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

spiceypy.furnsh("../Kernels/lsk/naif0012.tls")
spiceypy.furnsh("../Kernels/spk/de430.bsp")
import pandas as pd
dates=[]
start_date = '{}-01-01'
end_date = '{}-12-31'
year=1550
toggle_trail=False

multiplier=1000
def km2au(dist_in_km: float):
    global multiplier
    return (spiceypy.convrt(dist_in_km,'km','au'))*multiplier

def gen_pos(target: int, cur_et):
    global multiplier
    planet_state_wrt_sun,earth_sun_light_time=spiceypy.spkgeo(targ=target,et=cur_et
                                                        ,ref="ECLIPJ2000",obs=10)
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


sun=Entity(model='sphere',scale=km2au(696000),texture=r"..\Assets\sun.jpg", color=color.white)
sun.position=Vec3(0,0,0)

mercury=Entity(model='sphere', scale = km2au(2439), color=color.violet)
venus=Entity(model='sphere', scale = km2au(6052), color=color.cyan)

earth=Entity(name='Earth',model='sphere',texture=r"..\Assets\earth4k.jpg", scale = km2au(6387))
earth.collider = BoxCollider(earth, center=Vec3(0,0,0), size=earth.scale*50)
earth.collider.visible=True

moon=Entity(model='sphere', scale = km2au(1738),color=color.white)

mars=Entity(model='sphere', scale = km2au(3393), color=color.green)
jupiter=Entity(model='sphere', texture="..\Assets\jupiter.png",scale = km2au(71398))
saturn=Entity(model='sphere', scale = km2au(60000), color=color.orange)
uranus=Entity(model='sphere', scale = km2au(25559), color=color.red)
neptune=Entity(model='sphere', scale = km2au(24800), color=color.pink)
pluto=Entity(model='sphere', scale = km2au(1140), color=color.white)

mercury_text=Text(text='MERCURY',scale=0.5)
venus_text=Text(text='VENUS')
earth_text=Text(text='EARTH')
mars_text=Text(text='MARS')
jupiter_text=Text(text='JUPITER')
saturn_text=Text(text='SATURN')
uranus_text=Text(text='URANUS')
neptune_text=Text(text='NEPTUNE')
pluto_text=Text(text='PLUTO')

trail_mercury=deque([],maxlen=100)
trail_venus=deque([],maxlen=100)
trail_earth=deque([],maxlen=100)
trail_moon=deque([],maxlen=100)

trail_mars=deque([],maxlen=100)
trail_jupiter=deque([],maxlen=100)
trail_saturn=deque([],maxlen=100)
trail_uranus=deque([],maxlen=100)
trail_neptune=deque([],maxlen=100)
trail_pluto=deque([],maxlen=100)

curve_renderer_mercury=Entity()
curve_renderer_venus=Entity()
curve_renderer_earth=Entity()
curve_renderer_moon=Entity()

curve_renderer_mars=Entity()
curve_renderer_jupiter=Entity()
curve_renderer_saturn=Entity()
curve_renderer_uranus=Entity()
curve_renderer_neptune=Entity()
curve_renderer_pluto=Entity()

zoom_field = InputField(x=-.60,y=-0.45, default_value='earth', active=False,color=color.white,text_color=color.red)

follow_earth=False
def goto():
    global follow_earth,zoom_field,camera
    x=zoom_field.text
    print(x)
    if x=='earth':  
        follow_earth=True

planets_info={"sun":{'entity':sun,'planet_id': 10, 'follow': False },
              "mercury":{'entity':mercury,'planet_id': 1,'follow': False },
              "venus":{'entity':venus,'planet_id': 2,'follow': False },
              "earth":{'entity':earth,'planet_id': 399,'follow': False },
              "moon":{'entity':moon,'planet_id': 301,'follow': False },
              "mars":{'entity':mars,'planet_id': 4,'follow': False },
              "jupiter":{'entity':jupiter,'planet_id': 5,'follow': False },
              "saturn":{'entity':saturn,'planet_id': 6,'follow': False },
              "uranus":{'entity':uranus,'planet_id': 7,'follow': False },
              "neptune":{'entity':neptune,'planet_id': 8,'follow': False },
              "pluto":{'entity':pluto,'planet_id': 9,'follow': False },
              }
def set_all_follow_false():
    global planets_info
    for i in planets_info.keys():
        planets_info[i]['follow']=False

def set_follow(planet_name: str):
    global planets_info
    set_all_follow_false()
    planets_info[planet_name]['follow']=True


zoom_b=Button(x=-.30,y=-0.45, text='GO TO', active=True,color=color.green,text_color=color.red,on_click=goto)
zoom_b.fit_to_text()


button_list=[DropdownMenuButton('Sun',on_click=Func(set_follow,'sun')),
             DropdownMenuButton('Mercury',on_click=Func(set_follow,'mercury')),
             DropdownMenuButton('Venus',on_click=Func(set_follow,'venus')),
             DropdownMenu(text='Earth and Moon',buttons=[DropdownMenuButton('Earth',on_click=Func(set_follow,'earth')),
                                                DropdownMenuButton('Moon',on_click=Func(set_follow,'moon')),],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenuButton('Mars',on_click=Func(set_follow,'mars')),
             DropdownMenuButton('Jupiter',on_click=Func(set_follow,'jupiter')),
             DropdownMenuButton('Saturn',on_click=Func(set_follow,'saturn')),
             DropdownMenuButton('Uranus',on_click=Func(set_follow,'uranus')),
             DropdownMenuButton('Neptune',on_click=Func(set_follow,'neptune')),
             DropdownMenuButton('Pluto',on_click=Func(set_follow,'pluto')),
             ]



drop_menu=DropdownMenu(x=-.60,y=0.45,text='FOCUS ON', 
                       buttons=button_list,color=color.white,text_color=color.red,highlight_color=color.green,
                       scale=(0.3,0.03,0.0))



#camera.position=Vec3(0,10,-100)
#camera.look_at(sun)
original_camera=EditorCamera(position=(0,0,-10))
original_camera.collider=BoxCollider(camera, center=Vec3(0,0,0), size=Vec3(10,10,10))
camera.clip_plane_far_setter(150000)

focus_cam_entity=Entity()
focus_cam_entity.collider=BoxCollider(focus_cam_entity, center=Vec3(0,0,0), size=Vec3(0.5,0.5,0.5))

focus_camera=EditorCamera()
focus_camera.parent=focus_cam_entity
print(focus_camera.name)
camera.clip_plane_far_setter(150000)
focus_camera.disable()

def magnitude(vector):
    return numpy.linalg.norm(vector)

def focus(planet_name: str, cur_et):
    global planets_info,focus_camera,original_camera
    if planet_name=='sun':
        original_camera.enable()
        focus_camera.disable()
    
    elif planets_info[planet_name]['follow']:
        temp_planet_id=planets_info[planet_name]['planet_id']
        temp_planet_entity=planets_info[planet_name]['entity']
        #original_camera.disable()
        focus_camera.enable()
        #focus_camera.position=gen_pos(temp_planet_id,cur_et)
        focus_cam_entity.position=gen_pos(temp_planet_id,cur_et)
        focus_camera.look_at(temp_planet_entity)
        #focus_cam_entity.collider.position=camera.position
        focus_camera.ignore=True
        focus_cam_entity.collider.world_position=focus_cam_entity.world_position
        hit_info=original_camera.intersects(debug=True)
        if hit_info.hit:
            print(hit_info.entity.name)
        

            


def input(key):
    global sun,toggle_trail
    if key=='t':
        if toggle_trail==True:
            global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth,curve_renderer_moon
            global curve_renderer_mars,curve_renderer_jupiter,curve_renderer_saturn
            global curve_renderer_uranus,curve_renderer_neptune,curve_renderer_pluto
            try:
                destroy(curve_renderer_mercury)
                destroy(curve_renderer_venus)
                destroy(curve_renderer_earth)
                destroy(curve_renderer_moon)
                
                destroy(curve_renderer_mars)
                destroy(curve_renderer_jupiter)
                destroy(curve_renderer_saturn)
                destroy(curve_renderer_uranus)
                destroy(curve_renderer_neptune)
                destroy(curve_renderer_pluto)
            except:
                pass    
        toggle_trail=not(toggle_trail)            
                
def update():
    
    global follow_earth

    original_camera.z+=1000* held_keys['w']*time.dt
    original_camera.z-=1000* held_keys['s']*time.dt    
    original_camera.y-=100* held_keys['a']*time.dt
    original_camera.y+=100* held_keys['d']*time.dt    
    focus_camera.z+=100* held_keys['w']*time.dt
    focus_camera.z-=100* held_keys['s']*time.dt    
    focus_camera.y-=100* held_keys['a']*time.dt
    focus_camera.y+=100* held_keys['d']*time.dt    
    
    

    #camera.look_at(sun)

    global last_time,cur_year_txt,year_text,curve_renderer,start_date,end_date,i,year,dates
    global trail_mercury,trail_venus,trail_earth,trail_moon,trail_mars,trail_jupiter,trail_saturn,trail_uranus,trail_neptune
    global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth,curve_renderer_moon
    global curve_renderer_mars,curve_renderer_jupiter,curve_renderer_saturn
    global curve_renderer_uranus,curve_renderer_neptune,curve_renderer_pluto

    global mercury_text,venus_text,earth_text
    global mars_text,jupiter_text,saturn_text
    global uranus_text,neptune_text,pluto_text

    global planets_info
    
    if not(focus_camera.enabled):
        cur_year_txt.text = year_text.format(year,original_camera.z) 
    else:
        cur_year_txt.text = year_text.format(year,camera.z) 


    cur_utc=str(dates[i])
    cur_utc=cur_utc.replace(" ",'T')
    i=(i+1)
    if i==len(dates):
        year+=1
        gen_dates(start_date.format(year),end_date.format(year))
        i=0
        print(year)
    cur_et=spiceypy.utc2et(cur_utc)


    #cur_view_info = raycast(origin= camera.position,ignore=(focus_cam_entity,), direction= camera.forward, distance= 1000, debug= True)
    #print(cur_view_info.entity)
    
    focus('sun',cur_et)
    focus('mercury',cur_et)   
    mercury.position=gen_pos(1,cur_et)
    mercury_text.world_position=mercury.position
    
    focus('venus',cur_et)   
    venus.position=gen_pos(2,cur_et)
    venus_text.world_position=venus.position
    
    focus('earth',cur_et)   
    earth.position=gen_pos(399,cur_et)
    earth_text.world_position=earth.position
    
    focus('moon',cur_et)   
    moon.position=gen_pos(301,cur_et)
    
    focus('mars',cur_et)  
    mars.position=gen_pos(4,cur_et)
    mars_text.world_position=mars.position
    
    focus('jupiter',cur_et)   
    jupiter.position=gen_pos(5,cur_et)
    jupiter_text.world_position=jupiter.position
    
    focus('saturn',cur_et)   
    saturn.position=gen_pos(6,cur_et)
    saturn_text.world_position=saturn.position
    
    focus('uranus',cur_et)   
    uranus.position=gen_pos(7,cur_et)
    uranus_text.world_position=uranus.position
    
    focus('neptune',cur_et)   
    neptune.position=gen_pos(8,cur_et)
    #print(neptune_text.world_position)
    neptune_text.world_position=neptune.position

    focus('pluto',cur_et)   
    pluto.position=gen_pos(9,cur_et)
    pluto_text.world_position=pluto.position
    

    
    trail_mercury.append(mercury.position)
    trail_venus.append(venus.position)
    trail_earth.append(earth.position)
    trail_moon.append(moon.position)
    trail_mars.append(mars.position)
    trail_jupiter.append(jupiter.position)
    trail_saturn.append(saturn.position)
    trail_uranus.append(uranus.position)
    trail_neptune.append(neptune.position)
    trail_pluto.append(pluto.position)
    
    
    if toggle_trail:
        destroy(curve_renderer_mercury)
        destroy(curve_renderer_venus)
        destroy(curve_renderer_earth)
        destroy(curve_renderer_moon)
        destroy(curve_renderer_mars)
        destroy(curve_renderer_jupiter)
        destroy(curve_renderer_saturn)
        destroy(curve_renderer_uranus)
        destroy(curve_renderer_neptune)
        destroy(curve_renderer_pluto)
        
        try:
            thick=0.05
            curve_mode='line'
            curve_renderer_mercury= Entity(model=Mesh(vertices=trail_mercury, mode=curve_mode,thickness=thick),color=color.violet )
            curve_renderer_venus= Entity(model=Mesh(vertices=trail_venus, mode=curve_mode,thickness=thick),color=color.cyan )
            curve_renderer_earth= Entity(model=Mesh(vertices=trail_earth, mode=curve_mode,thickness=thick),color=color.blue )
            curve_renderer_moon= Entity(model=Mesh(vertices=trail_moon, mode=curve_mode,thickness=thick),color=color.blue )
            
            curve_renderer_mars= Entity(model=Mesh(vertices=trail_mars, mode=curve_mode,thickness=thick),color=color.green )
            curve_renderer_jupiter= Entity(model=Mesh(vertices=trail_jupiter, mode=curve_mode,thickness=thick),color=color.yellow )
            curve_renderer_saturn= Entity(model=Mesh(vertices=trail_saturn, mode=curve_mode,thickness=thick),color=color.orange )
            curve_renderer_uranus= Entity(model=Mesh(vertices=trail_uranus, mode=curve_mode,thickness=thick),color=color.red )
        
            curve_renderer_neptune= Entity(model=Mesh(vertices=trail_neptune, mode=curve_mode,thickness=thick),color=color.pink )
            curve_renderer_pluto= Entity(model=Mesh(vertices=trail_pluto, mode=curve_mode,thickness=thick),color=color.white )
            
        except:
            pass

        #time.sleep(0.5)

app.run()    