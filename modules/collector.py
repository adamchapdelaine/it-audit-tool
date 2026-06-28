import datetime
import platform
import ctypes
import socket
import getpass
import time
import psutil

def get_snapshot():
    System_Snapshot = {
        "OS_Version": platform.version(),
        "System_Uptime": str(getTime()),
        "Host_Name": socket.gethostname(),
        "Current_User": getpass.getuser(),
        "CPU_Usage": f"{psutil.cpu_percent(interval=1)}%",
        "RAM_Usage": f"{psutil.virtual_memory().total / 1073741824:.2f} GB Total, {psutil.virtual_memory().percent}% Utilized",
        "Disk_Usage": f"{psutil.disk_usage('C:').free / 1073741824:.2f} GB Free, {psutil.disk_usage('C:').used / 1073741824:.2f} GB Used",
    }
    print(System_Snapshot)

def getTime():
    t1 = datetime.datetime.fromtimestamp(time.time())
    t2 = datetime.datetime.fromtimestamp(psutil.boot_time())
    return t1 - t2

    
get_snapshot()