#IMPORTS
from kivy.app import App
from kivy.lang.builder import Builder

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from turn import Turn
from turn import AITurn
from scoreboard import Scoreboard
from player import Player
from main import SOS
import main
import os

NONE = 0
S = 1
O = 2
checks = []

class SOSBoard(GridLayout):
    """
    The class for the board of the game with the graphics.
    """
    def __init__(self, player1, player2='AI', cols=9, rows=9):
        """
        The constructor
        player1 the name of the first player
        player2: the name of the second player, default value to 'AI', which means game against the computer
        cols: the number of the cols on the board, default value to 9
        rows: the number of the rows on the board, default value to 9
        """
        super(SOSBoard, self).__init__()
        self.ai = True if player2 == 'AI' else False

        self.cols = cols
        self.rows = rows
        self.player1 = Player(player1, True)
        self.player2 = Player(player2, False)
        self.scoreboard = Scoreboard()
        self.grid = [[None for col in range(self.cols)] for row in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                tile = SOSPoints(row, col)
                self.grid[row][col] = tile
                tile.bind(on_release=self.on_release)
                self.add_widget(tile)
        self.currentturn=Turn(1)

    def s(self):
        """
        changes the selection of the current turn to S, or initializes it to S
        """
        self.currentturn.s()

    def o(self):
        """
        changes the selection of the current turn to O, or initializes it to O
        """
        self.currentturn.o()

    def done(self, tile):
        """
        tile: needed for the on_release/on_press function
        finishes the turn and resets the current selection
        """
        if self.currentturn.choice == NONE:
            return False
        elif tile.occupied:
            return False
        else:
            tile.text = self.on_done()
            return True

    def on_release(self, instance):
        '''
        does the turn when needed
        instance: needed for kivy 
        returns when the turn is over
        '''
        if App.get_running_app().game.board.currentturn.choice == NONE:
            return
        if instance.text:
            return None
        self.done(instance)
        instance.disabled = True
        instance.disabled_color = (1,1,1,1)
        instance.background_disabled_normal = ''
        instance.background_color = (0.1, 0.2, 0.3, 0.6)
        currentnum = self.currentturn.num
        if currentnum%2 == 1:
            toadd = self.scoreboard.player1points + self.addpoints(instance)
            self.scoreboard.player1points = toadd
        else:
            toadd = self.scoreboard.player2points + self.addpoints(instance)
            self.scoreboard.player2points = toadd
        self.currentturn = Turn(currentnum+1)
        App.get_running_app().game.s_btn.background_color = (1, 1, 1, 1)
        App.get_running_app().game.o_btn.background_color = (1, 1, 1, 1)
        if self.currentturn.num == (self.rows * self.cols) + 1:
            if self.scoreboard.player1points > self.scoreboard.player2points:
                    winnerstr = App.get_running_app().game.player1name.text + ' is the winner!'
                    popup = Popup(title=winnerstr, size_hint=(None, None), size=(600, 600))
                    popup.open()

            elif self.scoreboard.player1points < self.scoreboard.player2points:
                winnerstr = App.get_running_app().game.player2name.text + ' is the winner!'
                popup = Popup(title=winnerstr, size_hint=(None, None), size=(600, 600))
                popup.open()

            else:
                popup = Popup(title='Draw!', size_hint=(None, None), size=(600, 600))
                popup.open()
            return
       # if 'Simple Game' in checks:
       #     if self.currentturn.num == (self.rows * self.cols) + 1:
        #        if self.scoreboard.player1points >= 1:
        #            winnerstr = App.get_running_app().game.player1name.text + ' is the winner!'
        #            popup = Popup(title=winnerstr, size_hint=(None, None), size=(600, 600))
         #           popup.open()
          #      elif self.scoreboard.player2points >= 1:
         #            winnerstr = App.get_running_app().game.player2name.text + ' is the winner!'
         #            popup = Popup(title=winnerstr, size_hint=(None, None), size=(600, 600))
         #            popup.open()
      #  elif 'Game mode' in checks:
       #     print ("go select gamemode")
       #     return 0

        if self.ai and self.currentturn.num%2 == 0:
            turn = AITurn(self.currentturn.num)
            turn.doPriorityMove()
        if not self.ai:
            if self.currentturn.num % 2 == 0:
                App.get_running_app().game.whoplay.text = '{}`s turn'.format(App.get_running_app().game.player2name.text)
                App.get_running_app().game.whoplay.color = (1, 0, 0, 1)
            else:
                App.get_running_app().game.whoplay.text = '{}`s turn'.format(App.get_running_app().game.player1name.text)
                App.get_running_app().game.whoplay.color = (0, 0, 1, 1)

    def on_done(self):
        """
        finishes turn and writes the selection of player on selected square.
        """
        if self.currentturn.choice == S:
            return "S"
        elif self.currentturn.choice == O:
            return "O"


    def addpoints(self, instace):
        """
        instace: for "on_release/on_press" function
        returns the number of points to be added after the last turn
        Again, Sorry for the long implementation. Couldnt think of how else to do it
        """
        points = 0
        row = instace.r
        col = instace.c
        if row == 0 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row+1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row+2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row-1][col+1].text == "S":
                points += 1
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row-2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row-1][col+1].text == "S":
                points += 1
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row-2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+2][col-2].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row-1][col+1].text == "S":
                points += 1
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        return points


class SOSPoints(Button):
    """
    The class for squares on the board
    """
    def __init__(self, x, y):
        """
        The constructor
        x: the row number
        y: the col number
        """
        super(SOSPoints, self).__init__()
        self.x = x
        self.y = y
        self.r = x
        self.c = y
        self.points = 0
        self.text = ""
        self.occupied = False
        self.font_size = 50

    def put_s(self):
        """
        checks if the chosen square is occupied then returns True if occupied, False if not
        """
        if not self.occupied:
            self.text = "S"
            self.occupied = True
            return True
        return False

    def put_o(self):
        """
        checks if the chosen square is occupied then returns True if occupied, False if not
        """
        if not self.occupied:
            self.text = "O"
            self.occupied = True
            return True
        return False

    

        
 