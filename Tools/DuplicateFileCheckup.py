import os
import hashlib
from collections import defaultdict
from rich.console import Console
from rich.table import Table

print("\n\033[1m    🪩 --------------------------------- 🪩\033[0m")
print("\033[1m     📀  -  Duplicate File Checkup  -  📀\033[0m")
print("\033[1m    🪩 --------------------------------- 🪩\033[0m\n")

def calculate_file_hash(file_path, chunk_size=1024):
    """Calcule le hash SHA256 d'un fichier."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
    except (OSError, IOError):
        return None
    return sha256.hexdigest()

def find_duplicates_by_name(directory):
    """Trouve les fichiers en doublon dans un dossier et ses sous-dossiers en fonction du nom sans extension."""
    name_dict = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            file_name_without_extension = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)
            name_dict[file_name_without_extension].append(file_path)

    duplicates = {name: paths for name, paths in name_dict.items() if len(paths) > 1}
    return duplicates

def display_duplicates(duplicates):
    """Affiche les doublons dans un tableau coloré."""
    console = Console()
    table = Table(title="Fichiers en doublon (par nom sans extension)", show_lines=True)

    table.add_column("Nom du fichier (sans extension)", style="cyan", justify="center")
    table.add_column("Chemins", style="magenta")

    for file_name, paths in duplicates.items():
        table.add_row(file_name, "\n".join(paths))

    if duplicates:
        console.print(table)
    else:
        console.print("[bold green]Aucun doublon trouvé ![/bold green]")

if __name__ == "__main__":
    directory = input("Entrez le chemin du dossier à analyser : ")

    if os.path.isdir(directory):
        console = Console()
        console.print(f"[bold blue]Analyse du dossier :[/bold blue] {directory}")
        duplicates = find_duplicates_by_name(directory)
        display_duplicates(duplicates)
    else:
        print("[bold red]Le chemin spécifié n'est pas un dossier valide.[/bold red]")
