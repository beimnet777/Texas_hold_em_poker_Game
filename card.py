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
     

    def hasStraight(self):
        self.cards.sort(key = lambda x:x.num)
        cardLetters = [x.letter for x in self.cards]
        straights = []
        previous = None
        count = 0
        for i in self.cards:
            if previous == None or i.num == previous+1:
                previous = i.num
                count+=1
                if count>=5:
                    straights = [i,count]
                elif count==4 and i.letter == "5" and "a" in cardLetters:
                    straights = [i,count]
            elif previous == i.num:
                pass
            else:
                count = 0
                previous = i.num
        if len(straights)>0:
            return [straights[0]]
        return None


    def hasFlush(self):
        shapeCards = {}
        visitedShapes = []
        for i in self.cards:
            if i.shape in visitedShapes:
                shapeCards[i.shape].append(i)
            else:
                shapeCards[i.shape] = [i]
                visitedShapes.append(i.shape)
        flushCards = [shapeCards[x] for x in shapeCards.keys() if len(shapeCards[x])>=5]
        if len(flushCards)>0:
            return [max(flushCards[0], key = lambda x: x.num)]
        return None


    def hasFullHouse(self):
        cardRepeatitions = {}
        visitedCards = []
        for i in self.cards:
            if i.num in visitedCards:
                cardRepeatitions[i.num].append(i)
            else:
                cardRepeatitions[i.num] = [i]
                visitedCards.append(i.num)
        repeated = [x for x in cardRepeatitions.values() if len(x)>=2]
        repeated3times = [x for x in repeated if len(x)>=3]
        if len(repeated3times)>=1 and len(repeated)>=2:
            best = max(repeated3times,key=lambda x:x[0].num)
            repeated.remove(best)
            best = best[0]
            secondBest = max(repeated, key=lambda x:x[0].num)
            secondBest = secondBest[0]
            return [best,secondBest]
        return None



    def hasFourOfAKind(self):
        cardRepeatitions = {}
        visitedCards = []
        for i in self.cards:
            if i.num in visitedCards:
                cardRepeatitions[i.num].append(i)
            else:
                cardRepeatitions[i.num] = [i]
                visitedCards.append(i.num)
        quads = [x for x in cardRepeatitions.values() if len(x) >= 4]
        return [max(quads , key = lambda x: x[0].num)[0]] if len(quads) > 0 else None


    def hasStraightFlush(self):
        shapeRepeatitions = {}
        visitedShapes = []
        for i in self.cards:
            if i.shape in visitedShapes:
                shapeRepeatitions[i.shape].append(i)
            else:
                visitedShapes.append(i.shape)
                shapeRepeatitions[i.shape] = [i]
        repeatitions5times = [x for x in shapeRepeatitions.values() if len(x)>=5]
        if len(repeatitions5times)==0:
            return None
        straight = None
        for i in repeatitions5times:
            count = 0
            i.sort(key=lambda x:x.num)
            previous = None
            cardLetters = [x.letter for x in i]
            for j in i:
                if previous == None or j.num == previous+1:
                    previous = j.num
                    count+=1
                    if count>=5:
                        straight = j
                    elif count==4 and j.letter == "5" and "a" in cardLetters:
                        straight = j
                elif previous == j.num:
                    pass
                else:
                    count = 0
                    previous = j.num

        return [straight] if straight is not None else None


    def checkAll(self):
        functions = [self.hasStraightFlush,self.hasFourOfAKind,self.hasFullHouse,self.hasFlush,self.hasStraight,self.hasThreeOfAKind,self.hasTwoPair,self.hasPair,self.highestCard]
        counter  = 9
        for i in functions:
            ans = i()
            if ans is not None:
                return [counter]+ans
            counter-=1



# a = Card("A","spade",14)
# b = Card("2","spade",2)
# c = Card("3","spade",3)
# d = Card("4","spade",4)
# e = Card("5","spade",5)
# # f = Card("6","spade",6)
# l = Card("7","spade",7)
# g = Card("8","spade",8)
# h = Card("9","spade",9)
# i = Card("10","spade",10)
# j = Card("j","spade",11)
# k = Card("q","spade",12)

# cardList = [a,b,c,d,e,g,h,i]#,j,k,l,f]

# cardbuk = CardBucket(cardList)

# print(cardbuk.hasFlush())
# cards = [card for card in  CardBucket.generateRandom()]
# cards2 = [card for card in  CardBucket.generateRandom()]
# print([card.__str__() for card in  cards])
# print([card.__str__() for card in CardBucket(cards).hasFullHouse()])
# print(CardBucket(cards).hasFullHouse().__str__())



# print([card.__str__() for card in cards])
# print([card.__str__() for card in cards2])
# print(CardBucket.compare(CardBucket(cards),CardBucket(cards2)))


# print([card.__str__() for card in CardBucket(cards).checkAll()])
# print([card.__str__() for card in CardBucket(cards2).checkAll()])