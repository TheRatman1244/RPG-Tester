# python rpg tester V0.1

worldMap = [ # in the map, 0 = movable space, 1=wall, 2=npc
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,0],
    [0,0,1,0,0,1,0,1,0,0,0,1,0,0,1,0],
    [0,0,1,0,1,1,0,1,0,0,0,1,0,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0],
    [0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0],
    [0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0],
    [0,0,0,1,0,2,1,0,0,1,0,0,0,1,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]

allowedTurns = ["N","S","E","W","I"] # this program uses a list of allowed moves for easier checking

with open("Python-Projects/Knight.txt") as f:
    knight = f.read()

fileToOpen = "Python-Projects/NPCTester.txt"
f = open(fileToOpen)
fileOpen = False

playerX = 4 # the player spawns at the position (4,2)
playerY = 2 # due to how arrays work, the y has to go first (e.g. example map[y][x])

moveError = False
nextToNPC = False
NPCDialogue = False
displayMap = True
displayNPC = False

def movePlayer():
    global playerY, playerX, worldMap, allowedTurns, moveError, nextToNPC,NPCDialogue
    global displayNPC, displayMap, fileOpen

    move = str(input("move N/S/E/W\n>>>"))
    move = move.upper() # allows for both upper and lower case input without errors
    if move in allowedTurns: # checks to see if the move is in the list
        if move == "N": # if the player chooses to go north, go north
            if playerY-1 >= 0: # checks to see that the move won't take the player out of the array
                if worldMap[playerY-1][playerX] == 0: # checks to see if the next tile is movable
                    playerY -= 1 
                    moveError = False # no movement error
                else:
                    moveError = True
            else:
                moveError = True # if there is any issue, it is classed as a move error
        elif move == "S": # the same comments apply for the rest of the directions
            if playerY+1 < len(worldMap):
                if worldMap[playerY+1][playerX] == 0:
                    playerY += 1
                    moveError = False
                else:
                    moveError = True
            else:
                moveError = True
        elif move == "W":
            if playerX-1 >= 0:
                if worldMap[playerY][playerX-1] == 0:
                    playerX -= 1
                    moveError = False
                else:
                    moveError = True
            else:
                moveError = True
        elif move == "E":
            if playerX+1 < len(worldMap[0]):
                if worldMap[playerY][playerX+1] == 0:
                    playerX += 1
                    moveError = False
                else:
                    moveError = False
            else:
                moveError = False
            
    else:
        moveError = False

    # checks to see if the player is touching an npc
    if worldMap[playerY-1][playerX] == 2: # checks ahead
        nextToNPC = True
    elif worldMap[playerY+1][playerX] == 2: # checks below
        nextToNPC = True
    elif worldMap[playerY][playerX-1] == 2: # checks to the left
        nextToNPC = True
    elif worldMap[playerY][playerX+1] == 2: # checks to the right
        nextToNPC = True
    else:
        nextToNPC = False

    # if the player is next to an npc, stop displaying map, display npc and npc dialogue
    if nextToNPC and move == "I":
        NPCDialogue = True
        displayNPC = True
        displayMap = False
        fileOpen = True
        
    else: # otherwise, display map and don't display anything else
        NPCDialogue = False
        displayMap = True
        displayNPC = False
        fileOpen = False
        
def realMapToTemp():
    global worldMap
    # the player's location is saved as an X
    tempList = [] # make a temporary list to save the row
    tempMap = [] # make a temporary map to save the rows
    for i in range(len(worldMap)):
        tempList = [] # clear the temporary list for each row
        for e in (worldMap[i]):
            if e == 0: # if a movable tile, make is a comma
                tempList.append(",")
            elif e == 1: # if a wall, make it a hashtag
                tempList.append("#")
            elif e == 2: # if an npc, make it a smiley face
                tempList.append("☺")
        tempMap.append(tempList)
    return tempMap # return the new array

        
def printMap(Map):
    x = 0 # set counter to zero 
    while x < len(Map): # while counter is less than the amount of rows in the map, repeat
        print(*tempMap[x], sep=" ") # print the row while seperating each item with a space
        x += 1 # increase counter by one


def choice(): 
    option = 0 # clear the option
    print("choose what you do:")
    option = input(">>> ")
    # if the option is not within the range, prompt the player until it is
    if int(option) < 0 or int(option) > 100: 
        while option < 0 or option > 100:
            option = input(">>> ")

    return option # return the option

def openFile():
    global fileToOpen, fileOpen
    x = [] # x is a list that holds all of the options for the question
    lineList =[] # this is a list that saves all of the lines to print
    pathOne = [] # set up the divergent paths, 1 and 2
    pathTwo = []
    fileOpen = False # do not open the file yet

    with open(fileToOpen) as file: # make a list, lines, that holds each line
        lines = [line.rstrip() for line in file]

    for i in range(len(lines)):
        # this is to check if the player should be speaking
        if "-" in lines[i]:
            translation_table = dict.fromkeys(map(ord, '-'), None)
            lines[i] = lines[i].translate(translation_table)
            lineList.append("player: {}".format(lines[i]))
        # this is to check if the npc is asking a question
        elif lines[i][0] == "^":
            translation_table = dict.fromkeys(map(ord, '^'), None)
            lines[i] = lines[i].translate(translation_table)
            lineList.append("question: {}".format(lines[i]))

        # this is to check if the line is an option for a question
        elif lines[i][0] == "#":
            translation_table = dict.fromkeys(map(ord, '#'), None)
            lines[i] = lines[i].translate(translation_table)
            x.append(i) # add line adress to x
            lineList.append(lines[i])
        
        # these are to decide the player path (one or two)
        elif lines[i][0] == "1":
            translation_table = dict.fromkeys(map(ord, '1'), None)
            lines[i] = lines[i].translate(translation_table)
            pathOne.append(i)
            lineList.append(lines[i])
        elif lines[i][0] == "2":
            translation_table = dict.fromkeys(map(ord, '2'), None)
            lines[i] = lines[i].translate(translation_table)
            pathTwo.append(i)
            lineList.append(lines[i])
        # if the line has no formatting, it is from the npc
        else:
            lineList.append("NPC: {}".format(lines[i]))
        

    for i in range(len(lineList)): # for i in the amount of lines, loop
        if i-1 == x[len(x)-1]: # if i is at the end of the question options, prompt for a choice
            option = choice()
            if int(option) > len(x):
                while int(option) > len(x):
                    option = choice()

        if i in pathOne: # if the player chooses option one, print path one
            if option == "1":
                print(lineList[i])
        elif i in pathTwo: # if the player otherwise chooses option two, print path two
            if option == "2":
                print(lineList[i])
        else: # else, print off the regular line
            print(lineList[i])

play = True # this initialises the main game loop

while play: # main game loop
    tempMap = realMapToTemp()
    tempMap[playerY][playerX] = "X" # this sets the player location to x on the temporary map
    
    for i in range(100): # this writes 100 lines to "clear" the screen for the player
        print("")

    if displayMap: # if it says to display the map, display it
        printMap(tempMap)
    elif displayNPC: # otherwise, try to display the npc
        print(knight)
        if fileOpen:
            openFile()
            fileOpen = False


    if moveError: # if there is an error in trying to move
        print("you need to make a valid move.")
    if nextToNPC: # if the player is next to an npc, tell the player
        print("there is an NPC, type 'I' to interact")
    
    movePlayer() # excecute the code to move the player
