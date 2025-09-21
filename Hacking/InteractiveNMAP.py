import subprocess
import os
import time
from colorama import init, Fore, Style

# Initialisation de colorama
init(autoreset=True)

# Dossier des scans
SCAN_DIR = "./ScanNMAP"
HISTORY_FILE = os.path.join(SCAN_DIR, "history.log")

# Crée le dossier scans si besoin
os.makedirs(SCAN_DIR, exist_ok=True)

def banner():
    print("\n")
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.GREEN + Style.BRIGHT + "             SCRIPT NMAP INTERACTIF PRO")
    print(Fore.CYAN + Style.BRIGHT + "="*50)

def menu():
    print(Fore.YELLOW + "\nQue voulez-vous faire ?")
    print(Fore.BLUE + "[1]" + Fore.WHITE + " Scan rapide (-T4)")
    print(Fore.BLUE + "[2]" + Fore.WHITE + " Scan de ports spécifiques")
    print(Fore.BLUE + "[3]" + Fore.WHITE + " Scan réseau (ping scan -sn)")
    print(Fore.BLUE + "[4]" + Fore.WHITE + " Scan furtif SYN (-sS)")
    print(Fore.BLUE + "[5]" + Fore.WHITE + " Scan UDP (-sU)")
    print(Fore.BLUE + "[6]" + Fore.WHITE + " Scan OS seul (-O)")
    print(Fore.BLUE + "[7]" + Fore.WHITE + " Scan complet (-A)")
    print(Fore.BLUE + "[8]" + Fore.WHITE + " Scan de vulnérabilités (--script vuln)")
    print(Fore.BLUE + "[9]" + Fore.WHITE + " Voir l'historique des scans")
    print(Fore.BLUE + "[10]" + Fore.WHITE + " Quitter")

def get_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

def save_scan(command, output):
    filename = f"scan_{get_timestamp()}.txt"
    filepath = os.path.join(SCAN_DIR, filename)
    with open(filepath, "w") as f:
        f.write(output)
    with open(HISTORY_FILE, "a") as h:
        h.write(f"[{get_timestamp()}] {command} -> {filename}\n")
    print(Fore.GREEN + f"\nRésultat enregistré dans : {filepath}")

def run_scan(args):
    print(Fore.MAGENTA + f"\n[+] Exécution : {' '.join(args)}\n")
    try:
        result = subprocess.check_output(args, stderr=subprocess.STDOUT, text=True)
        print(Fore.WHITE + result)
        save_scan(' '.join(args), result)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Erreur : {e.output}")

def input_target():
    return input(Fore.CYAN + "Cible (IP, nom d'hôte ou plage IP) : ")

def option_scan_rapide():
    target = input_target()
    run_scan(["nmap", "-T4", target])

def option_ports_specifiques():
    target = input_target()
    ports = input(Fore.CYAN + "Ports à scanner (ex: 22,80,443) : ")
    run_scan(["nmap", "-p", ports, target])

def option_ping_scan():
    target = input(Fore.CYAN + "Plage IP (ex: 192.168.1.0/24) : ")
    run_scan(["nmap", "-sn", target])

def option_scan_syn():
    target = input_target()
    run_scan(["nmap", "-sS", target])

def option_scan_udp():
    target = input_target()
    use_combo = input(Fore.YELLOW + "Combiner avec scan TCP SYN (-sS) ? (y/n) : ").lower()
    if use_combo == 'y':
        run_scan(["nmap", "-sS", "-sU", target])
    else:
        run_scan(["nmap", "-sU", target])

def option_scan_os():
    target = input_target()
    run_scan(["nmap", "-O", target])

def option_scan_complet():
    target = input_target()
    run_scan(["nmap", "-A", target])

def option_scan_vuln():
    target = input_target()
    run_scan(["nmap", "--script", "vuln", target])

def afficher_historique():
    if os.path.exists(HISTORY_FILE):
        print(Fore.CYAN + "\nHistorique des scans :\n")
        with open(HISTORY_FILE, "r") as f:
            print(Fore.WHITE + f.read())
    else:
        print(Fore.RED + "Aucun historique trouvé.")

def main():
    while True:
        banner()
        menu()
        choice = input(Fore.MAGENTA + "\nVotre choix (1-10) : ")

        if choice == '1':
            option_scan_rapide()
        elif choice == '2':
            option_ports_specifiques()
        elif choice == '3':
            option_ping_scan()
        elif choice == '4':
            option_scan_syn()
        elif choice == '5':
            option_scan_udp()
        elif choice == '6':
            option_scan_os()
        elif choice == '7':
            option_scan_complet()
        elif choice == '8':
            option_scan_vuln()
        elif choice == '9':
            afficher_historique()
        elif choice == '10':
            print(Fore.RED + "Fermeture du script. À bientôt !")
            break
        else:
            print(Fore.RED + "Choix invalide.")
        
        input(Fore.YELLOW + "\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
