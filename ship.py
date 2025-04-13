# Ship Class
class Ship(object):
    # Constructor
    def __init__(self, type, lives):
        self.state = (
            "intact"  # Attribute indicating the state of the ship (intact, hit, sunk)
        )
        self.type = type  # Attribute indicating the type of ship (aircraft carrier, battleship, frigate, patrol boat)
        self.lives = lives  # Attribute indicating how many lives the ship has left

    # Setters and Getters
    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_lives(self, lives):
        self.lives = lives

    def get_lives(self):
        return self.lives

    # Method that attacks the ship and reduces its lives
    def AttackShip(self):
        self.lives -= 1
        if self.lives > 0:
            result = "hit"
        else:
            result = "sunk"
        return result, self.type
