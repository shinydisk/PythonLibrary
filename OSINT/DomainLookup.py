###################################################
#     INTERACTIVE DOMAIN LOOKUP PYTHON SCRIPT     #
###################################################

import whois
import dns.resolver
import sublist3r
from ipwhois import IPWhois
import socket
import requests
from bs4 import BeautifulSoup

# Variable to store the results of the analysis
results = []

def append_to_results(data):
    """Appends data to the global result list for saving later."""
    global results
    results.append(data)

def get_whois_info(domain):
    try:
        append_to_results(f"\n[+] WHOIS Information for: {domain}\n")
        domain_info = whois.whois(domain)
        for key, value in domain_info.items():
            info = f"{key}: {value}\n"
            append_to_results(info)
            print(info)
    except Exception as e:
        error = f"\n⛔ Error retrieving WHOIS information: {e}\n"
        append_to_results(error)
        print(error)

def get_dns_records(domain):
    try:
        append_to_results(f"\n[+] DNS Records for: {domain}\n")
        record_types = ['A', 'AAAA', 'MX', 'NS', 'SOA', 'TXT']
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                append_to_results(f"\n[+] {record_type} Records:\n")
                for answer in answers:
                    result = f"{answer.to_text()}\n"
                    append_to_results(result)
                    print(result)
            except dns.resolver.NoAnswer:
                no_record = f"⛔ No {record_type} record found.\n"
                append_to_results(no_record)
                print(no_record)
    except Exception as e:
        error = f"⛔ Error retrieving DNS records: {e}\n"
        append_to_results(error)
        print(error)

def get_subdomains(domain):
    try:
        append_to_results(f"\n[+] Subdomains for: {domain}")
        subdomains = sublist3r.main(domain, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
        if subdomains:
            result = "\n".join(subdomains)
            append_to_results(result + "\n")
            print(result)
        else:
            no_subdomain = "⛔ No subdomains found."
            append_to_results(no_subdomain)
            print(no_subdomain)
    except Exception as e:
        error = f"⛔ Error retrieving subdomains: {e}"
        append_to_results(error)
        print(error)

def get_ip_info(domain):
    try:
        append_to_results(f"\n[+] IP and Geolocation Info for: {domain}\n")
        ip_address = socket.gethostbyname(domain)
        append_to_results(f"IP Address: {ip_address}\n")
        print(f"IP Address: {ip_address}")
        
        ip_info = IPWhois(ip_address)
        result = ip_info.lookup_rdap()
        
        network_info = f"Network: {result['network']['name']}\nCountry: {result['asn_country_code']}\nASN: {result['asn']}\n"
        append_to_results(network_info)
        print(network_info)
    except Exception as e:
        error = f"⛔ Error retrieving IP and geolocation information: {e}\n"
        append_to_results(error)
        print(error)

def get_links_from_page(domain):
    try:
        append_to_results(f"\n[+] Extracting links from {domain}\n")
        response = requests.get(f"http://{domain}")
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith("http"):
                links.add(href)
        if links:
            for link in links:
                result = f"{link}"
                append_to_results(result)
                print(link)
        else:
            no_links = "⛔ No links found.\n"
            append_to_results(no_links)
            print(no_links)
    except Exception as e:
        error = f"⛔ Error retrieving links from page: {e}\n"
        append_to_results(error)
        print(error)

def save_results_to_file():
    file_name = input("\nEnter the name of the file to save results (default: 'results.txt'): ").strip()
    if not file_name:
        file_name = "results.txt"
    
    try:
        with open(file_name, 'w') as file:
            file.writelines(results)
        print(f"\n💾 Results have been saved to the file: {file_name}\n")
    except Exception as e:
        print(f"⛔ Error saving results: {e}")

def prompt_for_save():
    while True:
        save = input("\n💾 Do you want to save the results to a text file? (y/n): ").strip().lower()
        if save == 'y':
            save_results_to_file()
            break
        elif save == 'n':
            print("⛔ Results were not saved.\n")
            break
        else:
            print("⛔ Invalid input. Please enter 'y' or 'n'.")

def main():
    print("\n     -------------------------------------------------")
    print("     👀          D O M A I N  L O O K U P          👀")
    print("     -------------------------------------------------")
    domain = input("\nEnter the domain to analyze (e.g., example.com): ").strip()

    if not domain:
        print("\n⛔ [ERROR] No domain specified.")
        return

    # WHOIS information
    get_whois_info(domain)

    # DNS records
    get_dns_records(domain)

    # Subdomains
    get_subdomains(domain)

    # IP and Geolocation information
    get_ip_info(domain)

    # Extract links from the main page
    get_links_from_page(domain)

    # Prompt for saving results
    prompt_for_save()

if __name__ == "__main__":
    main()
