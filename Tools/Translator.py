####################################
#     TRANSLATOR PYTHON SCRIPT     #
####################################

from googletrans import Translator
from langdetect import detect
from datetime import datetime

# List of the 10 most translated languages with their codes
languages = {
    'english': 'en',
    'french': 'fr',
    'spanish': 'es',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'dutch': 'nl',
    'russian': 'ru',
    'chinese': 'zh-cn',
    'japanese': 'ja'
}

# Function to detect the language of the text
def detect_language(text):
    return detect(text)

# Function to translate the text
def translate_text(text, dest_language='en'):
    translator = Translator()
    # Perform the translation
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# Function to save the original and translated text to a file
def save_to_file(original_text, translated_text):
    # Get the current date and time in the format YYYYMMDD-HHMMSS
    now_str = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"Translator-{now_str}.txt"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Original text : {original_text}\n")
        file.write(f"Translated text : {translated_text}\n")
    
    print(f"The result has been saved to the file: {filename}")

# Main function for user interaction
def main():
    print("\n\033[1m-------------------------------------\033[0m")
    print("🌍     \033[1mINTERACTIVE TRANSLATOR\033[0m     🌍")
    print("\033[1m-------------------------------------\033[0m")

    # Ask the user to enter the text to translate
    original_text = input("\n\033[1mEnter the text to translate: \033[1m")

    # Display the available languages for translation
    print("\nAvailable languages for translation:\n")
    for language, code in languages.items():
        print(f"{language.capitalize()}: {code}")
    
    # Detect the language of the text
    detected_language = detect_language(original_text)
    print(f"\n\033[1mDetected language:\033[0m {detected_language}")
    
    # Ask the user to enter the target language code
    target_language = input("\nEnter the target language code (e.g., 'en' for English, 'fr' for French) : ").strip()

    # Check if the target language code is valid
    if target_language not in languages.values():
        print(f"Invalid language code: {target_language}. Please choose a valid code.")
        return

    # Translate the text
    translated_text = translate_text(original_text, dest_language=target_language)
    
    print(f"\n\033[1mOriginal text :\033[0m {original_text}")
    print(f"\n\033[1mTranslated text :\033[0m {translated_text}")

    # Ask if the user wants to save the result to a text file
    save_option = input("\nDo you want to save the result to a text file? \033[1m(yes/no)\033[0m : ").strip().lower()
    if save_option in ['yes', 'oui']:
        save_to_file(original_text, translated_text)

if __name__ == "__main__":
    main()
