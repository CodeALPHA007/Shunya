import spiceypy
from ursina import *
import datetime
import math
from collections import deque
import xarray as xr

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
    dates=list(xr.cftime_range(start_date, end_date, freq='M'))
    #dates = list(pd.date_range(start_date, end_date, freq='M'))

gen_dates(start_date.format(year),end_date.format(year))

    
    
i=0

app=Ursina()

window.color=color.black
year_text='<red>YEAR</red>\n<green>{}</green><red>\nZoom</red>\n<green>{}</green>'
cur_year_txt = Text(scale=1,position=(-0.85,0.45,0))


sun=Entity(model='sphere',scale=km2au(696000),texture="..\Assets\Sun.jpg", color=color.white)
sun.position=Vec3(0,0,0)

mercury=Entity(model='sphere', scale = km2au(2439),texture=r"..\Assets\mercury.png")
venus=Entity(model='sphere', scale = km2au(6052), texture=r"..\Assets\venus_atmosphere.png")

earth=Entity(model='sphere',texture=r"..\Assets\earth.jpg", scale = km2au(6387))

moon=Entity(model='sphere', scale = km2au(1738), texture="..\Assets\moon.jpg")

mars=Entity(model='sphere', scale = km2au(3393), texture="..\Assets\mars.png")
jupiter=Entity(model='sphere', texture="..\Assets\jupiter.png",scale = km2au(71398))
saturn=Entity(model='sphere', scale = km2au(60000), texture="..\Assets\saturn.png")
uranus=Entity(model='sphere', scale = km2au(25559), texture=r"..\Assets\uranus.png")
neptune=Entity(model='sphere', scale = km2au(24800), texture=r"..\Assets\neptune.png")
pluto=Entity(model='sphere', scale = km2au(1140), texture="..\Assets\moon.jpg", color=color.white)

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

zoom_field = InputField(x=-.45, default_value='earth', active=True,color=color.white,text_color=color.red)

follow = {
    mercury: False,
    venus: False,
    earth: False,
    mars: False,
    jupiter: False,
    saturn: False,
    uranus: False,
    neptune: False,
    moon: False
}

def resetFollow(dict):
    for i in dict:
        dict[i] = False

follow_earth=False
def goto():
    global follow_earth,zoom_field,camera, follow
    x=zoom_field.text
    print(x)
    if x=='earth':  
        follow[earth] = True
    elif x=="mars":
        resetFollow(follow)
        follow[mars] = True
    elif x=="mercury":
        resetFollow(follow)
        follow[mercury] = True
    elif x=="venus":
        resetFollow(follow)
        follow[venus] = True
    elif x=="jupiter":
        resetFollow(follow)
        follow[jupiter] = True
    elif x=="saturn":
        resetFollow(follow)
        follow[saturn] = True
    elif x=="uranus":
        resetFollow(follow)
        follow[uranus] = True
    elif x=="neptune":
        resetFollow(follow)
        follow[neptune] = True
    elif x=="moon":
        resetFollow(follow)
        follow[moon] = True
    else:
        for i in follow:
            follow[i] = False

        camera.position = Vec3(0, 0, -20)
        camera.look_at(sun)

zoom_b=Button(x=-.35,y=-0.10, text='GO TO', active=True,color=color.green,text_color=color.red,on_click=goto)
zoom_b.fit_to_text()


