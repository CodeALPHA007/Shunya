from ursina import *
import math

app = Ursina()
e1 = Entity(model='sphere', texture='..\Assets\jupiter.jpg', scale=(3, 3, 3))
zoom=-20
left_right=0
cam_x,cam_y,cam_z=0,0,zoom
angle_hor,angle_ver=0,0
free_rotation=True
camera.position=Vec3(left_right,0,zoom)

def reset_view():
    global zoom
    camera.position=Vec3(0,0,zoom)

def input(key):
    global free_rotation
    if key=='f':
        free_rotation=not(free_rotation)
        reset_view()

def update():
    #zoom

    global zoom,left_right,cam_x,cam_z,angle_hor,angle_ver
    zoom +=10 *held_keys['up arrow'] * time.dt
    zoom -= 10 *held_keys['down arrow'] * time.dt
    camera.position = Vec3(left_right,0,zoom) 

    #movement left and right
    left_right +=10 *held_keys['left arrow'] * time.dt
    left_right -= 10 *held_keys['right arrow'] * time.dt
    camera.position = Vec3(left_right,0,zoom) 
    
    
    #camera rotation
    if not(free_rotation):
        print(cam_x,cam_z,angle_hor,angle_ver)
        angle_hor+=10*held_keys['d'] * time.dt
        angle_hor-=10*held_keys['a'] * time.dt
        angle_ver+=10*held_keys['w'] * time.dt
        angle_ver-=10*held_keys['s'] * time.dt
        
        #angle%=360
        
        cam_x=zoom*math.sin(math.radians(angle_hor))
        cam_z=zoom*math.cos(math.radians(angle_hor))
        
        camera.position=Vec3(cam_x,0,cam_z)
        camera.rotation=Vec3(0,angle_hor,0)
        
app.run()