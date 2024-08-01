import requests

try:
    cur_version_req=requests.get(r"https://shunyathespaceapp.onrender.com/public/version.txt",timeout=40)
    cur_version_req.encoding="utf-8"
    cur_version=(cur_version_req.text).split(':')[1].strip()
    print(cur_version)
    with open(r"version.txt",'+w') as version:
        avl_version=version.read().strip()
        if avl_version!=cur_version:
         version.write(cur_version)
except:
    try:
        version.close()
    except:
       pass    
    SystemExit