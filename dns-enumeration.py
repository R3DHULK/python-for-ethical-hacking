import dns.resolver

# Set the target domain and record type
print ('''\033[93m
    **********************************************
    *       Simple DNS Enumeration Tool          *
    *  github page : https://github.com/r3dhulk  *
    **********************************************
       ''')
target_domain = input("\033[92m [*] Hulk Wants The URL: ")
record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
# Create a DNS resolver
resolver = dns.resolver.Resolver()
for record_type in record_types:
    # Perform DNS lookup for the specified domain and record type
    try:
        answers = resolver.resolve(target_domain, record_type)
    except dns.resolver.NoAnswer:
        continue
    # Print the answers
    print(f"{record_type} records for {target_domain}:")
    for rdata in answers:
        print(f" {rdata}")
