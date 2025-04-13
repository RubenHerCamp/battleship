import random

from cell import Cell
from ship import Ship


# Board Class
class Board(object):
    # Constructor
    def __init__(self):
        self.board = self.Generate_Board()  # Board attribute

    # Setters and Getters
    def set_board(self, board):
        self.state = board

    def get_board(self):
        return self.board

    # Method that generates the Board object where each cell is a Cell object
    def Generate_Board(self):
        ll = []
        for i in range(10):
            row = []
            for column in range(10):
                row.append(Cell())
            ll.append(row)
        return ll

    # Method that prints the board
    def Print_Board(self):
        count = 0
        print("   ", end="")
        for num in range(10):
            print(f" {num}", end="")
        print("\n=======================")
        for row in self.board:
            print(f"{count} | ", end="")
            for column in row:
                if column.state == "hidden":
                    print("O ", end="")
                else:
                    if column.content == "🚢":
                        print("🚢 ", end="")
                    elif column.content == "B":
                        print("B ", end="")
                    else:
                        print("O ", end="")
            count += 1
            print()
        print("=======================")

    # Method that returns a valid position to place a ship
    def Calculate_Position(self, ship_count):
        valid_position = False
        while not valid_position:
            pos_row = random.randint(0, 9)
            pos_column = random.randint(0, 9)
            ver_hor = random.randint(1, 2)  # 1 for vertical, 2 for horizontal

            if ver_hor == 1:  # Vertical placement
                if pos_row + ship_count <= 10:  # Ensure ship fits vertically
                    valid_position = all(
                        self.board[pos_row + i][pos_column].content != "🚢"
                        for i in range(ship_count)
                    )
            else:  # Horizontal placement
                if pos_column + ship_count <= 10:  # Ensure ship fits horizontally
                    valid_position = all(
                        self.board[pos_row][pos_column + i].content != "🚢"
                        for i in range(ship_count)
                    )

        return [pos_row, pos_column, ver_hor]

    # Method that generates ships on the board
    def Generate_Ships(self, ships, ship_positions):
        for key, value in ships.items():
            for _ in range(value[0]):
                ship_count = value[1]
                ship_object = Ship(key, ship_count)
                position = self.Calculate_Position(ship_count)
                for i in range(ship_count):
                    if position[2] == 1:  # Vertical placement
                        row = position[0] + i
                        column = position[1]
                    else:  # Horizontal placement
                        row = position[0]
                        column = position[1] + i
                    self.board[row][column].content = "🚢"
                    positions = f"{row},{column}"
                    ship_positions[positions] = ship_object
