import tkinter as tk
from mastergame import MasterGame
import constants
from functools import partial

main = tk.Tk()
main.title("Mastermind by Duy Le")

images = {}

class MasterGUI():
  def __init__(self):
    """
    Form a GUI for Mastermind
    """
    self.init_images()

    #game and a line of guessing code
    self.game = MasterGame()
    self.guess = []

    #buttons for deleting and guessing
    self.del_button = tk.Button(main, bg = 'white', text = 'delete', command = self.delete_click)
    self.guess_button = tk.Button(main, bg = 'white', text = 'guess', command = self.guess_click, state = tk.DISABLED)
    self.rule_button = tk.Button(main, bg = 'white', text = 'show rule', command = self.rule_click)

    #buttons for adding colors
    self.color_buttons = []
    for color in constants.COLORS:
      self.color_buttons.append(self.new_color_button(color))

    #label for number of guesses left
    self.guess_left = tk.Label(main, bg = 'white', text = str(self.game.guess_left) + ' guess left')
    
    #label for each guess line (code that u guess) 
    #  and result for each guess line (in black and white pegs)
    self.guess_lines = []
    self.pegs = []

    for i in range(self.game.guess_left):
      self.pegs.append(tk.Label(main, bg = 'gray', image = images["emptypegs"]))
      self.guess_lines.append([])
      for j in range(self.game.len):
        new = tk.Label(main, bg = 'gray', image = images["empty"])
        self.guess_lines[i].append(new)
    
    #variable for editting line
    self.now = -1
    self.update_line()  #self.now = 0

    #answer labels
    self.ans_text = tk.Label(main, bg = 'white', text = 'Answer:')
    self.ans_line = []
    for k in range(self.game.len):
      self.ans_line.append(tk.Label(main, bg = '#E0FFFF', image = images["empty"]))

    #notification labels
    self.notify = tk.Label(main, bg = 'white', text = constants.gui_explain)


  def init_images(self):
    """
    Put every image directory into a dictionary.
    """
    for color in constants.COLORS:
      images[color] = tk.PhotoImage(file = "./images/colors/" + color+".png")
    
    images["empty"] = tk.PhotoImage(file = "./images/colors/empty.png")

    images["emptypegs"] = tk.PhotoImage(file = "./images/pegs/emptypegs.png")

    for b in range(0,5):
      for w in range(0,5-b):
        imagename = str(b) + "black" + str(w) + "white"
        images[imagename] = tk.PhotoImage(file = "./images/pegs/" + imagename + ".png")


  def new_color_button(self,color):
    """
    Form a new button for adding a specific color.
    """
    function = partial(self.color_click,color)
    button = tk.Button(main, bg = 'white', image = images[color], command = function)
    return button
  

  def color_click(self,color):
    """
    Activates when a color button is clicked.
    Add the color to the editting line.
    """
    self.guess.append(color)
    self.update()
  

  def delete_click(self):
    """
    Activates when the delete button is clicked.
    Clear the editting line.
    """
    self.guess.clear()
    self.update()


  def guess_click(self):
    """
    Activates when the guess button is clicked.
    Check the editting line and output the result(pegs) of that line. 
    """
    b,w = self.game.take_guess(self.guess)
    image_name = str(b) + "black" + str(w) + "white"
    self.pegs[self.now]["image"] = images[image_name]
    self.update_line()
    self.delete_click()
  

  def rule_click(self):
    """
    Activates when the rule button is clicked
    """
    if self.rule_button["text"] == 'show rule':
      self.rule_button["text"] = 'hide rule'
      self.notify.grid()
    else:
      self.rule_button["text"] = 'show rule'
      self.notify.grid_remove()
    

  def update(self):
    """
    Activates whenever a button is clicked.
    Update all the graphical elements.
    """
    #change the label for # of guesses left
    self.guess_left['text'] = str(self.game.guess_left) + ' guess left'

    #check if the game is ended (by losing or winning)
    if self.game.guess_left == 0 or self.game.victory == True:
      self.end()
      return
    
    #check the state of buttons
    self.update_buttons()

    #update the editting guess line
    for k in range(self.game.len):
      try:
        self.guess_lines[self.now][k]["image"] = images[self.guess[k]]
      except:
        self.guess_lines[self.now][k]["image"] = images["empty"]


  def update_buttons(self):
    """
    Update the state of the guess button and the color buttons.
    Depend on whether the editting line is full.
    """
    isFull = len(self.guess) == self.game.len
    state = [tk.DISABLED, tk.ACTIVE]

    self.guess_button["state"] = state[isFull]
    for colorbutton in self.color_buttons:
      colorbutton["state"] = state[not isFull]


  def update_line(self):
    """
    Update line of editting when a code is guessed.
    Change guessed line background to gray, editting line to white.
    """
    for square in self.guess_lines[self.now]:
      square["bg"] = 'gray'
    self.pegs[self.now]["bg"] = 'gray'

    self.now += 1
    if self.now == len(self.guess_lines):
      return

    for square in self.guess_lines[self.now]:
        square["bg"] = 'white'
    self.pegs[self.now]["bg"] = 'white'


  def run(self):
    """
    Put the labels and buttons on the program and run!
    """
    #buttons
    self.del_button.grid(row = 0, column = 0)
    self.guess_button.grid(row = 1, column = 0)
    self.rule_button.grid(row = 2, column = 0)

    rowbutton = 3
    for colorbutton in self.color_buttons:
      colorbutton.grid(row = rowbutton, column = 0)
      rowbutton += 1

    #label for number of guesses left and notification
    self.guess_left.grid(row = 0, column = 20)
    
    #guess lines
    for row in range(len(self.guess_lines)):
      column = 1
      for square in self.guess_lines[row]:
        square.grid(row = row, column = column)
        column += 1
      self.pegs[row].grid(row = row, column = column)

    #answer
    self.ans_text.grid(row = 20, column = 0)
    anscolumn = 1
    for square in self.ans_line:
      square.grid(row = 20, column = anscolumn)
      anscolumn += 1

    #notification
    self.notify.grid(row = 1, column = 20, rowspan = 20)
    self.notify.grid_remove()

    #run the loop!
    main.mainloop()
  

  def end(self):
    """
    End the game! 
    """
    #show the answer
    for k in range(self.game.len):
      self.ans_line[k]["image"] = images[self.game.answer[k]]

    #disable all buttons
    self.guess_button["state"] = tk.DISABLED
    self.del_button["state"] = tk.DISABLED
    self.rule_button["state"] = tk.DISABLED
    for colorbutton in self.color_buttons:
      colorbutton["state"] = tk.DISABLED
    
    #notify the result
    self.notify.grid()
    if self.game.victory:
      self.notify["text"] = "Well played.\nYou win!"
      self.notify["fg"] = 'green'
    else:
      self.notify["text"] = "You lose...\nBetter luck \nnext time!"
      self.notify["fg"] = 'red'


if __name__ == "__main__":   
  MasterGUI().run()