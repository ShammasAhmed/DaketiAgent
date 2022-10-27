import random
import numpy as np
class Player :
    def __init__(self):
        self.deck=np.array([])
        self.stack=np.array([])
    def addToStack(self,cards):
        self.stack.append(cards)
    def removeFromStack(self):
        self.stack.pop()

class dealing:
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
            11:4,
            12:4,
            13:4,
            14:4  
        }
    def initDeck(self):

        cardsInDeck=0
        deck= np.array([])
        while cardsInDeck<52:
            activeCard= random.randint(2,14)
            if self.deckCounter[activeCard] >0:
                deck.append(activeCard)
                self.deckCounter[activeCard]-=1
                cardsInDeck+=1
            else:
                for x in self.deckCounter:
                    if self.deckCounter[x]>=1:
                        deck.append(x)
                        self.deckCounter[x]-=1
                        cardsInDeck+=1
                        break  
        return deck
    
    def dealCards(self,deck,player1,player2):
        i=0
        center=[]
        while i<4:
            player1.deck[i]= deck.pop()
            player2.deck[i]= deck.pop()
            i+=1 
        for i in range(0,3):
            center[i]= deck.pop()
        return center

class actions: 
    def throwInCenter(self,center,playerOn,card):   #playerOn= active player
        x=np.where(playerOn.deck == card)
        cardIndex=x[0]                              #Picking one element only in case there are more than 1 of the same card in the deck
        center.append(playerOn.deck.pop(cardIndex)) #adding card to center and removing from active player's deck

    def steal(self,playerOn,playerOff,card):
        index=np.where(playerOn.deck == card)
        playerOff.addToStack(playerOn.deck.pop(index))
        while True:
            if playerOff.stack[-1] == card:
                playerOn.addtoStack(playerOff.stack.pop(-1))
            else:
                break

        




        
