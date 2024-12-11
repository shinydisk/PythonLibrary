##################################################
#     ROCK PAPER SCISSORS GAME PYHTON SCRIPT     #
##################################################

import random

# Header
print(f"\n\033[1m-----------------------------------------\033[0m")
print(f"🕹️      \033[1mROCK 🪨  PAPER 📄 SCISSORS ✂️\033[0m     🕹️")
print(f"\033[1m-----------------------------------------\033[0m\n")

# Function to get the user's choice
def get_user_choice():
    while True:
        choice = input("Enter \033[1mR\033[0m for 🪨, \033[1mP\033[0m for 📄, \033[1mS\033[0m for ✂️ : ").upper()
        if choice in ['R', 'P', 'S']:
            return choice
        else:
            print("❌ \033[1mInvalid input.\033[0m Please enter R, P, or S.\n")

# Function to get the computer's choice
def get_computer_choice():
    choices = ['R', 'P', 'S']
    return random.choice(choices)

# Function to determine the winner of a round
def determine_winner(user, computer):
    if user == computer:
        return "Draw"
    elif (user == 'R' and computer == 'S') or (user == 'P' and computer == 'R') or (user == 'S' and computer == 'P'):
        return "User"
    else:
        return "Computer"

# Main function to run the game
def play_game():
    # Ask the user for the number of rounds
    while True:
        try:
            rounds = int(input("Enter the number of rounds you want to play: "))
            if rounds > 0:
                break
            else:
                print("❌ Invalid input. Please enter a positive number.\n")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.\n")

    user_score = 0
    computer_score = 0

    # Loop through the number of rounds
    for round_num in range(1, rounds + 1):
        print(f"\n\n🥊          \033[1mROUND {round_num}\033[0m            🥊")  
        print(f"----------------------------------")
        
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        
        winner = determine_winner(user_choice, computer_choice)
        
        if winner == "User":
            user_score += 1
            print("\n\033[1mYou win this round! 🟩\033[0m")
        elif winner == "Computer":
            computer_score += 1
            print("\n\033[1mComputer wins this round! 🟥\033[0m")
        else:
            print("\n\033[1mIt's a draw! 🟧\033[0m")

    # Display the final scores in the desired format
    print("\nGame Over!")
    print(f"\033[1mFinal Score:\033[0m {user_score}-{computer_score}")
    
    if user_score > computer_score:
        print(f"\n🏆 \033[1mCongratulations!\033[0m  🏆 You won the game!\n")
    elif computer_score > user_score:
        print(f"\n🖕 \033[1mComputer wins the game!\033[0m  Better luck next time! 🖕\n")
    else:
        print(f"\n🤚🏽 \033[1mThe game is a draw!\033[0m 🤚🏽\n")

# Start the game
if __name__ == "__main__":
    play_game()