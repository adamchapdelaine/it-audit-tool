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
        "critical_running": ["Print Spooler", "LanmanServer", "Dhcp"]
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


    for service in services_data:

        name = service["name"]
        status = service["status"]

        if name in critical_services:

            if status != "Running":
                service_findings.append({"metric": f"Service: {name}", "value": status, "status": "CRITICAL"})
            else:
                service_findings.append({"metric": f"Service: {name}", "value": status, "status": "OK"})
    
    return service_findings

def check_host_health(raw_collector_data):

    cpu_finding = evaluate_cpu(raw_collector_data["cpu"])

    disk_finding = evaluate_disk(raw_collector_data["disk"])

    ram_finding = evaluate_ram(raw_collector_data["ram"])

    services_finding = evaluate_services(raw_collector_data["services"])

    master_list = [cpu_finding, disk_finding, ram_finding]

    for item in services_finding:
        master_list.append(item)
    return master_list