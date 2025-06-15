
import dns.resolver
import logging

def run(domain, verbosity):
    record_types = ['A', 'MX', 'TXT', 'NS']
    if verbosity == 0:
        record_types = ['A']  # Show only A records
    elif verbosity == 1:
        record_types = ['A', 'MX', 'NS']  # Show key records
    else:
        record_types = ['A', 'MX', 'TXT', 'NS']  # Show everything
    
    dns_results = []  # <-- NEW: Store records for report

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            print(f"\n{record_type} Records for {domain}:")
            for rdata in answers:
                if record_type == 'MX':
                    entry = print(f"  {rdata.exchange} (Preference: {rdata.preference})")
                elif record_type == 'TXT':
                    entry = print(f"  {' '.join([part.decode('utf-8') for part in rdata.strings])}")
                else:
                    entry = print(f"  {rdata}")
                print(f"  {entry}")  # Terminal output
                dns_results.append(entry)  # <-- Save for report

        except dns.resolver.NoAnswer:
            logging.info(f"No {record_type} records found for {domain}")
        except dns.resolver.NXDOMAIN:
            logging.error(f"Domain {domain} does not exist.")
            break
        except dns.exception.DNSException as e:
            logging.warning(f"Failed to fetch {record_type} records: {e}")

    return dns_results  # <-- ✅ FINAL FIX: return results for report
