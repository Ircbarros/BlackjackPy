#!usr/bin/python3

import random

# Global Variables
#* Variables that Represents the Suits
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
#* Variables that Represents the Ranks
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
#* Variables that Represents the Values (Dic)
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,
          'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10,
          'King':10, 'Ace':11}

playing = True

# Create an Class for the Card
class Card:
    ''' Generate an Card with the variables suit and rank

    Returns:
        suit (str): The card suit
        rank (str): The card Rank
    '''
    # Init the Class with the variables Suit and Rank
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank
    # Class special metod to return the card Suit and Rank text
    def __str__(self):

        return self.rank + ' of ' + self.suit

# Create an Class for the Deck
class Deck:
    ''' Generate an Deck with the variables suit and rank

    Returns:
        single_card (str): The card poped from the deck
    '''
    # Init the Class Deck
    def __init__(self):
        # Create with an Empty Deck
        self.deck = []
        # Create an Deck with suit and Ranks
        #* For suit in suits (global) Hearts to Clubs do:
        for suit in suits:
            #* For rank in ranks (global) two to Ace do:
            for rank in ranks:
                # Append the Deck with the card suit and rank
                self.deck.append(Card(suit,rank))

    # Class special metod to return Deck comp
    def __str__(self):
        # Create and empty deck_comp
        deck_comp = ''
        # For every card in deck do:
        for card in self.deck:
            # Concatenate in a new line and use the string concatenation
            deck_comp += '\n'+ card.__str__()
        # Print the Deck Comp
        return "The Deck has: "+ deck_comp

    # Shuffle the Deck
    def shuffle(self):
        
        random.shuffle(self.deck)

    # Pops and grab a single card
    def deal(self):

        single_card = self.deck.pop()

        return single_card


# Represents what card are in someone hands
class Hand:
    '''
    Generate the cards on Player Hands

    '''
    # Init the Class Hand
    def __init__(self):
        # Start with Empty Hands
        self.cards = []
        # Start with Zero Values
        self.value = 0
        # Keep track on aces
        self.aces = 0

    def add_card(self, card):
        #* The card from the Deck.deal()
        self.cards.append(card)
        #* Pick the Card Value and add to the Total Player Hand Value
        #? Is 21 achieved? Here we sum the values to find the answer
        self.value += values[card.rank]
        # Track Aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        #* IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        #* CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        while self.value > 21 and self.aces > 0:

            self.value -= 10
            self.aces -= 1

# Keep track of Player's starting chips, bets, and ongoing winnings
class Chips:
    '''
    Generate the Player's Chips

    '''

    # Init the Class Hand
    def __init__(self, total=100):
        #? Can be a default number or user input value
        self.total = total
        self.bet = 0
    # Receive some bet if Win
    def win_bet(self):

        self.total += self.bet
    # Lose some bet if Loses
    def lose_bet(self):

        self.total -= self.bet

# Take a bet
def take_bet(chips):

    while True:

        try:
            # Receive the Chips for the bet
            chips.bet = int(input("How many Chips would you like to bet? "))

        except:

            print('Sorry please provide an  integer number!')
        
        else:
            # Check if have bets available
            if chips.bet > chips.total:

                print(f'Sorry, you do not have enough chips! You have: {chips.total}')

            else:
                # Break the While loop
                break

# Takes the Deck and someones Hand
def hit(deck, hand):
    # Grabs a single card from the Deck
    single_card = deck.deal()
    # Adds to the hand
    hand.add_card(single_card)
    # Adjust for Ace
    hand.adjust_for_ace()

# Check if the Player Hits or Stands
def hit_or_stand(deck, hand):
    # Uses to break the while loop
    global playing

    while True:

        x = input('Hit or Stand? Enter h or s: ')
        #* If someone missunderstand the question and input HIT, or stand
        if x[0].lower() == 'h':

            hit(deck, hand)

        elif x[0].lower() == 's':

            print("Player Stands Dealer's Turn")
            # Breack the While Loop
            playing = False
        
        else:

            print('Sorry, I did not understant, Please enter h or s only!')
            continue
        
        break

# Function to Display Some Cards
def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

# Function to Display All Cards
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

# Functions to interact and feedback the Player
def player_busts(player, dealer, chips):

    print('BUST PLAYER!')

    chips.lose_bet()


def player_wins(player, dealer, chips):

    print('PLAYER WINS!')

    chips.win_bet()

def dealer_busts(player, dealer, chips):

    print('PLAYER WINS! DEALER BUSTED!')

    chips.win_bet()

def dealer_wins(player, dealer, chips):

    print('DEALER WINS!')

    chips.lose_bet()

def push():

    print('Dealer and player tie! PUSH')

#* GAME FUNCTION
while True:

    print("Welcome to BLACKJACK.py")
    # Create & Shuffle the Deck
    deck = Deck()
    deck.shuffle()
    # Deal two cards to the player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    # Deal two cards to the dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    # Set up the Player's Chips
    player_chips = Chips()
    # Prompt the Player for their bet
    take_bet(player_chips)
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    #* Variable playing on hit_or_stand function
    while playing:
        # Prompt for Player Hit or Stand
        hit_or_stand(deck, player_hand)
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        # If player's hand exceeds 21, run player_busts() and break
        if player_hand.value > 21:

            player_busts(player_hand, dealer_hand, player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:

            hit(deck, dealer_hand)
        # Show all cards
        show_all(player_hand, dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    # Inform Player of their total chips
    print(f'\n Player total chips are at: {player_chips.total}')
    # Ask to play again
    new_game = input('Would you like to play another hand? y/n ')

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for Playing!')
        break
