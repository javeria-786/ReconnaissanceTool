# tech_detect.py
import logging
from webtech import WebTech

def run(target, verbosity=0):
    print(f"\n[*] Scanning technologies for: {target}")

    try:
        wt = WebTech(options={'json': True})
        result = wt.start_from_url(target)
        
        if not result:
            print("[-] No technologies detected.")
            return

        techs = result.get('tech', [])
        detected = []

        for tech in techs:
            name = tech.get("name", "Unknown")
            version = tech.get("version", "")
            confidence = tech.get("confidence", "N/A")
            tech_info = f"{name} {version} (Confidence: {confidence})"
            detected.append(tech_info)

        logging.debug(f"[+] Technologies detected: {detected}")
        return detected

    except Exception as e:
        logging.error(f"[!] Technology detection failed: {e}")
        return [f"Technology detection failed: {e}"]

        if verbosity == 0:
                print(f"[+] {name}")
        elif verbosity == 1:
                print(f"[+] {name} (confidence: {confidence})")
        else:
                print(f"[+] {name} {version} (confidence: {confidence})")

    except Exception as e:
        logging.error(f"[!] Error detecting technologies: {e}")
