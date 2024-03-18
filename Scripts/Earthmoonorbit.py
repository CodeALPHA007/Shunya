import math
import numpy as np
from ursina.prefabs.trail_renderer import TrailRenderer
from ursina import *

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

print(MOON_MOMENTUM)
cam = False

def unit_vector(vector):
    """ Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)

def magnitude(vector):
    return np.linalg.norm(vector)


app = Ursina()
window.color = color.black

""" def cameraSetup():
    global cam
    camera.position = Vec3(0, 0, -4000)
    cam = True """

camera.position = (0, 0, -10000)

def cameraControl():
    camera.z += 10000*held_keys['w'] * time.dt
    camera.z -= 10000*held_keys['s'] * time.dt
    camera.x += 1000 *held_keys['d'] * time.dt
    camera.x -= 1000 *held_keys['a'] * time.dt
    camera.y += 1000 *held_keys['z'] * time.dt
    camera.y -= 1000 *held_keys['x'] * time.dt
    


camera.clip_plane_far_setter(40000)

earth = Entity(model='sphere', texture='earth.jpg', scale=RADIUS_EARTH)
moon = Entity(model='sphere', texture='moon.jpg', scale=RADIUS_MOON)
moon.position = Vec3(RADIUS_EARTH_MOON, 0, 0)
#moon_trail = TrailRenderer(parent = moon, )
""" trail_renderers = []
for i in range(1):
    tr = TrailRenderer(size=[1,1], segments=8, min_spacing=0.5, fade_speed=0, parent=moon, color_gradient=[color.magenta, color.cyan.tint(-.5), color.clear])
    trail_renderers.append(tr) """
t = 0
dt = 500
""" r = moon.position - earth.position
print(unit_vector(r))
print(magnitude(r)) """

print(orbitalVelocity)


def update():

    global t, MOON_MOMENTUM, EARTH_MOMENTUM
    #if cam == False:
       #cameraSetup()
    #cameraSetup()
    cameraControl()
    #print(camera.position)

    r = moon.position - earth.position
    F = -G_MODIFIED*MASS_EARTH*MASS_MOON*unit_vector(r)/magnitude(r)**2
    MOON_MOMENTUM = MOON_MOMENTUM + F*dt
    EARTH_MOMENTUM = EARTH_MOMENTUM - F*dt
    moon.position = moon.position + MOON_MOMENTUM*dt/MASS_MOON
    earth.position = earth.position + EARTH_MOMENTUM*dt/MASS_EARTH
    t = t + dt
    #print(moon.position)
    #print(MOON_MOMENTUM)
    print(earth.position)

app.run()
