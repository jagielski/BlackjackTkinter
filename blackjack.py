"""
blackjack.py: Assignment 5, CIS 211
Author: Matthew Jagielski

Runs a Graphical User Interface designed to play blackjack. There are two hands, each
containing up to six cards (dealer and player), and buttons to facilitate dealing, passing,
hitting, and betting with a fake pile of money.
"""

from tkinter import * ## we must import things from many modules
from Deck import *
from CardLabel import *
from tkinter.messagebox import showinfo

deck = Deck(BlackjackCard) ## initializing variables such as the deck
dealerhand=[] ## the list of the dealer's BlackjackCards
playerhand=[] ## that of the player's
MONEY = 1000000 ## the cash stack of the player
playerwon = 'push' ## and a variable telling us who won

def squareone():
    """
    A function to reset all values of the blackjack game to the defaults.
    """
    hitbutton['state']='normal'  ## reset all the buttons
    standbutton['state']='normal'
    betton['state']='disabled'
    betentry['state']='disabled'
    deck.restore(dealerhand)
    deck.restore(playerhand)
    deck.shuffle()  ## return the deck to shuffled
    for cardnum in range(6):  ## reset all graphics
        dealer[cardnum].display('blank')
        player[cardnum].display('blank')
    
def deal():
    """
    Deals out cards: one facedown and one faceup for the dealer, and two faceup cards for the player.
    Also checks for blackjacks.
    """
    global deck, dealerhand, playerhand
    squareone()  ## back to square one
    
    dealerhand = deck.deal(2)
    dealer[0].display('back')
    dealer[1].display('front', dealerhand[1]._id) ## deal out the dealer's hand and display it
    
    playerhand = deck.deal(2)
    for cardno in range(2):
        player[cardno].display('front', playerhand[cardno]._id) ## deal out the player's hand and display it
    
    if total(dealerhand)[0] == 21:  ## check for all blackjacks
        if total(playerhand)[0] == 21: ## if player also has blackjack
            dealer[0].display('front', dealerhand[0]._id)
            showinfo("Push", "Two blackjacks")
            pay_out('push')
        else: ## if dealer has only blackjack
            dealer[0].display('front', dealerhand[0]._id)
            showinfo("You lose", "Dealer blackjack")
            pay_out('dealer')
        hitbutton['state'] = 'disabled'
        standbutton['state'] = 'disabled'
    
    if total(playerhand)[0] == 21:
        dealer[0].display('front', dealerhand[0]._id)
        if total(dealerhand)[0] < 21: ## if the player has the only blackjack
            showinfo("You win", "Blackjack!")
            pay_out('playerbj') ## pay out the player blackjack
        hitbutton['state'] = 'disabled'
        standbutton['state'] = 'disabled'

def total(hand):
    """
    Returns a list of two items. The first item is the total number of points in
    the hand and the second is the number of aces in the hand. Not currently used,
    the number of aces in the hand is useful for extending the program to suggest 
    strategies for the player
    """
    result = 0 ## initialize values
    numAces = 0
    for card in hand:
        result += card.points() ## add up all the points of each card
        if card.rank() == 12:    
            numAces += 1 ## increment the number of aces
    while result > 21 and numAces > 0:
        result -= 10 ## fix the total if an ace counts as too many points
        numAces -= 1
    return [result, numAces] ## return the list

def hit():
    """
    Adds a card to the player's hand, and displays it. Also checks for a bust.
    """
    playercount = len(playerhand)
    playerhand.extend(deck.deal(1)) ## add a card to the deck
    player[playercount].display('front', playerhand[playercount]._id) ## display that card
    
    if total(playerhand)[0] > 21: ## check for a bust
        showinfo("Bust!", "Better luck next time...")
        pay_out('dealer') ## if so, display a window and the player loses
        hitbutton['state']='disabled'
        standbutton['state']='disabled'

