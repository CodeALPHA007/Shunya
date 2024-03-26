from ursina import *
import Camera

app = Ursina()

#free camera buttons
zoom_in = Button(parent=camera.ui, name = 'zoom in', icon='..\Assets\zoom_in.png', scale=.05, origin=(-14.5,8))
zoom_in.tooltip = Tooltip('Zoom In')

zoom_out = Button(icon='..\Assets\zoom_out.png', scale=.05, name = 'zoom out', radius= 0.1, origin=(-16,8))
zoom_out.tooltip = Tooltip('Zoom Out')

move_left = Button(icon='..\Assets\left.png', scale=.05, name = 'move left', radius= 0.1, origin=(-14.25,3.5), text= 'entity\'s movement', text_origin=(-0.25,1.5))
move_left.tooltip = Tooltip('To Left')

move_right = Button(icon='..\Assets\\right.png', scale=.05, name = 'move right', radius= 0.1, origin=(-15.75,3.5))
move_right.tooltip = Tooltip('To Right')

#focused camera buttons
cam_up = Button(parent=camera.ui, name = 'camera up', icon='..\Assets\\up.png' ,scale=.05, origin=(16.5,6), text='camera movements', text_origin=(-0.33,1.75))
cam_up.tooltip = Tooltip('Rolls up')

cam_down = Button(icon='..\Assets\down.png', scale=.05, name = 'camera down', radius= 0.1, origin=(15,6))
cam_down.tooltip = Tooltip('Rolls down')

cam_left = Button(icon='..\Assets\left.png', scale=.05, name = 'camera left', radius= 0.1, origin=(16.5,7.5))
cam_left.tooltip = Tooltip('Rolls left')

cam_right = Button(icon='..\Assets\\right.png', scale=.05, name = 'camera right', radius= 0.1, origin=(15,7.5))
cam_right.tooltip = Tooltip('Rolls right')

#entity
entity= Entity(model='sphere', scale=(3, 3, 3),  texture='..\Assets\jupiter.png')

toggle = Button(parent=camera.ui, scale=.1, origin=(-7.5,2.75), icon = '..\Assets\Switch.png', text='zooming options', text_origin=(-0.2,-1))
toggle.tooltip = Tooltip('For free camera')

mycam = Camera.MyCamera(initial_zoom=-20)
display_text=mycam.get_text()
txt = Text(text=display_text,scale=1,position=(-0.85,0.45,0))
mycam.reset_cam_var()

def input(key):
        if key == 'left mouse down':
            toggle.on_click = mycam.toggle_free_rotation
        elif key == 'scroll up':
               mycam.linear_zoom_in(10* time.dt,status=True)
        elif key == 'scroll down':
               mycam.linear_zoom_in(10 * time.dt,status=False)

def update():
        txt.text=mycam.get_text()
        #Rotation of Entity
        try:
            if mouse.collision.entity.name == 'zoom in':
                zoom_in.on_click =  mycam.linear_zoom_in(10* held_keys['left mouse'] *time.dt, True)
        except:
              pass
        try:
            if mouse.collision.entity.name == 'zoom out':
                zoom_out.on_click =  mycam.linear_zoom_in(10* held_keys['left mouse'] *time.dt, False)
        except:
              pass
        try:
            if mouse.collision.entity.name == 'move left':
                move_left.on_click =  mycam.linear_mov_left(10 *held_keys['left mouse'] * time.dt,status=True)
        except:
              pass
        try:
            if mouse.collision.entity.name == 'move right':
                move_right.on_click =  mycam.linear_mov_left(10 *held_keys['left mouse'] * time.dt,status=False)
        except:
              pass
        #Rotation of camera
        try:
            if mouse.collision.entity.name == 'camera up':
                cam_up.on_click =  mycam.rotate_camera(10*held_keys['left mouse'] * time.dt,direction='up')
        except:
              pass
        try:
            if mouse.collision.entity.name == 'camera down':
                cam_down.on_click =  mycam.rotate_camera(10*held_keys['left mouse'] * time.dt,direction='down')
        except:
              pass
        try:
            if mouse.collision.entity.name == 'camera left':
                cam_left.on_click =  mycam.rotate_camera(10*held_keys['left mouse'] * time.dt,direction='left')
        except:
              pass
        try:
            if mouse.collision.entity.name == 'camera right':
                cam_right.on_click =  mycam.rotate_camera(10*held_keys['left mouse'] * time.dt,direction='right')
        except:
              pass


app.run()    