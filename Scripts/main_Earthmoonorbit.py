import math
import numpy as np
from ursina.prefabs.trail_renderer import TrailRenderer
from ursina import *

from collections import deque

import Planet
import Camera

focus=False
focus_text="Focus {}"

relativeMultiplier = 0.00001
G = 6.67e-11
G_MODIFIED = 6.67e-21
MASS_EARTH = 5.972e24*relativeMultiplier
RADIUS_EARTH = 6.378e6*relativeMultiplier
RADIUS_EARTH_MOON = 384.4e6*relativeMultiplier
RADIUS_MOON = 1.737e6*relativeMultiplier
MASS_MOON = 7.348e22*relativeMultiplier
SIDEREAL_TIME_PERIOD = 27.321*24*3600
RADIUS_EARTH_MOON_MAX = 405.4e6*relativeMultiplier
MEAN_INCLINATION_TO_ECLIPTIC_PLANE = 5.145

orbitalVelocity = 2*math.pi*RADIUS_EARTH_MOON/SIDEREAL_TIME_PERIOD
MOON_MOMENTUM = MASS_MOON*Vec3(0, orbitalVelocity, 0)
EARTH_MOMENTUM = -MOON_MOMENTUM #MASS_EARTH*Vec3(0, 0, 0)

#print(MOON_MOMENTUM)
cam = False

