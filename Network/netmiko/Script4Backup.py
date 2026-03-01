######################################################
#     BACKUP CONFIGURATION NETMIKO PYTHON SCRIPT     #
######################################################

import csv
import os
import logging
from datetime import datetime
from getpass import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)

# Create directories for logging and backups if they do not exist
os.makedirs("Logging", exist_ok=True)
os.makedirs("Backup", exist_ok=True)

# Logging configuration (saving logs in the "Logging" directory)
logging.basicConfig(
    filename="Logging/netmiko_backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(levelname)s - %(message)s"
)

def save_switch_config(ip, username, password, device_type="aruba_osswitch"):
    """Connects to a switch, retrieves the hostname and configuration, and saves them."""
    try:
        print("\n-----------------------------------------------------------------------------")
        print(f"\n🌐 Connecting to switch {ip}...")
        logging.info(f"🌐 Connecting to switch {ip}")

        connection = ConnectHandler(
            device_type=device_type,
            host=ip,
            username=username,
            password=password
        )

        print(f"✅ Successfully connected to {ip}. Retrieving hostname and configuration...")
        logging.info(f"✅ Successfully connected to {ip}")

        # Retrieve the hostname (more robust parsing)
        hostname_output = connection.send_command("show running-config | include hostname")
        hostname = "unknown_hostname"
        if hostname_output:
            parts = hostname_output.strip().split()
            if len(parts) >= 2:
                hostname = parts[-1]

        # Retrieve the running configuration
        config_output = connection.send_command("show running-config")

        # Save the configuration with a timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Backup/{ip}_{hostname}_backup_{timestamp}.cfg"

        with open(file_name, "w") as config_file:
            config_file.write(config_output)

        print(f"✅ Configuration for {hostname} ({ip}) saved to {file_name}")
        logging.info(f"✅ Configuration for {hostname} ({ip}) saved to {file_name}")

        connection.disconnect()
        print(f"❌ Connection closed for {ip} ({hostname}).")

    except NetmikoTimeoutException:
        print(f"⛔ ERROR: Timeout while connecting to {ip}")
        logging.error(f"⛔ Timeout while connecting to {ip}")

    except NetmikoAuthenticationException:
        print(f"⛔ ERROR: Authentication failed for {ip}")
        logging.error(f"⛔ Authentication failed for {ip}")

    except Exception as e:
        print(f"⛔ Unexpected error with {ip}: {str(e)}")
        logging.error(f"⛔ Unexpected error with {ip}: {str(e)}")


def read_csv(file_csv):
    """Reads a CSV file and returns a list of switch IPs (1st column)."""
    print(f"\n👀 Reading IP list from {file_csv}...")
    ip_list = []

    with open(file_csv, mode="r", newline="") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:
                continue
            ip = row[0].strip()
            if ip:
                ip_list.append(ip)

    print(f"👀 Found {len(ip_list)} IPs in {file_csv}.")
    return ip_list


def main(file_csv, device_type="aruba_osswitch"):
    """Main function to process switches in bulk and save configurations."""
    print("\n#################################################")
    print("#     Starting bulk configuration backup...     #")
    print("#################################################")
    logging.info("##############################################")
    logging.info("#     Starting bulk configuration backup     #")
    logging.info("##############################################")

    # 🔐 Ask for credentials at runtime (not stored in clear text)
    username = input("\nLogin: ")
    password = getpass("Password: ")

    ip_list = read_csv(file_csv)

    for ip in ip_list:
        save_switch_config(ip, username, password, device_type=device_type)

    print("\n################################################")
    print("#     Bulk configuration backup completed.     #")
    print("################################################\n")
    logging.info("###############################################")
    logging.info("#     Bulk configuration backup completed     #")
    logging.info("###############################################")


if __name__ == "__main__":
    # CSV file containing switch IPs
    file_csv = "iplist.csv"

    # Netmiko device type
    device_type = "aruba_osswitch"

    main(file_csv, device_type=device_type)