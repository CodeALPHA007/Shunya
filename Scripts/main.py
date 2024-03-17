from ursina import *
import Planet
import Camera

free_mode=False


app=Ursina()

planet=Planet.Planet()
my_tilt=45
jupiter=planet.Create_entity(model='sphere', texture_path=r"..\Assets\jupiter.jpg",radius=3,tilt=my_tilt)
mycam=Camera.MyCamera(initial_zoom=-20)
mycam.fov=30

display_text='<white>NERD STATS</white>'
free_mode_text='<blue>\nFree mode: {}</blue>'
txt = Text(scale=1,position=(-0.85,0.45,0))

def toggle_free_mode():
    global free_mode,my_tilt
    jupiter.toggle_auto_rotation()
    free_mode=not(free_mode)
    if free_mode:
        jupiter.tilt(status=False)
    else:
        mycam.reset_cam_var(reset_zoom=True)
        jupiter.reset_pos_rot()
        jupiter.tilt(status=True, val=my_tilt)
        


    
button = Button(position=(0,-0.45,0), text='button_text')
button.fit_to_text(radius=0)
#button.on_click = toggle_free_mode
button.on_click=toggle_free_mode
    
def input(key):    
    if key=='r' and not(free_mode):
        jupiter.toggle_auto_rotation()
    elif key=='f' and free_mode:
        mycam.toggle_free_rotation()
        if jupiter._auto_rotation:
            jupiter.toggle_auto_rotation()
    
def update():
    global free_mode
    txt.text=display_text+free_mode_text.format(free_mode)+jupiter.get_text()+mycam.get_text()

    
    if jupiter._auto_rotation:
        jupiter.rotation(left_to_right_rotation=True,axis='y',rotation_value=1)
    
    if free_mode:
        mycam.linear_zoom_in(10 *held_keys['up arrow'] * time.dt,status=True)   
        mycam.linear_zoom_in(10 *held_keys['down arrow'] * time.dt,status=False)
        mycam.linear_mov_left(10 *held_keys['left arrow'] * time.dt,status=True)
        mycam.linear_mov_left(10 *held_keys['right arrow'] * time.dt,status=False)
        mycam.rotate_camera(10*held_keys['w'] * time.dt,direction='up')
        mycam.rotate_camera(10*held_keys['s'] * time.dt,direction='down')
        mycam.rotate_camera(10*held_keys['a'] * time.dt,direction='left')
        mycam.rotate_camera(10*held_keys['d'] * time.dt,direction='right')
app.run()