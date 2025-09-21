######################################################
#       BACKUP LOGS FROM ARUBA SWITCHES SCRIPT       #
######################################################

import csv
import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging
from datetime import datetime

# Create directories for logging and log backups if they do not exist
if not os.path.exists('Logging'):
    os.makedirs('Logging')
if not os.path.exists('Logs'):
    os.makedirs('Logs')

# Logging configuration (saving logs in the "Logging" directory)
logging.basicConfig(
    filename='Logging/netmiko_logs_backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_switch_logs(ip, username, password, device_type="aruba_osswitch"):
    """Connects to a switch, retrieves the hostname and logs, and saves them to a .log file."""
    try:
        print(f"\n-----------------------------------------------------------------------------")
        print(f"\n🌐 Connecting to switch {ip}...")
        logging.info(f"🌐 Connecting to switch {ip}")
        
        # Device connection details
        connection = ConnectHandler(
            device_type=device_type,
            host=ip,
            username=username,
            password=password
        )
        
        print(f"✅ Successfully connected to {ip}. Retrieving hostname and logs...")
        logging.info(f"✅ Successfully connected to {ip}")
        
        # Retrieve the hostname
        hostname_output = connection.send_command("show running-config | include hostname")
        hostname = hostname_output.split()[-1]  # Extract the hostname from the command output
        
        # If the hostname is not retrieved, use a default name
        if not hostname:
            hostname = "unknown_hostname"
        
        # Retrieve the logs
        logs_output = connection.send_command("show logging")
        
        # Save the logs to a .log file in the "Logs" directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Logs/{ip}_{hostname}_logs_{timestamp}.log"
        with open(file_name, 'w') as log_file:
            log_file.write(logs_output)
        
        print(f"✅ Logs for {hostname} ({ip}) saved to {file_name}")
        logging.info(f"✅ Logs for {hostname} ({ip}) saved to {file_name}")
        
        # Closing the connection
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
    with open(file_csv, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            ip_list.append(row[0])  # Assumes the first column contains the IP
    print(f"👀 Found {len(ip_list)} IPs in {file_csv}.")
    return ip_list

def main(file_csv, username, password):
    """Main function to process switches in bulk and save logs."""
    print("\n#################################################")
    print("#        Starting bulk logs retrieval...        #")
    print("#################################################")
    logging.info("###############################################")
    logging.info("#       Starting bulk logs retrieval          #")
    logging.info("###############################################")
    
    # Read the IP addresses from the CSV file
    ip_list = read_csv(file_csv)
    
    for ip in ip_list:
        save_switch_logs(ip, username, password)
    
    print(f"\n-----------------------------------------------------------------------------")
    print("\n################################################")
    print("#      Bulk logs retrieval completed.          #")
    print("################################################\n")
    logging.info("###############################################")
    logging.info("#      Bulk logs retrieval completed          #")
    logging.info("###############################################")

if __name__ == "__main__":
    # Username and password for the connection
    username = "admin"
    password = "password"

    # CSV file containing switch IPs
    file_csv = "iplist.csv"
    
    # Call the main function
    main(file_csv, username, password)
