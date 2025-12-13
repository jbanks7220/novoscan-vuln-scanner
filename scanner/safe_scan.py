from scanner.port_scanner import scan_ports, detect_services
from scanner.vuln_checks import run_vulnerability_checks


def run_safe_scan(target):
    results = []

    ports = scan_ports(target)
    services = detect_services(ports)

    for port, service in services.items():
        results.append({
            "name": f"Open Port {port}",
            "description": f"Service detected: {service}",
            "severity": "Medium",
            "cvss": 5.0
        })

    vuln_results = run_vulnerability_checks(services)
    results.extend(vuln_results)

    return results
