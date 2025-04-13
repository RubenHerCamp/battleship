from tkinter import *
from tkinter import ttk

from board import Board
from translations import messages


# Interface Class
class Interface:
    # Constructor
    def __init__(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.Close_Application)  # Handle close event
        self.button_matrix = []
        self.counter = 1
        self.games = (
            {}
        )  # Dictionary where games are stored (key -> game name, value -> board object)
        self.ships = {
            "aircraft carrier": (1, 4),
            "battleships": (2, 3),
            "frigates": (3, 2),
            "patrol boats": (4, 1),
        }  # Dictionary to initialize ships (key -> ship type, value -> tuple(number of ships, lives))
        self.game_ships = (
            {}
        )  # Dictionary that relates the game with the positions of the ships (key -> game id, value -> ship positions)
        self.lang = "en"
        self.root.withdraw()
        self.Menu_Interface()
        self.root.mainloop()

    # Method to handle application close
    def Close_Application(self):
        self.root.quit()  # Stop the Tkinter main loop
        self.root.destroy()  # Destroy the root window
        exit()  # Exit the program

    # Method that generates a new board
    def GenerateBoard_Interface(self):
        self.menu.withdraw()
        self.board = Board()
        self.board.Generate_Board()
        self.board.Generate_Ships(self.ships, self.ship_positions)
        game = self.counter
        self.counter += 1
        self.games[game] = self.board
        self.game_ships[game] = self.ship_positions

        return game

    # Method that displays the board
    def Show_Board(self, board):
        self.board_window = Toplevel(self.root)
        self.board_window.resizable(0, 0)
        self.board_window.title(messages[self.lang]["board_window"])
        button_dict = {}
        self.button_matrix = []
        for row in range(10):
            row_buttons = []
            for column in range(10):
                cell = board.board[row][column]
                if cell.state == "hidden":
                    button_text = "?"
                    button_state = "normal"
                    color = "white"
                elif cell.content == "🚢":
                    button_text = "🚢🚢"  # Larger representation of the ship
                    button_state = "disabled"
                    color = "grey82"
                else:
                    button_text = ""
                    button_state = "disabled"
                    color = "deep sky blue"
                button_dict[column] = Button(
                    self.board_window,
                    disabledforeground="black",
                    state=button_state,
                    text=button_text,
                    bg=color,
                    width=10,
                    command=lambda x=row, y=column, cell=cell, board=board: self.EnterCell_Interface(
                        x, y, cell, board
                    ),
                )
                button_dict[column].grid(column=column, row=row, sticky="nsew")
                row_buttons.append(button_dict[column])
            self.button_matrix.append(row_buttons)
        menu_button = ttk.Button(
            self.board_window,
            text=messages[self.lang]["menu"],
            padding=(5, 5),
            command=lambda window=self.board_window: self.Change_Menu(window),
        )
        menu_button.grid(column=11, row=0)

    # Method that enters a cell into the board
    def EnterCell_Interface(self, x, y, cell, board):
        if cell.state == "hidden":
            if cell.content == "🚢":
                self.button_matrix[x][y]["text"] = "🚢"
                self.button_matrix[x][y]["bg"] = "grey82"
            else:
                self.button_matrix[x][y]["text"] = ""
                self.button_matrix[x][y]["bg"] = "deep sky blue"
            self.button_matrix[x][y]["state"] = "disabled"
            result, ship_type, winner = cell.EnterCell(x, y, self.ship_positions)

            self.message = StringVar()
            self.message_label = Label(
                self.board_window, textvariable=self.message, width=15, height=1
            )
            self.message_label.grid(column=11, row=3, ipadx=20)
            if ship_type is not None:
                message = f"{messages[self.lang][result]} {ship_type}"
                self.message.set(message)
            else:
                message = messages[self.lang]["water"]
                self.message.set(message)

            if winner:
                self.winner_message = StringVar()
                self.winner_message_label = Label(
                    self.board_window,
                    textvariable=self.winner_message,
                    width=15,
                    height=1,
                )
                self.winner_message_label.grid(column=11, row=2)
                for row_buttons in self.button_matrix:
                    for button in row_buttons:
                        button["state"] = "disabled"
                        button["disabledforeground"] = "grey"
                message = messages[self.lang]["winner"]
                self.message.set(message)
                for game in self.games:
                    if self.games[game] == board:
                        delete_game = game
                self.games.pop(delete_game)

    # Method that selects a game to load
    def SelectGame_Interface(self, game):
        self.load_game_window.withdraw()
        board = self.games[game]
        self.ship_positions = self.game_ships[game]
        self.Show_Board(board)

    # Method that generates a new_game
    def NewGame_Interface(self):
        self.ship_positions = (
            {}
        )  # Dictionary where ship positions are stored (key -> string = "row,column", value -> Ship object)
        game = self.GenerateBoard_Interface()
        board = self.games[game]
        self.ship_positions = self.game_ships[game]
        self.Show_Board(board)

    # Method that shows the games that can be loaded
    def LoadGame_Interface(self):
        self.menu.withdraw()
        self.load_game_window = Toplevel(self.root)
        self.load_game_window.grid_columnconfigure(0, weight=1)
        self.load_game_window.title(messages[self.lang]["load_game_window"])

        if len(self.games) != 0:
            count = 1
            for game in self.games.keys():
                button_name = "button" + str(count)
                message = f"{messages[self.lang]['game']} {game}"
                button = ttk.Button(
                    self.load_game_window,
                    text=message,
                    padding=(5, 5),
                    width=10,
                    command=lambda game=game: self.SelectGame_Interface(game),
                )
                button.grid(column=0, row=count, ipady=10, ipadx=50, sticky="nsew")
                count += 1
        else:
            self.message = StringVar()
            self.message_label = Label(
                self.load_game_window, textvariable=self.message, width=30, height=1
            )
            self.message_label.grid(column=0, row=0)
            message = messages[self.lang]["error_saved_game"]
            self.message.set(message)
            window = self.load_game_window
            menu_button = ttk.Button(
                self.load_game_window,
                text=messages[self.lang]["menu"],
                padding=(5, 5),
                command=lambda: self.Change_Menu(window),
            )
            menu_button.grid(column=2, row=0)

    # Method that opens the menu
    def Menu_Interface(self):
        self.menu = Toplevel(self.root)
        self.menu.resizable(0, 0)
        self.menu.grid_columnconfigure(0, weight=1)
        self.menu.geometry("444x295")
        self.menu.title(messages[self.lang]["menu_window"])
        new_game_button = ttk.Button(
            self.menu,
            text=messages[self.lang]["new_game"],
            padding=(5, 5),
            command=lambda: self.NewGame_Interface(),
        )
        load_game_button = ttk.Button(
            self.menu,
            text=messages[self.lang]["load_game"],
            padding=(5, 5),
            command=lambda: self.LoadGame_Interface(),
        )
        change_language_button = ttk.Button(
            self.menu,
            text=messages[self.lang]["change_language"],
            padding=(5, 5),
            command=lambda: self.Language_Interface(),
        )
        exit_button = ttk.Button(
            self.menu, text=messages[self.lang]["exit"], padding=(5, 5), command=quit
        )
        new_game_button.grid(column=0, row=0, ipady=20, sticky="nsew")
        load_game_button.grid(column=0, row=1, ipady=20, sticky="nsew")
        change_language_button.grid(column=0, row=2, ipady=20, sticky="nsew")
        exit_button.grid(column=0, row=3, ipady=20, sticky="nsew")

    # Method that opens the language window
    def Language_Interface(self):
        self.menu.withdraw()
        self.language_window = Toplevel(self.root)
        self.language_window.resizable(0, 0)
        self.language_window.grid_columnconfigure(0, weight=1)
        self.language_window.geometry("444x220")
        self.language_window.title(messages[self.lang]["change_language_window"])
        catalan_button = ttk.Button(
            self.language_window,
            text=messages[self.lang]["catalan"],
            padding=(5, 5),
            command=lambda language="ca": self.Change_Language(language),
        )
        spanish_button = ttk.Button(
            self.language_window,
            text=messages[self.lang]["spanish"],
            padding=(5, 5),
            command=lambda language="es": self.Change_Language(language),
        )
        english_button = ttk.Button(
            self.language_window,
            text=messages[self.lang]["english"],
            padding=(5, 5),
            command=lambda language="en": self.Change_Language(language),
        )
        catalan_button.grid(column=0, row=0, ipady=20, sticky="nsew")
        spanish_button.grid(column=0, row=1, ipady=20, sticky="nsew")
        english_button.grid(column=0, row=2, ipady=20, sticky="nsew")

    # Method that changes the language of the game
    def Change_Language(self, language):
        self.lang = language
        window = self.language_window
        self.Change_Menu(window)

    # Method that takes a window as a parameter, closes it, and opens the menu_window
    def Change_Menu(self, window):
        window.withdraw()
        self.Menu_Interface()


# Main
def main():
    Interface()


if __name__ == "__main__":
    main()
