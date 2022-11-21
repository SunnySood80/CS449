#IMPORTS
from kivy.app import App

NONE = 0
S = 1
O = 2


class Action:
    """
    The class for an action, needed for ai turns
    """
    def __init__(self, let, dist, instance):
        """
        let is the letter (S or O)
        instance needed for kivy
        """
        self.let = let
        self.dist = dist
        self.instance = instance

    def take(self):
        """
        returns the selection of the computer
        """
        if self.let == S:
            App.get_running_app().game.board.currentturn.s()
        elif self.let == O:
            App.get_running_app().game.board.currentturn.o()
        App.get_running_app().game.board.on_release(self.instance)
