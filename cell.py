# Cell Class
class Cell(object):
    # Constructor
    def __init__(self):
        self.state = "hidden"  # Attribute that indicates the state of the cell (hidden or discovered)
        self.content = "O"  # Attribute that indicates the content of the cell (O -> hidden, 🚢 -> ship, B -> water)

    # Setters and Getters
    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    # Method that introduces a cell to the board
    def EnterCell(self, row, column, ship_positions):
        if self.content == "🚢":
            position = f"{row},{column}"
            self.state = "discovered"
            for key, ship in ship_positions.items():
                if position == key:
                    result, ship_type = ship.AttackShip()
            ship_positions.pop(position)

            if len(ship_positions) == 0:
                winner = True
            else:
                winner = False
        else:
            self.content = "B"
            self.state = "discovered"
            result = "B"
            ship_type = None
            winner = False

        return result, ship_type, winner
