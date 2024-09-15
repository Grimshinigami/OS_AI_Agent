import os
# import subprocess
# Start Notepad
# try:
# subprocess.Popen(['Windows Explorer.exe'])
#     print("App opened successfully")
# except:
#     print("Couldn't open this app with subprocess")

applist = {
    0:'Chrome.exe',
    1:'Spotify.exe',
    2:'Explorer.exe',
    3:'calc.exe',
    4:'taskmgr.exe',
    5:'notepad.exe'
}

def launch_app(launch_index):
    try:
        os.startfile(applist[launch_index])
    # os.startfile('D:/Softwares/Open HW Monitor/openhardwaremonitor-v0.9.6/OpenHardwareMonitor/OpenHardwareMonitor.exe')
        print("App opened successfully")
    except:
        print("Couldn't open this app")

launch_app(3)