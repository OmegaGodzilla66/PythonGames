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


class GUIFreezeableDie(GUIDie):
    '''a GUIDie that can be "frozen" so that it can't be rolled'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIFreezeableDie(master,[valueList,colorList]) -> GUIFreezeableDie
        creates a GUI 6-sided freeze-able die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        self.frozen = False
        GUIDie.__init__(self,master,valueList,colorList)

    def is_frozen(self):
        '''GUIFreezeableDie.is_frozen() -> bool
        returns True if the die is frozen, False otherwise'''
        return self.frozen
    
    def toggle_freeze(self):
        '''GUIFreezeableDie.toggle_freeze()
        toggles the frozen status'''
        if self.frozen:
            # if die is frozen
            self.frozen = False
            self['bg'] = 'white'
            pass
        else:
            # die isn't frozen
            self.frozen = True
            self['bg'] = 'gray'

    def roll(self):
        '''GuiFreezeableDie.roll()
        overloads GUIDie.roll() to not allow a roll if frozen'''
        if self.frozen:
            # if the die if frozen do nothing
            pass
        else:
            # else roll the die
            GUIDie.roll(self)


class Discus(Frame):
    '''Decathlon game called Discus'''

    def __init__(self,master,name):
        Frame.__init__(self,master)
        self.grid()
        self.dice = []
        self.freezeList = []
        self.score = 0
        self.numFreeze = 1
        self.attemptNum = 1
        self.scoreLabel = Label(self,text='Attempt #1: Score: 0',font=('Arial',16))
        self.scoreLabel.grid(row=0, column=1,columnspan=3)
        self.alert = Label(text = 'Click the roll button to start',font=('Arial',16))
        self.alert.grid(row=3,column=0,columnspan = 10,sticky=W)
        Label(self,text=name,font=('Arial',16)).grid(row=0,column=0,columnspan=2, sticky=W)
        self.highScoreLabel = Label(self, text='High Score: 0',font=('Arial',16))
        self.highScore = 0
        self.highScoreLabel.grid(row=0,column=5)
        for i in range(5):
            self.dice.append(GUIFreezeableDie(self, [1, 2, 3, 4, 5, 6], ['red', 'black']*3))
            self.dice[i].grid(row=1,column=i)
            self.freezeList.append(Button(self,text='Freeze', command=self.dice[i].toggle_freeze))
            self.freezeList[i].grid(row=2,column=i)
            self.freezeList[i]['state']=DISABLED
        self.rollButton = Button(self,text='Roll', command=self.roll)
        self.rollButton.grid(row=1,column=5)
        self.keepButton = Button(self,text='Stop',command=self.stop)
        self.keepButton.grid(row=2,column=5)

    def roll(self):
        for i in range(5):
            if self.dice[i].is_frozen():
                if self.freezeList[i]['state'] in [ACTIVE, 'normal']:
                    self.numFreeze += 1
        if self.numFreeze > 0:
            for i in range(5):
                self.dice[i].roll()
                if self.dice[i].is_frozen():
                    self.freezeList[i]['state'] = DISABLED
                elif self.dice[i].get_top() in [1, 3, 5]:
                    self.freezeList[i]['state'] = DISABLED
                else:
                    self.freezeList[i]['state'] = ACTIVE
            self.score = 0
            for i in range(5):
                if self.dice[i].get_top() in [1, 5, 3]:
                    pass
                else:
                    self.score += self.dice[i].get_top()
            self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum) + ': Score: ' + str(self.score)
            self.numFreeze = 0
            self.alert['text'] = 'Click the stop button to keep'
            self.fouled = True
            for i in range(5):
                if self.dice[i].get_top() in [2,4,6] and not self.dice[i].is_frozen():
                    self.fouled = False
            if self.fouled:
                self.rollButton['state'] = DISABLED
                self.keepButton['text'] = 'FOUL'
                self.scoreLabel['text'] = 'FOULED ATTEMPT'
                self.alert['text'] = 'CLick the FOUL button to continue'
                self.score = 0
                return
        else:
            self.alert['text'] = 'You must freeze a die to reroll'

    def stop(self):
        # high score test
        if self.highScore < self.score:
            self.highScore = self.score
            self.highScoreLabel['text'] = 'High Score: ' + str(self.highScore)
        # game data reset/change
        self.attemptNum += 1
        self.score = 0
        self.scoreLabel['text'] = 'Attempt #' + str(self.attemptNum) + ': Score: 0'
        for i in range(5):
            self.dice[i].erase()
            if self.dice[i].is_frozen():
                self.dice[i].toggle_freeze()
            self.dice[i]['state'] = NORMAL
        self.rollButton['state'] = ACTIVE
        self.keepButton['text'] = 'Stop'
        self.numFreeze =1
        if self.attemptNum == 4:
            self.scoreLabel['text'] = 'Game over'
            self.rollButton.grid_remove()
            self.keepButton.grid_remove()
        
        
def play_discus():              
    # test application
    root = Tk()
    test = Discus(root,'jorge')
    root.mainloop()
