################################################
#     GEOLOCATION IP ADDRESS PYTHON SCRIPT     #
################################################

import socket
import requests
from ipwhois import IPWhois

# Variable to store the results of the analysis
results = []

def append_to_results(data):
    """Appends data to the global result list for saving later."""
    global results
    results.append(data)

def get_ip_info(domain):
    """Retrieve IP address and basic information for a domain."""
    try:
        append_to_results(f"\n[+] Looking up IP for: {domain}")
        ip_address = socket.gethostbyname(domain)
        append_to_results(f"IP Address: {ip_address}\n")
        print(f"\n[+] IP Address for {domain}: {ip_address}")

        # Use IPWhois to get more information about the IP address
        ip_info = IPWhois(ip_address)
        result = ip_info.lookup_rdap()
        network_info = (f"Network Name: {result['network']['name']}\n"
                        f"ASN: {result['asn']}\n"
                        f"ASN Country: {result['asn_country_code']}\n")
        append_to_results(network_info)
        print(network_info)
    except Exception as e:
        error = f"⛔ Error retrieving IP information: {e}\n"
        append_to_results(error)
        print(error)

def get_geolocation_info(ip_address):
    """Fetch geolocation data for the given IP address using ip-api.com."""
    try:
        append_to_results(f"\n[+] Fetching geolocation for IP: {ip_address}")
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        geo_data = response.json()

        if geo_data['status'] == 'success':
            geo_info = (f"Country: {geo_data['country']}\n"
                        f"Region: {geo_data['regionName']}\n"
                        f"City: {geo_data['city']}\n"
                        f"Latitude: {geo_data['lat']}\n"
                        f"Longitude: {geo_data['lon']}\n"
                        f"ISP: {geo_data['isp']}\n")
            append_to_results(geo_info)
            print(geo_info)
        else:
            append_to_results("⛔ Could not retrieve geolocation data.\n")
            print("⛔ Could not retrieve geolocation data.")
    except Exception as e:
        error = f"⛔ Error retrieving geolocation information: {e}\n"
        append_to_results(error)
        print(error)

def save_results_to_file():
    """Save the results to a text file."""
    file_name = input("\nEnter the name of the file to save results (default: 'ip_geolocation_results.txt'): ").strip()
    if not file_name:
        file_name = "ip_geolocation_results.txt"

    try:
        with open(file_name, 'w') as file:
            file.writelines(results)
        print(f"\n💾 Results have been saved to the file: {file_name}\n")
    except Exception as e:
        print(f"⛔ Error saving results: {e}")

def prompt_for_save():
    """Prompt the user to save the results."""
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
    """Main function to handle user input and run the script."""
    print("\n     ---------------------------------------------------")
    print("     🌍       IP ADDRESS AND GEOLOCATION LOOKUP       🌍")
    print("     ---------------------------------------------------")

    while True:
        domain_or_ip = input("\nEnter a domain or IP address to analyze: ").strip()

        if not domain_or_ip:
            print("\n⛔ [ERROR] No input specified.")
            continue

        # Check if the input is an IP address or domain
        if domain_or_ip.replace('.', '').isdigit():
            # It seems to be an IP address
            ip_address = domain_or_ip
        else:
            # It's a domain, get the IP address first
            get_ip_info(domain_or_ip)
            ip_address = socket.gethostbyname(domain_or_ip)

        # Fetch geolocation data for the IP address
        get_geolocation_info(ip_address)

        # Ask if the user wants to analyze another domain or IP
        another = input("\n🔍 Do you want to lookup another domain/IP? (y/n): ").strip().lower()
        if another == 'n':
            break

    # Prompt to save results
    prompt_for_save()

if __name__ == "__main__":
    main()
