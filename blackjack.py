from tkinter import *
from Deck import *
from CardLabel import *
from tkinter.messagebox import showinfo

deck = Deck(BlackjackCard)
dealerhand=[]
playerhand=[]

def squareone():
    hitbutton['state']='normal'
    standbutton['state']='normal'
    deck.restore(dealerhand)
    deck.restore(playerhand)
    deck.shuffle()
    for cardnum in range(6):
        dealer[cardnum].display('blank')
        player[cardnum].display('blank')
    
    
def deal():
    global deck, dealerhand, playerhand
    squareone()
    
    dealerhand = deck.deal(2)
    dealer[0].display('back')
    dealer[1].display('front', dealerhand[1]._id)
    
    playerhand = deck.deal(2)
    for cardno in range(2):
        player[cardno].display('front', playerhand[cardno]._id)
    
    if total(dealerhand)[0] == 21:
        if total(playerhand)[0] == 21:
            dealer[0].display('front', dealerhand[0]._id)
            showinfo("Push", "Two blackjacks")
        else:
            dealer[0].display('front', dealerhand[0]._id)
            showinfo("You lose", "Dealer blackjack")
        hitbutton['state'] = 'disabled'
        standbutton['state'] = 'disabled'
    
    if total(playerhand)[0] == 21:
        dealer[0].display('front', dealerhand[0]._id)
        if total(dealerhand)[0] < 21:
            showinfo("You win", "Blackjack!")
        hitbutton['state'] = 'disabled'
        standbutton['state'] = 'disabled'

def total(hand):
    result = 0
    numAces = 0
    for card in hand:
        """
        if card.rank() < 9:
            result += card.rank() + 2 # Takes the numerical value of number cards
        elif 8 < card.rank() < 12:
            result += 10 # All face cards are worth 10 points
        elif card.rank() == 12:
            result += 11"""
        result += card.points()
        if card.rank() == 12:    
            numAces += 1
    while result > 21 and numAces > 0:
        result -= 10
        numAces -= 1
    return [result, numAces]

def hit():
    playercount = len(playerhand)
    playerhand.extend(deck.deal(1))
    player[playercount].display('front', playerhand[playercount]._id)
    
    if total(playerhand)[0] > 21:
        showinfo("Bust!", "Better luck next time...")
        hitbutton['state']='disabled'
        standbutton['state']='disabled'



def stand():
    hitbutton['state']='disabled'
    standbutton['state']='disabled'
    dealer[0].display('front', dealerhand[0]._id)
    
    while total(dealerhand)[0] < 17:
        dealercount = len(dealerhand)
        dealerhand.extend(deck.deal(1))
        dealer[dealercount].display('front', dealerhand[dealercount]._id)
    
    if total(dealerhand)[0] > 21:
        showinfo("Dealer bust", "You win!")
    elif total(dealerhand)[0] > total(playerhand)[0]:
        showinfo("Dealer wins", "Better luck next time...")
    elif total(dealerhand)[0] == total(playerhand)[0]:
        showinfo("Push!", "Maybe you'll win next time...")
    else:
        showinfo("You win!", "Congratulations!")





root = Tk()

CardLabel.load_images()

dealer = [0]*6
player = [0]*6

for cardnum in range(6):
    dealer[cardnum] = CardLabel(root)
    dealer[cardnum].grid(row=0, column=cardnum, padx=10)
    dealer[cardnum].display('blank')

for cardnum in range(6):
    player[cardnum] = CardLabel(root)
    player[cardnum].grid(row=1, column=cardnum, padx=10)
    player[cardnum].display('blank')

dealbutton = Button(root, text = "Deal", command=deal)
dealbutton.grid(row=2, column = 0, columnspan=2, pady=20)

hitbutton = Button(root, text = "Hit", command=hit)
hitbutton.grid(row=2, column=2, columnspan=2, pady=20)

standbutton = Button(root, text = "Pass", command=stand)
standbutton.grid(row=2, column=4, columnspan=6, pady=20)

if __name__ == "__main__":
    root.mainloop()