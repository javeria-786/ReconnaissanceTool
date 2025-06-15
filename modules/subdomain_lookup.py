import requests
import logging

# Fetch subdomain data from crt.sh
def get_crtsh_data(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        logging.debug(f"Requesting data from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for HTTP issues
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching crt.sh data: {e}")
        return []

# Main subdomain enumeration function
def run(domain, verbosity):
    print(f"\n[*] Enumerating subdomains using crt.sh for: {domain}")
    
    # Fetch JSON data from crt.sh
    data = get_crtsh_data(domain)
    if not data:
        print("[-] No data retrieved.")
        return[]

    subdomains = set()  # To hold unique subdomains
    metadata = []       # To hold extended metadata when verbosity >= 2

    # Parse the fetched certificate entries
    for entry in data:
        name_value = entry.get("name_value", "")
        # Each certificate may contain multiple newline-separated domains
        for sub in name_value.split('\n'):
            if domain in sub:
                sub = sub.strip()
                subdomains.add(sub)
                if verbosity >= 2:
                    # Collect certificate details for advanced verbosity
                    metadata.append({
                        "subdomain": sub,
                        "issuer_name": entry.get("issuer_name"),
                        "serial_number": entry.get("serial_number"),
                        "not_before": entry.get("not_before"),
                        "not_after": entry.get("not_after")
                    })

    # Verbosity Level 0: Show only count
    if verbosity == 0:
        print(f"[+] Total subdomains found: {len(subdomains)}")

    # Verbosity Level 1: Show list of subdomains
    elif verbosity == 1:
        print(f"[+] Subdomains found ({len(subdomains)}):")
        for sub in sorted(subdomains):
            print(f"  - {sub}")
    

    # Verbosity Level 2 or more: Show subdomains + certificate metadata
    else:
        print(f"[+] Subdomains with certificate metadata ({len(metadata)}):")
        for cert in metadata:
            print(f"  - {cert['subdomain']}")
            print(f"     Issuer      : {cert['issuer_name']}")
            print(f"     Serial No.  : {cert['serial_number']}")
            print(f"     Valid From  : {cert['not_before']}")
            print(f"     Valid Until : {cert['not_after']}")
    return sorted(subdomains)  # <-- Final result returned to main.py for the report