#camera.position=Vec3(0,10,-100)
#camera.look_at(sun)
camera.clip_plane_far_setter(150000)

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
    
    print(camera.position)
    global follow_earth

    camera.z+=1000* held_keys['w']*time.dt
    camera.z-=1000* held_keys['s']*time.dt    
    camera.y-=100* held_keys['e']*time.dt
    camera.y+=100* held_keys['d']*time.dt    
    
    

    #camera.look_at(sun)

    global last_time,cur_year_txt,year_text,curve_renderer,start_date,end_date,i,year,dates
    global trail_mercury,trail_venus,trail_earth,trail_moon,trail_mars,trail_jupiter,trail_saturn,trail_uranus,trail_neptune
    global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth,curve_renderer_moon
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
        #print(year)
    cur_et=spiceypy.utc2et(cur_utc)


    
    if follow[earth] == True:
        camera.look_at(earth)
        camera.position=gen_pos(399,cur_et)+Vec3(0.1,0.1,0.1)
    
    if follow[mars] == True:
        camera.look_at(mars)
        camera.position=gen_pos(4,cur_et)+Vec3(0, 0, 1)
    
    if follow[jupiter] == True:
        camera.look_at(jupiter)
        camera.position=gen_pos(5,cur_et)+Vec3(0, 0, 2)
    
    if follow[saturn] == True:
        camera.look_at(saturn)
        camera.position=gen_pos(6,cur_et)+Vec3(0, 0, 2)

    if follow[uranus] == True:
        camera.look_at(uranus)
        camera.position=gen_pos(7,cur_et)+Vec3(0, 0, 2)

    if follow[neptune] == True:
        camera.look_at(neptune)
        camera.position=gen_pos(8,cur_et)+Vec3(0, 0, 2)

    if follow[mercury] == True:
        camera.look_at(mercury)
        camera.position=gen_pos(1,cur_et)+Vec3(0.1,0.1,0.1)

    if follow[venus] == True:
        camera.look_at(venus)
        camera.position=gen_pos(2,cur_et)+Vec3(0.1,0.1,0.1)
       
    if follow[moon] == True:
        camera.look_at(moon)
        camera.position=gen_pos(301,cur_et)+Vec3(0.1,0.1,0.1)

    mercury.position=gen_pos(1,cur_et)
    mercury_text.world_position=mercury.position
    #print([mercury_text.world_position,mercury.position])
    
    venus.position=gen_pos(2,cur_et)
    venus_text.world_position=venus.position
        
    earth.position=gen_pos(399,cur_et)
    earth_text.world_position=earth.position
    
    moon.position=gen_pos(301,cur_et)
    

    mars.position=gen_pos(4,cur_et)
    mars_text.world_position=mars.position
    
    jupiter.position=gen_pos(5,cur_et)
    jupiter_text.world_position=jupiter.position
    
    saturn.position=gen_pos(6,cur_et)
    saturn_text.world_position=saturn.position
    
    uranus.position=gen_pos(7,cur_et)
    uranus_text.world_position=uranus.position
    
    neptune.position=gen_pos(8,cur_et)
    #print(neptune_text.world_position)
    neptune_text.world_position=neptune.position

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
        
            curve_renderer_mercury= Entity(model=Mesh(vertices=trail_mercury, mode='point',thickness=thick),color=color.violet )
            curve_renderer_venus= Entity(model=Mesh(vertices=trail_venus, mode='point',thickness=thick),color=color.cyan )
            curve_renderer_earth= Entity(model=Mesh(vertices=trail_earth, mode='point',thickness=thick),color=color.blue )
            curve_renderer_moon= Entity(model=Mesh(vertices=trail_moon, mode='point',thickness=thick),color=color.blue )
            
            curve_renderer_mars= Entity(model=Mesh(vertices=trail_mars, mode='point',thickness=thick),color=color.green )
            curve_renderer_jupiter= Entity(model=Mesh(vertices=trail_jupiter, mode='point',thickness=thick),color=color.yellow )
            curve_renderer_saturn= Entity(model=Mesh(vertices=trail_saturn, mode='point',thickness=thick),color=color.orange )
            curve_renderer_uranus= Entity(model=Mesh(vertices=trail_uranus, mode='point',thickness=thick),color=color.red )
        
            curve_renderer_neptune= Entity(model=Mesh(vertices=trail_neptune, mode='point',thickness=thick),color=color.pink )
            curve_renderer_pluto= Entity(model=Mesh(vertices=trail_pluto, mode='point',thickness=thick),color=color.white )
        
            
        except:
            pass

        #time.sleep(0.5)

app.run()    