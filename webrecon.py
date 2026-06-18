import requests
import socket
import json
import threading
from urllib.parse import urlparse
from datetime import datetime

open_ports = []
found_subdomains = []

# =======================
# COLORS
# =======================
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
B = "\033[94m"
RESET = "\033[0m"

# =======================
# BANNER (Dashboard style)
# =======================
def banner():
    print(f"""{B}
=========================================
         WEBRECON FINAL BOSS v6
=========================================
   Fast Recon | Threaded | Pro Mode ⚡
=========================================
{RESET}""")

# =======================
# IP RESOLVER
# =======================
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return "N/A"

# =======================
# FAST PORT CHECK
# =======================
def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)

    if sock.connect_ex((ip, port)) == 0:
        print(f"{G}[OPEN] {port}{RESET}")
        open_ports.append(port)

    sock.close()

# =======================
# PORT SCANNER (FAST MODE)
# =======================
def scan_ports(ip):
    print(f"\n{Y}[+] Scanning ports...{RESET}")

    ports = list(range(20, 1024))  # expanded range
    threads = []

    for port in ports:
        t = threading.Thread(target=check_port, args=(ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_ports

# =======================
# SUBDOMAIN BRUTE FORCE
# =======================
def subdomain_scan(domain):
    print(f"\n{Y}[+] Subdomain Scan...{RESET}")

    words = [
        "www", "mail", "ftp", "dev", "api",
        "test", "admin", "blog", "shop", "vpn"
    ]

    for sub in words:
        url = f"http://{sub}.{domain}"

        try:
            requests.get(url, timeout=2)
            print(f"{G}[FOUND] {url}{RESET}")
            found_subdomains.append(url)
        except:
            pass

    return found_subdomains

# =======================
# TECH DETECTION
# =======================
def tech_detect(headers):
    print(f"\n{Y}[+] Tech Detection:{RESET}")

    server = headers.get("Server", "").lower()

    if "nginx" in server:
        print("Detected: Nginx")
    elif "apache" in server:
        print("Detected: Apache")
    elif "cloudflare" in server:
        print("Detected: Cloudflare")
    else:
        print("Unknown stack")

# =======================
# SAVE REPORT
# =======================
def save_report(data):
    with open("webrecon_report.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n{G}[✓] Report saved -> webrecon_report.json{RESET}")

# =======================
# MAIN ENGINE
# =======================
def scan(target):
    try:
        if not target.startswith("http"):
            target = "http://" + target

        domain = urlparse(target).netloc
        ip = get_ip(domain)

        print(f"\n{B}TARGET: {target}{RESET}")
        print(f"IP: {ip}")

        res = requests.get(target, timeout=5)

        print(f"Status: {res.status_code}")
        print(f"Server: {res.headers.get('Server')}")

        # MODULES
        ports = scan_ports(ip)
        subs = subdomain_scan(domain)
        tech_detect(res.headers)

        report = {
            "target": target,
            "ip": ip,
            "status": res.status_code,
            "server": res.headers.get("Server"),
            "open_ports": ports,
            "subdomains": subs,
            "time": str(datetime.now())
        }

        save_report(report)

    except Exception as e:
        print(f"{R}Error: {e}{RESET}")

# =======================
# DASHBOARD MENU
# =======================
def main():
    banner()

    while True:
        print(f"""
{Y}1){RESET} Scan Target
{Y}2){RESET} Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            target = input("Enter website: ")
            scan(target)

        elif choice == "2":
            print("Bye 👋")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
