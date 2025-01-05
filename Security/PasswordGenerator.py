import random
import string
import sys
import pyperclip

# Header
print(f"\n\033[1m---------------------------------\033[0m")
print(f"🔑     \033[1mPASSWORD GENERATOR\033[0m     🔑")
print(f"\033[1m---------------------------------\033[0m\n")
print(f"\n\033[93mIf you wish to leave the interaction, type 'exit'.\033[0m\n")

def get_user_preferences():
    while True:
        use_uppercase = get_yes_no_input("Do you want uppercase 🔠 letters in your password? (Y/N): ")
        use_lowercase = get_yes_no_input("Do you want lowercase 🔡 letters in your password? (Y/N): ")
        use_digits = get_yes_no_input("Do you want numbers 🔢 in your password? (Y/N): ")
        use_special = get_yes_no_input("Do you want special 🔣 characters in your password? (Y/N): ")

        if not any([use_uppercase, use_lowercase, use_digits, use_special]):
            print("\033[91m❌ Please select at least one character type.\033[0m\n")
        else:
            return use_uppercase, use_lowercase, use_digits, use_special

def get_yes_no_input(prompt):
    while True:
        answer = input_with_exit(prompt).strip().lower()
        if answer in ['y', 'n']:
            return answer == 'y'
        print("❌ \033[91mInvalid input. Please enter 'Y' for Yes or 'N' for No.\033[0m\n")

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    char_pool = ""
    if use_uppercase: char_pool += string.ascii_uppercase
    if use_lowercase: char_pool += string.ascii_lowercase
    if use_digits: char_pool += string.digits
    if use_special: char_pool += string.punctuation

    return ''.join(random.choice(char_pool) for _ in range(length)) if char_pool else ""

def evaluate_password_strength(password):
    length = len(password)
    if length < 8:
        print("👎🏽\033[91mYour password is weak.\033[0m\n")
    elif length <= 16:
        print("🤚🏽\033[93mYour password is medium.\033[0m\n")
    elif length <= 24:
        print("👍🏽\033[96mYour password is strong.\033[0m\n")
    else:
        print("🥳\033[92mYour password is robust!\033[0m\n")

def input_with_exit(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == 'exit':
        print("\033[93mExiting the Password Generator. Goodbye!\033[0m\n")
        sys.exit()
    return user_input

def password_generator():
    use_uppercase, use_lowercase, use_digits, use_special = get_user_preferences()

    while True:
        try:
            length = int(input_with_exit("\nEnter the desired length for your password: "))
            if length > 0:
                break
            print("❌ \033[91mPlease enter a positive number.\033[0m\n")
        except ValueError:
            print("❌ \033[91mInvalid input. Please enter a valid number.\033[0m\n")

    password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
    if password:
        print(f"\n\033[92mYour generated password is:\033[0m\n\033[1;44m {password} \033[0m\n")
        pyperclip.copy(password)
        print("\033[92mPassword copied to clipboard!\033[0m")
        evaluate_password_strength(password)

if __name__ == "__main__":
    password_generator()
