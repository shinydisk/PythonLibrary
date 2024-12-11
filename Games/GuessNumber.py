###########################################
#     GUESS NUMBER GAME PYTHON SCRIPT     #
###########################################

import random

# Header
print(f"\n\033[1m--------------------------------------\033[0m")
print(f"🕹️      \033[1mGUESS THE NUMBER GAME 🔢\033[0m     🕹️")
print(f"\033[1m--------------------------------------\033[0m")
print("\nI'm thinking of a number between 1 and 100... 🧠\n")

def guess_the_number():

    # Choose a random number between 1 and 100
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guessed = False

    while not guessed:
        # Ask the user to enter a number
        try:
            user_number = int(input("\nEnter your guess: "))
            attempts += 1

            # Check if the user guessed the correct number
            if user_number < number_to_guess:
                print("\n\033[1mHigher! ⬆️\033[0m")
                print("----------")
            elif user_number > number_to_guess:
                print("\n\033[1mLower! ⬇️\033[0m")
                print("---------")
            else:
                print(f"\n\n\033[1m🏆 Congratulations! 🏆\033[0m You've guessed the number \033[1m{number_to_guess}\033[0m in \033[1m{attempts}\033[0m attempts.\n")
                guessed = True
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

# Start the game
guess_the_number()