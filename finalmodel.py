import random
import numpy as np
#human players of the game and agent
class Player :
    def __init__(self):
        self.deck=[]
        self.stack=[] 
        self.stackrewardPerc=[]
        self.rewardAcc=0
        self.cardAgeInDeck=[]
        self.role='opponent'
        self.previousLock=-1
        self.qtable=np.array(
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3])
#methods and attributes of cards to be dealt
class dealing:
    #initializes fresh deck of 52 cards
    def __init__(self):
        self.deckCounter={
            2:4,
            3:4,
            4:4,
            5:4,
            6:4,
            7:4,
            8:4,
            9:4,
            10:4,
            11:4, #jack
            12:4, #queen
            13:4, #king
            14:4  #ace
        }
    #Initializes deck of 52 cards in random order           
    def initDeck(self):
        cardsInDeck=0
        deck= []
        while cardsInDeck<52:
            activeCard= random.randint(2,14)
            if self.deckCounter[activeCard] >0:
                deck.append(activeCard)
                self.deckCounter[activeCard]-=1
                cardsInDeck+=1
            else:
                #if the random integer generated is already used
                for x in list(self.deckCounter.keys()):
                    if self.deckCounter[x]>=1:
                        deck.append(x)
                        self.deckCounter[x]-=1
                        cardsInDeck+=1
                        break  
        return deck
    #deals all required cards(4 to each player + 4 in center)
    def dealCards(self,deck,player1,player2):
        i=0
        center=[]
        while i<4:
            player1.deck.append(deck.pop())
            player2.deck.append(deck.pop())
            i+=1 
        for x in range(0,4):
            center.append(deck.pop())
        return center

#Set of actions possible by each player
class actions: 

    #Action to be done if steal is not possible
    def throwInCenter(self,center,playerOn,card):       #playerOn= active player 
        cardIndex=playerOn.index(card)
        center.append(playerOn.deck.pop(cardIndex))     #adding card to center and removing from active player's deck
        return['throwCenter',card,0,True]

    #Steal cards from opposing player's stack
    def stealPlayer(self,playerOn,playerOff,card):
        index=playerOn.index(card)
        playerOn.stack.append(playerOn.deck.pop(index))
        cardsStolen=0
        #Removing all of the same cards from opponent stack
        if playerOn.role=='agent':
            while True:
                if playerOff.stack[-1] == card:
                    playerOn.stack.append(playerOff.stack.pop(-1))
                    cardsStolen+=1
                else:
                    break
        #if opponent is stealing from us
        else:
            while True:
                if playerOff.stack[-1] == card:
                    playerOn.stack.append(playerOff.stack.pop(-1))
                    playerOff.cardAgeInDeck.pop()
                    cardsStolen+=1
                else:
                    break
        return ['stealPlayer',card,cardsStolen,True]

    #Steal cards from center
    def stealCenter(self,center,playerOn,card):
        cardIndexPlayer=playerOn.deck.index(card)
        #Removing all 
        cardsStolen=0
        for i in center:                       
            if i == card:
                playerOn.stack.append(center.pop(i))
                cardsStolen+=1
        playerOn.stack.append(playerOn.deck.pop(cardIndexPlayer))
        return ['stealCenter',card,cardsStolen,True]
        
    #Choose random card to do any of the above actions
    def chooseRandomCard(self,playerOn):
        x=random.choice(playerOn.deck)
        return x
    
    #Choose lowest point cards to do any of the above actions
    def chooseLowCards(self,Environment,playerOn):
        possibleCards=[0,0,0,0,0,0]
        counter=0
        for i in playerOn.deck:
            if Environment.cardPoints.get(i)==5:
                possibleCards[i]=i
            elif possibleCards.count(0)==5 and Environment.cardPoints.get(i)==10:
                possibleCards[counter]=i
                counter+=1
        #Last index shows the points gainable by each of the cards in the array
        if possibleCards[0]>10:
            possibleCards[5]=10
        else:
            possibleCards[5]=5        
        return possibleCards

    #Checking which actions are possible
    def compilePossibleActions(self,playerOn,playerOff,center):
        #Binary classification of (0,1) for 3 possible actions
        #Index 0:Steal from player
        #Index 1:Steal from center
        #Index 2:Throw in Center(Always Possible)
        possibleActions=[0,0,1]
        possibleLock=[0,0]
        centerCardspossible=[]
        opponentStealCard=-1
        centerLockCard=0

        #Checking Steal from player
        for x in playerOn.deck:
            if x == playerOff.stack[-1]:
                possibleActions[0] = 1
                if playerOff.stack[-3] == x and playerOff.stack[-1]==x:
                    possibleLock[0]=1
                opponentStealCard=x
                break

        #Checking Steal from center
        for x in playerOn.deck:
            for j in center:
                if x == j and centerCardspossible.count(j)< 1:
                    centerCardspossible.append(j)
                    possibleActions[1]=1 
                    if playerOn.stack[-2] == j:
                        possibleLock[1]=1
                        centerLockCard=j
                    if center.count(j)==3:
                        possibleLock[1]=1
        return possibleActions,possibleLock,centerCardspossible,opponentStealCard,centerLockCard

