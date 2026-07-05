# IT Audit & Host Health Tool

A lightweight, modular Python utility designed for IT administrators to audit local Windows hosts. The tool collects vital system metrics (CPU, RAM, Disk), evaluates background service compliance via WMI, verifies active antivirus installations, and outputs a clean console summary or emails a formatted HTML report to an administrator.

## Features

- **System Metrics:** Checks real-time CPU usage, RAM utilization, and dynamically calculates free storage percentage.
- **Service Compliance Monitoring:** Queries the Windows Service Control Manager via WMI to ensure critical infrastructure services (such as DHCP and Windows Update) are running.
- **Endpoint Security Audit:** Checks and filters active Antivirus provider registrations to ensure endpoint compliance.
- **Dual Reporting Engines:** Outputs a scannable summary directly to the terminal or compiles a styled HTML report sent via local SMTP network channels.

---

## Architecture

The project follows a modular pipeline separation of concerns:

- `collector.py`: Interfaces directly with the Windows OS via WMI to pull raw hardware and security snapshots.
- `health.py`: Validates the raw snapshot data against configurable operations thresholds and assigns statuses (`OK`, `WARNING`, `CRITICAL`).
- `report.py`: Handles the presentation layer, formatting metrics and compiling the dynamic HTML templates.
- `main.py`: Coordinates the runtime pipeline execution and provides the CLI argument parsing interface.

---

## Installation & Setup

### Prerequisites
- Windows 10 / 11
- Python 3.10 or higher
- Administrator Privileges (required to query some high-privilege system services)

### Dependencies
Install the required packages using pip:

```bash
pip install pywin32 wmi psutil pythonping jinja2