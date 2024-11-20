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
# This variable may have been missed in the video
end_game = "no"
guesses_allowed = 0

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
low_num = int_check("Low number? ")
high_num = int_check("High number? ", low=low_num+1)
guesses_allowed = calc_guesses(low_num, high_num)

# Game loop starts here
while rounds_played < num_rounds:

    # Rounds headings (based on mode)
    if mode == "infinite":
        rounds_heading = f"\nRound {rounds_played + 1} (Infinite Mode) "
    else:
        rounds_heading = f"\nRound {rounds_played + 1} of {num_rounds}"

    print(rounds_heading)
    print()

    # Add one to the number of rounds played
    rounds_played += 1

    # If users are in infinite mode, increase number of rounds
    if mode == "infinite":
        num_rounds += 1

    # Guessing loop

    # Generate a secret number between the low number and high number
    secret = random.randint(low_num, high_num)
    print(f"Spoiler alert: {secret}")

    # Set guesses used to zero at the start of each round
    guesses_used = 0
    already_guessed = []

    # Initialise guess
    guess = ""

    while guess != secret and guesses_used < guesses_allowed:

        # Get user choice
        guess = int_check("Choose: ", low_num, high_num, "xxx")

        # If guess is the exit code, break the loop
        if guess == "xxx":
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

        # Print feedback to user
        print(feedback)

        # Additional feedback (warn user that they are running out of guesses
        if guesses_used == guesses_allowed - 1:
            print("\n 💣💣💣 Careful - you only have one guess left!💣💣💣\n")

print()
print("End of round")

# if end_game == "yes":
# break

# Game loop ends here

# Game history/statistics area
