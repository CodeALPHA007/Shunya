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


sun=Entity(name='Sun', model='sphere',scale=km2au(696000),texture=r"..\Assets\sun.jpg",collider='box')
sun.position=Vec3(0,0,0)

mercury=Entity(name='Mercury', model='sphere',texture=r"..\Assets\mercurymap.jpg", scale = km2au(2439),collider='box')
venus=Entity(name='Venus', model='sphere', texture=r"..\Assets\venusmap.jpg" ,scale = km2au(6052),collider='box')
earth=Entity(name='Earth',model='sphere',texture=r"..\Assets\earth4k.jpg",collider='box', scale = km2au(6387))
moon=Entity(name='Moon', model='sphere', texture=r"..\Assets\moonmap4k.jpg" ,scale = km2au(1738),collider='box')
mars=Entity(name=' Mars', model='sphere', texture=r"..\Assets\marsmap.jpg",scale = km2au(3393),collider='box')
jupiter=Entity(name='Jupiter',model='sphere', texture=r"..\Assets\jupiter.png",scale = km2au(71398),collider='box')
saturn=Entity(name='Saturn', model='sphere', texture=r"..\Assets\saturnmap.jpg", scale = km2au(60000),collider='box')
uranus=Entity(name='Uranus', model='sphere', texture=r"..\Assets\uranusmap.jpg", scale = km2au(25559),collider='box')
neptune=Entity(name='Neptune', model='sphere',texture=r"..\Assets\neptunemap.jpg", scale = km2au(24800),collider='box')
pluto=Entity(name='Pluto', model='sphere', texture=r"..\Assets\plutomap2k.jpg", scale = km2au(1140),collider='box')


sun_text=Text(parent=sun,text='Sun', scale=camera.z*0.4)
mercury_text=Text(parent=mercury , text='Mercury', scale=camera.z*0.4)
venus_text=Text(parent=venus , text='Venus', scale=camera.z*0.4)

earth_text=Text(parent=earth , text='Earth', scale=camera.z*0.4)
moon_text=Text(parent=moon , text='Moon', scale=camera.z*0.4)

mars_text=Text(parent=mars , text='Mars', scale=camera.z*0.4)
jupiter_text=Text(parent=jupiter , text='Jupiter', scale=camera.z*0.4)
saturn_text=Text(parent=saturn , text='Saturn', scale=camera.z*0.4)
uranus_text=Text(parent=uranus , text='Uranus', scale=camera.z*0.4)
neptune_text=Text(parent=neptune , text='Neptune', scale=camera.z*0.4)
pluto_text=Text(parent=pluto , text='Pluto', scale=camera.z*0.4)

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
              "mars":{'entity':mars,'planet_id': 4, 'text_tag_entity':mars_text ,'follow': False },
              "jupiter":{'entity':jupiter,'planet_id': 5, 'text_tag_entity':jupiter_text ,'follow': False },
              "saturn":{'entity':saturn,'planet_id': 6, 'text_tag_entity':saturn_text ,'follow': False },
              "uranus":{'entity':uranus,'planet_id': 7, 'text_tag_entity':uranus_text ,'follow': False },
              "neptune":{'entity':neptune,'planet_id': 8, 'text_tag_entity':neptune_text ,'follow': False },
              "pluto":{'entity':pluto,'planet_id': 9, 'text_tag_entity':pluto_text ,'follow': False },
              }
def set_all_follow_false():
    global planets_info
    for i in planets_info.keys():
        planets_info[i]['follow']=False
        planets_info[i]['text_tag_entity'].visible=False

current_focus='sun'
toggle_free=False

camera.parent=scene
default_zoom=-20
camera.z=default_zoom
camera.collider=BoxCollider(camera,center=Vec3(0,0,5),size=(5,5,20))
camera.collider.visible=False
camera.clip_plane_far_setter(300000)            

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
                                                DropdownMenuButton('Moon',on_click=Func(set_follow,'moon')),],
                                                color=color.white,text_color=color.red,highlight_color=color.yellow),
             DropdownMenuButton('Mars',on_click=Func(set_follow,'mars')),
             DropdownMenuButton('Jupiter',on_click=Func(set_follow,'jupiter')),
             DropdownMenuButton('Saturn',on_click=Func(set_follow,'saturn')),
             DropdownMenuButton('Uranus',on_click=Func(set_follow,'uranus')),
             DropdownMenuButton('Neptune',on_click=Func(set_follow,'neptune')),
             DropdownMenuButton('Pluto',on_click=Func(set_follow,'pluto')),
             ]



