##########################################
#     NETMIKO PUSHING CONFIGURATION      #
##########################################

import csv
import logging
import os
from getpass import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Create directories for logging if they do not exist
if not os.path.exists("Logging"):
    os.makedirs("Logging")

# Logging configuration
logging.basicConfig(
    filename="Logging/netmiko-push.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def send_switch_config(ip, commands, username, password, device_type="aruba_aoscx"):
    """Connects to a switch and sends the configuration."""
    try:
        print("\n-----------------------------------------------------------------------------")
        print(f"\n🌐 Connecting to switch {ip}...")
        logging.info(f"🌐 Connecting to switch {ip}")

        # Device connection details
        connection = ConnectHandler(
            device_type=device_type,
            host=ip,
            username=username,
            password=password,
        )

        print(f"✅ Successfully connected to {ip}. Sending configuration...")
        logging.info(f"✅ Successfully connected to {ip}")

        # Sending the configuration commands
        output = connection.send_config_set(commands)
        print(f"\nConfiguration sent to {ip}:\n{output}")
        logging.info(f"✅ Successfully sent configuration to {ip}")

        # Closing the connection
        connection.disconnect()
        print(f"\n❌ Connection closed for {ip}.")

    except NetmikoTimeoutException:
        print(f"\n⛔ ERROR: Timeout while connecting to {ip}")
        logging.error(f"⛔ Timeout while connecting to {ip}")

    except NetmikoAuthenticationException:
        print(f"\n⛔ ERROR: Authentication failed for {ip}")
        logging.error(f"⛔ Authentication failed for {ip}")

    except Exception as e:
        print(f"\n⛔ Unexpected error with {ip}: {str(e)}")
        logging.error(f"⛔ Unexpected error with {ip}: {str(e)}")


def read_csv(file_csv):
    """Reads a CSV file and returns a list of switch IPs."""
    print(f"\n👀 Reading IP list from {file_csv}...")
    ip_list = []
    with open(file_csv, mode="r", newline="") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:
                continue
            ip = row[0].strip()  # Assumes the first column contains the IP
            if ip:
                ip_list.append(ip)
    print(f"👀 Found {len(ip_list)} IPs in {file_csv}.")
    return ip_list


def main(file_csv, commands, device_type="device_type"):
    """Main function to process switches in bulk."""
    print("\n######################################")
    print("#     Starting bulk operation...     #")
    print("######################################")
    logging.info("######################################")
    logging.info("#     Starting bulk operation...     #")
    logging.info("######################################")

    # 🔐 Ask for credentials at runtime (not stored in clear text)
    username = input("\nLogin: ")
    password = getpass("Password: ")

    # Read the IP addresses from the CSV file
    ip_list = read_csv(file_csv)

    for ip in ip_list:
        send_switch_config(ip, commands, username, password, device_type=device_type)

    print("#####################################")
    print("#     Bulk operation completed.     #")
    print("#####################################\n")
    logging.info("####################################")
    logging.info("#     Bulk operation completed     #")
    logging.info("####################################")


if __name__ == "__main__":
    # Configuration commands to send
    commands = [
        "show version",
    ]

    # CSV file containing switch IPs
    file_csv = "IPv4-list.csv"

    # IMPORTANT: replace with your actual Netmiko device_type
    # Examples: "cisco_ios", "aruba_os", "hp_procurve", etc.
    device_type = "aruba_aoscx"

    # Call the main function
    main(file_csv, commands, device_type=device_type)