"""
Card.py: Assignment 2, CIS 211
Author: Matthew Jagielski

Defines the Card and BlackjackCard classes for more advanced usage. Also 
contains functions for calculating how many points are in a list of Cards or 
BlackjackCards, and a deck creator for either type of card.
"""

class Card:
    """
    A card, defined by its ID, or its place in a sorted deck
    """
    def __init__(self, num):
        """
        Creates a card with specified id.
        Arguments:
            self: the Card to be initialized
            num: the id of the specified card
        """
        
        if 0 <= num <= 51:
            self._id = num
        else:
            print('Error: initial value must be between 0 and 51')
    
    def rank(self):
        """
        An accessor function returning the rank of a card within its suit.
        Arguments:
            self: the requested card
        Returns:
            self.rank(): the rank of a card independent of suit
        """
        return self._id % 13
        
    def suit(self):
        """
        An accessor function returning the suit of a card.
        Arguments:
            self: the requested card
        Returns:
            self.suit(): the suit of the card: 0, 1, 2, or 3
                0: club; 1: diamond; 2: heart; 3: spade
        """
        return self._id//13
        
    def points(self):
        """
        An accessor function returning the number of points the card has
        in a game of cribbage.
        Arguments:
            self: the requested card
        Returns:
            self.points(): the cribbage points of the card
        """
        if self.rank() <= 8: # If not a suit card or ace, no points given
            return 0
        else:
            return self.rank() - 8
    
    def __repr__(self):
        """
        The representation of a card, with its symbol (number or J,Q,K,A) and suit
        Arguments:
            self: the requested card
        Returns:
            repr: the representation of the card using its symbol and suit
        """
        if self.rank() < 9:
            return str(self.rank() +2) + Card.syms[self.suit()] # Number cards are number + suit
        else:
            return Card.reprs[self.rank() - 9] + Card.syms[self.suit()] # Other cards have special symbols
        
    def __lt__(self, other):
        """
        A comparison function for two cards, comparing based on id.
        Arguments:
            self: the first requested card
            other: the other requested card
        Returns:
            Boolean indicating if the first card has a smaller id (True) or larger (False)
        """
        return self._id < other._id
        
    syms = ['C', 'D', 'H', 'S'] # The symbols for suit
    
    reprs = ['J', 'Q', 'K', 'A'] # The symbols for non-numeric cards

class BlackjackCard(Card):
    """
    A blackjack card, defined the same way as in Card, but with different point allocations.
    """
    def __init__(self, num):
        """
        Creates the blackjack card with specified id.
        Arguments:
            self: the card to be initialized
            num: the desired id for the card
        """
        Card.__init__(self, num) # Initialized in the same way as Card
    
    def points(self):
        """
        Calculates the number of points in blackjack a card will have
        Arguments:
            self: the requested card
        Returns:
            self.points(): the number of points the card would have in blackjack
        """
        if self.rank() < 9:
            return self.rank() + 2 # Takes the numerical value of number cards
        elif 8 < self.rank() < 12:
            return 10 # All face cards are worth 10 points
        elif self.rank() == 12:
            return 11 # Aces are worth 11 points
    
    def __lt__(self, other):
        """
        A comparison function for two cards, comparing based on point value.
        Arguments:
            self: the first requested card
            other: the other requested card
        Returns:
            Boolean indicating if the first card has a smaller point value (True) or larger (False)
        """
        return self.points() < other.points()

def points(li):
    """
    Takes a list of cards and calculates how many total points the list is worth
    Arguments:
        li: a list of cards of either Card or BlackjackCard
    Returns:
        total: the total number of points of the whole list of cards, using the 
            appropriate point system (cribbage or blackjack)
    """
    total = 0 # Initialize total point count
    for card in li:
        total += card.points() # Add up all of the points for each card
    return total
    
def new_deck(type):
    """
    Uses a type of card and creates a standard deck of cards with this type.
    Arguments:
        type: The class of card used: Card or BlackjackCard
    Returns:
        A standard deck of 52 cards, in order, of the type of card requested.
    """
    return [type(i) for i in range(52)]