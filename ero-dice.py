import random

class Die:
  '''Die class'''

  def __init__(self,sidesParam=6):
    '''Die([sidesParam])
    creates a new Die object
    int sidesParam is the number of sides
    (default is 6)
    -or- sidesParam is a list/tuple of sides'''
    # if an integer, create a die with sides
    #  from 1 to sides
    if isinstance(sidesParam,int):
      sidesParam = range(1,sidesParam+1)
    self.sides = list(sidesParam)
    self.numSides = len(self.sides)
    # roll the die to get a random side on top to start
    self.roll()

  def __str__(self):
    '''str(Die) -> str
    string representation of Die'''
    return str(self.numSides)+'-sided die with '+str(self.top)+' on top'

  def roll(self):
    '''Die.roll()
    rolls the die'''
    # pick a random side and put it on top
    self.top = self.sides[random.randrange(self.numSides)]

  def get_top(self):
    '''Die.get_top() -> object
    returns top of Die'''
    return self.top


def europadice():
  '''plays a game of eropadice'''
  #setup
  dielist = [Die([1, 2, 3, 4, 5, 'W']) for i in range(10)]
  for i in range(10):
    dielist[i].roll()
  goingFor = 'none'
  number =0
  highestNum =0
  for i in range(1, 6):
    number = 0
    for j in  range(10):
      if dielist[j].get_top() == i:
        number+=1
    if number >= highestNum:
      highestNum = number
      goingFor = i
  topList = [dielist[i].get_top() for i in range(10)]
  print(topList)
  print('going for', goingFor)
  for i in range(0, 3):
    print('reroll number ', i+1)
    input('press enter to reroll')
    for i in range(0, 10):
      if topList[i] == goingFor:
        pass
      elif topList[i] == 'W':
        pass
      else:
        dielist[i].roll()

    topList = [dielist[i].get_top() for i in range(10)]
    print(topList)
  won = 0
  for i in range(0, 10):
    if topList[i] == goingFor:
      pass
    elif topList[i] == 'W':
      pass
    else:
      won += 1

  if won == 0:
    print('Yay, you won!')
  else:
    print('so close... you had ', won, ' more to go!')
europadice()
