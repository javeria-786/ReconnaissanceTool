import argparse
import logging
import modules.whois_lookup as whois_lookup
import modules.dns_lookup as dns_lookup
import modules.subdomain_lookup as subdomain_lookup
import modules.port_scan as port_scan
import modules.banner_grab as banner_grab
import modules.tech_detect as tech_detect
import pyfiglet
import shutil
import datetime
import socket
import os

report_data = {
    "timestamp": str(datetime.datetime.now()),
    "ip_address": None,
    "whois": "",
    "dns": "",
    "subdomains": [],
    "ports": [],
    "banners": [],
    "technologies": []
}


def show_banner():
      # Use pyfiglet if available
    banner = pyfiglet.figlet_format("TraceInfo", font="slant")
      

    # Detect terminal width, default to 80
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80

    # Center the banner safely
    centered_banner = "\n".join(
        line.center(terminal_width) for line in banner.splitlines()
    )

    print(centered_banner)
    print("Red Team Reconnaissance Toolkit".center(terminal_width))

# Setup the logger based on verbosity level
def setup_logger(verbosity):
    level = logging.WARNING  # Default level
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')

def write_report(report_data, format="txt"):
    # Ensure the 'reports' directory exists
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Create the filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"traceinfo_report_{timestamp}.{format}"
    filepath = os.path.join(reports_dir, f"traceinfo_report_{timestamp}.{format}")  # Save in reports folder
    
    if format == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"TraceInfo Report - {report_data['timestamp']}\n")
            f.write(f"Resolved IP: {report_data['ip_address']}\n\n")
            f.write("=== WHOIS ===\n")
            f.write(str(report_data["whois"]) + "\n\n")
            f.write("=== DNS ===\n")
            f.write(str(report_data["dns"]) + "\n\n")
            f.write("=== Subdomains ===\n")
            for sub in report_data["subdomains"]:
                f.write(f"- {sub}\n")
            f.write("\n=== Open Ports ===\n")
            for port in report_data["ports"]:
                f.write(f"- {port}\n")
            f.write("\n=== Banners ===\n")
            for banner in report_data["banners"]:
                f.write(f"- {banner}\n")
            f.write("\n=== Technologies ===\n")
            for tech in report_data["technologies"]:
                f.write(f"- {tech}\n")
    elif format == "html":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"<h1>TraceInfo Report</h1>")
            f.write(f"<p><b>Generated:</b> {report_data['timestamp']}</p>")
            f.write(f"<p><b>Resolved IP:</b> {report_data['ip_address']}</p>")
            f.write(f"<h2>WHOIS</h2><pre>{report_data['whois']}</pre>")
            f.write(f"<h2>DNS</h2><pre>{report_data['dns']}</pre>")
            f.write(f"<h2>Subdomains</h2><ul>")
            for sub in report_data["subdomains"]:
                f.write(f"<li>{sub}</li>")
            f.write(f"</ul><h2>Open Ports</h2><ul>")
            for port in report_data["ports"]:
                f.write(f"<li>{port}</li>")
            f.write(f"</ul><h2>Banners</h2><ul>")
            for banner in report_data["banners"]:
                f.write(f"<li>{banner}</li>")
            f.write(f"</ul><h2>Technologies</h2><ul>")
            for tech in report_data["technologies"]:
                f.write(f"<li>{tech}</li>")
            f.write("</ul>")
    print(f"[+] Report saved to: {filepath}")



# Main command-line interface handler
def main():
    # Define the command-line interface
    show_banner()
    parser = argparse.ArgumentParser(description="Reconnaissance Tool")


    # Define individual flags for each module
    parser.add_argument("--whois", type=str, help="Perform WHOIS lookup on a domain")
    parser.add_argument("--dns", type=str, help="Perform DNS enumeration on a domain")
    parser.add_argument("--subdomains", type=str, help="Enumerate subdomains for a domain")
    parser.add_argument("--portscan", type=str, help="Perform port scan on target IP or domain")
    parser.add_argument("--banner", type=str, help="Perform banner grabbing on target (e.g., example.com:80)")
    parser.add_argument("--tech", type=str, help="Detect technologies of website")
    parser.add_argument("--html", action="store_true", help="Generate HTML report instead of TXT")

    # Verbosity control: -v, -vv, etc.
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity")

    # Parse arguments
    args = parser.parse_args()

    # Setup logging based on verbosity
    setup_logger(args.verbose)

    # Determine primary domain for IP resolution
    primary_target = args.whois or args.dns or args.subdomains or args.portscan or args.tech
    if primary_target:
        try:
            report_data["ip_address"] = socket.gethostbyname(primary_target)
        except:
            report_data["ip_address"] = "Could not resolve"
    

    # Call WHOIS module if --whois flag is used
    if args.whois:
     report_data["whois"] = whois_lookup.run(args.whois, args.verbose)

    # Call DNS module if --dns flag is used
    if args.dns:
     report_data["dns"] = dns_lookup.run(args.dns, args.verbose)

    # Call subdomain enumeration module if --subdomains is used
    if args.subdomains:
     report_data["subdomains"] = subdomain_lookup.run(args.subdomains, args.verbose)
    # call ports can enumeration module if --portscan is used
    if args.portscan:
     report_data["ports"] =  port_scan.run(args.portscan, args.verbose)
    # call bannergrabber enumeration module if --banner is used
    if args.banner:
        try:
          host, port = args.banner.split(":")
          report_data["banners"] = banner_grab.run(host, int(port), args.verbose)
        except ValueError:
         print("[!] Use format: --banner example.com:port (e.g., 80, 21, 22)")
    # call tech_detect enumeration module if --tech is used
    if args.tech:
      report_data["technologies"] = tech_detect.run(args.tech, args.verbose)

     #Write final report
    report_format = "html" if args.html else "txt"
    write_report(report_data, format=report_format)
    
    # If no arguments were given, show help
    if not any([args.whois, args.dns, args.subdomains]):
        parser.print_help()

# Run the main function
if __name__ == '__main__':
    main()