class Environment:
    def __init__(self):
        self.cardPoints={
            2:5,
            3:5,
            4:5,
            5:5,
            6:5,
            7:5,
            8:5,
            9:5,
            10:5,
            11:10,
            12:10,
            13:10,
            14:20
        }
        self.randomActionChance=1
        self.learningrate=0.1
    
    #Will run after action is done 
    def compileActionReward(self,Environment,playerOn,playerOff,center,deck,action): 
        #action=['action',cardThrown,cardsRemoved,bool] -- bool indicates whether action has occured
        reward=0
        if action[1] == 'stealPlayer':
            if action[3]==True:
                card=action[1]
                #if lock is obtained
                if playerOn.stack[-4]==card:
                    for i in playerOn.stack:
                        #adds 100 percent of reward for all previoously un-locked cards to accumulator
                        if playerOn.stack.index(i)>playerOn.previousLock and playerOn.stackRewardPerc[playerOn.stack.index(i)]!= 0 or 1:
                            remainingRewardPerc=1-playerOn.stackRewardPerc[i]
                            reward+=remainingRewardPerc*Environment.cardPoints.get(i)
                        elif playerOn.stack.index(i) != playerOn.previousLock and i ==card:
                            reward+=Environment.cardPoints.get(i)
                    #doubling reward for removing from opponent stack
                    reward+=Environment.cardPoints[card]*action[2]
                    playerOn.previousLock=len(playerOn.stack)-1
                #if lock isn't obtained
                else:
                    for i in range(1,4):
                        if playerOn.stack[-i]==card:
                            #Only giving 50 percent reward initially
                            reward+=(Environment.cardPoints.get(i)/0.5)
                            playerOn.stackRewardPerc.append(0.5)
                        else:
                            break
                    #doubling reward for removing from opponent stack
                    reward+=Environment.cardPoints[card]*action[2]

        elif action[1]=='stealCenter':
            if action[3]==True:
                card=action[1]
                #If lock is obtained
                if playerOn.stack[-4]==card:
                    for i in playerOn.stack:
                        #adds 100 percent of reward for all presviously un-locked cards to accumulator
                        if playerOn.stack.index(i)>playerOn.previousLock and playerOn.stackRewardPerc[playerOn.stack.index(i)]!= 0 or 1:
                            remainingRewardPerc=1-playerOn.stackRewardPerc[i]
                            reward+=remainingRewardPerc*Environment.cardPoints.get(i)
                        elif playerOn.stack.index(i)>playerOn.previousLock and i ==card:
                            reward+=Environment.cardPoints.get(i)
                            playerOn.stackRewardPerc.append(1)
                    playerOn.previousLock=len(playerOn.stack)-1
                #If lock isn't obtained
                else:
                    for i in range(1,4):
                        if playerOn.stack[-i]==card:
                            reward+=(Environment.cardPoints.get(i)/0.5)
                            playerOn.stackRewardPerc.append(0.5)
                        else:
                            break
        elif action[1]=='throwCenter':
            pass
        return reward
    def compileEstimatedFutureReward(self,actions,agent,opponent,deck,center):
        #cant compute exact reward since we dont know opponent action since it runs after opponent turn
        reward=0
        centerReward=0
        stealReward=0
        possibleActions,possibleLock,centerCardspossible,opponentStealCard,centerLockCard=actions.compilePossibleActions(agent,opponent,center)
        #Throwing in center is only option
        if possibleActions.count(0)==2:
            reward=0
        #If you can steal from player   
        elif possibleActions[0]==1:
            #if it results in a lock
            if possibleLock[0]==1:
                for i in agent.stack:
                        #adds 100 percent of reward for all previoously un-locked cards to accumulator
                    if agent.stack.index(i)>agent.previousLock and agent.stackRewardPerc[agent.stack.index(i)]!= 0 or 1:
                            remainingRewardPerc=1-agent.stackRewardPerc[i]
                            stealReward+=remainingRewardPerc*Environment.cardPoints.get(i)
                    elif agent.stack.index(i) != agent.previousLock and i ==opponentStealCard:
                            stealReward+=Environment.cardPoints.get(i)
                    #doubling reward for removing from opponent stack
                stealReward+=Environment.cardPoints[opponentStealCard]*3
            else:
            #If it doesnt result in a lock
                for i in range(1,4):
                    if agent.stack[-i]==opponentStealCard:
                        #Only giving 50 percent reward initially
                        stealReward+=(Environment.cardPoints.get(i)/0.5)
                    else:
                        break
                #doubling reward for removing from opponent stack
                    stealReward+=Environment.cardPoints[opponentStealCard]*3
                
        #If you can steal from center
        if possibleActions[1]==1:
            #if it results in a lock
            if possibleLock[1]==1:
                for i in agent.stack:
                    #adds 100 percent of reward for all presviously un-locked cards to accumulator
                    if agent.stack.index(i)>agent.previousLock and agent.stackRewardPerc[agent.stack.index(i)]!= 0 or 1:
                        remainingRewardPerc=1-agent.stackRewardPerc[i]
                        centerReward+=remainingRewardPerc*Environment.cardPoints.get(i)
                    elif agent.stack.index(i)>agent.previousLock and i ==centerLockCard:
                        centerReward+=Environment.cardPoints.get(i)
            #If it doesnt result in a lock
            else:
                for i in centerCardspossible:
                    x=center.count(i)*Environment.cardPoints.get(i)*0.5
                    if x>centerReward:
                        centerReward=x
                pass

        #Checking which reward is higher
        if stealReward==0 and centerReward==0:
            reward=0
        elif stealReward>centerReward:
            reward=stealReward
        elif centerReward>stealReward:
            reward=stealReward

        return reward

    #Will run after opponent does move to return positive/negative reward to agent
    def compileOpponentConsequences(self,Environment,agent,opponent,actionOpponent,agentCache):
        #agentCache is similar to the action array in the previous function
        reward=0
        card=actionOpponent[1]
        #incrementing card age in deck by 1:
        for i in agent.cardAgeInDeck:
            i+=1
        #Punishing immediate capture of thrown card
        if agentCache[0]=='throwCenter' and actionOpponent[0]=='stealCenter' and agentCache[1]==card:
            if opponent.stack[-4]==agentCache[1]:
                reward-=Environment.cardPoints.get(agentCache[1])*1.5
            else:
                reward-=Environment.cardPoints.get(agentCache[1])
        #Reducing reward for getting stack stolen
        if actionOpponent[0]=='stealPlayer':
            cardsStolen=actionOpponent[2]
            if opponent.stack[-4] != card:
                reward-=(agent.stackRewardPerc[-1]+0.5)*Environment.cardPoints.get(card)*cardsStolen
            else:
                reward-=(agent.stackRewardPerc[-1]+1)*Environment.cardPoints.get(card)*cardsStolen
            #Making stack and rewardPerc lists identical in length
            for i in range(1,cardsStolen+1):
                agent.stackRewardPerc.pop()
        #compute increasing reward for past action -- 50 percent intitial gain -- 74 percent after 3 turns -- 100 percent if lock
        for i in agent.stackRewardPerc:
            if i<0.74:
                i+=0.08
                reward+=0.08*Environment.cardPoints.get(agent.deck[i])
    
    def checkStates(self,playerOn,deck):
        state=-1

        return state
    
    def updateQtable(self,state,nextState,optimalAction,agent,opponent,RT1,learningRate,discountFactor,action):
        Qtable=agent.qtable
        # Updated Q Value= Old Q-Value + learningRate*Temporal Difference
        Qtable[state,action]+=learningRate*(RT1+discountFactor(Qtable[nextState,optimalAction])-Qtable.iloc(state,action))

        return Qtable
    
#compileestimateed future wreward is wrong
#check states function
#implement qtable update 
#script
        
    

Agent=Player()
Agent.role='agent'
player2=Player()
initDealing=dealing()
deck=initDealing.initDeck()
print(len(deck))
centerCards=initDealing.dealCards(deck,Agent,player2)
print(centerCards)
print(Agent.deck,player2.deck,deck,len(deck))
