from tkinter import *
from tkinter import messagebox
import random

class Minesweeper_Cell(Label):
    '''a cell in the minesweeper game'''
    def __init__(self,master,coord):
        '''SudokuCell(master,coord) -> SudokuCell
        creates a new blank SudokuCell with (row,column) coord'''
        Label.__init__(self,master,height=1,width=2,text='',\
                       bg='white',font=('Arial',24))
        self.coord = coord  # (row,column) coordinate tuple
        self['relief'] = 'raised'
        self.master = master
        # set up listeners
        self.bind('<Button-1>',self.reveal)
        self.bind('<Button-2>',self.flag)
        self.bind('<Button-3>',self.flag)
        self.isbomb = False
        self.isRevealed = False
        self.isFlagged = False

    def  get_coord(self):
        '''get the coord'''
        return self.coord

    def reveal(self,other):
        '''reveal the square'''
        self.isRevealed = True
        
        if self.isFlagged:
            pass
        elif self.isbomb: # if it is a bomb set to game over
            self['bg'] = 'red'
            self['text'] = '*'
            if self.master.is_game_over():
                pass
            else:
                self.master.gameover()
        else:
            # or reveal the number
            self['relief'] = 'sunken'
            if self.master.numCheck(self.coord) == 0:
                # if number is 0 no text
                self['text'] = ''
            else:
                # for any other number reveal that number
                self['text'] = self.master.numCheck(self.coord)
            # style changes
            self['bg'] = 'light gray'
            colormap = ['black','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
            self['fg'] = colormap[self.master.numCheck(self.coord)]
            # start autoreveal
            if self.master.numCheck(self.coord) == 0:
                self.master.autoReveal(self.coord)

    def is_bomb(self):
        '''return is a bomb'''
        return self.isbomb

    def plant_mine(self):
        '''make square a mine'''
        self.isbomb = True

    def is_revealed(self):
        '''if it is a revealed square'''
        return self.isRevealed

    def flag(self,other):
        '''flag square'''
        if self.isFlagged:
            # if it already is flagged, unflag
            self['text'] = ''
            self.isFlagged = False
            self.master.return_flag()
        elif self.master.get_num_flags() < 1:
            # if there is not enough flags left, do nothing
            pass
        
        elif not self.isFlagged:
            # or flag the square
            self['text'] = '*'
            self.isFlagged = True
            self.master.use_flag()
            self.master.has_won()

    def is_flagged(self):
        '''return if a certain square is flagged'''
        return self.isFlagged


class Minesweeper_Grid(Frame):
    '''represents the grid and main game mechanics'''
    def __init__(self,master,numrow,numcolumn,numBombs):
        '''initialize the grid'''
        Frame.__init__(self,master,bg='black')
        self.grid()
        self.master=master
        self.numrow = numrow
        self.numcolumn = numcolumn
        self.gameOver = False
        self.cellList = []
        # create the grid
        for r in range(0,numrow):
            self.cellList.append([])
            for c in range(0,numcolumn):
                self.cellList[r].append(Minesweeper_Cell(self,(r,c)))
                self.cellList[r][c].grid(row=r,column=c)
        # plant the bombs
        self.mineList = []
        for i in range(numBombs):
            r = random.randrange(numrow)
            c = random.randrange(numcolumn)
            while self.cellList[r][c].is_bomb():
                r = random.randrange(numrow)
                c = random.randrange(numcolumn)
                
            self.cellList[r][c].plant_mine()
            self.mineList.append(self.cellList[r][c])

        # set number of flags
        self.numFlags = IntVar()
        self.numFlags.set(numBombs)
        self.flagNum = Label(self,textvariable=self.numFlags,font=('Arial',20))
        self.flagNum.grid(row=numrow,column=numcolumn//2)

    def numCheck(self,coord):
        '''find what number a square should reveal'''
        numBombs = 0
        for r in range(-1,2):
            for c in range(-1,2):
                # if the square doesn't exist
                if r+coord[0]<0 or c+coord[1]<0 or r+coord[0]>len(self.cellList)-1 or c+coord[1]>len(self.cellList[r])-1:
                    continue
                # or if it is a bomb
                if self.cellList[r+coord[0]][c+coord[1]].is_bomb():
                    # add the number to the number of bombs
                    numBombs += 1

        return numBombs

    def gameover(self):
        '''Game over condition'''
        self.gameOver = True
        for r in range(self.numrow):
            for c in range(self.numcolumn):
                # if it is a bomb
                if self.cellList[r][c].is_bomb():
                    self.cellList[r][c].reveal(self) # reveal
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)

    def autoReveal(self,coord):
        '''autoreveal a 0 square (uses recusrion)'''
        numBombs = 0
        for r in range(-1,2):
            for c in range(-1,2):
                # if the square doesn't exist, do nothing
                if r+coord[0]<0 or c+coord[1]<0 or r+coord[0]>len(self.cellList)-1 or c+coord[1]>len(self.cellList[r])-1:
                    continue
                # if it has already been revealed, do nothing (so as to prevent infinite recursion)
                if self.cellList[r+coord[0]][c+coord[1]].is_revealed():
                    continue

                self.cellList[r+coord[0]][c+coord[1]].reveal(self)
        

    def is_game_over(self):
        '''return if it is game over'''
        return self.gameOver

    def use_flag(self):
        '''use a flag'''
        self.numFlags.set(self.numFlags.get()-1)

    def return_flag(self):
        '''unuse a flag'''
        self.numFlags.set(self.numFlags.get()+1)
         

    def get_num_flags(self):
        '''get the number of flags'''
        return self.numFlags.get()

    def has_won(self):
        '''return if the game is over'''
        # if every mine has been flagged
        for i in range(len(self.mineList)):
            if not self.mineList[i].is_flagged():
                return False
        # you won!
        messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)
        return True
            
            
        
def play_minesweeper():
    '''play the game of Minesweeper'''
    root = Tk()
    root.title('Minesweeper')
    Minesweeper_Grid(root,12,10,15)
    root.mainloop()
play_minesweeper()
