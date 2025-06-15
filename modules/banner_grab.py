import socket
import logging

# Banner grabbing function
def run(target, port=80, verbosity=0):
    print(f"\n[*] Attempting banner grab on {target}:{port}")
    banner = None  # Initialize banner to None for return

    try:
        with socket.socket() as s:
            s.settimeout(2)  # timeout in seconds
            s.connect((target, port))

            # Send protocol-specific request (HTTP example)
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode(errors="ignore").strip()

            if verbosity == 0:
                print(f"[+] Banner detected on port {port}")
            elif verbosity == 1:
                print(f"[+] Banner (port {port}): {banner.splitlines()[0]}")
            else:
                print(f"[+] Full Banner from {target}:{port}:\n{banner}")

    except socket.timeout:
        logging.warning(f"[!] Connection timed out for {target}:{port}")
    except Exception as e:
        logging.error(f"[!] Error grabbing banner: {e}")
    return f"{target}:{port} → {banner}" if banner else None  # Return the result