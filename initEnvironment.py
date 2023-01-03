# normal numbers 5
# jack queen king 10
# ace 20
import random
import numpy as np
#human players of the game
class Player :
    def __init__(self):
        self.deck=[]
        self.stack=[] 
        self.rewardAcc=0
    def addToStack(self,cards):
        self.stack.append(cards)
    def removeFromStack(self):
        self.stack.pop()
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

    #Steal cards from opposing player's stack
    def stealPlayer(self,playerOn,playerOff,card):
        index=playerOn.index(card)
        playerOff.addToStack(playerOn.deck.pop(index))
        #Removing all of the same cards from opponent stack
        while True:
            if playerOff.stack[-1] == card:
                playerOn.addtoStack(playerOff.stack.pop(-1))
            else:
                break

    #Steal cards from center
    def stealCenter(self,center,playerOn,card):
        cardIndexPlayer=playerOn.deck.index(card)
        #Removing all 
        for i in center:                       
            if center[i] == card:
                playerOn.stack.append(playerOn.center.pop(i))
        playerOn.stack.append(playerOn.deck.pop(cardIndexPlayer))
        
    #Choose random card to do any of the above actions
    def chooseRandomCard(self,playerOn):
        x=random.choice(playerOn.deck)
        return x

    #Checking which actions are possible
    def compilePossibleActions(self,playerOn,playerOff,center):
        #Binary classification of (0,1) for 3 possible actions
        #Index 0:Steal from player
        #Index 1:Steal from center
        #Index 2:Throw in Center(Always Possible)
        possibleActions=[0,0,1]
        possibleLock=[0,0]
        centerCardspossible=[]
        opponentStealCard=1
        #Checking Steal from player
        for x in playerOn.deck:
            if x == playerOff.stack[-1]:
                possibleActions[0] = 1
                if playerOff.stack[-3] == x:
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
                    if center.count(j)==3:
                        possibleLock[1]=1
        return possibleActions,possibleLock,centerCardspossible
        #runs after every turn and tells whether you lost from your stack, gained a lock in your stack or what

class Environment:
    def __init__(self):
        self.qtable=np.array(
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3])
        self.rewards=np.array(
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
        )
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
        #Will run after action is done or when probing reward of 't+1' state
    def compileActionReward(self,Environment,playerOn,playerOff,center,deck,action ): #action=['action','cardThrown',bool] -- bool indicates whether action has occured
        if action[1] == 'stealPlayer':
            lock=False
            locklessReward=0
            lockReward=0
            if action[2]==True:
                card=action[1]
                #if lock is obtained
                if playerOn.stack[-4]==card:
                    lock=True
                    for i in playerOn.stack:
                        lockReward+=Environment.cardPoints.get(i)
                #if lock isn't obtained
                else:
                    for i in range(1,5):
                        if playerOn.stack[-i]==card:
                            locklessReward+=(Environment.cardPoints.get(i))
                        else:
                            break
            return locklessReward,lockReward
            
            #CREATE MATRIX OF POINTS FOR EACH CARD    


            

            playerOn.rewardacc=0
            


        
    
        
    

player1=Player()
player2=Player()
initDealing=dealing()
deck=initDealing.initDeck()
print(len(deck))
centerCards=initDealing.dealCards(deck,player1,player2)
print(centerCards)
print(player1.deck,player2.deck,deck,len(deck))

