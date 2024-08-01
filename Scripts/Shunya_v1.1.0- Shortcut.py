import os
import time
os.system(r'start "" /d "%cd%\dist\Shunya_v1.1.0"  "%cd%\dist\Shunya_v1.1.0\Shunya_v1.1.0.exe"')
print("...............*_*    LAUNCHING SHUNYA    *_*...............")
print()
print("...............*_*      PLEASE WAIT       *_*...............")
print()
print()
for i in range(1000,-1,-1):
    i=str(i)
    i='0'*(4-len(i))+i
    print('LIFT OFF in --> {} : {} '.format(i[:2],i[2:]),end="\r")
    time.sleep(0.01)
print()
print()    
print("SHUNYA is now ONLINE.......")    
print()
os.system(r'pause')    
os.system('EXIT')


