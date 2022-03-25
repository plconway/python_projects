# INLS 570 - Project 1 - Adventure!
# Patrick Conway

# This project is a simple, text-based adventure game. It is based on the importing of a configuration file.

# import pretty print for development purposes.
import pprint as pp


# Function that reads an import file and creates a data structure of the map.
def CreateMap():
    map = {}
    # while True:
    #     try:
    #         file = open(input('Please enter the name of the configuration file: '),'r')
    #         break
    #     except FileNotFoundError:
    #         print('File not found! Try again. ')
    file = open('game1.txt', 'r')
    # create an empty list. each line will be read, split by its ':' and turned into a list.
    # lines will become a list of lists that will then be read and turned into a dictionary.
    lines = []
    for line in file:
        lines.append(line.strip().split(':'))
    # initialize counter at 0. This means that the first information in the configuration file will be capture as a
    # key:value pair.
    square = 0
    for item in lines:
        # if the item is dashes, increment the counter, that will allow each game square to be its own entry in the
        # dictionary with the key being the square and the value being a list of attributes associated with it.
        if item[0] == '---':
            square += 1
        # if the file has not read dashes yet, then game information is being read.
        # these are stored as k:v pairs in the main dictionary.
        elif square == 0:
            map.setdefault(item[0], item[1].lstrip())
        # if dashes are read, then the square gets added as a key, and the attributes are a dictionary within the main
        # dictionary.
        elif square != 0:
            if square not in map:
                # turn every attribute into a list. because objects and items are movable, this makes sense.
                map.setdefault(square, {item[0]: [item[1].lstrip()]})
                # set a default for the object. Not every square has this, so an empty list should be created.
                map[square].setdefault('r_obj', [])
            else:
                map[square][item[0]] = [item[1].lstrip()]
    return map


def MoveLocation(oldLocation, direction, y_axis, x_axis, size):
    new_location = int()
    if direction == 'east':
        # need to determine whether current location is on the edge of the map, otherwise it needs to loop back
        if oldLocation % x_axis == 0:
            new_location = oldLocation - x_axis + 1
        else:
            new_location = oldLocation + 1
    elif direction == 'west':
        if (oldLocation - 1) % x_axis == 0:
            new_location = oldLocation + x_axis - 1
        else:
            new_location = oldLocation - 1
    elif direction == 'north':
        new_location = oldLocation - x_axis
        if new_location <= 0:
            new_location = oldLocation + 2 * x_axis
    elif direction == 'south':
        new_location = oldLocation + x_axis
        if new_location > size:
            new_location = oldLocation - 2 * x_axis

    return new_location


def PlayGame(map):
    # print welcome message
    print('Game Loaded: ', map['game_name'])
    print('The goal of this game is to: ', map['game_goal'])
    # read the map file and set the game variables. Size, movement calculations, etc..
    directions = ['north', 'south', 'east', 'west']
    height = int(map['game_ysize'])
    width = int(map['game_xsize'])
    area = (int(map['game_xsize']) * (int(map['game_ysize'])))
    goal_location = int(map['game_goalloc'])
    # set starting location, this will change based on commands.
    location = int(map['game_start'])
    player_inventory = []
    while True:
        # check for winning condition
        if map[goal_location]['r_obj'] == [map['game_goalobj']]:
            print('Congratulations!', '\n')
            print('You delivered the', map[goal_location]['r_obj'][0], 'to the proper person!', '\n')
            return print('You Win!')
        print('You are', map[location]['r_desc'][0])
        # if the object list is not empty, print the object.
        # This resource was very helpful in solving this problem: https://flexiple.com/check-if-list-is-empty-python/
        if bool(map[location]['r_obj']):
            quantity = len(map[location]['r_obj'])
            for i in range(quantity):
                print('There is', map[location]['r_obj'][i], 'here')
        # if a path has been discovered, print that there's a path. otherwise(keyerror), do nothing.
        try:
            if bool(map[location]['path_discovered']):
                print('You have discovered a secret path!')
        except KeyError:
            pass
        print('What would you like to do?')
        command = input('------> ')
        # exit quits the game
        if command.lower() == 'exit':
            return print('Game exited. Thank you for playing!')
        # inventory prints
        elif command.lower() == 'inv':
            print('Your current inventory is: ', player_inventory, '\n')
        # print the goal of the game
        elif command.lower() == 'goal':
            print('The goal of the game is to: ', map['game_goal'], '\n')
        # search for hidden objects and paths
        elif command.lower() == 'search':
            print('searching...', '\n')
            try:
                print('You found a', map[location]['r_hiddenobj'][0] + '!', '\n')
                map[location]['r_obj'].append(map[location]['r_hiddenobj'][0])
                # delete hidden items after appending it to inventory
                del (map[location]['r_hiddenobj'])
            except KeyError:
                print('There are no hidden items.', '\n')
            try:
                # if a hidden path exists, add the location it goes to as a new entry in the dictionary as a discovered
                # path. otherwise, do nothing.
                map[location]['path_discovered'] = int(map[location]['r_hiddenpath'][0])
                print('you found a hidden path!', '\n')
            except KeyError:
                pass
        elif len(command.split()) == 2:
            verb = command.split()[0]
            object = command.split()[1]
            # move function
            if verb.lower() == 'move' and object.lower() in directions:
                # create a directional trigger and see if it exists in the location, if so, take it.
                try:
                    trigger = 'r_' + str(object.lower())
                    location = int(map[location][trigger][0])
                # otherwise (key doesnt exist), perform the move function and return the location, starting up top
                # again.
                except KeyError:
                    location = MoveLocation(location, object, height, width, area)
            # move to the path location, only if it has already been discovered.
            elif verb.lower() == 'move' and object.lower() == 'path':
                try:
                    location = int(map[location]['path_discovered'])
                except KeyError:
                    print('no hidden path')
            # i use the 'index()' method in this section. I don't know if it was covered in class but this site made
            # it easy to understand. I use it if there are multiple items in a spot or inventory
            # https://appdividend.com/2019/11/16/how-to-find-element-in-list-in-python/
            elif verb.lower() == 'take' and object not in directions:
                if object in map[location]['r_obj']:
                    index = map[location]['r_obj'].index(object)
                    player_inventory.append(map[location]['r_obj'][index])
                    map[location]['r_obj'].pop(index)
                else:
                    print('There is not a', object, 'here to take.', '\n')
            elif verb.lower() == 'drop' and object not in directions:
                if object in player_inventory:
                    index = player_inventory.index(object)
                    map[location]['r_obj'].append(player_inventory[index])
                    player_inventory.pop(index)
                else:
                    print('You do not have a', object, 'in your inventory!', '\n')

            else:
                print('Error! That is an invalid command. Please try again.')
        else:
            print('Error! That is an invalid command. Please try again.')


def main():
    map = CreateMap()
    #pp.pprint(map)
    PlayGame(map)


main()
