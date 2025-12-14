from scanner.port_scanner import scan_ports
from scanner.vuln_checks import check_vulnerabilities
from scanner.attack_mapper import build_attack_chains
from utils.helpers import detect_service


def run_safe_scan(target, profile="quick"):
    """
    Executes a context-aware vulnerability scan and attack surface analysis.
    """

    # Scan profiles
    if profile == "quick":
        ports = [21, 22, 80, 443, 3306, 5432]
    elif profile == "stealth":
        ports = [22, 80, 443]
    else:  # full
        ports = list(range(1, 1025))

    vulnerabilities = []

    # Port scan
    open_ports = scan_ports(target, ports)
    print("[DEBUG] Open ports:", open_ports)

    # Service + vulnerability analysis
    for port in open_ports:
        service = detect_service(target, port)
        print(f"[DEBUG] Scanning port {port} ({service})")

        vulns = check_vulnerabilities(port)
        print("[DEBUG] Vulnerabilities found:", vulns)

        for v in vulns:
            vulnerabilities.append({
                "name": v.get("name", "Unknown Issue"),
                "severity": v.get("severity", "Low"),
                "description": v.get("description", ""),
                "impact": v.get("impact", ""),
                "owasp": v.get("owasp", ""),
                "mitre": v.get("mitre", []),
                "port": port,
                "service": service
            })

    # Attack chain generation
    attack_chains = build_attack_chains(vulnerabilities)
    print("[DEBUG] Attack chains:", attack_chains)

    return {
        "vulnerabilities": vulnerabilities,
        "attack_chains": attack_chains
    }
