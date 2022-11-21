class Player:
    """
    The class for player.
    """
    def __init__(self, name, first):
        """
        name: the name of the player
        first: True if he/she is first in the game
        """
        self.name = name
        self.starter = first
        self.now = True if self.starter else False
