#TEST FILE FOR UNIT TESTING 
import unittest
import board
import turn
import action
from turn import Turn

class TestClass(unittest.TestCase):

    def test_choice(self):
        
        result = turn.s()
        self.assertEqual(result, S)
    def test_radioButtons(self):

        check_box(self, instance, True)
        self.assertEqual(self.gamemode.text, "General Game")

        self.assertNotEqual(self.gamemode.text, "Simple Game")
    def test_SandOplacement(self):
         result = on_s_pressed(True)
        
         self.assertEqual(result, True)

    def test_board(self):
        result = board.SOSBoard()
        self.assertEqual(result, cols = 9)
        self.assertEqual(result, rows = 9)

    def test_winner_general(self):
        player1points = 5
        player2points = 6
        result = on_release(self, instance)
        self.assertEqual(result, player1points < player2points)

    def test_aiTurn(self): 
        turn = 1
        result = doPriorityMove(self)
        self.assertNotEqual(result, 0)

    def test_placement(self):
        maxattlist.append(Action(S, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
        self.assertEqual(self.attacks[i], maxatt)
        
   
    if __name__ == '__main__':
        unittest.main()
        
