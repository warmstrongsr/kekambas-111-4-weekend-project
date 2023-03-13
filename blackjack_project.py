import random

class Card:
    def __init__(self,value,suit):
        self.rank = value
                      #1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 
        self.value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'][value-1] # -1 because ex. 10 is in index[9] so minus 1 index
        self.suit = '♥♦♣♠'[suit-1] # 1,2,3,4 = ♥♦♣♠
        
    def two_d(self):   # https://stackoverflow.com/questions/31011395/python-print-unicode-character 
        print('┌───────┐')
        print(f'| {self.value:<2}    |')
        print('|       |')
        print(f'|   {self.suit}   |')
        print('|       |')
        print(f'|    {self.value:>2} |')
        print('└───────┘') 

    def nums(self):
        if self.rank >= 10:
            return 10
        elif self.rank == 1:
            return 11
        return self.rank
    
class Deck: 
     def __init__(self):
         self.cards = []
     def generate(self): # possible combinations loop to generate deck .shuffle essentially but more like a rotating deck 
         for face in range(1, 14):
             for suit in range(4):
                 self.cards.append(Card(face, suit))
     def draw(self, iter): 
         cards = []
         for i in range(iter):
             card = random.choice(self.cards) # https://www.w3schools.com/python/module_random.asp
             self.cards.remove(card)
             cards.append(card)
         return cards
     def count(self):
         return len(self.cards)
class Hand:
    def __init__(self, isDealer, deck): # https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b  Boolean value representation
        self.cards = []
        self.isDealer = isDealer
        self.deck = deck
        self.points = 0

    def hit(self): #appending from the iterable to the list
        self.cards.extend(self.deck.draw(1))
        self.check_score()
        if self.points > 21:
            return 1
        return 0

    def deal(self):
        self.cards.extend(self.deck.draw(2))
        self.check_score()
        if self.points == 21:
            return 1
        return 0
    # Check the score of the hand
    def check_score(self):
        counter = 0
        self.points = 0
        for card in self.cards:
            if card.nums() == 11:
                counter += 1
            self.points += card.nums()

        while counter != 0 and self.points > 21:
            counter -= 1
            self.points -= 10
        return self.points

    def two_d(self):
        if self.isDealer:
            print("Dealer's Cards")
        else:
            print("Your Cards")

        for i in self.cards:
            i.two_d()

        print("Score: " + str(self.points))
class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.generate()
        self.Hand = Hand(False, self.deck)
        self.dealer = Hand(True, self.deck)

    def play(self):
        player = self.Hand.deal()
        d_status = self.dealer.deal()

        self.Hand.two_d()

        if player == 1:
            print("Blackjack! Congrats!")
            if d_status == 1:
                print("Dealer and Player got Blackjack! It's a push. (Tie)")
            return 1

        p_action = ""
        while p_action != "Stay":
            bust = 0
            p_action = input("Hit or Stay? ")

            if p_action == "Hit":
                bust = self.Hand.hit()
                self.Hand.two_d()
            if bust == 1:
                print("Bust!! Good Game!")
                return 1
        print("\n")
        self.dealer.two_d()
        if d_status == 1:
            print("Dealer got Blackjack! Better luck next time!")
            return 1

        while self.dealer.check_score() < 17:
            if self.dealer.hit() == 1:
                self.dealer.two_d()
                print("Dealer bust. Congrats!")
                return 1
            self.dealer.two_d()

        if self.dealer.check_score() == self.Hand.check_score():
            print("It's a Push (Tie). Atleast you broke even.")
        elif self.dealer.check_score() > self.Hand.check_score():
            print("Dealer wins. Good Game!")
        elif self.dealer.check_score() < self.Hand.check_score():
            print("You won. Congratulations!")
            
    def play_again(self):
        while True:
            self.play()
            play_again = input("Do you want to play again? (Y/N) ")
            if play_again.upper() == "N":
                break
               
g = Game()
g.play()