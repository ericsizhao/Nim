#CHECKED
#Function Purpose - protects input for integers
#phrase - (String): line that will be printed to ask for variable
#lessThan - (int): entered integer will not be less than this number
def intInputProtection(phrase,lessThan):
    #ensure an integer is entered - protects against strings and floats
    #ensures no negative numbers are entered
    validInt = False
    negative = False
    while(not validInt or negative):
        validInt = False
        negative = False
        try:
            #Splits the user input into a list of strings,
            #Then converts the that list of strings into a list of integers
            print(phrase)
            entered = int(input())
            if(entered < lessThan):
                    print("Don't enter invalid numbers!!")
                    negative = True
        except:
            print("Invalid input! Enter an integer!\n")
        else:
            validInt = True
    return entered


def gen_win_list(n,action_space):

    winMatrix = []
    winActionOrder = []

    #for loop that will iterate through until the table is complete
    #each iteration will add one to the solution table
    for currentStone in range(n):

        #intial state
        if currentStone == 0:
            winMatrix.append(2)
            winActionOrder.append([-1])

        else:
            moveFound = False
            action_order = 0
            action_order_matrix = []

            #for each possible move in a given state
            for pMove in action_space:

                #the move must be legal
                if currentStone >= pMove and winMatrix[currentStone-pMove] == 2:
                    action_order_matrix.append(action_order)
                    moveFound = True

                action_order +=1
            if(moveFound):
                winMatrix.append(1)
                winActionOrder.append(action_order_matrix)

            else:
                winMatrix.append(2)
                winActionOrder.append([-1])
            print(winMatrix)
            print(winActionOrder)
            input()


    return winActionOrder

print(gen_win_list(10,[1,3,4]))