# Patrick Conway
# INLS 560 - Assignment 3 - Recommended Dietary Allowance

# to-dos: determine if calculating calcium could be more efficient.

# Prompt the user to enter age. The prompts should be obvious. Will return the individual's age in years.
# Using a modified error checking loop I used in assignment 2.
# returns a float of the users age for use in the 'calculate_calcium' function.
def get_age():
    while True:
        try:
            age = float(input('Please enter the age of the individual in years: '))
            if age < 0:
                print('Error. You must enter a number greater than zero.')
                continue
            if age > 100:
                print('Error.')
                continue
            else:
                return age
        except ValueError:
            print('Error. You must enter a number.')


# Prompt the user to enter sex. the prompts should be obvious.
# Using a modified error checking loop that I used in assignement 2.
# returns a string that is either 'male' or 'female'
def get_sex():
    while True:
        try:
            sex = str(input('Please enter the sex of the individual ("M" for male, "F" for female): '))
            if len(sex) > 1:
                print('Error. Please enter a one-character string.')
                continue
            if sex == 'M' or sex == 'm':
                # assign a string for output.
                sex = 'male'
                return sex
            if sex == 'F' or sex == 'f':
                # assign a string for output.
                sex = 'female'
                return sex
            else:
                print('Error. This string is not recognized. ')
                continue
        except ValueError:
            print('Error. Please enter a string.')


# Determine the recommended daily allowance of calcium based on the provided chart.
# The inputs will be age, sex, and a true/false value determined by while loop in main function.
# will return a formatted string with the determined values.
def calculate_calcium(age, sex, pregnant):
    calcium = str()
    calcium_formatted = str()
    # convert age to months for calculations, this might be solved a more effecient way but want to capture
    #
    age_inmonths = age * 12
    if age_inmonths <= 6:
        calcium = '200'
    if 6 < age_inmonths < 12:
        calcium = '260'
    if 12 <= age_inmonths <= 47:
        calcium = '700'
    if 48 <= age_inmonths <= 107:
        calcium = '1000'
    if 108 <= age_inmonths <= 167:
        calcium = '1300'
    if 168 <= age_inmonths <= 227 and pregnant == True:
        calcium = '1300'
    if 168 <= age_inmonths <= 227 and pregnant == False:
        calcium = '1300'
    if 228 <= age_inmonths <= 612 and pregnant == True:
        calcium = '1000'
    if 228 <= age_inmonths <= 612 and pregnant == False:
        calcium = '1000'
    if 612 <= age_inmonths <= 852 and sex == 'male':
        calcium = '1000'
    if 612 <= age_inmonths <= 852 and sex == 'female':
        calcium = '1200'
    if age_inmonths >= 852:
        calcium = '1200'
    # round age for printing purposes
    # change to integer to remove the decimal point
    age = int(age)
    age = str(age)
    sex = str(sex)
    age_inmonths_string = str(int(age_inmonths))
    # use '+' signs to combine this all into one string. was getting a funky output when using commas. why?
    # https://stackoverflow.com/questions/21542694/ this made it very clear to me.
    # pregnant = false, a default value is given in Main, only the prompt will change it.
    # this is the first if checker, will return a properly formatted string taking into consideration they are an infant.
    if age_inmonths < 12:
        calcium_formatted = calcium_formatted = 'Recommended daily allowance of calcium for a ' + age_inmonths_string + ' month old ' + sex + ' is ' + calcium + ' milligrams per day.'
        return calcium_formatted
    # this is the second if checker, if it makes it passed the age chekcer, the user is either pregnant or not and this
    # returns the proper string.
    if pregnant == False:
        calcium_formatted = 'Recommended daily allowance of calcium for a ' + age + ' year old ' + sex + ' is ' + calcium + ' milligrams per day.'
    elif pregnant == True:
        calcium_formatted = 'Recommended daily allowance of calcium for a ' + age + ' year old ' + sex + ' that is pregnant or lactating is ' + calcium + ' milligrams per day.'
    return calcium_formatted


# Source: I couldn't figure out why I was unable to access variables outside of the function. I would define them within
# a function, and then try to print the results and it would give me an 'Undefined' error. After some googling I
# discovered global variables. https://book.pythontips.com/en/latest/global_&_return.html. I'm not sure if this
# is an appropriate use of them, however.
# edit: I removed global variables, everything is done in the main function.
def main():
    print('Welcome to the Recommended Daily Allowance for Calcium calculator.')
    print()
    calculated_age = get_age()
    calculated_sex = get_sex()
    # assign a default value of value so the 'calculate_calcium' function has an input. will be changed in the loop to true
    # if the input is female. This is here because it is possible that the following while loop can be bypassed
    # if the user input is male.
    is_pregnant = False
    while calculated_sex == 'female' and 14 <= calculated_age <= 50:
        try:
            pregnant = input('Are you pregnant or lactating? Enter "Y" for yes or "N" for no. ')
            try:
                if pregnant == type(int) or pregnant == type(float):
                    print('Please enter a string.')
                    continue
                if len(pregnant) > 1:
                    print('Error. Please enter a 1 digit string.')
                    continue
                if pregnant == 'y' or pregnant == 'Y':
                    is_pregnant = True
                    break
                if pregnant == 'n' or pregnant == 'N':
                    is_pregnant = False
                    break
                else:
                    print('Error. That string is not recognized.')
                    continue
            except ValueError:
                print('Error. Please try again.')
        except ValueError:
            print("Error. How'd you manage this?")
    # output will be a properly formatted string that takes into account asked and checked age, asked and checked sex
    # and their pregnancy status. reminder: is_pregnant is defaulted to male, can be changed in this function.
    output = calculate_calcium(calculated_age, calculated_sex, is_pregnant)
    print('')
    print('Calculating...')
    print('')
    print(output)

main()