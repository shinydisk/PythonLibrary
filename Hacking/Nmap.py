##########################################
#     INTERACTIVE NMAP PYTHON SCRIPT     #
##########################################

import subprocess
import os

# Variable to store the results of the scan
results = []

def append_to_results(data):
    """Appends data to the global result list for saving later."""
    global results
    results.append(data)

def run_nmap_scan(target, scan_type, use_pn=False):
    """Runs the specified Nmap scan on the target or network range."""
    try:
        # Append -Pn before the target if the user chooses to use it
        pn_option = "-Pn " if use_pn else ""

        # Nmap scan command based on user choice
        if scan_type == '1':
            command = f"nmap {pn_option}{target}"  # Regular scan
        elif scan_type == '2':
            command = f"nmap {pn_option}-sS {target}"  # SYN scan
        elif scan_type == '3':
            command = f"nmap {pn_option}-sV {target}"  # Service version detection
        elif scan_type == '4':
            command = f"nmap {pn_option}-O {target}"  # OS detection
        elif scan_type == '5':
            command = f"nmap {pn_option}-A {target}"  # Aggressive scan
        else:
            print("⛔ Invalid scan type.")
            return

        print(f"\nRunning Nmap scan: {command}")
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        # Decode the output
        scan_result = out.decode('utf-8')
        error_message = err.decode('utf-8')

        # Print the scan results or errors
        if scan_result:
            print(scan_result)
            append_to_results(scan_result)

        if "Host seems down" in scan_result and "try -Pn" in scan_result:
            retry_with_pn(target, scan_type)

    except Exception as e:
        error = f"⛔ Error running Nmap scan: {e}\n"
        append_to_results(error)
        print(error)

def retry_with_pn(target, scan_type):
    """Prompt the user to retry the scan with the -Pn option if the host seems down."""
    while True:
        print("⚠️ Host seems down. Do you want to run the scan again with the -Pn option?")
        retry = input("This option allows NMAP to override the ping. (Y/N): ").strip().lower()
        if retry == 'y':
            print(f"\nRetrying scan with -Pn for {target}...")
            run_nmap_scan(target, scan_type, use_pn=True)
            break
        elif retry == 'n':
            print("⛔ Skipping retry with -Pn.\n")
            break
        else:
            print("⛔ Invalid input. Please enter 'Y' or 'N'.\n")

def save_results_to_file():
    """Saves the scan results to a text file."""
    file_name = input("\nEnter the name of the file to save results (default: 'nmap_scan_results.txt'): ").strip()
    if not file_name:
        file_name = "nmap_scan_results.txt"

    try:
        with open(file_name, 'w') as file:
            file.writelines(results)
        print(f"💾 Results have been saved to the file: {file_name}\n")
    except Exception as e:
        print(f"⛔ Error saving results: {e}")

def prompt_for_save():
    """Prompt the user to save the results."""
    while True:
        save = input("💾 Do you want to save the results to a text file? (Y/N): ").strip().lower()
        if save == 'y':
            save_results_to_file()
            break
        elif save == 'n':
            print("⛔ Results were not saved.\n")
            break
        else:
            print("⛔ Invalid input. Please enter 'Y' or 'N'.")

def main():
    """Main function to handle user input and run the script."""
    print("\n     #################################################")
    print("     🔍         NMAP INTERACTIVE SCAN TOOL         🔍")
    print("     #################################################")

    while True:
        # Get the target IP or network range in CIDR format
        target = input("\nEnter the IP address or network range to scan (e.g., 192.168.1.0/24): ").strip()
        if not target:
            print("⛔ [ERROR] No target specified.")
            continue

        # Choose the type of scan
        print("\n Choose the type of Nmap scan:\n")
        print("   1. 🤓  Regular Scan (nmap <target>)")
        print("   2. 🥸  SYN Scan (nmap -sS <target>)")
        print("   3. 😈  Service Version Detection (nmap -sV <target>)")
        print("   4. 👿  OS Detection (nmap -O <target>)")
        print("   5. ☠️  Aggressive Scan (nmap -A <target>)")
        scan_type = input("\nEnter the number corresponding to the scan type: ").strip()

        # Run the scan on the network or IP address
        print("\n-------------------------------------------------------------------------------------")
        run_nmap_scan(target, scan_type)

        # Ask if the user wants to run another scan
        another = input("🔍 Do you want to run another scan? (Y/N): ").strip().lower()
        if another == 'n':
            break

    # Prompt to save results
    prompt_for_save()

if __name__ == "__main__":
    main()
