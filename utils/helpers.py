import socket
import ssl


COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    27017: "MongoDB"
}


def grab_banner(host, port, timeout=2):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner
    except Exception:
        return ""


def detect_http_service(host, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((host, port))
        sock.sendall(b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n")
        data = sock.recv(1024).decode(errors="ignore")
        sock.close()

        for line in data.splitlines():
            if line.lower().startswith("server:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass

    return "HTTP Service"


def detect_service(host, port):
    # HTTP / HTTPS
    if port in (80, 8080):
        return detect_http_service(host, port)

    if port == 443:
        return "HTTPS Service"

    # Banner-based detection
    banner = grab_banner(host, port)

    if banner:
        return banner.split("\n")[0][:60]

    # Fallback
    return COMMON_SERVICES.get(port, "Unknown")
