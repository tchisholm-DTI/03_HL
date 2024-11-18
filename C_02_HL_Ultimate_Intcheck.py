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


# Main Routine goes here

rounds = "test"
while rounds != "":
    rounds = int_check("Rounds <enter for infinite>: ", low=1, exit_code="")
    print(f"You asked for {rounds}")

# Check for low number
low_num = int_check("Low number? ")
print(f"You chose a low number of {low_num}")

# Check for high number
high_num = int_check("High number? ", low=1)
print(f"You chose a high number of {high_num}")

# Check user guesses
guess = ""
while guess != "xxx":
    guess = int_check("Guess: ", low=0, high=10, exit_code="xxx")
    print(f"You guessed: {guess}")
    print()
