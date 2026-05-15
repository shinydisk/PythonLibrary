######################################################
#       BACKUP LOGS FROM ARUBA SWITCHES SCRIPT       #
######################################################

import sys
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

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from banner import print_banner

# Create directories if they do not exist
if not os.path.exists('Logging'):
    os.makedirs('Logging')

if not os.path.exists('Logs'):
    os.makedirs('Logs')

# Logging configuration
logging.basicConfig(
    filename='Logging/netmiko_logging.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_switch_logs(ip, username, password, device_type="aruba_osswitch"):
    """Connects to a switch, retrieves hostname and logs, and saves them."""
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

        print(f"✅ Successfully connected to {ip}. Retrieving hostname and logs...")
        logging.info(f"✅ Successfully connected to {ip}")

        # Retrieve hostname
        hostname_output = connection.send_command("show running-config | include hostname")
        
        hostname = "unknown_hostname"
        if hostname_output:
            parts = hostname_output.strip().split()
            if len(parts) >= 2:
                hostname = parts[-1]

        # Retrieve logs
        logs_output = connection.send_command("show logging")

        # Save logs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Logs/{ip}_{hostname}_logs_{timestamp}.log"

        with open(file_name, 'w') as log_file:
            log_file.write(logs_output)

        print(f"✅ Logs for {hostname} ({ip}) saved to {file_name}")
        logging.info(f"✅ Logs for {hostname} ({ip}) saved to {file_name}")

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
    """Reads a CSV file and returns a list of switch IPs."""
    print(f"\n👀 Reading IP list from {file_csv}...")
    ip_list = []

    with open(file_csv, mode='r', newline='') as file:
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
    """Main function to retrieve logs from multiple switches."""
    print_banner(
        name        = "📜 Switch Logging",
        description = "🌐 Retrieve and archive logs from Aruba switches",
        version     = "1.0",
        author      = "shinydisk",
    )
    logging.info("###############################################")
    logging.info("#       Starting bulk logs retrieval          #")
    logging.info("###############################################")

    # 🔐 Ask credentials at runtime
    username = input("\nLogin: ")
    password = getpass("Password: ")

    ip_list = read_csv(file_csv)

    for ip in ip_list:
        save_switch_logs(ip, username, password, device_type=device_type)

    print("\n################################################")
    print("#      Bulk logs retrieval completed.          #")
    print("################################################\n")
    logging.info("###############################################")
    logging.info("#      Bulk logs retrieval completed          #")
    logging.info("###############################################")


if __name__ == "__main__":

    # CSV file containing switch IPs
    file_csv = "iplist.csv"

    # Device type (change if needed)
    device_type = "aruba_osswitch"

    main(file_csv, device_type=device_type)