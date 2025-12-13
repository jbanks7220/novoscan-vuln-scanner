from utils.threat_rating import cvss_score


def run_vulnerability_checks(services):
    findings = []

    for port, service in services.items():
        if service in ["MySQL", "PostgreSQL"]:
            findings.append({
                "name": "Database Service Exposed",
                "description": f"{service} service exposed on port {port}",
                "severity": "Critical",
                "cvss": cvss_score("critical")
            })

        if service in ["FTP", "HTTP"]:
            findings.append({
                "name": "Outdated Service Detected",
                "description": f"{service} may be running outdated software",
                "severity": "High",
                "cvss": cvss_score("high")
            })

    return findings
