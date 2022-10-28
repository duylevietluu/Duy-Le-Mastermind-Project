import random
import constants


class MasterGame():
  def __init__(self,max_guess=10,length=4):
    self.guess_left = max_guess
    self.len = length
    self.victory = False
    self.answer = self.generate_code()

  def rand_color(self):
    """
    Return a random color from the list
    """
    return random.choice(constants.COLORS)

  def generate_code(self):
    """
    Return a sequence of self.len random colors.
    """
    #return list("GGGR")
    res = []
    for i in range(0,self.len):
      res.append(self.rand_color())
    return res

  def take_guess(self,String):
    """
    Guess if a string is the right one.
    Count the number of black pegs and white pegs, given a guessing sequence.
    """
    self.guess_left -= 1

    temp1 = self.answer.copy()
    temp2 = String.copy()

    if temp1 == temp2:
      self.victory = True
      return self.len,0

    black = 0
    white = 0

    #count for black pegs
    for i in range(0,self.len):
      if temp1[i] == temp2[i]:
        black += 1
        temp1[i] = constants.BLACK_PEG
        temp2[i] = constants.BLACK_PEG
    
    #count for white pegs
    for i in range(0,self.len):
      for j in range(0,self.len):
        if temp1[i] != constants.BLACK_PEG and temp1[i] == temp2[j]:
          white += 1
          temp1[i] = constants.WHITE_PEG
          temp2[j] = constants.WHITE_PEG
          break

    return black,white


def test():
  """
  A test function that creates a terminal-based MasterMind.
  """
  game = MasterGame()
  print(constants.explain)

  while game.guess_left > 0 and game.victory == False:
    guess_str = list(input("Please insert guess with length 4: ").upper())

    if len(guess_str) != game.len:
      print("Wrong length")
      continue
    
    b,w = game.take_guess(guess_str)

    print("You get {} black pegs, {} white pegs. {} guesses left.".format(b,w,game.guess_left))

  print()
  if game.victory:
    print("victory!")
  else:
    print("loser!")
  
if __name__ == "__main__":   
  test()