drop_menu=DropdownMenu(x=-.60,y=0.45,text=drop_down_text.format(current_focus), 
                       buttons=button_list,color=color.white,text_color=color.red,highlight_color=color.green,
                       scale=(0.3,0.03,0.0))

mouse_enabled_movement=False

def mouse_enabled_movement_function():
    global mouse_enabled_movement,toggle_free
    if not mouse_enabled_movement:
        if toggle_free:
            mouse_enabled_movement=True
    else:
        mouse_enabled_movement=False
        
mouse_text="Mouse control: {}"
mouse_button=Button(y=0.43,scale=1,text=mouse_text.format(mouse_enabled_movement),text_color=color.black,
                    color=color.red,highlight_color=color.white, disabled=False)
mouse_button.fit_to_text()
mouse_button.on_click=mouse_enabled_movement_function
mouse_button.visible=True
#mouse_button.on_mouse_enter= mouse_button.enable
#mouse_button.on_mouse_exit=mouse_button.disable
mouse_button.fit_to_text()


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
    
    camera_control()

    global follow_earth,zoom_on,delay_counter
    global last_time,cur_year_txt,year_text,curve_renderer,start_date,end_date,i,year,dates
    global trail_mercury,trail_venus,trail_earth,trail_moon,trail_mars,trail_jupiter,trail_saturn,trail_uranus,trail_neptune
    global curve_renderer_mercury,curve_renderer_venus,curve_renderer_earth,curve_renderer_moon
    global curve_renderer_mars,curve_renderer_jupiter,curve_renderer_saturn
    global curve_renderer_uranus,curve_renderer_neptune,curve_renderer_pluto

    global sun_text,mercury_text,venus_text,earth_text,moon_text
    global mars_text,jupiter_text,saturn_text
    global uranus_text,neptune_text,pluto_text

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

    
    cur_utc=str(dates[i])
    cur_utc=cur_utc.replace(" ",'T')
    if delay_counter>=1:
        i=(i+1)
        delay_counter=0
    if i==len(dates):
        year+=1
        if year>=2649:
            year=1550
        gen_dates(start_date.format(year),end_date.format(year))
        i=0
        print(year)
    cur_et=spiceypy.utc2et(cur_utc)


    #cur_view_info = raycast(origin= camera.position,ignore=(focus_cam_entity,), direction= camera.forward, distance= 1000, debug= True)
    #print(cur_view_info.entity)
    
    focus('sun',cur_et)
    sun_text.world_position=sun.position
    sun_text.world_scale=abs(camera.z)*0.40

    focus('mercury',cur_et)   
    mercury.position=gen_pos(1,cur_et)
    mercury_text.world_position=mercury.position
    mercury_text.world_scale=abs(camera.z)*0.40

    focus('venus',cur_et)   
    venus.position=gen_pos(2,cur_et)
    venus_text.world_position=venus.position
    venus_text.world_scale=abs(camera.z)*0.40

    focus('earth',cur_et)
    earth.position=gen_pos(399,cur_et)
    earth_text.world_position=earth.position
    earth_text.world_scale=abs(camera.z)*0.40
   
    
    focus('moon',cur_et)   
    moon.position=gen_pos(301,cur_et)
    moon_text.world_position=moon.position
    moon_text.world_scale=abs(camera.z)*0.2
    
    focus('mars',cur_et)  
    mars.position=gen_pos(4,cur_et)
    mars_text.world_position=mars.position
    mars_text.world_scale=abs(camera.z)*0.40
    
    focus('jupiter',cur_et)   
    jupiter.position=gen_pos(5,cur_et)
    jupiter_text.world_position=jupiter.position
    jupiter_text.world_scale=abs(camera.z)*0.40
    
    focus('saturn',cur_et)   
    saturn.position=gen_pos(6,cur_et)
    saturn_text.world_position=saturn.position
    saturn_text.world_scale=abs(camera.z)*0.40
    
    focus('uranus',cur_et)   
    uranus.position=gen_pos(7,cur_et)
    uranus_text.world_position=uranus.position
    uranus_text.world_scale=abs(camera.z)*0.40
    
    focus('neptune',cur_et)   
    neptune.position=gen_pos(8,cur_et)
    neptune_text.world_position=neptune.position
    neptune_text.world_scale=abs(camera.z)*0.40

    focus('pluto',cur_et)   
    pluto.position=gen_pos(9,cur_et)
    pluto_text.world_position=pluto.position
    pluto_text.world_scale=abs(camera.z)*0.40
    


    if delay_counter==0:
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
