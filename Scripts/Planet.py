from ursina import *
from PIL import Image

PI= 3.14
class Planet:
    def __init__(self) -> None:
        pass
        
        
    class Create_entity :
        def __init__(self,texture_path: str, model: str='sphere', radius: float=3, tilt: float= 0.0 ) :  
            self.obj=Entity(model=model, texture=texture_path)   
            self.pos(0,0,0)
            self.tilt(status=True, val= tilt)
            self.obj.scale=(radius,radius,radius)
            self._auto_rotation=True
            self._tilt=tilt
            self._auto_rotation_text='<yellow>\nAutorotation: {}</yellow>'
        
        def reset_pos_rot(self):
            self.pos(0,0,0)
            self.obj.rotation=Vec3(0,0,0)

        def tilt(self,status: bool= False, val : float= 0):
            self.obj.rotation=Vec3(0,0,0)
            if not(status):
                self.obj.rotation_z=0
            else:
                self.obj.rotation_z=val
                
        def pos(self, x: float, y: float, z: float):
            self.obj.position=Vec3(x,y,z)

        def get_text(self) -> str:
            if self._auto_rotation:
                temp_text=self._auto_rotation_text.format(self._auto_rotation)
            else:
                temp_text=self._auto_rotation_text.format(self._auto_rotation)
            return temp_text
        
        
        def rotation(self,left_to_right_rotation: bool =True, axis : str ='y' , rotation_value: int = 10):
            
            if left_to_right_rotation:
                rotation_value*=-1
            if axis=='z':
                self.obj.rotate(Vec3(0,0,rotation_value))   
            elif axis=='y':
                self.obj.rotate(Vec3(0,rotation_value,0))
        
        def toggle_auto_rotation(self):
            self._auto_rotation=not(self._auto_rotation)

            

if __name__=='__main__':
    app= Ursina()
    planet=Planet()
    jupiter=planet.Create_entity(model='sphere', texture_path=r"..\Assets\jupiter.jpg",radius=3,tilt=45)
    jupiter.pos(0,0,0)
    
    def input(key):
        if key=='r':
            if jupiter.auto_rotation==False:
                #error
                #jupiter.transform = Func(Transform,scale=(2, 2, 2))
                #not error
                jupiter.scale=Vec3(3,3,3)
            jupiter.auto_rotation=not(jupiter.autorotation)
        elif key in ['w','up arrow','a','left arrow','s','down arrow','d','right arrow'] :
            jupiter.auto_rotation=False
            jupiter.rotate_z=0
    def update():
        if not(jupiter._auto_rotation):
           
            y_val_l_r=100*(held_keys['d'] or held_keys['right arrow']) * time.dt
            y_val_r_l=100*(held_keys['a'] or held_keys['left arrow']) * time.dt
            z_val_d_u=100*(held_keys['w'] or held_keys['up arrow']) * time.dt
            z_val_u_d=100*(held_keys['s'] or held_keys['down arrow']) * time.dt
           
            jupiter.rotation(left_to_right_rotation=True,axis='y',rotation_value=y_val_l_r)
            jupiter.rotation(left_to_right_rotation=False,axis='y',rotation_value=y_val_r_l)
            jupiter.rotation(left_to_right_rotation=True,axis='z',rotation_value=z_val_d_u)
            jupiter.rotation(left_to_right_rotation=False,axis='z',rotation_value=z_val_u_d)
            
        else:
            jupiter.rotation(left_to_right_rotation=True,axis='y',rotation_value=1)
            jupiter.pos(0,0,0)
    app.run()
    
