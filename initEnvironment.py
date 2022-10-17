import random
class Player :
    def __init__(self):
        self.deck=[]
        self.stack=[]
    def addToStack(self,cards):
        self.stack.append(cards)
    def removeFromStack(self):
        self.stack.pop()

class cards :
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

        deckCards=0
        deck=[]
        while deckCards<52:
            activeCard= random.randint(2,14)
            if self.deckCounter[activeCard] >0:
                deck.append(activeCard)
                self.deckCounter[activeCard]-=1
                deckCards+=1
            else:
                for x in self.deckCounter:
                    if self.deckCounter[x]>=1:
                        deck.append(x)
                        self.deckCounter[x]-=1
                        deckCards+=1
                        break  
        return deck
    
    def dealCards(self,deck,player1,player2):
        i=0
        while i<5:
            player1.deck[i]== deck.pop()
            player2.deck[i]== deck.pop()
            i+=1 




        