def stand():
    """
    Removes the ability to continue to hit. The dealer then starts to add cards until it
    reaches a score of 17 or higher. Pays out money accordingly.
    """
    hitbutton['state']='disabled'
    standbutton['state']='disabled' ## no more cards added to the player's hand
    dealer[0].display('front', dealerhand[0]._id) ## show the dealer's secret card
    
    while total(dealerhand)[0] < 17: ## add cards to the dealer's hand
        dealercount = len(dealerhand)
        dealerhand.extend(deck.deal(1))
        dealer[dealercount].display('front', dealerhand[dealercount]._id)
    
    ### allocate money based on who won the game and display a window
    if total(dealerhand)[0] > 21: ## dealer bust, player wins
        showinfo("Dealer bust", "You win!")
        pay_out('player')
    elif total(dealerhand)[0] > total(playerhand)[0]: ## player loses
        showinfo("Dealer wins", "Better luck next time...")
        pay_out('dealer')
    elif total(dealerhand)[0] == total(playerhand)[0]: ## player and dealer tie
        showinfo("Push!", "Maybe you'll win next time...")
        pay_out('push')
    else: ## player wins by totals
        showinfo("You win!", "Congratulations!")
        pay_out('player')

def bet():
    """
    Bet money based on an amount inputted by the user.
    """
    if betentry.get() == '': ## if there is no bet, don't bet anything
        cashbet = 0
    else: ## get the bet from the betentry entry box
        cashbet = int(betentry.get())
    cashstack = int(cashentry.get())
    newcashstack = cashstack-cashbet 
    
    betentry['state'] = 'disabled' ## no betting during the match!
    cashentry['state'] = 'normal'
    
    cashentry.delete(0, END)
    cashentry.insert(0, newcashstack)
    cashentry['state'] = 'disabled'
    betton['state'] = 'disabled'
    
def pay_out(winner):
    """
    Pays out money to the player based on the result of the game
    """
    betentry['state'] = 'normal'
    cashentry['state'] = 'normal'
    if betentry.get() == '':
        cashbet = 0
    else:    
        cashbet = int(betentry.get())
    cashstack = int(cashentry.get())
    
    if winner == 'player':
        newcashstack = cashstack + 2*cashbet ## player wins and gets his bet
    elif winner == 'dealer':
        newcashstack = cashstack ## no money given to the loser
    elif winner == 'push':
        newcashstack = cashstack + cashbet ## give back money if a tie
    elif winner == 'playerbj':
        newcashstack = cashstack + 5*cashbet//2 ## big payout for a blackjack win
    
    betentry.delete(0, END)
    cashentry.delete(0, END)
    cashentry.insert(0, newcashstack)
    cashentry['state'] = 'disabled'
    betton['state'] = 'normal'
        

root = Tk()

CardLabel.load_images() ## load the images

dealer = [0]*6
player = [0]*6

for cardnum in range(6): ## make six images for the dealer's cards
    dealer[cardnum] = CardLabel(root)
    dealer[cardnum].grid(row=0, column=cardnum, padx=10)
    dealer[cardnum].display('blank')

for cardnum in range(6): ## do the same for the player's cards
    player[cardnum] = CardLabel(root)
    player[cardnum].grid(row=1, column=cardnum, padx=10)
    player[cardnum].display('blank')

dealbutton = Button(root, text = "Deal", command=deal) ## make a button for dealing
dealbutton.grid(row=2, column = 0, columnspan=2, pady=20)

hitbutton = Button(root, text = "Hit", command=hit) ## and for hitting
hitbutton.grid(row=2, column=2, columnspan=2, pady=20)

standbutton = Button(root, text = "Stand", command=stand) ## and for standing
standbutton.grid(row=2, column=4, columnspan=6, pady=20)

cashlabel = Label(root, text="Cash:") 
cashlabel.grid(row=3, column=0, pady=20)

cashentry = Entry(root) ## an entry box for how much money the player has
cashentry.grid(row=3, column=1, columnspan=2)
cashentry.insert(0, MONEY)
cashentry['state'] = 'disabled'

betlabel = Label(root, text="Bet:")
betlabel.grid(row=3, column=3)

betentry = Entry(root) ## where the player bets
betentry.grid(row=3, column=4)

betton = Button(root, text="Bet", command=bet) ## a button for betting
betton.grid(row=3, column=5)

if __name__ == "__main__":
    root.mainloop()