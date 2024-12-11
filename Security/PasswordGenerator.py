############################################
#     PASSWORD GENERATOR PYTHON SCRIPT     #
############################################

import random
import string

# Header
print(f"--------------------------------")
print(f"🔑     \033[1mPASSWORD GENERATOR\033[0m     🔑")
print(f"--------------------------------\n")

# Function to get user preferences for the password
def get_user_preferences():
    # Asking user if they want uppercase letters in the password
    use_uppercase = get_yes_no_input("Do you want uppercase 🔠 letters in your password? (Y/N): ")
    # Asking user if they want lowercase letters in the password
    use_lowercase = get_yes_no_input("Do you want lowercase 🔡 letters in your password? (Y/N): ")
    # Asking user if they want digits in the password
    use_digits = get_yes_no_input("Do you want numbers 🔢 in your password? (Y/N): ")
    # Asking user if they want special characters in the password
    use_special = get_yes_no_input("Do you want special 🔣 characters in your password? (Y/N): ")
    
    return use_uppercase, use_lowercase, use_digits, use_special

# Function to validate yes/no input from the user
def get_yes_no_input(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ['y', 'n']:
            return answer == 'y'
        else:
            print("❌ Invalid input. Please enter 'Y' for Yes or 'N' for No.\n")

# Function to generate the password based on user preferences
def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special):
    # Available character sets based on user preferences
    char_pool = ""
    
    if use_uppercase:
        char_pool += string.ascii_uppercase  # Uppercase letters
    if use_lowercase:
        char_pool += string.ascii_lowercase  # Lowercase letters
    if use_digits:
        char_pool += string.digits           # Digits
    if use_special:
        char_pool += string.punctuation      # Special characters
    
    # If no character set is chosen, inform the user and exit
    if not char_pool:
        print("\nNo character type selected. Please select at least one option.")
        return ""
    
    # Generate password by randomly selecting from the chosen character pool
    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password

# Function to evaluate password strength
def evaluate_password_strength(password):
    length = len(password)
    
    if length < 8:
        print("Your password is weak. It is less than 8 characters long.")
    elif 8 <= length <= 16:
        print("Your password is medium strength. Consider increasing the length for better security.")
    elif 17 <= length <= 24:
        print("Good job! Your password is of good strength.")
    else:
        print("Congratulations! Your password is strong and robust!")

# Main function to run the password generator
def password_generator():
    # Get user preferences
    use_uppercase, use_lowercase, use_digits, use_special = get_user_preferences()
    
    # Ask user for desired password length
    while True:
        try:
            length = int(input("Enter the desired length for your password: "))
            if length > 0:
                break
            else:
                print("❌ Please enter a positive number.\n")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.\n")
    
    # Generate password
    password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
    
    # If a valid password is generated, display it and evaluate its strength
    if password:
        print(f"\n{password}\n")
        evaluate_password_strength(password)

# Start the password generator
if __name__ == "__main__":
    password_generator()
