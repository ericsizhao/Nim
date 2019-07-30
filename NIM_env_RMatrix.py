import random
import numpy as np
from NIM_winTable import gen_win_list

class NIM_env:

    #CHECKED
    #later we can add cash and stuff
    def __init__(self):
        self.action_space = gen_action_space()
        self.state_space = gen_state_space()
        self.current_stones = len(self.state_space) - 1
        self.intial_stones = len(self.state_space) - 1
        self.reward_matrix = self.gen_reward_matrix()
        self.optimal_action_space = self.gen_optimal_action_space()


    #WE ARE NOT CHECKING IF THE MACHINE IS MAKING A LEGAL MOVE OR NOT
    
    #given an action, how does the enviornment react?
    #param action: action the agent wishes to take      
    #returns a tuple (state, reward, done, info)
    #   state - the agent's next observation of the current environment
    #   reward - the reward from doing that action
    #   done - has the game ended yet
    #   info - diagnostic information helped for debugging - opponent's move
    def step(self,action_order,intelligence = 0,human = False):

        #establish the current states of the game
        done = False
        info = 0 #This means that opponent removed 0 stones
        action_remove = self.action_space[action_order]


        #Machine recieves award from matrix
        reward = self.reward_matrix[self.current_stones][action_order]

        #Check if game is over yet
        if reward == -1 or reward == 100:
            done = True

        #If game is not done
        if (not done):
            
            #Machine makes his move
            self.current_stones -= action_remove

            #Opponent makes his move
            oppoMove = self.opponentMove(intelligence,human)
            info = oppoMove
            self.current_stones -= oppoMove

        #Return the new state to Machine
        tupleStep = (self.current_stones,reward,done,info)
        
        return tupleStep

    
    #random opponent
    #Will return 0 if machine has won (b/c oppo cannot make a move)
    #Will return -1 if machine has made an illegal move
    #Will return (amount of stones opponent wishes to remove) otherwise
    def opponentMove(self,intelligence = 0,human = False):
        if human:

            self.render()
            
            #asks for the number of stones you wish to remove
            #input protection ensures a valid response
            illegalMove = True
            removeStonesPhrase = "How many stones do you want to remove?: "

            while(illegalMove):
                removeStones = intInputProtection(removeStonesPhrase, min(self.action_space))
                illegalMove = self.isIllegalMove(removeStones)
                
                if illegalMove:
                    print("Illegal move!")

            return removeStones

        #A move should 100% be possible, since the game has not ended yet
        else:

            illegal_Move = True
            while(illegal_Move):
                #get a random action
                mistakeMove = random.random()
                if intelligence > mistakeMove:
                    #action_order must be an int, and optimal_action_space[stones] returns a list
                    action_order = self.optimal_action_space[self.current_stones][0]
                    #if there is no optimal move, just remove the least number of stones possible
                    if action_order == -1:
                        action_order = 0
                else:
                    action_order = rand_action(self.action_space)

                action_remove = self.action_space[action_order]

                illegal_Move = self.isIllegalMove(action_remove)
 

            return action_remove

    #EXPERIMENTABLE
    #Param s: state of the game
    #Param a: the action taken
    #returns a matrix that returns 100 when machine makes a winning move
    #returns a -1 when the machine makes an illegal move/has 0 stones
    #returns a 0 when the Machine makes non-game ending play
    def gen_reward_matrix(self):
        #generate a table of all zeros
        reward_matrix = np.zeros((len(self.state_space),len(self.action_space)))

        #keeps track of each row
        row_count = 0
        for row in reward_matrix:
            #for each possible action
            for action_order in range(len(self.action_space)):
                
                action_remove = self.action_space[action_order]

                #if the number of stones on board = number of stones machine wants to remove
                #then machine wins the game
                if row_count == action_remove:
                    reward_matrix[row_count][action_order] = 100
                    
                #if the number of stones on board < number of stones machine wants to remove
                #then machine lose the game
                elif row_count < action_remove:
                    reward_matrix[row_count][action_order] = -1
                else:
                    reward_matrix[row_count][action_order] = 0
            row_count += 1

        return reward_matrix


    #CHECKED
    #return boolean - if a move is possible  
    def movePossible(self):
        if self.current_stones > -1 and self.current_stones >= min(self.action_space):
            return True
        else:
            return False

    #CHECKED
    def isIllegalMove(self,remove_stones):
        #if move is illegal - return True
        if remove_stones > self.current_stones or remove_stones not in self.action_space:
            return True
        #if move is valid - return False
        else:
            return False

    #CHECKED
    #resets the state of the environment and returns intial state
    def reset(self):
        self.current_stones = self.intial_stones
        return self.current_stones
        #return - the intial state

    #CHECKED
    #display the environment's current state
    def render(self):
        print("\n")
        print ("There are", self.current_stones, "stones on the board!")
        #just prints the current game's state...      

    #generates the optimal move matrix
    def gen_optimal_action_space(self):
        return gen_win_list(len(self.state_space), self.action_space)

#generates a random action
#returns a tuple: (action_order)
    #action_order - the index of stones we wish to remove
def rand_action(action_space):
    action_order = random.randint(0,len(action_space)-1)
    return action_order

#CHECKED
#Will generate the action space
#We are playing 1,2,3 NIM
#so only actions are 1,2,3
#obviously right now it's pretty simple, but when cash comes this will be useful
def gen_action_space():
    #ensure an input of a list of integers - protects against strings and floats
    #need to ensure that numbers greater than 0 are entered
    validIntList = False
    greaterZero = False
    while(not validIntList or greaterZero):
        validIntList = False
        greaterZero = False
        try:
            #Splits the user input into a list of strings,
            #Then converts the that list of strings into a list of integers
            print("Enter a1,a2,a3...n with each number seperated by a comma.")
            print("Example:1,3,4 ")
            userStringList = input().split(",")
            userIntList = []
            for x in userStringList:
                userIntList.append(int(x))
                if(int(x) < 1):
                    print("Enter numbers greater than 0!")
                    greaterZero = True
        except:
            print("Invalid input! Enter the numbers and commas properly!\n")
        else:
            validIntList = True

    return userIntList

#CHECKED
#Will generate the state space
#this is pretty simple too
def gen_state_space():
    #later will be input from user but whatever
    n = intInputProtection("Enter number of stones:", 0)
    stateSpace = []
    for x in range (n + 1):
        stateSpace.append(x)
    return stateSpace

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

def reward_function(x):
    return 1

