import random
import math


# Checks users enter yes (y) or no (n)
def yes_no(question):
    while True:
        response = input(question).lower()

        # Checks user response, question
        # repeats of users don't enter yes/no
        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes/no")


def instruction():
    print('''

**** Instructions ****

To begin, choose the number of rounds and either customise
the game parameters or go with the default game (where the 
secret number will be between 1 and 100).

Then choose how many rounds you'd like to play <enter> for 
infinite mode.

Your goal is to try to guess the secret number without
running out of guesses. 

Good luck

    ''')


# Check for an integer with optional upper/lower
# limits and an optional exit code for infinite mode
# /quitting the game
def int_check(question, low=None, high=None, exit_code=None):

    # Set up error messages

    # If any integer is allowed ...
    if low is None and high is None:
        error = "Please enter an integer"

    # If the number needs to be more than an
    # integer (i.e. rounds/'high number')
    elif low is not None and high is None:
        error = (f"Please enter an integer that is"
                 f" more than/equal to {low}")

    # If the number needs to be between low and high
    else:
        error = (f"Please enter an integer that is"
                 f" between {low} and {high} (inclusive)")

    while True:
        response = input(question).lower()

        # Check for infinite mode/exit code
        if response == exit_code:
            return response

        try:
            response = int(response)

            # Check the integer is not too low
            if low is not None and response < low:
                print(error)

            # Check response is more than the low number
            elif high is not None and response > high:
                print(error)

            # If response is valid, return it
            else:
                return response

        except ValueError:
            print(error)


# Calculate the number of guesses allowed
def calc_guesses(low, high):
    num_range = high - low + 1
    max_raw = math.log2(num_range)
    max_upped = math.ceil(max_raw)
    max_guesses = max_upped + 1
    return max_guesses


# Main Routine

# Intialise game variables
mode = "regular"
rounds_played = 0
end_game = "no"
guesses_allowed = 0
feedback = ""

game_history = []
all_scores = []

print("⬆️⬆️⬆️ Higher Lower Game ⬇️⬇️⬇️")
print()

want_instructions = yes_no("Do you want to read the instructions?")

# Checks users enter yes (y) or no (n)
if want_instructions == "yes":
    instruction()

# Ask user for number of rounds/infinite mode
num_rounds = int_check("Rounds <enter for infinite>: ",
                       low=1, exit_code="")

# Video may say if num_rounds == "infinite":, this is wrong
if num_rounds == "":
    mode = "infinite"
    num_rounds = 5

# Get game parameters
# Ask user if they want to customise the number range
default_params = yes_no("Do you want to use the default game parameters? ")
if default_params == "yes":
    low_num = 0
    high_num = 10
# Allow users to choose the high/low number
else:
    low_num = int_check("Low number? ")
    high_num = int_check("High number? ", low=low_num+1)

# Calculate the maximum number of guesses based on the low and high numbers
guesses_allowed = calc_guesses(low_num, high_num)

# Master Game loop starts here (include end_game == "no" to break out of this loop)
while rounds_played < num_rounds:

    # Rounds headings (based on mode)
    if mode == "infinite":
        rounds_heading = f"\n💿💿💿 Round {rounds_played + 1} (Infinite Mode) 💿💿💿 "
    else:
        rounds_heading = f"\n💿💿💿 Round {rounds_played + 1} of {num_rounds} 💿💿💿"

    print(rounds_heading)

    # Round starts here
    # Set guesses used to zero at the start of each round
    guesses_used = 0
    already_guessed = []

    # If users are in infinite mode, increase number of rounds
    if mode == "infinite":
        num_rounds += 1

    # Choose a 'secret' number between the low number and high number
    secret = random.randint(low_num, high_num)
    # Remove this line after testing
    print(f"Spoiler alert: {secret}")

    # Initialise guess
    guess = ""

    # Add one to the number of rounds played
    rounds_played += 1

    while guess != secret and guesses_used < guesses_allowed:

        # Get user choice
        guess = int_check("Guess: ", low_num, high_num, "xxx")

        # Check that they don't want to quit
        if guess == "xxx":
            # Set end_game to yes so that the outer loop can be broken
            end_game = "yes"
            break

        # Check that guess is not a duplicate
        if guess in already_guessed:
            print(f"You've already guessed {guess}. You've *still* used "
                  f"{guesses_used} / {guesses_allowed} guesses")
            continue

        # If guess is not a duplicate, add it to the 'already guessed' list
        else:
            already_guessed.append(guess)

        # Add one to the number of guesses used
        guesses_used += 1

        # Compare the user's guess with the secret number and set up feedback statement

        # If we have guesses left ...
        if guess < secret and guesses_used < guesses_allowed:
            feedback = ("Too low, please try a higher number. "
                        f"You've used {guesses_used} / {guesses_allowed} guesses")
        elif guess > secret and guesses_used < guesses_allowed:
            feedback = ("Too high, please try a lower number. "
                        f"You've used {guesses_used} / {guesses_allowed} guesses")

        # When the secret number is guessed, we have three different
        # feedback options (lucky/'phew'/well done)
        elif guess == secret:

            if guesses_used == 1:
                feedback = "🍀 Lucky! You got it on the first guess. 🍀🍀"
            elif guesses_used == guesses_allowed:
                feedback = f"Phew! You got it in {guesses_used} guesses."
            else:
                feedback = f"Well done! You guessed the secret number in {guesses_used} guesses."

        # If there are no guesses left
        else:
            feedback = "Sorry - you have no more guesses. You lose this round"

            # add 1 to maximum number of guesses allowed for stats / score
            guesses_used = guesses_allowed + 1

        # Print feedback to user
        print(feedback)
        all_scores.append(guesses_used)

        # Additional feedback (warn user that they are running out of guesses
        if guesses_used == guesses_allowed - 1:
            print("\n 💣💣💣 Careful - you only have one guess left!💣💣💣\n")

        # ***** end of guessing loop, outdent to increase rounds *****&*&

        # Round ends here

    # If user has entered exit code - end game
    if end_game == "yes":
        break

    # Add round result to game history
    history_feedback = f"Round {rounds_played}: {feedback}"

    game_history.append(history_feedback)

    # If users are in infinite mode, increase number of rounds
    if mode == "infinite":
        num_rounds += 1

# Game loop ends here

# Check users have played at least one round
# before calculating statistics

if rounds_played > 1:
    # Game history/statistics area

    # Calculate statistics
    all_scores.sort()
    best_score = all_scores[0]
    worst_score = all_scores[-1]
    average_score = sum(all_scores) / len(all_scores)

    # Output the statistics
    print("\n📊📊📊 Statistics 📊📊📊")
    print(f"Best: {best_score} | Worst: {worst_score} | Average Score: {average_score:.2f} ")
    print()

    # Display the game history on request
    see_history = yes_no("Do you want to see your game history? ")
    if see_history == "yes":
        for item in game_history:
            print(item)

    print()
    print("Thanks for playing")

else:
    print("🐔🐔🐔 Oops - You chickened out! 🐔🐔🐔")
