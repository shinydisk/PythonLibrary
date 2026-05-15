######################################################
#              ARUBA SWITCH INVENTORY SCRIPT         #
######################################################

import sys
import csv
import os
import logging
from getpass import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from banner import print_banner

# Définition des dossiers
os.makedirs("Logging", exist_ok=True)
os.makedirs("SwitchInventory", exist_ok=True)

output_file = os.path.join("SwitchInventory", "switch_inventory.csv")

# Configuration des logs
logging.basicConfig(
    filename='Logging/netmiko_inventory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_switch_info(ip, username, password, device_type="aruba_osswitch"):
    """Récupère les informations du switch et les enregistre dans un fichier CSV."""
    try:
        print(f"\n🌐 Connexion à {ip}...")
        logging.info(f"Connexion à {ip}")

        device = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
        }

        connection = ConnectHandler(**device)
        output = connection.send_command("show version")
        connection.disconnect()

        print(f"✅ Données récupérées pour {ip}")

        # Valeurs par défaut
        data = {
            "Model": "Unknown",
            "Firmware Version": "Unknown",
            "Release Date": "Unknown",
            "Hostname": "Unknown",
            "MAC Address": "Unknown",
            "Serial Number": "Unknown",
            "Uptime": "Unknown",
            "Total Ports": "Unknown",
            "Manufacturer": "Unknown",
            "Last Reboot": "Unknown"
        }

        # Parsing
        for line in output.split('\n'):
            for key in data.keys():
                if key in line:
                    data[key] = line.split(":")[-1].strip()

        # Écriture CSV
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                ip,
                data["Hostname"],
                data["Model"],
                data["Firmware Version"],
                data["Release Date"],
                data["MAC Address"],
                data["Serial Number"],
                data["Uptime"],
                data["Total Ports"],
                data["Manufacturer"],
                data["Last Reboot"]
            ])

        logging.info(f"Données enregistrées pour {ip}")

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"⛔ Erreur de connexion à {ip}: {str(e)}")
        logging.error(f"Erreur de connexion à {ip}: {str(e)}")

    except Exception as e:
        print(f"⛔ Erreur inattendue sur {ip}: {str(e)}")
        logging.error(f"Erreur inattendue sur {ip}: {str(e)}")


def read_csv(file_csv):
    """Lit un CSV et retourne la liste des IP."""
    ip_list = []

    with open(file_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            ip = row[0].strip()
            if ip:
                ip_list.append(ip)

    return ip_list


def main(file_csv, device_type="aruba_osswitch"):

    print_banner(
        name        = "📋 Switch Inventory",
        description = "🌐 Build a CSV inventory of Aruba switches",
        version     = "1.0",
        author      = "shinydisk",
    )

    # 🔐 Credentials demandés au lancement
    username = input("Login: ")
    password = getpass("Password: ")

    ip_list = read_csv(file_csv)

    # Initialisation du fichier CSV avec les en-têtes
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "IP Address",
            "Hostname",
            "Model",
            "Firmware Version",
            "Release Date",
            "MAC Address",
            "Serial Number",
            "Uptime",
            "Total Ports",
            "Manufacturer",
            "Last Reboot"
        ])

    for ip in ip_list:
        get_switch_info(ip, username, password, device_type=device_type)

    print("\n########################################")
    print("#        Inventory Completed           #")
    print("########################################\n")


if __name__ == "__main__":

    file_csv = "iplist.csv"
    device_type = "aruba_osswitch"

    main(file_csv, device_type=device_type)