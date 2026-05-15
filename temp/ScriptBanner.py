import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from banner import print_banner

# --- Exemple d'utilisation ---
print_banner(
    name        = "Mon Script",
    description = "Ce script fait quelque chose d'utile",
    version     = "1.0",
    author      = "shinydisk",
)

print("Contenu principal du script ici...")
