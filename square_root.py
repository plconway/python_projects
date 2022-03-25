# Patrick Conway
# Square Root Calculator

# to-do's:


# Ask the user if they want to calculate the square root for a single value or a range of values.
# If range... User inputs the minimum value, then the maximum value. It will then calculate the square root
# for each of the integers in the range and their square roots. Rounded to 3 decimal places.
# use the range() function and round() function.
# I will use the range function in this, it stops before the final number, so I will need to add one to my maximum.
# https://www.w3schools.com/python/ref_func_range.asp


# This function will determine the range, when 'range' is entered in the main loop.
# use modified error checking loop used in all previous assignments.
# Returns a range
def get_range():
    while True:
        try:
            minimum = int(input('Enter a positive integer to start your range: '))
            if minimum < 0:
                print('Error. You must enter a number greater than zero.')
                continue
            else:
                minimum = minimum
                break
        except ValueError:
            print('Error. You must enter a number.')
    while True:
        try:
            maximum = int(input('Enter a positive integer to end your range: '))
            if maximum < 0:
                print('Error. You must enter a number greater than zero.')
                continue
            if maximum <= minimum:
                print('Error. You must enter a number greater than the minimum you previously entered.')
                continue
            else:
                # add one to set an upper limit on the range() function.
                maximum = maximum + 1
                break
        except ValueError:
            print('Error. You must enter a number.')
    input_range = range(minimum, maximum)
    return input_range

# if single integer...

# Prompt the user to enter an integer above zero. Do error checking to ensure it is an integer and positive.
# this will be triggered in the main loop, if the user selects 'integer'
# returns a single integer for calculations.
def get_integer():
    while True:
        try:
            single = int(input('Enter a positive integer: '))
            if single < 0:
                print('Error. You must enter a number greater than zero.')
                continue
            else:
                return single
        except ValueError:
            print('Error. You must enter a number.')


# Compute the square value using the babylonian method, round the answer to 3 decimal places.
# complete the calculations for one integer.
#  If a range is selected, then a for loop can be used to iterate through it in main function.

# i need to check my 'guess' with the 'answer, and if they are the same i can quit

# will return an integer that is 'close enough' when guess is close to answer
def get_sqrt(int):
    # set up initial values, as well as an initial guess. intital guess = .1, created a larger number then does the
    # calculations. This is inefficient but it helps with perfect squares 1 and 2.
    initial = int
    guess = initial/.1
    # start a loop to keep checking that guess * guess does not equal the initial.
    while True:
        if guess * guess == initial:
            # print('Success.')
            # assign the result to sqrt
            sqrt = guess
            return sqrt
        else:
            # create a new guess that is the average of the previous guess and the initial value by the current guess
            new_guess = (guess + initial/guess) / 2
            # compare guess to previous, if they are close enough by the set threshold, return the sqrt as the new guess.
            if guess - new_guess <= .0001:
                sqrt = new_guess
                # round the answer to 3 decimal places
                sqrt = round(sqrt, 3)
                return sqrt
            # otherwise continue until the threshold is met, update the guess to the value of the failed guess, so
            # that it can be averaged
            else:
                guess = new_guess
            continue

# create a function that asks the user to input 'single' or 'range' to calculate.
# use an embedded try/except to ensure there is a string entered, similar to error checking loop from assignemnt 2/3
# will return a string that is used in the main function.
def get_choice():
    while True:
        try:
            choice = str(input("Enter 'single' or 'range' to solve for a single square root or a range, respectively: "))
            # need to check for case errors, could be all caps, mix, etc.
            # https://www.geeksforgeeks.org/isupper-islower-lower-upper-python-applications/
            if choice.lower() == 'single':
                choice = 'single'
                return choice
            if choice.lower() == 'range':
                choice = 'range'
                return choice
            else:
                print('Error. This string is not recognized. Try again.')
                continue
        except ValueError:
            print('Error. Please enter a string.')
            continue

# create a main function that welcomes the user,
# asks if they want single or range - get_choice()
# if single, calculate square root and print result - get_integer(), get_sqrt()
# if range, use a for loop to iterate for each in range - get_range(), get_sqrt() with a for loop
# print results nicely formatted.

def main():
    print('Welcome to the square root calculator!','\n')
    choice = get_choice()
    if choice == 'single':
        number = get_integer()
        sqrt = get_sqrt(number)
        print('Number:       Square Root:')
        print(number,'          ',sqrt)
    if choice == 'range':
        range = get_range()
        print('Number:      Square Root:')
        for number in range:
            range_item = get_sqrt(number)
            print(number,'          ',range_item)

main()
