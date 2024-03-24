import spiceypy
from ursina import *
import datetime
import math
from collections import deque
import time
import xarray as xr

spiceypy.furnsh("../Kernels/lsk/naif0012.tls")
spiceypy.furnsh("../Kernels/spk/de430.bsp")
import pandas as pd
dates=[]
start_date = '{}-01-01'
end_date = '{}-12-31'
year=1550
last_time=time.time()
def gen_pos(target: int, cur_et):
    planet_state_wrt_sun,earth_sun_light_time=spiceypy.spkgeo(targ=target,et=cur_et
                                                        ,ref="ECLIPJ2000",obs=10)
    x,y,z=planet_state_wrt_sun[:3]
    #earth_vel_x,earth_vel_y,earth_vel_z=earth_state_wrt_sun[3:]
    x=spiceypy.convrt(x,'km','au')
    y=spiceypy.convrt(y,'km','au')
    z=spiceypy.convrt(z,'km','au')
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


sun=Entity(model='sphere',scale=0.5, color=color.white)
sun.position=Vec3(0,0,0)

mercury=Entity(model='sphere', scale = 0.1, color=color.violet)
venus=Entity(model='sphere', scale = 0.1, color=color.cyan)
earth=Entity(model='sphere', scale = 0.1, color=color.blue)
mars=Entity(model='sphere', scale = 0.1, color=color.green)
jupiter=Entity(model='sphere', scale = 0.1, color=color.yellow)
saturn=Entity(model='sphere', scale = 0.1, color=color.orange)
uranus=Entity(model='sphere', scale = 0.1, color=color.red)
neptune=Entity(model='sphere', scale = 0.1, color=color.pink)
pluto=Entity(model='sphere', scale = 0.1, color=color.white)

mercury_text=Text(text='MERCURY')
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
trail_mars=deque([],maxlen=100)
trail_jupiter=deque([],maxlen=100)
trail_saturn=deque([],maxlen=100)
trail_uranus=deque([],maxlen=100)
trail_neptune=deque([],maxlen=100)
trail_pluto=deque([],maxlen=100)

curve_renderer_mercury=Entity()
curve_renderer_venus=Entity()
curve_renderer_earth=Entity()
curve_renderer_mars=Entity()
curve_renderer_jupiter=Entity()
curve_renderer_saturn=Entity()
curve_renderer_uranus=Entity()
curve_renderer_neptune=Entity()
curve_renderer_pluto=Entity()

camera.position=Vec3(0,10,-100)
camera.look_at(neptune)

def input(key):
    global sun
    if key=='w':
        camera.z+=10
        camera.look_at(sun)
    elif key=='s':
        camera.z-=10
        camera.look_at(sun)

def update():
    
    global last_time,cur_year_txt,year_text,curve_renderer,start_date,end_date,i,year,dates
    global trail_mercury,trail_venus,trail_earth,trail_mars,trail_jupiter,trail_saturn,trail_uranus,trail_neptune
    global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth
    global curve_renderer_mars,curve_renderer_jupiter,curve_renderer_saturn
    global curve_renderer_uranus,curve_renderer_neptune,curve_renderer_pluto

    global mercury_text,venus_text,earth_text
    global mars_text,jupiter_text,saturn_text
    global uranus_text,neptune_text,pluto_text

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

    mercury.position=gen_pos(1,cur_et)
    mercury_text.world_position=mercury.position
    
    venus.position=gen_pos(2,cur_et)
    venus_text.world_position=venus.position
    
    earth.position=gen_pos(3,cur_et)
    earth_text.world_position=earth.position
    
    mars.position=gen_pos(4,cur_et)
    mars_text.world_position=mars.position
    
    jupiter.position=gen_pos(5,cur_et)
    jupiter_text.world_position=jupiter.position
    
    saturn.position=gen_pos(6,cur_et)
    saturn_text.world_position=saturn.position
    
    uranus.position=gen_pos(7,cur_et)
    uranus_text.world_position=uranus.position
    
    neptune.position=gen_pos(8,cur_et)
    print(neptune_text.world_position)
    neptune_text.world_position=neptune.position

    pluto.position=gen_pos(9,cur_et)
    pluto_text.world_position=pluto.position
    

    
    trail_mercury.append(mercury.position)
    trail_venus.append(venus.position)
    trail_earth.append(earth.position)
    trail_mars.append(mars.position)
    trail_jupiter.append(jupiter.position)
    trail_saturn.append(saturn.position)
    trail_uranus.append(uranus.position)
    trail_neptune.append(neptune.position)
    trail_pluto.append(pluto.position)
    
    
    destroy(curve_renderer_mercury)
    destroy(curve_renderer_venus)
    destroy(curve_renderer_earth)
    destroy(curve_renderer_mars)
    destroy(curve_renderer_jupiter)
    destroy(curve_renderer_saturn)
    destroy(curve_renderer_uranus)
    destroy(curve_renderer_neptune)
    destroy(curve_renderer_pluto)
    
    try:
        thick=0.05
    
        curve_renderer_mercury= Entity(model=Mesh(vertices=trail_mercury, mode='line',thickness=thick),color=color.violet )
        curve_renderer_venus= Entity(model=Mesh(vertices=trail_venus, mode='line',thickness=thick),color=color.cyan )
        curve_renderer_earth= Entity(model=Mesh(vertices=trail_earth, mode='line',thickness=thick),color=color.blue )
        curve_renderer_mars= Entity(model=Mesh(vertices=trail_mars, mode='line',thickness=thick),color=color.green )
        curve_renderer_jupiter= Entity(model=Mesh(vertices=trail_jupiter, mode='line',thickness=thick),color=color.yellow )
        curve_renderer_saturn= Entity(model=Mesh(vertices=trail_saturn, mode='line',thickness=thick),color=color.orange )
        curve_renderer_uranus= Entity(model=Mesh(vertices=trail_uranus, mode='line',thickness=thick),color=color.red )
    
        curve_renderer_neptune= Entity(model=Mesh(vertices=trail_neptune, mode='line',thickness=thick),color=color.pink )
        curve_renderer_pluto= Entity(model=Mesh(vertices=trail_pluto, mode='line',thickness=thick),color=color.white )
    
        
    except:
        pass
    #time.sleep(0.5)

app.run()    
