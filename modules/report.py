from email.message import EmailMessage
import smtplib
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

def generate_email_report(audit_data):
    return template.render(reports=audit_data)

def send_email_report(html_content, recipient_email):
    msg = EmailMessage()
    
    # replace these later with smtp_config dict parameters
    msg['Subject'] = "IT Audit Report"
    msg['From'] = "send@yourcompany.local"
    msg['To'] = recipient_email

    # add HTML content
    msg.set_content("Placeholder.")
    msg.add_alternative(html_content, subtype="html")
    
    # connect to server
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)