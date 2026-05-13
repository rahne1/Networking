import socket


# week 1 port scanner (no asyncio)
def scan_port(host: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.0)
        s.connect((host, port))
        print(f"port {port} is open")
    except ConnectionRefusedError:
        pass
    except socket.timeout:
        pass
    finally:
        s.close()


for i in range(0, 1024):
    scan_port("scanme.nmap.org", i)
