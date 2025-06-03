import subprocess
from telegram import Bot

# Remplace par le token de ton bot et ton chat_id
BOT_TOKEN = "7987390047:AAFovuo7C3hPWWqWp1XnTQ2md7rzDehjHbQ"
CHAT_ID = "2572646976"

def get_outdated_brews():
    result = subprocess.run(["brew", "outdated"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def send_message(message):
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    outdated = get_outdated_brews()
    if outdated:
        message = "🧪 Paquets Homebrew à mettre à jour :\n\n" + outdated
    else:
        message = "✅ Tous les paquets Homebrew sont à jour !"
    send_message(message)

if __name__ == "__main__":
    main()
