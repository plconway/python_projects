# Based on code by Prof. David Gotz. Modified by Sayamindu Dasgupta.

# TO-DOS: ensure that ID is entered for CI and CO functions.


# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
def load_collections():
    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")

    # Check for error.
    if book_collection is None or movie_collection is None:
        return (None, None)

    # Return the composite dictionary.
    return {"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)


# Loads a single collection and returns the data as a list.  Upon error, None is returned.
def load_collection(file_name):
    try:
        collection_file = open(file_name, "r")
        # Catch different types of errors
        # Each of the two except blocks below catches two
        # different types of errors.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return (None, None)
    except IOError:
        print("Error in data file when reading", file_name)
        return (None, None)

    max_id = -1
    # Create an empty collection.
    collection = []

    # Open the file and read the field names
    field_names = collection_file.readline().rstrip().split(",")

    # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
    for item in collection_file:
        field_values = item.rstrip().split(",")
        collection_item = {}
        for index in range(len(field_values)):
            if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                collection_item[field_names[index]] = int(field_values[index])
            else:
                collection_item[field_names[index]] = field_values[index]
        # Add the full item to the collection.
        collection.append(collection_item)
        # Update the max ID value
        max_id = max(max_id, collection_item["ID"])

    # Close the file now that we are done reading all of the lines.
    collection_file.close()

    # Return the collection.
    return collection, max_id


# START OF plconway's CODE

# I frequently use the  '.find()' function which returns a '-1' if the string is not contained in the larger string.
# In my check_in, check_out, and query functions I  am searching through each item in the collection, as a string,
# to see if it contains the query.
#  http://net-informations.com/python/basics/contains.htm


# this function gathers an input, and ensures that it is a 5 digit number.
# it will then search the collection dictionary and if the ID number is found, it will then check the availability
# by subtracting the available from the copies. If it is 0, it will give an error saying all the copies are in stock.
# otherwise, it will add one to the available copies and print the collection information.
# there is also a results counter that will go up if an item  is found. If it is still zero, it will alert the user and
# return the menu. I do this because I gather input before checking the collection, so i can only account for so much
# user input errors.
def check_in(collection):
    while True:
        try:
            item = int(input('Please enter the ID of the item you want to check in: '))
            if len(str(item)) != 5:
                print('Error. Please enter a 5 digit ID Number.')
                continue
        except ValueError:
            print('Error. Please enter a valid ID number.')
            continue
        else:
            break
    item = str(item)
    counter = 0
    results = 0
    while counter < len(collection):
        if str(collection[counter].values()).find(item) != -1:
            results = results + 1
            if float(collection[counter]['Copies']) - float(collection[counter]['Available']) == 0:
                print('Error. All copies are currently in stock, so this item can not be checked in.')
            else:
                print('Your checkin request has been successfully processed.', '\n')
                collection[counter]['Available'] = int(collection[counter]['Available']) + 1
                for key, value in collection[counter].items():
                    print(key, ':', value)
        counter = counter + 1
    if results == 0:
        print()
        print('Error. The ID number you entered could not be found. Returning to main menu.')


# this is a similar process to the check_in function. the main difference is that when the ID is located, it checks
# the 'available' slot to ensure that it is available. if it is '0' then all copies are currently checked out, otherwise
# the function subtracts 1 from copies and prints the collection info.
def check_out(collection):
    while True:
        try:
            item = int(input('Please enter the ID of the item you want to check out: '))
            if len(str(item)) != 5:
                print('Error. Please enter a 5 digit ID Number.')
                continue
        except ValueError:
            print('Error. Please enter a valid ID number.')
            continue
        else:
            break
    item = str(item)
    counter = 0
    results = 0
    while counter < len(collection):
        if str(collection[counter].values()).find(item) != -1:
            results = results + 1
            if float(collection[counter]['Available']) == 0:
                print('Error. There are no copies available for checkout.')
            else:
                print('Your checkout request has been successfully processed.', '\n')
                collection[counter]['Available'] = int(collection[counter]['Available']) - 1
                for key, value in collection[counter].items():
                    print(key, ':', value)
        counter = counter + 1
    if results == 0:
        print('Error. The ID number you entered could not be found. Returning to menu.')


# input is a list that is a list of dictionaries
# accept a user input, then search through the .values() of a dictionary. if it exists, print the key/value pairs.
# results error will trigger if counter is 0.
def query_collection(collection):
    query = input('Please enter a query to use for the search: ')
    print()
    counter = 0
    results = 0
    while counter < len(collection):
        if str(collection[counter].values()).find(query) != -1:
            results = results + 1
            for key, value in collection[counter].items():
                print(key, ':', value)
            print()
        counter = counter + 1
    # after searching the entire collection, if nothing has found an error message will be printed.
    if results == 0:
        print('No results found. Returning to main menu.')


# This function uses the items() function to print each key & value in a given collection.
# I use the modulo function to only print results
# https://www.codegrepper.com/code-examples/python/press+enter+to+continue+python
def display_collection(collection):
    counter = 0
    while counter < len(collection):
        for key, value in collection[counter].items():
            print(key, ':', value)
        if counter == 0:
            pass
        elif counter % 10 == 0:
            print()
            user_input = input("Press 'Enter' to see more items, or type 'm' to return to the menu. ")
            if user_input == 'm':
                return
        print()
        counter = counter + 1

# created a new dictionary, each value will be a user input.
# available initially is set to 0, will be the same as the copies.
# ID is a string of the max id + 1
def add_movie(collection, max_id):
    print('Please enter the following attributes for the new movie.')
    newmovie = {'Title': input('Title: '),
                'Director': input('Director: '),
                'Length': input('Length: '),
                'Genre': input('Genre: '),
                'Year': input('Year: '),
                'Copies': input('Copies: '),
                'Available': 0,
                'ID': str(max_id + 1)
                }
    newmovie['Available'] = newmovie['Copies']
    print('You have entered the following data:')
    # while counter < len(newbook):
    for key, value in newmovie.items():
        print(key, ':', value)
    print()
    user_input = input("Press enter to add this item to the collection. Type 'x' to cancel")
    if user_input == 'x':
        return
    collection.append(newmovie)
    max_id = newmovie['ID']
    return max_id

# sae as add_movie function
def add_book(collection, max_id):
    print('Please enter the following attributes for the new book.')
    newbook = {'Title': input('Title: '),
               'Author': input('Author: '),
               'Publisher': input('Publisher: '),
               'Pages': input('Pages: '),
               'Year': input('Year: '),
               'Copies': input('Copies: '),
               'Available': 0,
               'ID': str(max_id + 1)
               }
    newbook['Available'] = newbook['Copies']
    print('You have entered the following data:')
    for key, value in newbook.items():
        print(key, ':', value)
    print()
    user_input = input("Press enter to add this item to the collection. Type 'x' to cancel")
    if user_input == 'x':
        return
    collection.append(newbook)
    max_id = newbook['ID']
    return max_id


# Display the menu of commands and get user's selection.  Returns a string with  the user's executed command.
def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND    FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  x          Exit")
    return input("Please enter a command to proceed: ")


# This is the main program function.  It runs the main loop which prompts the user and performs the requested actions.
def main():
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()
    books, books_max_id = load_collection('books.csv')
    movies, movies_max_id = load_collection('movies.csv')
    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")
    combined = library_collections['books'] + library_collections['movies']

    # Display the error and get the operation code entered by the user.  We perform this continuously until the
    # user enters "x" to exit the program.  Calls the appropriate function that corresponds to the requested operation.
    operation = prompt_user_with_menu()
    while operation != "x":
        if operation == "ci":
            check_in(combined)
        elif operation == "co":
            check_out(combined)
        elif operation == "ab":
            print()
            books_max_id = add_book(library_collections["books"], books_max_id)
            # update the combined variable with the newly appended book.
            combined = library_collections['books'] + library_collections['movies']
        elif operation == "am":
            print()
            movies_max_id = add_movie(library_collections["movies"], movies_max_id)
            combined = library_collections['books'] + library_collections['movies']
        elif operation == "db":
            print()
            display_collection(library_collections["books"])
        elif operation == "dm":
            print()
            display_collection(library_collections["movies"])
        elif operation == "qb":
            query_collection(library_collections['books'])
        elif operation == "qm":
            query_collection(library_collections['movies'])
        else:
            print("Unknown command.  Please try again.")

        operation = prompt_user_with_menu()


# Run the program#
main()