def unit_vector(vector):
    """ Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)

def magnitude(vector):
    return np.linalg.norm(vector)



""" def cameraSetup():
    global cam
    camera.position = Vec3(0, 0, -4000)
    cam = True """

max_zoom=-30000
min_zoom=-350

def cameraControl():
    camera.z = min(min_zoom,camera.z+10000*held_keys['w'] * time.dt)
    camera.z = max(max_zoom,camera.z-10000*held_keys['s'] * time.dt)

    camera.x += 1000 *held_keys['d'] * time.dt
    camera.x -= 1000 *held_keys['a'] * time.dt
    camera.y += 1000 *held_keys['z'] * time.dt
    camera.y -= 1000 *held_keys['x'] * time.dt
    





trail = deque([], maxlen=2000)
#trail = deque([])
curve_renderer=Entity()

t = 0
dt = 500
""" r = moon.position - earth.position
print(unit_vector(r))
print(magnitude(r)) """

class Focus:
    def __init__(self,myplanet: Planet.Planet.Create_entity,mytilt: int,mycam: Camera.MyCamera):
        self.my_tilt=mytilt
        #jupiter=planet.Create_entity(model='sphere', texture_path=r"..\Assets\jupiter.jpg",radius=3,tilt=my_tilt)
        self.myplanet=myplanet
        self.mycam=mycam
        self.display_text='<white>NERD STATS</white>'
        self.free_mode_text='<blue>\nFree mode: {}</blue>'
        
        self.free_mode=False
        self.entities=[]
        
#DirectionalLight(y=2, z=3, shadows=True, rotation=(45, -45, 45))
    def call(self):
        self.txt = Text(scale=1,position=(-0.85,0.45,0))
        self.button = Button(position=(0,-0.45,0), text='Toggle Free Mode',color='white')
        self.button.text_color=color.red
        self.button.fit_to_text(radius=0)
        self.button.on_click=self.toggle_free_mode
        self.entities.extend([self.button,self.txt])

    def toggle_free_mode(self):
        
        self.free_mode=not(self.free_mode)
        if self.free_mode:
            #self.myplanet.tilt(status=False)
            if self.myplanet._auto_rotation:
                self.myplanet.toggle_auto_rotation()
        else:
            #self.mycam.reset_cam_var(reset_zoom=True)
            #self.myplanet.reset_pos_rot()
            #self.myplanet.tilt(status=True, val=self.my_tilt)
            if not(self.myplanet._auto_rotation):
                self.myplanet.toggle_auto_rotation()


app = Ursina()
window.color = color.black


mycam=Camera.MyCamera(-10000)
mycam.camera.position=Vec3(0, 0, -10000)
mycam.camera.clip_plane_far_setter(40000)

my_tilt_earth=23.44
my_tilt_moon=-24
earth=Planet.Planet.Create_entity(model='sphere', texture_path=r"..\Assets\earth4k.jpg",radius=RADIUS_EARTH,tilt=my_tilt_earth)    
moon=Planet.Planet.Create_entity(model='sphere', texture_path=r"..\Assets\ma.png",radius=RADIUS_MOON,tilt=my_tilt_moon)
moon.obj.position = Vec3(RADIUS_EARTH_MOON, 0, 0)

myplanet_focus=Focus(earth,my_tilt_earth,mycam)

def toggle_focus():
    global focus,mycam,myplanet_focus,earth,my_tilt_earth
    if focus:
        [destroy(i) for i in myplanet_focus.entities]
        mycam=Camera.MyCamera(-10000)
        mycam.camera.position=Vec3(0, 0, -10000)
        mycam.camera.clip_plane_far_setter(40000)

    else:
        mycam=Camera.MyCamera(-300)
        mycam.camera.position=Vec3(0, 0, -3000)
        mycam.camera.clip_plane_far_setter(40000)
        myplanet_focus=Focus(earth,my_tilt_earth,mycam)
        myplanet_focus.call()
    focus=not(focus)

focus_button=Button(text=focus_text.format(focus),color=color.red,text_color=color.white)
focus_button.fit_to_text()
focus_button.position=Vec3(-0.45,-0.45,0)
focus_button.on_click=toggle_focus    

def input(key):
    global focus
    if focus:    
        if key=='r' and not(myplanet_focus.free_mode):
            myplanet_focus.myplanet.toggle_auto_rotation()
        elif key=='f' and myplanet_focus.free_mode:
            myplanet_focus.mycam.toggle_free_rotation()
            if myplanet_focus.myplanet._auto_rotation:
                myplanet_focus.myplanet.toggle_auto_rotation()
        

def update():
    global focus
    focus_button.text=focus_text.format(focus)
    if focus:
        myplanet_focus.txt.text=myplanet_focus.display_text+myplanet_focus.free_mode_text.format(myplanet_focus.free_mode)+myplanet_focus.myplanet.get_text()+myplanet_focus.mycam.get_text()

        if myplanet_focus.myplanet._auto_rotation:
            myplanet_focus.myplanet.rotation(left_to_right_rotation=True,axis='y',rotation_value=1)
        
        if myplanet_focus.free_mode:
            myplanet_focus.mycam.linear_zoom_in(100 *held_keys['up arrow'] * time.dt,status=True)   
            myplanet_focus.mycam.linear_zoom_in(100 *held_keys['down arrow'] * time.dt,status=False)
            myplanet_focus.mycam.linear_mov_left(100 *held_keys['left arrow'] * time.dt,status=True)
            myplanet_focus.mycam.linear_mov_left(100 *held_keys['right arrow'] * time.dt,status=False)
            myplanet_focus.mycam.rotate_camera(100*held_keys['w'] * time.dt,direction='up')
            myplanet_focus.mycam.rotate_camera(100*held_keys['s'] * time.dt,direction='down')
            myplanet_focus.mycam.rotate_camera(100*held_keys['a'] * time.dt,direction='left')
            myplanet_focus.mycam.rotate_camera(100*held_keys['d'] * time.dt,direction='right')
    if not(focus):
        global t, MOON_MOMENTUM, EARTH_MOMENTUM,curve_renderer,trail
        #if cam == False:
        #cameraSetup()
        #cameraSetup()
        cameraControl()
        #print(camera.position)

        r = moon.obj.position - earth.obj.position
        F = -G_MODIFIED*MASS_EARTH*MASS_MOON*unit_vector(r)/magnitude(r)**2
        MOON_MOMENTUM = MOON_MOMENTUM + F*dt
        EARTH_MOMENTUM = EARTH_MOMENTUM - F*dt
        moon.obj.position = moon.obj.position + MOON_MOMENTUM*dt/MASS_MOON
        earth.obj.position = earth.obj.position + EARTH_MOMENTUM*dt/MASS_EARTH
        t = t + dt

        
        trail.append(moon.obj.position)
        destroy(curve_renderer)
        try:
            curve_renderer = Entity(model=Mesh(vertices=trail, mode='line'),color=color.violet )
        except:
            pass
        #print(moon.position)
        #print(MOON_MOMENTUM)
        #print(earth.obj.position)

app.run()