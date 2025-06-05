import csv
import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging
from datetime import datetime

# Définition du dossier de sauvegarde
output_directory = "SwitchInventory"
os.makedirs(output_directory, exist_ok=True)
output_file = os.path.join(output_directory, "switch_inventory.csv")

# Configuration des logs
logging.basicConfig(
    filename='Logging/netmiko_inventory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_switch_info(ip, username, password, device_type="aruba_osswitch"):
    """ Récupère les informations du switch et les enregistre dans un fichier CSV."""
    try:
        device = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
        }
        
        connection = ConnectHandler(**device)
        output = connection.send_command("show version")
        connection.disconnect()
        
        # Extraction des informations importantes
        model = "Unknown"
        firmware = "Unknown"
        release_date = "Unknown"
        hostname = "Unknown"
        mac_address = "Unknown"
        serial_number = "Unknown"
        uptime = "Unknown"
        num_ports = "Unknown"
        manufacturer = "Unknown"
        last_reboot = "Unknown"
        
        for line in output.split('\n'):
            if "Model" in line:
                model = line.split(":")[-1].strip()
            elif "Firmware Version" in line:
                firmware = line.split(":")[-1].strip()
            elif "Release Date" in line:
                release_date = line.split(":")[-1].strip()
            elif "Hostname" in line:
                hostname = line.split(":")[-1].strip()
            elif "MAC Address" in line:
                mac_address = line.split(":")[-1].strip()
            elif "Serial Number" in line:
                serial_number = line.split(":")[-1].strip()
            elif "Uptime" in line:
                uptime = line.split(":")[-1].strip()
            elif "Total Ports" in line:
                num_ports = line.split(":")[-1].strip()
            elif "Manufacturer" in line:
                manufacturer = line.split(":")[-1].strip()
            elif "Last Reboot" in line:
                last_reboot = line.split(":")[-1].strip()
        
        # Enregistrement des données dans un fichier CSV
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip, hostname, model, firmware, release_date, mac_address, serial_number, uptime, num_ports, manufacturer, last_reboot])
        
        logging.info(f"Données enregistrées pour {ip}: {hostname}, {model}, {firmware}, {release_date}, {mac_address}, {serial_number}, {uptime}, {num_ports}, {manufacturer}, {last_reboot}")
    
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        logging.error(f"Erreur de connexion à {ip}: {str(e)}")

# Initialisation du fichier CSV avec les en-têtes
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IP Address", "Hostname", "Model", "Firmware Version", "Release Date", "MAC Address", "Serial Number", "Uptime", "Total Ports", "Manufacturer", "Last Reboot"])
