import tkinter as tk
from tkinter import messagebox
import random
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Representing 3x3 board
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')  # Empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # Ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # Switch player

        # Tiny break to make it easier to read the output
        if print_game:
            time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')

class HumanPlayer:
     def __init__(self, letter):
        self.letter = letter
     def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn.')
        return val

class SmartComputerPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # Choose a random move
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # AI
        other_player = 'O' if player == 'X' else 'X'

        # Check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                    state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}  # Each score should maximize
        else:
            best = {'position': None, 'score': float('inf')}  # Each score should minimize

        for possible_move in state.available_moves():
            # Make a move and try that spot
            state.make_move(possible_move, player)
            # Simulate a game after making that move
            sim_score = self.minimax(state, other_player)  # Alternate players
            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score  # replace best
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score  # replace best

        return best

class TicTacToeGUI:
    def __init__(self, master, x_player, o_player):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.x_player = x_player
        self.o_player = o_player
        self.create_widgets()

    def create_widgets(self):
        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text='', font=('normal', 20), height=2, width=5,
                                              command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        if self.game.board[row * 3 + col] == ' ' and not self.game.current_winner:
            self.buttons[row][col].config(text=self.x_player.letter)
            self.game.make_move(row * 3 + col, self.x_player.letter)

            if not self.game.current_winner and self.game.empty_squares():
                o_move = self.o_player.get_move(self.game)
                self.game.make_move(o_move, self.o_player.letter)
                self.buttons[o_move // 3][o_move % 3].config(text=self.o_player.letter)

            if self.game.current_winner or not self.game.empty_squares():
                self.show_winner()

    def show_winner(self):
        if self.game.current_winner:
            winner = self.game.current_winner
            if winner == self.x_player.letter:
                winner_text = "YOU win!"
            else:
                winner_text = "AI wins!"
        else:
            winner_text = "It's a tie!"

        messagebox.showinfo("Game Over", winner_text)
        self.reset_game()

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='')
                self.game = TicTacToe()

def play_gui():
    root = tk.Tk()
    x_player = HumanPlayer('X')
    o_player = SmartComputerPlayer('O')
    app = TicTacToeGUI(root, x_player, o_player)
    root.mainloop()

if __name__ == '__main__':
    play_gui()
