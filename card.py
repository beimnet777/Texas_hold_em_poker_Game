import random


class Card:
    def __init__(self,letter:str,shape:str,num:int):
        self.letter = letter
        self.shape = shape
        self.num = num

    def __str__(self):
        return self.letter + self.shape
    
class CardBucket:
    def __init__(self,cards:list[Card]):
        self.cards = cards


    def addCard(self,card):
        self.cards.append(card)
    

    def addCards(self,cards):
        self.cards = self.cards + cards


    def hasCard(self,card):
        if card in self.cards:
            return True
        return False


    @staticmethod
    def generateRandom(num:int = 9):
        letters = ["2","3","4","5","6","7","8","9","10","j","q","k","a"]
        numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        shapes = ["d","f","h","s"]
        generated = []
        generatedCardsStrings = []
        while len(generated)<num:
            index = random.randint(0,12)
            shape = random.choice(shapes)
            card = Card(letter = letters[index],shape = shape,num = numbers[index])
            if card.__str__() not in generatedCardsStrings:
                generatedCardsStrings.append(card.__str__())
                generated.append(card)
        return generated

    @staticmethod
    def compare(bucket1,bucket2):
        ans1 = bucket1.checkAll()
        ans2 = bucket2.checkAll()
        if ans1[0]>ans2[0]:
            return -1
        if ans1[0]<ans2[0]:
            return 1 
        else:
            for i in range(1,len(ans1)):
                if ans1[i].num>ans2[i].num:
                    return -1
                elif ans1[i].num<ans2[i].num:
                    return 1
            return 0


    
    def highestCard(self):
        return [max(self.cards,key=lambda x:x.num)]
    

    def hasPair(self):
        repeatedCards = {}
        visitedCards = []
        for i in self.cards:
            if i.num in visitedCards:
                repeatedCards[i]  = True
            else:
                visitedCards.append(i.num)

        if(len(repeatedCards.keys())>0):
            return [max(repeatedCards.keys(), key = lambda x: x.num)]
        return None


    def hasTwoPair(self):
        repeatedCards = {}
        visited = []
        for i in self.cards:
            if i.num in visited:
                repeatedCards[i.num].append(i)
            else:
                visited.append(i.num) 
                repeatedCards[i.num] = [i]               
        repeated = [x[0] for x in repeatedCards.values() if len(x)>=2]
        if len(repeated)>=2:
            best = max(repeated, key=lambda x:x.num)
            repeated.remove(best)
            secondBest = max(repeated, key=lambda x:x.num)
            return [best,secondBest]
        return None


    def hasThreeOfAKind(self):
        cardRepeatitions = {}
        visitedCards = []
        for i in self.cards:
            if i.num in visitedCards:
                cardRepeatitions[i.num].append(i)
            else:
                cardRepeatitions[i.num] = [i]
                visitedCards.append(i.num)
        triplets = [x for x in cardRepeatitions.values() if len(x) >= 3]
        return [max(triplets , key = lambda x: x[0].num)[0]] if len(triplets) > 0 else None
   