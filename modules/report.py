from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Load file
file_loader = FileSystemLoader("config")

# Tell Jinja where to look (file path)
env = Environment(loader=file_loader, autoescape=select_autoescape())
# Create manager
template = env.get_template("report_template.html")

def generate_email_report(audit_data):
    return template.render(reports=audit_data)

def send_email_report(html_content, recipient_email):
    msg = EmailMessage()
    
    # Replace these later with smtp_config dict parameters
    msg['Subject'] = "IT Audit Report"
    msg['From'] = "send@yourcompany.local"
    msg['To'] = recipient_email

    # Add HTML content
    msg.set_content("Placeholder.")
    msg.add_alternative(html_content, subtype="html")
    
    # Connect to server
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)