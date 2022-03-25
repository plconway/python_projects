# Patrick Conway
# Compound Interest Calculator

print('Welcome to the Compound Interest Calculator')

# get Principal amount, convert to float, check for non-number entry.
# non-textbook sources:
# I was getting errors when entering strings, because I convert the input to float immediately. So i needed a way to
# send it back to the input if a string is entered. Here is where I learned about the 'ValueError' buitlin.
# https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
# Note: Loops are not covered until Chapter 5 in P4E, but I read ahead because this is a good way to do error
# checking.

while True:
    try:
        principal = float(input('Please enter the initial amount of your investment: '))
        if principal <= 0:
            print('Error. Please enter a number that is greater than zero.')
            continue
    except ValueError:
        print('Error. Please enter a number.')
        continue
    else:
        break

# get interest rate, while checking that it is between 0 and 1 and check for non-number entry.
while True:
    try:
        interest_rate = float(input("Please enter the interest rate (e.g., '.03' for 3% interest): "))
        if interest_rate > 1 or interest_rate < 0:
            print('Error. Please enter a number between 0 and 1.')
            continue
    except ValueError:
        print('Error. Please enter a number.')
        continue
    else:
        break

# Get years of investment, while checking for non number entry.
while True:
    try:
        years = float(input('Please enter the number of years for the investment:  '))
        if years <= 0:
            print('Error. Please enter a number greater than zero.')
            continue
    except ValueError:
        print('Error. Please enter a number.')
        continue
    else:
        break

# Get the compoundings for the equation while checking for non- number entries. used an integer so that only whole ...
# numbers are accepted.

while True:
    try:
        compounds = int(input('Please enter the number of compoundings per year: '))
        if compounds <= 0:
            print('Error. Please enter a whole number greater than zero.')
            continue
    except ValueError:
        print('Error. Please enter a whole number.')
        continue
    else:
        break

print('Calculating...')
print('...')
print('..')
print('.')

# Calculations
final_balance = principal * ((1 + (interest_rate/compounds))**(compounds*years))
interest = final_balance - principal

# Print results
print('Original Investment: ', '$', round(principal, 2))
print('Interest Earned:     ', '$', round(interest, 2))
print('Final Balance:       ', '$', round(final_balance, 2))
