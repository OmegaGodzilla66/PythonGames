from tkinter import *

class Checkers_Square(Canvas):
    def __init__(self,master,color,coord):
        '''create a checkers square'''
        Canvas.__init__(self,master,width=60,height=60,bg=color,highlightthickness=5, highlightbackground=color)
        self.checker_on = False
        self.checker_color = None
        self.master = master
        self.coord = coord
        self.color = color

    # red checker mechanics start
    
    def move_on_red(self,other):
        '''move on a red checker'''
        self.create_red_checker()
        self.bind('<Button-1>',self.move_red)
        self.master.unready()
        self.master.move_off()

    def move_on_red_king(self,other):
        '''move on a red king'''
        self.create_red_king()
        self.bind('<Button-1>',self.move_red_king)
        self.master.unready()
        self.master.move_off()

    def bind_red(self):
        '''bind a red checker'''
        self.bind('<Button-1>',self.move_red)

    def ready_red(self,rl):
        '''ready a red checker move'''
        if self.checker_on and self.checker_color == 'white':
            self.master.ready_jump_red(self.coord,rl)
        else:
            self.bind('<Button-1>',self.move_on_red)

    def ready_red_king(self,rl):
        '''ready a red king'''
        if self.checker_on and self.checker_color == 'white':
            self.master.ready_jump_red_king(self.coord,rl)
        else:
            self.bind('<Button-1>',self.move_on_red_king)

    def move_red(self,other):
        '''result of a square being clicked on (red)'''
        self.master.unready()
        if self.checker_on:
            self['highlightbackground'] = 'black'
            self.master.ready_squares_red(self.coord)

    def move_red_king(self,other):
        '''move a red king (result of being clicked on)'''
        self.master.unready()
        if self.checker_on:
            self['highlightbackground'] = 'black'
            self.master.ready_squares_red_king(self.coord)

    def create_red_checker(self):
        '''create a red checker'''
        self.checker_on = True
        self.create_oval(10,10,60,60,fill='red')
        self.checker_color = 'red'

    def create_red_king(self):
        '''creates a red king'''
        self.create_red_checker()
        self.create_text(40,50,text='*',font=('Arial',55))

    def make_red_king(self):
        '''makes a square a red king'''
        self.move_off()
        self.move_on_red_king(self)


    # white checker mechanics start

    def move_on_white(self,other):
        '''move on a white checker'''
        self.create_white_checker()
        self.bind_white()
        self.master.unready()
        self.master.move_off()

    def bind_white(self):
        '''bind a white checker'''
        self.bind('<Button-1>',self.move_white)

    def move_on_white_king(self,other):
        '''move on a white checker'''
        self.create_white_king()
        self.bind('<Button-1>',self.move_white_king)
        self.master.unready()
        self.master.move_off()

    def create_white_checker(self):
        '''create a new white checker'''
        self.checker_on = True
        self.create_oval(10,10,60,60,fill='white')
        self.checker_color = 'white'

    def ready_white(self,rl):
        '''ready a mvoe for  a white checker'''
        if self.checker_on and self.checker_color == 'red':
            self.master.ready_jump_white(self.coord,rl)
        else:
            self.bind('<Button-1>',self.move_on_white)

    def ready_white_king(self,rl):
        '''ready a mvoe for  a white checker'''
        if self.checker_on and self.checker_color == 'red':
            self.master.ready_jump_white_king(self.coord,rl)
        else:
            self.bind('<Button-1>',self.move_on_white_king)

    def move_white(self,other):
        '''result of being clicked (white)'''
        self.master.unready()
        if self.checker_on:
            self['highlightbackground'] = 'black'
            self.master.ready_squares_white(self.coord)

    def move_white_king(self,other):
        '''result of being clicked (white)'''
        self.master.unready()
        if self.checker_on:
            self['highlightbackground'] = 'black'
            self.master.ready_squares_white_king(self.coord)

    def create_white_king(self):
        '''create a white king'''
        self.create_white_checker()
        self.create_text(40,50,text='*',font=('Arial',55))

    def make_white_king(self):
        '''make a square a white king'''
        self.move_off()
        self.move_on_white_king(self)

    # Universal mechanics start

    def get_bg(self):
        '''getter method for bg color'''
        return self['bg']

    def unready(self):
        '''UNIVERSAL unready'''
        self['highlightbackground'] = self.color
        if not self.checker_on:
            self.unbind('<Button-1>')

    def unbind_(self,other):
        '''unbind a square'''
        self.unbind('<Button-1>')
        
    def move_off(self):
        '''move off all checkers'''
        checkers = self.find_all()
        for checker in checkers:
            self.delete(checker)
        self.checker_on = False
        self.unbind('<Button-1>')
        self.checker_color = None
        self.jump_square = None

    def is_checker_on(self):
        '''getter method for if a checker is on'''
        return self.checker_on

    def get_checker_color(self):
        '''getter method for checker color'''
        return self.checker_color
            

