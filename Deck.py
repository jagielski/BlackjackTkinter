"""
Deck.py: Assignment 3, CIS 211
Author: Matthew Jagielski

Defines the Deck and PinochleDeck classes initialized from less specific base classes.
Also has some error prevention tools.
"""

from random import shuffle
from Card import *

class Deck(list):
    """
    A deck of 52 standard playing cards, initialized in standard order, 
    using list as a base class.
    """
    
    def __init__(self):
        """
        Initializes a deck of 52 standard playing cards in order using list base class.
        Arguments:
            self: the deck to be initialized
        """
        list.__init__(self) # initialize as an empty
        self.extend([Card(i) for i in range(52)]) # add all of the cards in the deck
    
    def shuffle(self):
        """
        Uses shuffle from random module to shuffle the deck.
        Arguments:
            self: the Deck to be shuffled
        """
        shuffle(self) # shuffle list from random module
    
    def deal(self, n, players = 1):
        """
        Deals a hand or hands from the deck with specified length.
        Arguments: 
            self: the Deck to be dealt from
            n: the number of cards to be dealt to each hand
            players: the number of hands to be dealt, assumed to be 1
        """
        if players == 1: # with one player, we only deal one hand
            hand = []
            i = 0
            while i < n:
                i = i + 1
                hand.append(self.pop(0)) # get the first card until there are n dealt cards
            return hand
        hands = []
        for person in range(players):
            hand = [] # using the same code to make each hand
            i = 0
            while i < n:
                i = i + 1
                hand.append(self.pop(0))
            hands.append(hand)
        return hands # we have a list of hands if there are many hands to be dealt
    
    def restore(self, a):
        """
        Returns a list of Cards to the Deck
        Arguments:
            self: the Deck to be restored
            a: the list of Cards to be added to the Deck
        """
        for element in a:
            if not isinstance(element, Card): # we check to see that a is a list of Cards
                print("Only cards can be added to a deck")
                return
        self.extend(a) # Simply extend the list of Cards!
        
class PinochleDeck(Deck):
    """
    A Deck of Pinochle Cards, initialized with the Deck class
    """
    
    def __init__(self):
        """
        Initializes the Pinochle Deck with the Deck base class
        Arguments:
            self: the Deck to be initialized
        """
        Deck.__init__(self)
        lowcards = [] # We have two lists of cards: those to be removed
        goodcards = []  # and those to be duplicated
        for card in self: # we go through the Deck to arrange these cards
            if card.rank() < 7:  # based on their rank
                lowcards.append(card)
            else:
                goodcards.append(card)
        for card in lowcards: # remove all the cards under 9
            self.remove(card)
        for card in goodcards: # and duplicate the rest
            self.append(card)
        self.sort() # and finally sort the deck