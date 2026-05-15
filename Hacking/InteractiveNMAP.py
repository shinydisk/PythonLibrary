import sys
import os
import subprocess
import socket
import ipaddress
import time
import json
import re
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.rule import Rule
from rich import box

console = Console()

SCAN_DIR = Path(__file__).parent / "ScanNMAP"
HISTORY_FILE = SCAN_DIR / "history.json"

SCAN_TYPES = {
    "1": {
        "label": "Scan rapide",
        "flags": ["-T4"],
        "needs_target": True,
        "edu": "Utilise le timing agressif T4 pour accélérer le scan des ports TCP les plus courants (top 1000). Idéal pour une première reconnaissance rapide.",
        "note": None,
    },
    "2": {
        "label": "Scan de ports TCP spécifiques",
        "flags": ["-p", "{ports}", "-sT"],
        "needs_target": True,
        "needs_ports": True,
        "edu": "Scanne uniquement les ports TCP que tu spécifies. Utilise un connect()-scan complet, sans privilèges root requis.",
        "note": None,
    },
    "3": {
        "label": "Découverte réseau (ping scan)",
        "flags": ["-sn"],
        "needs_target": True,
        "edu": "Envoie des paquets ICMP echo + TCP SYN/ACK sur le port 443 pour lister les hôtes actifs sans scanner leurs ports. Rapide pour cartographier un réseau.",
        "note": None,
    },
    "4": {
        "label": "Scan SYN furtif (root requis)",
        "flags": ["-sS"],
        "needs_target": True,
        "edu": "Envoie un SYN et observe la réponse (SYN-ACK = ouvert, RST = fermé) sans jamais terminer le handshake TCP. Plus discret qu'un connect-scan.",
        "note": "Nécessite les droits root (sudo).",
    },
    "5": {
        "label": "Scan UDP",
        "flags": ["-sU", "--top-ports", "100"],
        "needs_target": True,
        "edu": "Sonde les 100 ports UDP les plus courants (DNS:53, DHCP:67, SNMP:161...). Plus lent que TCP car UDP ne confirme pas la fermeture.",
        "note": "Lent. Nécessite les droits root (sudo).",
    },
    "6": {
        "label": "Détection de services et versions",
        "flags": ["-sV"],
        "needs_target": True,
        "edu": "Envoie des sondes pour identifier le service et sa version sur chaque port ouvert (ex: OpenSSH 8.9, Apache 2.4.54). Utile pour l'inventaire.",
        "note": None,
    },
    "7": {
        "label": "Détection d'OS (root requis)",
        "flags": ["-O"],
        "needs_target": True,
        "edu": "Analyse les particularités de la pile TCP/IP (TTL, taille de fenêtre, options TCP) pour deviner le système d'exploitation cible.",
        "note": "Nécessite les droits root (sudo).",
    },
    "8": {
        "label": "Scan complet -A",
        "flags": ["-A", "-T4"],
        "needs_target": True,
        "edu": "Combine détection OS (-O), versions (-sV), scripts NSE par défaut (-sC) et traceroute. Le scan le plus complet, mais aussi le plus visible.",
        "note": "Lent et bruyant sur le réseau.",
    },
    "9": {
        "label": "Scan de vulnérabilités NSE",
        "flags": ["--script", "vuln"],
        "needs_target": True,
        "edu": "Lance les scripts NSE de la catégorie 'vuln' pour détecter des failles connues (CVE) sur les services ouverts. Utilise uniquement sur des systèmes autorisés.",
        "note": "Très lent. Utiliser uniquement sur des systèmes dont tu as l'autorisation.",
    },
    "10": {
        "label": "Scan de plage de ports TCP",
        "flags": ["-p", "{ports}", "-sT", "-T4"],
        "needs_target": True,
        "needs_port_range": True,
        "edu": "Scanne une plage de ports TCP continue (ex: 1-1024). Permet de tester des services non-standards sur des ports inattendus.",
        "note": None,
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def banner():
    title = Text("🔭  Interactive NMAP", style="bold cyan")
    sub   = Text("Scan réseau interactif avec historique et mode éducatif", style="dim")
    console.print(Panel.fit(Text.assemble(title, "\n", sub), border_style="blue"))
    console.print()


def detect_local_network() -> str | None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return str(ipaddress.ip_network(ip + "/24", strict=False))
    except Exception:
        return None


def ask_target(ping_scan: bool = False) -> str:
    hint = detect_local_network()
    label = "Plage IP (ex: 192.168.1.0/24)" if ping_scan else "Cible (IP, nom d'hôte ou plage)"
    if hint:
        console.print(f"  [dim]Réseau local détecté : [cyan]{hint}[/cyan][/dim]")
    return Prompt.ask(f"  [bold yellow]{label}[/bold yellow]", default=hint or "")


def ask_ports(label: str = "Ports (ex: 22,80,443)") -> str:
    return Prompt.ask(f"  [bold yellow]{label}[/bold yellow]")


def ensure_scan_dir():
    SCAN_DIR.mkdir(parents=True, exist_ok=True)


def load_history() -> list[dict]:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except json.JSONDecodeError:
            return []
    return []


def save_history(entry: dict):
    ensure_scan_dir()
    history = load_history()
    history.append(entry)
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False))


