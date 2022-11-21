#IMPORTS
from kivy.app import App

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class Scoreboard(EventDispatcher):
    """
    The class for points on scoreboard.
    """
    player1points = NumericProperty(0) # The points of player 1
    player2points = NumericProperty(0) # The points of player 2
    def on_player1points(self, instance, value):
        """
        executed when the points of player 1 change
        instance: needed for kivy
        value: the new value
        changes the number of points in the graphics
        """
        app = App.get_running_app()
        app.game.player1points.text = str(value)

    def on_player2points(self, instance, value):
        """
        executed when the points of player 2 change
        instance: needed for kivy
        value: the new value
        changes the number of points in the graphics
        """
        app = App.get_running_app()
        app.game.player2points.text = str(value)
