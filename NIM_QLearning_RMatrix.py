import numpy as np
from NIM_env_RMatrix import *
import random
import time
from IPython.display import clear_output

#That can be changed
#Learning_rate, how much the Machine cares about new info
#Discount_rate, how much the Machine cares about expected rewards
#Exploration_rate, how much the Machine explores vs exploits
#Number of intial stones
#Rules of game
#Training Opponent

env = NIM_env()


#modified these to len
action_space_size = len(env.action_space)
state_space_size= len(env.state_space)

q_table = np.zeros((state_space_size, action_space_size))


num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.9

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

win_count = []

rewards_all_episodes = []

#Q-learning algorithm

#everything that happens each episode
for episode in range(num_episodes):
    #reset the env to inital state
    state = env.reset()

    #keeps track of whether or not the episode is finished
    done = False

    #keeps track of rewards in each episode
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):

        #exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            action_order = np.argmax(q_table[state,:])
        else:
            #pick a random action
            action_order = rand_action(env.action_space)
            
        new_state,reward, done, info = env.step(action_order)

        #Update Q-table for Q(s,a)
        q_table[state,action_order] = q_table[state,action_order] * (1 - learning_rate) + \
                                learning_rate * (reward + discount_rate * np.max(q_table[new_state,:]))
        state = new_state
        rewards_current_episode += reward

        if done == True:
            break
    #Exploration rate decay
    exploration_rate = min_exploration_rate +\
                           (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)

    #count the wins
    if reward == 100:
        win_count.append(1)
    else:
        win_count.append(0)


#Calculate and print the average reward per thousand episodes
print("done!")


rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
win_per_thousand_episodes = np.split(np.array(win_count), num_episodes/1000)
count = 1000
print("************Average reward per thousand episodes *************\n")
for r in win_per_thousand_episodes:
    print(count, ": ", str(sum(r)))
    count +=1000

#Print updated Q-table
print("\n\n*********Q-table************")
print(q_table)




print("\n\n********************************")
print(" Time to play the Machine!")

#Get who plays first
playFirstPhrase = "Enter (1) to play first, Enter (2) to play second:"
playFirst = intInputProtection(playFirstPhrase,1)
if playFirst == 1:
    print("You are Player One!")
    computerTurn = False
    playFirst = True
elif playFirst == 2:
    print("You are Player Two!")
    computerTurn = True
    playFirst = False
else:
    print("Bad input! You just lost your right to choose!")
    print("You will be Player Two!")

#after the program is trained, we, as a human, want to play!
state = env.reset()
done = False

if playFirst:
    #check for a winner - trivial case
    if not env.movePossible():
        done = True
        print("Machine Wins.. but honestly was that fun?")
        
    #asks for the number of stones you wish to remove
    #input protection ensures a valid response
    else:
        illegalMove = True
        removeStonesPhrase = "How many stones do you want to remove?: "

        while(illegalMove):
            removeStones = intInputProtection(removeStonesPhrase, min(env.action_space))
            illegalMove = env.isIllegalMove(removeStones)
            
            if illegalMove:
                print("Illegal move!")
                
        env.current_stones -= removeStones

        5#check for another winner
        if not env.movePossible():
            done = True
            env.render()
            print("You Win! but honestly was that fun?")

while(not done):
    env.render()

    #Computer has decided on an action to make
    action_order = np.argmax(q_table[state,:])
    action_remove = env.action_space[action_order]
    print("Machine wants to remove", action_remove, "stone(s)")

    new_state,reward, done, info = env.step(action_order, True)
    
   
    #If you cannot make a move, end the game
    if(reward == -1):
        env.render()
        print("Machine cannot make a move")
        print("You win!")
    elif (reward == 100):
        print("You cannot make a move :(")
        print("Machine wins!")
    else:
        print("You have removed" , info, "stone(s)")
    
        
    state = new_state