class Checkers_Grid(Frame):
    def __init__(self,master):
        '''create a new grid (also handels game mechanics'''
        Frame.__init__(self,master,bg='white')
        self.grid()
        self.jump_square = None
        Label(self,text='Turn: ',bg='white').grid(row=8,column=1)
        self.squareList = []
        mainColorList = [['dark green','blanched almond'],['blanched almond','dark green']]
        for r in range(8):
            colorList = mainColorList[r%2]
            self.squareList.append([])
            for c in range(8):
                self.squareList[r].append(Checkers_Square(self,colorList[c%2],(r,c)))
                self.squareList[r][c].grid(row=r,column=c)
        
        self.readiedSquare = self.squareList[0][1]
        self.turnFrame = Checkers_Square(self,'gray',(8,1))
        self.turnFrame.grid(row=8,column=2)
        self.turnFrame.create_white_checker()
        for r in [0,1,2]:
            for c in range(8):
                if self.squareList[r][c].get_bg() == 'dark green':
                    self.squareList[r][c].move_on_red(self)
        for r in [5,6,7]:
            for c in range(8):
                if self.squareList[r][c].get_bg() == 'dark green':
                    self.squareList[r][c].move_on_white(self)

    
        self.jump_made = False
        self.move_off()
    def ready_squares_red(self,coord):
        '''ready squares for red move'''
        self.jump_square = None
        self.jump_made = False
        if coord[0] == 7:
            self.squareList[coord[0]][coord[1]].make_red_king()
            # MAKE KING
        elif coord[1] == 0:
            if coord[0]+1 != 8 and coord[1]+1 != 8 and self.squareList[coord[0]+1][coord[1]+1].get_checker_color() != 'red':
                self.squareList[coord[0]+1][coord[1]+1].ready_red(0) #RIGHT
        elif coord[1] == 7:
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]+1][coord[1]-1].get_checker_color() !='red':
                self.squareList[coord[0]+1][coord[1]-1].ready_red(1) #LEFT
        else:
            if coord[0]+1 != 8 and coord[1]+1 != 8 and self.squareList[coord[0]+1][coord[1]+1].get_checker_color() !='red':
                self.squareList[coord[0]+1][coord[1]+1].ready_red(0) #RIGHT
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]+1][coord[1]-1].get_checker_color() !='red':
                self.squareList[coord[0]+1][coord[1]-1].ready_red(1) #LEFT


        self.readiedSquare = self.squareList[coord[0]][coord[1]]
        if self.jump_made == True:
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]+1][coord[1]+1].unready() #RIGHT
            
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:
                self.squareList[coord[0]+1][coord[1]-1].unready() #LEFT

    def ready_jump_red(self,coord,rl):
        '''ready squares for a red move'''
        self.squareList[coord[0]][coord[1]].unready()
        self.jump_made = True
        if rl == 0:
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8 and not self.squareList[coord[0]+1][coord[1]+1].is_checker_on():
                self.squareList[coord[0]+1][coord[1]+1].ready_red(0) #RIGHT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # RIGHT
        else:
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8 and not self.squareList[coord[0]+1][coord[1]-1].is_checker_on():
                self.squareList[coord[0]+1][coord[1]-1].ready_red(1) #LEFT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # LEFT
    def ready_jump_white(self,coord,rl):
        '''ready a white jump'''
        self.jump_made = True
        self.squareList[coord[0]][coord[1]].unready()
        if rl == 1:
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8 and not self.squareList[coord[0]-1][coord[1]-1].is_checker_on():
                self.squareList[coord[0]-1][coord[1]-1].ready_white(1) #LEFT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # LEFT
        elif rl == 0:
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8 and not self.squareList[coord[0]-1][coord[1]+1].is_checker_on():
                self.squareList[coord[0]-1][coord[1]+1].ready_white(0) #RIGHT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # RIGHT
 
    def ready_squares_white(self,coord):
        '''ready squares for a white move'''
        self.jump_made = False
        self.jump_sqaure = None
        if coord[0] == 0:
            self.squareList[coord[0]][coord[1]].make_white_king()
            # MAKE KING
        elif coord[1] == 7:
            if coord[0]-1 != -1 and coord[1]-1 != 8 and self.squareList[coord[0]-1][coord[1]-1].get_checker_color() != 'white':
                self.squareList[coord[0]-1][coord[1]-1].ready_white(1) #LEFT
        elif coord[1] == 0:
            if coord[0]-1 != -1 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]+1].get_checker_color() != 'white':
                self.squareList[coord[0]-1][coord[1]+1].ready_white(0) #RIGHT
        else:
            if coord[0]-1 != -1 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]+1].get_checker_color() != 'white':
                self.squareList[coord[0]-1][coord[1]+1].ready_white(0) #RIGHT
            if coord[0]-1 != -1 and coord[1]-1 != 8 and self.squareList[coord[0]-1][coord[1]-1].get_checker_color() != 'white':
                self.squareList[coord[0]-1][coord[1]-1].ready_white(1) #LEFT
        self.readiedSquare = self.squareList[coord[0]][coord[1]]
        if self.jump_made == True:
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]-1][coord[1]+1].unready() #RIGHT
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:
                self.squareList[coord[0]-1][coord[1]-1].unready() #LEFT

    def unready(self):
        '''unready all squares'''
        for r in range(8):
            for c in range(8):
                self.squareList[r][c].unready()

    def move_off(self):
        '''after a move has been completed'''
        self.readiedSquare.move_off()
        if self.jump_square != None:
            self.jump_square.move_off()
        if self.turnFrame.get_checker_color() == 'red':
            self.turnFrame.create_white_checker()
        else:
            self.turnFrame.create_red_checker()
        
        for r in range(8):
            for c in range(8):
                self.squareList[r][c].unbind_(self)
        for r in range(8):
            for c in range(8):
                if self.squareList[r][c].get_checker_color()  == self.turnFrame.get_checker_color():
                    self.squareList[r][c].move_off()
                    if self.turnFrame.get_checker_color() == 'red':
                        self.squareList[r][c].create_red_checker()
                        self.squareList[r][c].bind_red()
                    elif self.turnFrame.get_checker_color() == 'white':
                        self.squareList[r][c].create_white_checker()
                        self.squareList[r][c].bind_white()

    def ready_squares_white_king(self,coord):
        '''ready squares for a white king'''
        self.jump_sqaure = None
        self.jump_made = True
        if coord[0] == 0:
            pass

        # RED
        elif coord[1] == 7:
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]-1].get_checker_color() == 'white':
                self.squareList[coord[0]-1][coord[1]-1].ready_white_king(1) #LEFT
        elif coord [1] == 0:
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]+1].get_checker_color() == 'white':
                self.squareList[coord[0]-1][coord[1]+1].ready_white_king(0) #RIGHT
        else:
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]+1].get_checker_color() == 'white':
                self.squareList[coord[0]-1][coord[1]+1].ready_white_king(0) #RIGHT
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]-1].get_checker_color() == 'white':
                self.squareList[coord[0]-1][coord[1]-1].ready_white_king(1) #LEFT
        self.readiedSquare = self.squareList[coord[0]][coord[1]]
        if coord[0] == 7:
            pass

        # White
        elif coord[1] == 0:
            if coord[0]-1 != -1 and coord[1]+1 != -1 and self.squareList[coord[0]+1][coord[1]+1].get_checker_color() == 'white':
                self.squareList[coord[0]+1][coord[1]+1].ready_white_king(0) #RIGHT
        elif coord[1] == 7:
            if coord[0]-1 != -1 and coord[1]-1 != 8 and self.squareList[coord[0]+1][coord[1]-1].get_checker_color() =='white':
                self.squareList[coord[0]+1][coord[1]-1].ready_white_king(1) #LEFT
        else:
            if coord[0]-1 != -1 and coord[1]+1 != -1 and self.squareList[coord[0]+1][coord[1]+1].get_checker_color() =='white':
                self.squareList[coord[0]+1][coord[1]+1].ready_white_king(0) #RIGHT
            if coord[0]-1 != -1 and coord[1]-1 != 8 and self.squareList[coord[0]+1][coord[1]-1].get_checker_color() =='white':
    
                self.squareList[coord[0]+1][coord[1]-1].ready_white_king(1) #LEFT
    
        if self.jump_made == True:
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]+1][coord[1]+1].unready() #RIGHT
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:
                self.squareList[coord[0]+1][coord[1]-1].unready() #LEFT
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]-1][coord[1]+1].unready() #RIGHT
            if not coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]-1][coord[1]-1].unready() #LEFT




    def ready_squares_red_king(self,coord):
        '''ready squares for a red king'''
        self.jump_made = False
        self.jump_sqaure = None
        if coord[0] == 0:
            pass
        elif coord[1] == 7:
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]-1].get_checker_color() != 'red':
                self.squareList[coord[0]-1][coord[1]-1].ready_red_king(1) #LEFT
        elif coord [1] == 0:
            if  coord[0]+1 != 8 and coord[1]+1 != 8 and self.squareList[coord[0]-1][coord[1]+1].get_checker_color() != 'red':
                self.squareList[coord[0]-1][coord[1]+1].ready_red_king(0) #RIGHT
        else:
            if coord[0]+1 != 8 and coord[1]+1 != 8 and self.squareList[coord[0]-1][coord[1]+1].get_checker_color() != 'red':
                self.squareList[coord[0]-1][coord[1]+1].ready_red_king(0) #RIGHT
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]-1][coord[1]-1].get_checker_color() != 'red':
                self.squareList[coord[0]-1][coord[1]-1].ready_red_king(1) #LEFT
        self.readiedSquare = self.squareList[coord[0]][coord[1]]
        if coord[0] == 7:
            pass
        elif coord[1] == 0:
            if coord[0]+1 != 8 and coord[1]+1 != 8 and self.squareList[coord[0]+1][coord[1]+1].get_checker_color() != 'red':
                self.squareList[coord[0]+1][coord[1]+1].ready_red_king(0) #RIGHT
        elif coord[1] == 7:
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]+1][coord[1]-1].get_checker_color() !='red':
                self.squareList[coord[0]+1][coord[1]-1].ready_red_king(1) #LEFT
        else:
            if coord[0]+1 != 8 and coord[1]+1 != 8 and self.squareList[coord[0]+1][coord[1]+1].get_checker_color() !='red':
                self.squareList[coord[0]+1][coord[1]+1].ready_red_king(0) #RIGHT
            if coord[0]+1 != 8 and coord[1]+1 != -1 and self.squareList[coord[0]+1][coord[1]-1].get_checker_color() !='red':
                self.squareList[coord[0]+1][coord[1]-1].ready_red_king(1) #LEFT
        
        if self.jump_made == True:
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]+1][coord[1]+1].unready() #RIGHT
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:
                self.squareList[coord[0]+1][coord[1]-1].unready() #LEFT
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:
                self.squareList[coord[0]-1][coord[1]+1].unready() #RIGHT
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:
                self.squareList[coord[0]-1][coord[1]-1].unready() #LEFT



        
        
    def ready_jump_red_king(self,coord,rl):
        '''ready squares for a red king jump'''
        self.jump_made = True
        self.squareList[coord[0]][coord[1]].unready()
        if rl == 0:
            if coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8 and not self.squareList[coord[0]+1][coord[1]+1].is_checker_on():
                self.squareList[coord[0]+1][coord[1]+1].ready_red_king(0) #RIGHT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # RIGHT
        else:
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8 and not self.squareList[coord[0]+1][coord[1]-1].is_checker_on():
                self.squareList[coord[0]+1][coord[1]-1].ready_red_king(1) #LEFT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # LEFT
        if rl == 1:
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8 and not self.squareList[coord[0]-1][coord[1]-1].is_checker_on():
                self.squareList[coord[0]-1][coord[1]-1].ready_red_king(1) #LEFT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # LEFT
        elif rl == 0:
            if coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8 and not self.squareList[coord[0]-1][coord[1]+1].is_checker_on():
                self.squareList[coord[0]-1][coord[1]+1].ready_red_king(0) #RIGHT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # RIGHT
    def ready_jump_white_king(self,coord,rl):
        '''ready squares for a white king jump'''
        self.jump_made = True
        self.squareList[coord[0]][coord[1]].unready()
        if rl == 0:
            if self.squareList[coord[0]+1][coord[1]+1].is_checker_on()and coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:#+1+1
                self.squareList[coord[0]+1][coord[1]+1].ready_white_king(0)   #RIGHT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # RIGHT
        else:
            if self.squareList[coord[0]+1][coord[1]-1].is_checker_on()and coord[0]+1 != -1 and coord[0]+1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:#+1-1
                self.squareList[coord[0]+1][coord[1]-1].ready_white_king(1) #LEFT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # LEFT
        if rl == 1:
            if self.squareList[coord[0]-1][coord[1]-1].is_checker_on()and coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]-1 != -1 and coord[1]-1 != 8:#-1-1
                self.squareList[coord[0]-1][coord[1]-1].ready_white_king(1) #LEFT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # LEFT
        elif rl == 0:
            if self.squareList[coord[0]-1][coord[1]+1].is_checker_on()and coord[0]-1 != -1 and coord[0]-1 != 8 and coord[1]+1 != -1 and coord[1]+1 != 8:#-1+1
                self.squareList[coord[0]-1][coord[1]+1].ready_white_king(0) #RIGHT
                self.jump_square = self.squareList[coord[0]][coord[1]]
                # RIGHT
        
        


def play_checkers():
    '''play the game of checkers - note: there are still a few bugs, please report them if you find them'''
    root = Tk()
    root.title('Checkers')
    Checkers_Grid(root)
    root.mainloop()

play_checkers()
