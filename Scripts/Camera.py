import math
import ursina
class MyCamera:
    def __init__(self,initial_zoom: float,fov: float = 50):
        self.initial_zoom=initial_zoom
        self.camera=ursina.camera
        self.fov=fov
        self.camera.fov=self.fov
        self._free_rotation=False
        self._zoom=self.initial_zoom    
        self.reset_cam_var()

    def reset_cam_var(self,reset_zoom: bool =False):
        if reset_zoom:
            self._zoom=self.initial_zoom
        self._left_right=0
        self._cam_x=0
        self._cam_y=0
        self._cam_z=self._zoom
        self._text_linear='<green>\nFree Rotation: {}\nLeft_Right: {}\nZoom: {}<\green>'
        self._text_rotation='<red>\nFree Rotation: {}\ncam_x: {}\ncam_y: {}\ncam_z: {}\nangle_hor: {}\nangle_ver: {}\n</red>'
        self._angle_hor=0
        self._angle_ver=0
        self.camera.rotation=(0,0,0)
        self.camera.position=(0,0,self._zoom)
        
    def toggle_free_rotation(self):  #status None is used to toogle the free rotation
        self._free_rotation=not(self._free_rotation)
        self.reset_cam_var(reset_zoom=False)
        
    
    def linear_zoom_in(self,val: float = 1.0,status: bool= True):
        '''status = True for zoom in
           \nstatus = False for zoom out 
        '''
        if self._free_rotation:
            if status:
                self._zoom+=val
            else:
                self._zoom-=val
            self.camera.position=(self._left_right,0,self._zoom)
        #else:
        #    print("PRESS f TO START FREE ROTATION FIRST and then TRY AGAIN..........")            

    def linear_mov_left(self,val: float = 1.0,status: bool= True):
        '''status = True for left movement
           \nstatus = False for right movement
        '''
        if self._free_rotation:
            if status:
                self._left_right+=val
            else:
                self._left_right-=val
            self.camera.position=(self._left_right,0,self._zoom)
        #else:
        #    print("PRESS f TO START FREE ROTATION FIRST and then TRY AGAIN........")            
    
    def rotate_camera(self, val: float=1.0, direction: str='up'):
        ''''up' for moving the camera up 
        \n'down' for moving the camera down
        \n'left' for mocing the camera left
        \n'right' for moving the camera right

        '''
        direction=direction.lower()
        if not(self._free_rotation):
            if direction in ['up','down','left','right']:
                if direction=='up':
                    self._angle_ver+=val
                elif direction=='down': 
                    self._angle_ver-=val
                elif direction=='left':
                    self._angle_hor-=val
                elif direction=='right': 
                    self._angle_hor+=val

                self._cam_x= self._zoom * math.sin(math.radians(self._angle_hor)) * math.cos(math.radians(self._angle_ver))
                self._cam_y= self._zoom * math.sin(math.radians(self._angle_ver))    
                self._cam_z= self._zoom * math.cos(math.radians(self._angle_hor)) * math.cos(math.radians(self._angle_ver))        

                self.camera.position=(self._cam_x,self._cam_y,self._cam_z)
                self.camera.rotation=(self._angle_ver*-1,self._angle_hor,0)
            else:
                print('Invalid Direction given.........')
        #else:
        #    print("PRESS f TO END FREE ROTATION FIRST and then TRY AGAIN.......")            
        
    def get_text(self) -> str:
        if self._free_rotation:
            temp_text=self._text_linear.format(self._free_rotation,self._left_right,self._zoom)
        else:
            temp_text=self._text_rotation.format(self._free_rotation,self._cam_x,self._cam_y,self._cam_z,self._angle_hor,self._angle_ver)
        return temp_text
    
if __name__=='__main__':
    from ursina import *

    app = Ursina()

    jupiter= Entity(model='sphere', texture='..\Assets\jupiter.jpg', scale=(3, 3, 3))
    mycam=MyCamera(initial_zoom=-20)
    display_text=mycam.get_text()
    txt = Text(text=display_text,scale=1,position=(-0.85,0.45,0))
    
    def input(key):
        if key=='f':
            mycam.toggle_free_rotation()

    def update():
        txt.text=mycam.get_text()
        mycam.linear_zoom_in(10 *held_keys['up arrow'] * time.dt,status=True)   
        mycam.linear_zoom_in(10 *held_keys['down arrow'] * time.dt,status=False)
        mycam.linear_mov_left(10 *held_keys['left arrow'] * time.dt,status=True)
        mycam.linear_mov_left(10 *held_keys['right arrow'] * time.dt,status=False)
        mycam.rotate_camera(10*held_keys['w'] * time.dt,direction='up')
        mycam.rotate_camera(10*held_keys['s'] * time.dt,direction='down')
        mycam.rotate_camera(10*held_keys['a'] * time.dt,direction='left')
        mycam.rotate_camera(10*held_keys['d'] * time.dt,direction='right')

    app.run()    