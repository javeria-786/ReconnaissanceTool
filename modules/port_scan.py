import socket
import logging
from datetime import datetime

# Perform a TCP connect scan on common ports
def run(target, verbosity):
    print(f"\n[*] Starting port scan on {target}")
    
    # Common TCP ports to scan (can be extended)
    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 3306, 3389, 8080]

    open_ports = []       # <-- NEW: List to store open ports for the report
    banners = []          # <-- NEW: List to store banners for the report
    
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # short timeout to keep scan quick
                result = s.connect_ex((target, port))  # 0 if success
                if result == 0:
                    # Try to grab banner
                    try:
                        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                        banner = s.recv(1024).decode().strip()
                    except:
                        banner = "No banner"
                
                    open_ports.append(port)             # <-- NEW: Save open port
                    banners.append(f"{port}: {banner}") # <-- NEW: Save banner text

                    # Verbosity-based output
                    if verbosity == 0:
                        print(f"[+] Port {port} is open.")
                    elif verbosity == 1:
                        print(f"[+] Port {port} is open. Banner: {banner}")
                    else:
                        print(f"[+] Port {port} is open.")
                        print(f"    Banner      : {banner}")
                        print(f"    Checked At  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            logging.debug(f"Port {port}: Error - {e}")
    # <-- FINAL AND MOST IMPORTANT FIX FOR REPORT -->
    return open_ports, banners  # Return values for main.py to store in report_data
