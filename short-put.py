from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)



class ShortPutFrame(Frame):
    '''frame for a game of 1500 Meters'''

    def __init__(self,master,name):
        '''ShortPutFrame(master,name) -> Decath100MFrame
        creates a new 1500 Meters frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self,master)
        self.grid()
        # label for player's name
        Label(self,text=name,font=('Arial',16)).grid(columnspan=3,sticky=W)
        # set up score and rerolls
        self.scoreLabel = Label(self,text='Attempt #1: Score: 0',font=('Arial',16))
        self.scoreLabel.grid(row=0,column=2,columnspan=3)
        self.highScoreLabel = Label(self,text='High Score: 0',font=('Arial',16))
        self.highScore = 0
        self.highScoreLabel.grid(row=0,column=5,columnspan=3,sticky=E)
        # initialize game data
        self.score = 0
        self.rerolls = 5
        self.gameround = 0
        self.round = 1
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[-1,2,3,4,5, 6],['red']+['black']*5))
            self.dice[n].grid(row=1,column=n)
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2,columnspan=1)
        self.stopButton = Button(self,text='Stop',command=self.stop)
        self.stopButton.grid(row=3,columnspan=1)

    def roll(self):
        '''ShortPutFrame.roll()
        handler method for the roll button click'''
        # roll die
        for i in range(0, 1):
            self.dice[self.gameround+i].roll()
        #test for fouls
        if self.dice[self.gameround].get_top() == -1:
            self.rollButton['state'] = DISABLED
            self.stopButton['text'] = 'FOUL'
            self.scoreLabel['text'] = 'FOULED ATTEMPT'
            self.score = 0
            return
        # if this was the first roll of the round, turn on the keep button6
        # add dice to score and update the scoreboard
        for i in range(0, 1):
            self.score += self.dice[self.gameround+i].get_top()
        self.scoreLabel['text'] = 'Attempt #' + str(self.round) + ': Score: '+str(self.score)
        self.gameround += 1  # go to next round
        if self.gameround < 8:  # move buttons to next pair of dice
            self.rollButton.grid(row=2,column=self.gameround,columnspan=1)
            self.stopButton.grid(row=3,column=self.gameround,columnspan=1)
        else:
            self.rollButton['state'] = DISABLED

    def stop(self):
        '''end round of the game'''
        # high score test
        if self.highScore < self.score:
            self.highScore = self.score
            self.highScoreLabel['text'] = 'High Score: ' + str(self.highScore)
        # reset game data
        self.rollButton.grid(row=2, column = 0)
        self.stopButton.grid(row=3, column=0)
        self.score = 0
        self.gameround = 0
        self.round += 1
        # update game data
        self.scoreLabel['text'] = 'Attempt #' + str(self.round) + ': Score: 0'
        for i in range(8):
            self.dice[i].erase()
        self.rollButton['state'] = ACTIVE
        self.stopButton['text'] = 'Stop'
        # test if the game is over
        if self.round == 4:
            self.scoreLabel['text'] = 'Game over'
            self.rollButton.grid_remove()
            self.stopButton.grid_remove()

root = Tk()
# play the game
ShortPutFrame(root, input('Enter Name: '))
root.mainloop()
