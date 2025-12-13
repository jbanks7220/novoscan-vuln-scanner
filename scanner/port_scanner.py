import socket

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-ALT"
}


def scan_ports(target):
    open_ports = []
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            if sock.connect_ex((target, port)) == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports


def detect_services(ports):
    services = {}
    for port in ports:
        services[port] = COMMON_PORTS.get(port, "Unknown Service")
    return services
