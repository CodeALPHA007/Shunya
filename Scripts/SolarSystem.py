import spiceypy
from ursina import *
import datetime
import math
from collections import deque
import time

spiceypy.furnsh("../Kernels/lsk/naif0012.tls")
spiceypy.furnsh("../Kernels/spk/de430s.bsp")
import pandas as pd
dates=[]
start_date = '{}-01-01'
end_date = '{}-12-31'
year=1950

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
    dates = list(pd.date_range(start_date, end_date, freq='M'))

gen_dates(start_date.format(year),end_date.format(year))

    
i=0
#cur_utc_time = datetime.datetime.today()
#cur_utc_time = cur_utc_time.strftime("%{}-%{}-%{}T{}:%M:%S")
#cur_utc_time = "{}-{}-{}T{}:00:00"
#hour=0




'''
earth_state_wrt_sun,earth_sun_light_time=spiceypy.spkgeo(targ=399,et=cur_et
                                                         ,ref="ECLIPJ2000",obs=10)
print(earth_state_wrt_sun)
earth_sun_distance=math.sqrt(earth_state_wrt_sun[0]**2.0
                             + earth_state_wrt_sun[1]**2.0
                             + earth_state_wrt_sun[2]**2.0)
earth_sun_distance_au=spiceypy.convrt(earth_sun_distance,'km','au')
print(earth_sun_distance_au)
'''

app=Ursina()
window.color=color.black
year_text='<red>YEAR</red>\n<green>{}</green>'
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

trail_earth=deque([],maxlen=1000)
trail_jupiter=deque([],maxlen=1000)

curve_renderer_earth=Entity()
curve_renderer_jupiter=Entity()

camera.position=Vec3(0,10,-200)
camera.look_at(sun)
def update():
    global cur_year_txt,year_text,start_date,end_date,i,year,dates
    
    cur_year_txt.text = year_text.format(year) 


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
    venus.position=gen_pos(2,cur_et)
    earth.position=gen_pos(3,cur_et)
    mars.position=gen_pos(4,cur_et)
    jupiter.position=gen_pos(5,cur_et)
    saturn.position=gen_pos(6,cur_et)
    uranus.position=gen_pos(7,cur_et)
    neptune.position=gen_pos(8,cur_et)

    
    try:
        thick=0.05
        curve_renderer= Entity(model=Mesh(vertices=[mercury.position], mode='point',thickness=thick),color=color.violet )
        curve_renderer= Entity(model=Mesh(vertices=[venus.position], mode='point',thickness=thick),color=color.cyan )
        curve_renderer= Entity(model=Mesh(vertices=[earth.position], mode='point',thickness=thick),color=color.blue )
        curve_renderer= Entity(model=Mesh(vertices=[mars.position], mode='point',thickness=thick),color=color.green )
        curve_renderer= Entity(model=Mesh(vertices=[jupiter.position], mode='point',thickness=thick),color=color.yellow )
        curve_renderer= Entity(model=Mesh(vertices=[saturn.position], mode='point',thickness=thick),color=color.orange )
        curve_renderer= Entity(model=Mesh(vertices=[uranus.position], mode='point',thickness=thick),color=color.red )
        curve_renderer= Entity(model=Mesh(vertices=[neptune.position], mode='point',thickness=thick),color=color.pink )
        
        
    except:
        pass

app.run()    