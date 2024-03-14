from ursina import *
from PIL import Image

PI= 3.14
class Planet:
    def __init__(self) -> None:
        pass
        
        
    class Create_entity :
        def __init__(self, model: str, texture_path: str,radius: float, tilt: float= 0.0 ) :
            self.obj=Entity(model='sphere', texture=texture_path)   
            self.obj.rotation_z+=tilt
            self.obj.scale=(radius,radius,radius)
            self.autorotation=True

        def pos(self, x: float, y: float, z: float):
            self.obj.position=Vec3(x,y,z)

        def rotation(self,left_to_right_rotation: bool =True, axis : str ='y' , rotation_value: int = 10):
            absolute_rotation_value=abs(rotation_value)
            if left_to_right_rotation:
                rotation_value*=-1
            if axis=='z':
                self.obj.rotate(Vec3(0,0,rotation_value))   
            elif axis=='y':
                self.obj.rotate(Vec3(0,rotation_value,0))


if __name__=='__main__':
    app= Ursina()
    planet=Planet()
    jupiter=planet.Create_entity(model='sphere', texture_path=r"..\Assets\jupiter.jpg",radius=3,tilt=45)
    jupiter.pos(0,0,0)
    
    def input(key):
        if key=='r':
            jupiter.autorotation=not(jupiter.autorotation)
        elif key in ['w','up arrow','a','left arrow','s','down arrow','d','right arrow'] :
            jupiter.autorotation=False
         
    def update():
        if not(jupiter.autorotation):
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

    app.run()
    
