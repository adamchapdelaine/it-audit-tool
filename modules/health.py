DEFAULT_THRESHOLDS = {
    "disk": {
        "warning_percent_free": 20,
        "critical_percent_free": 10
    },
    "cpu": {
        "critical_percent": 90
    },
    "ram": {
        "critical_percent": 85
    },
    "services": {
        "critical_running": ["Dhcp", "Dnscache", "LanmanServer", "wuauserv", "Winmgmt"]
    }
}

def evaluate_cpu(cpu_data):

    limit = DEFAULT_THRESHOLDS["cpu"]["critical_percent"]

    if cpu_data > limit:
        return {"metric": "CPU Usage", "value": cpu_data, "status": "CRITICAL"}
    else:
        return {"metric": "CPU Usage", "value": cpu_data, "status": "OK"}

def evaluate_disk(disk_data):
    current_free = disk_data["free"]

    critical_limit = DEFAULT_THRESHOLDS["disk"]["critical_percent_free"]
    warning_limit = DEFAULT_THRESHOLDS["disk"]["warning_percent_free"]
    
    if current_free < critical_limit:
        return {"metric": "Disk Free", "value": current_free, "status": "CRITICAL"}

    elif current_free < warning_limit:
        return {"metric": "Disk Free", "value": current_free, "status": "WARNING"}

    else:
        return {"metric": "Disk Free", "value": current_free, "status": "OK"}

def evaluate_ram(ram_data):

    limit = DEFAULT_THRESHOLDS["ram"]["critical_percent"]

    if ram_data > limit:
        return {"metric": "RAM Usage", "value": ram_data, "status": "CRITICAL"}
    else:
        return {"metric": "RAM Usage", "value": ram_data, "status": "OK"}

def evaluate_services(services_data):
    service_findings = []
    critical_services = DEFAULT_THRESHOLDS["services"]["critical_running"]

    service_map = {svc["name"]: svc.get("status", "Stopped").title() for svc in services_data}

    for service_name in critical_services:
        current_status = service_map.get(service_name, "Stopped")

        if current_status == "Running":
            service_findings.append({
                "metric": f"Service: {service_name}",
                "value": "Running",
                "status": "OK"
            })
        else:
            service_findings.append({
                "metric": f"Service: {service_name}",
                "value": current_status,
                "status": "CRITICAL"
            })

    return service_findings

def evaluate_antivirus(av_data):
    if not av_data:
        return {"metric": "Antivirus Status", "value": "Missing / None", "status": "CRITICAL"}

    unique_avs = list(set([str(av) for av in av_data if av]))

    av_string = ", ".join(unique_avs)

    if len(unique_avs) > 0:
        return {"metric": "Antivirus Status", "value": av_string, "status": "OK"}
    else:
        return {"metric": "Antivirus Status", "value": "Disabled", "status": "CRITICAL"}

def check_host_health(raw_collector_data):

    disk_used = raw_collector_data.get("Disk_Usage_Used", 0)
    disk_free = raw_collector_data.get("Disk_Usage_Free", 0)
    total_disk = disk_used + disk_free

    if total_disk > 0:
        free_percent = (disk_free / total_disk) * 100
    else:
        free_percent = 0

    processed_disk_data = {"free": round(free_percent, 1)}
    ram_percent = raw_collector_data.get("RAM Percent", 0)

    cpu_finding = evaluate_cpu(raw_collector_data["CPU_Usage"])
    disk_finding = evaluate_disk(processed_disk_data)
    ram_finding = evaluate_ram(ram_percent)

    services_finding = evaluate_services(raw_collector_data.get("Processes", []))

    av_finding = evaluate_antivirus(raw_collector_data.get("AV_Status", []))

    master_list = [cpu_finding, disk_finding, ram_finding, av_finding]

    for item in services_finding:
        master_list.append(item)

    return master_list