from jinja2 import Environment, FileSystemLoader, select_autoescape


# Load file
file_loader = FileSystemLoader("config")

# Tell Jinja where to look (file path)
env = Environment(loader=file_loader, autoescape=select_autoescape())
# Create manager
template = env.get_template("report_template.html")

# mock variable
# Simulated output from your health.py analyzer
mock_audit_results = [
    {
        "hostname": "DESKTOP-IT-01",
        "ip_address": "192.168.1.50",
        "status": "Warning",
        "findings": [
            {"metric": "Disk Usage", "value": "92%", "status": "Warning"},
            {"metric": "RAM Usage", "value": "45%", "status": "Pass"},
            {"metric": "Windows Update Service", "value": "Stopped", "status": "Critical"}
        ]
    },
    {
        "hostname": "SERVER-PROD-01",
        "ip_address": "10.0.0.10",
        "status": "Pass",
        "findings": [
            {"metric": "Disk Usage", "value": "34%", "status": "Pass"},
            {"metric": "RAM Usage", "value": "12%", "status": "Pass"},
            {"metric": "Windows Update Service", "value": "Running", "status": "Pass"}
        ]
    }
]

# Pass data and extract string
html_output = template.render(reports=mock_audit_results)

