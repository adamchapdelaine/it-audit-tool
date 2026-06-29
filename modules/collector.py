import datetime
import ipaddress
import platform
import ctypes
import socket
import getpass
import time
import psutil
import wmi
from pythonping import ping

def get_snapshot():
    System_Snapshot = {
        "OS_Version": platform.version(),
        "Build": platform.platform(),
        "System_Uptime": getTime(),
        "Host_Name": socket.gethostname(),
        "Current_User": getpass.getuser(),
        "CPU_Usage": psutil.cpu_percent(interval=1),
        "RAM_Total": psutil.virtual_memory().total / 1073741824,
        "RAM Percent": psutil.virtual_memory().percent,
        "Disk_Usage_Free": psutil.disk_usage('C:').free / 1073741824,
        "Disk_Usage_Used": psutil.disk_usage('C:').used / 1073741824,
        "Local_IP": getIP(),
        "Subnet": str(ipaddress.IPv4Network(f"{getIP()}/{getNetmask()}", strict=False)),
        "DNS": getDNS(),
        "Ping": ping('google.com').rtt_avg_ms,
        "Processes": getProcesses(),
        "AV_Status": getInstalledAntivirus()
    }
    return System_Snapshot
    
def getTime():
    t1 = time.time()
    t2 = psutil.boot_time()
    return t1 - t2

def getIP():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return ip
    except Exception:
        return "Disconnected"

def getDNS():
    dns_info = socket.getaddrinfo('localhost', None) 
    for info in dns_info:
        return (info[4][0])

def getProcesses():
    f = wmi.WMI()
    process_list = []
    for process in f.Win32_Process():
        process_list.append({"pid": process.ProcessID, "name": process.Name})
    return process_list[:5]

def getInstalledAntivirus():
    f = wmi.WMI(namespace=r"root\SecurityCenter2")
    antivirus_list = []
    for av in f.AntiVirusProduct():
        antivirus_list.append(av.displayName)
    return antivirus_list

def getNetmask():
    local_ip = getIP()
    if local_ip == "Disconnected":
        return "255.255.255.255" # Fallback safe mask

    f = wmi.WMI()
    for adapter in f.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if local_ip in adapter.IPAddress:
            return adapter.IPSubnet[0]