# ── Scan execution ────────────────────────────────────────────────────────────

def run_scan(args: list[str], scan_label: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ensure_scan_dir()
    output_file = SCAN_DIR / f"scan_{timestamp}.txt"

    console.print()
    console.print(Rule(f"[bold magenta]{scan_label}[/bold magenta]"))
    console.print(f"  [dim]Commande : [cyan]{' '.join(args)}[/cyan][/dim]")
    console.print()

    lines: list[str] = []
    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        for line in process.stdout:
            line = line.rstrip()
            lines.append(line)
            _print_nmap_line(line)
        process.wait()
        success = process.returncode == 0
    except FileNotFoundError:
        console.print("[bold red]Erreur : nmap n'est pas installé ou introuvable dans le PATH.[/bold red]")
        return
    except PermissionError:
        console.print("[bold red]Erreur : permissions insuffisantes. Relancez avec sudo.[/bold red]")
        return

    full_output = "\n".join(lines)
    output_file.write_text(full_output)

    entry = {
        "timestamp": timestamp,
        "command": " ".join(args),
        "label": scan_label,
        "file": str(output_file),
        "success": success,
    }
    save_history(entry)

    console.print()
    if success:
        console.print(f"  [green]✔  Résultat sauvegardé dans[/green] [cyan]{output_file}[/cyan]")
    else:
        console.print(f"  [red]✘  Scan terminé avec des erreurs.[/red]")

    return full_output


def _print_nmap_line(line: str):
    """Colorise la sortie nmap ligne par ligne."""
    if line.startswith("Nmap scan report"):
        console.print(f"  [bold green]{line}[/bold green]")
    elif re.match(r"^\d+/tcp\s+open", line):
        console.print(f"  [green]{line}[/green]")
    elif re.match(r"^\d+/tcp\s+closed", line):
        console.print(f"  [red]{line}[/red]")
    elif re.match(r"^\d+/tcp\s+filtered", line):
        console.print(f"  [yellow]{line}[/yellow]")
    elif re.match(r"^\d+/udp\s+open", line):
        console.print(f"  [bold cyan]{line}[/bold cyan]")
    elif re.match(r"^\d+/udp\s+closed|filtered", line):
        console.print(f"  [dim]{line}[/dim]")
    elif line.startswith("OS details") or line.startswith("Running:"):
        console.print(f"  [bold yellow]{line}[/bold yellow]")
    elif line.startswith("|"):
        console.print(f"  [dim cyan]{line}[/dim cyan]")
    elif line.strip().startswith("Host is up"):
        console.print(f"  [bold blue]{line}[/bold blue]")
    else:
        console.print(f"  [white]{line}[/white]")


# ── Menu ──────────────────────────────────────────────────────────────────────

def print_menu():
    table = Table(box=box.ROUNDED, show_header=False, border_style="blue", padding=(0, 1))
    table.add_column("N°", style="bold cyan", width=4)
    table.add_column("Option", style="white")

    for key, info in SCAN_TYPES.items():
        note = f"  [dim red]({info['note']})[/dim red]" if info.get("note") else ""
        table.add_row(key, info["label"] + note)

    table.add_section()
    table.add_row("H", "Voir l'historique des scans")
    table.add_row("C", "Comparer deux scans")
    table.add_row("Q", "Quitter")

    console.print(table)


def show_edu(info: dict):
    console.print()
    console.print(Panel(
        f"[italic]{info['edu']}[/italic]",
        title="[bold blue]ℹ  Mode éducatif[/bold blue]",
        border_style="blue",
        padding=(0, 1),
    ))
    if info.get("note"):
        console.print(f"  [bold red]⚠  {info['note']}[/bold red]")
    console.print()


def build_args(info: dict, target: str, ports: str = "") -> list[str]:
    args = ["nmap"]
    for flag in info["flags"]:
        if flag == "{ports}":
            args.append(ports)
        else:
            args.append(flag)
    args.append(target)
    return args


# ── History ───────────────────────────────────────────────────────────────────

def show_history():
    history = load_history()
    if not history:
        console.print("  [yellow]Aucun scan dans l'historique.[/yellow]")
        return

    table = Table(title="Historique des scans", box=box.SIMPLE_HEAVY, border_style="cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Date", style="cyan", width=20)
    table.add_column("Type", style="white")
    table.add_column("Commande", style="dim")
    table.add_column("Fichier", style="dim green")

    for i, entry in enumerate(reversed(history[-20:]), 1):
        status = "✔" if entry.get("success") else "✘"
        color = "green" if entry.get("success") else "red"
        table.add_row(
            f"[{color}]{status}[/{color}]",
            entry["timestamp"].replace("_", " "),
            entry["label"],
            entry["command"],
            Path(entry["file"]).name,
        )

    console.print(table)


# ── Comparison ────────────────────────────────────────────────────────────────

def _extract_ports(text: str) -> dict[str, str]:
    """Retourne {port/proto: état} à partir d'une sortie nmap brute."""
    ports = {}
    for line in text.splitlines():
        m = re.match(r"^(\d+/(tcp|udp))\s+(\w+)", line)
        if m:
            ports[m.group(1)] = m.group(3)
    return ports


def compare_scans():
    history = load_history()
    if len(history) < 2:
        console.print("  [yellow]Il faut au minimum 2 scans sauvegardés pour comparer.[/yellow]")
        return

    console.print()
    for i, entry in enumerate(history[-10:], 1):
        console.print(f"  [cyan]{i}[/cyan]  {entry['timestamp'].replace('_', ' ')}  [dim]{entry['label']}  ({entry['command']})[/dim]")

    console.print()
    idx_a = int(Prompt.ask("  [bold yellow]Numéro du scan A[/bold yellow]")) - 1
    idx_b = int(Prompt.ask("  [bold yellow]Numéro du scan B[/bold yellow]")) - 1

    entries = history[-10:]
    try:
        file_a = Path(entries[idx_a]["file"])
        file_b = Path(entries[idx_b]["file"])
    except IndexError:
        console.print("  [red]Index invalide.[/red]")
        return

    if not file_a.exists() or not file_b.exists():
        console.print("  [red]Un ou plusieurs fichiers de scan sont introuvables.[/red]")
        return

    ports_a = _extract_ports(file_a.read_text())
    ports_b = _extract_ports(file_b.read_text())

    all_ports = sorted(set(ports_a) | set(ports_b))

    table = Table(title="Comparaison de scans", box=box.ROUNDED, border_style="magenta")
    table.add_column("Port", style="bold")
    table.add_column(f"Scan A\n[dim]{entries[idx_a]['timestamp']}[/dim]", justify="center")
    table.add_column(f"Scan B\n[dim]{entries[idx_b]['timestamp']}[/dim]", justify="center")
    table.add_column("Différence", justify="center")

    changed = 0
    for port in all_ports:
        state_a = ports_a.get(port, "—")
        state_b = ports_b.get(port, "—")
        if state_a == state_b:
            diff = ""
        elif state_a == "—":
            diff = "[green]+nouveau[/green]"
            changed += 1
        elif state_b == "—":
            diff = "[red]-disparu[/red]"
            changed += 1
        else:
            diff = f"[yellow]{state_a}→{state_b}[/yellow]"
            changed += 1

        color_a = "green" if state_a == "open" else ("red" if state_a == "closed" else "white")
        color_b = "green" if state_b == "open" else ("red" if state_b == "closed" else "white")
        table.add_row(port, f"[{color_a}]{state_a}[/{color_a}]", f"[{color_b}]{state_b}[/{color_b}]", diff)

    console.print(table)
    if changed == 0:
        console.print("  [green]✔  Aucune différence détectée.[/green]")
    else:
        console.print(f"  [yellow]⚠  {changed} différence(s) détectée(s).[/yellow]")


# ── Main loop ─────────────────────────────────────────────────────────────────

def handle_scan(key: str):
    info = SCAN_TYPES[key]

    show_edu(info)

    if not Confirm.ask("  [bold]Lancer ce scan ?[/bold]", default=True):
        return

    is_ping = key == "3"
    target = ask_target(ping_scan=is_ping)
    if not target:
        console.print("  [red]Cible vide, annulé.[/red]")
        return

    ports = ""
    if info.get("needs_ports"):
        ports = ask_ports("Ports TCP (ex: 22,80,443)")
        if not ports:
            console.print("  [red]Ports vides, annulé.[/red]")
            return
    elif info.get("needs_port_range"):
        ports = ask_ports("Plage de ports (ex: 1-1024)")
        if not ports:
            console.print("  [red]Plage vide, annulée.[/red]")
            return

    args = build_args(info, target, ports)
    run_scan(args, info["label"])


def main():
    ensure_scan_dir()

    while True:
        console.clear()
        banner()
        print_menu()
        console.print()

        choice = Prompt.ask("  [bold magenta]Votre choix[/bold magenta]").strip().upper()

        if choice == "Q":
            console.print("\n  [bold red]Au revoir ![/bold red]\n")
            break
        elif choice == "H":
            show_history()
        elif choice == "C":
            compare_scans()
        elif choice in SCAN_TYPES:
            handle_scan(choice)
        else:
            console.print("  [red]Choix invalide.[/red]")

        console.print()
        Prompt.ask("  [dim]Appuyer sur Entrée pour continuer[/dim]", default="")


if __name__ == "__main__":
    main()
