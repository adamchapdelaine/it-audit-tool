import argparse
from modules import collector
from modules import health
from modules import report

if __name__ == "__main__":

    # argument parser setup
    parser = argparse.ArgumentParser(description="IT Audit Report CLI Tool")
   
    parser.add_argument("--local", action="store_true", help="Print the report directly to the console")
    parser.add_argument("--email", type=str, help="Email the report to the specified address")
    
    args = parser.parse_args()

    # gathering data
    raw_data = collector.get_snapshot()
    findings_list = health.check_host_health(raw_data)

    audit_results = [
        {
            "hostname": "LOCAL-HOST",
            "ip_address": "127.0.0.1",
            "findings": findings_list
        }
    ]

    if args.local:
        print("\n=== LOCAL IT AUDIT REPORT ===")
        for host in audit_results:
            print(f"\nHost: {host['hostname']} ({host['ip_address']})")
            print("-" * 40)
            # Loop through your live large findings list and print each line cleanly
            for finding in host['findings']:
                # Adjust these keys if your health.py list uses different names!
                print(f"- {finding['metric']}: {finding['status']} ({finding['value']})")
        print("=============================\n")
    
    elif args.email:
        print(f"Compiling and sending report to {args.email}...")
        html_content = report.generate_email_report(audit_results)
        report.send_email_report(html_content, args.email)
        print("Email dispatched successfully!") 

    else: 
        print("No output flag specified. Use --local to view here, or --email <address> to send.")
