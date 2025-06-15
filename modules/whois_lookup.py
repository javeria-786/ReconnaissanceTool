import whois
import logging

def run(domain, verbosity):
    print(f"WHOIS requested for: {domain} with verbosity: {verbosity}")
    try:
         info = whois.whois(domain)
         return str(info)  # <- Return the result as a string for the report
    except Exception as e:
        logging.error(f"Who is lookup failed:{e}")
        return f"WHOIS lookup failed: {e}"  # <- Return error message to include in report
    
    if verbosity == 0:
        print(f"Domain:{info.domain_info}")
        if info.creation_date:
         if isinstance(info.creation_date, list):
          creation_date = info.creation_date[0]
          print("Creation Date:", creation_date.date())
        else:
          print("Creation date not available.")
    elif verbosity == 1:
       print("Registrar :", info.registrar)
       print("Name servers :",info.name_servers)
       if info.creation_date:
          if isinstance(info.creation_date, list):
            creation_date = info.creation_date[0]
            print("Creation Date:", creation_date.date())
          else:
           print("Creation date not available.")

       if info.expiration_date:
           if isinstance(info.expiration_date, list):
             expiration_date = info.expiration_date[0]
             print("Expiration Date:", expiration_date.date())
           else:
              print("Expiration date not available.")

    elif verbosity >= 2:
       for key, value in info.items():
            print(f"{key}:{value}")

    
    

