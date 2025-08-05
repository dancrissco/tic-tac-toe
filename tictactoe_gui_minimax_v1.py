import tkinter as tk
from tkinter import simpledialog
import pyttsx3
import threading
import time
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Voice setup
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Connect to CoppeliaSim
client = RemoteAPIClient()
sim = client.require('sim')
sim.startSimulation()

tile_handles = [sim.getObject(f'./tile_{i}') for i in range(9)]
token_x_handles = [sim.getObject(f'./token_X_{i}') for i in range(5)]
token_o_handles = [sim.getObject(f'./token_O_{i}') for i in range(5)]

x_index = 0
o_index = 0

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with CoppeliaSim")
        self.board = [''] * 9
        self.buttons = []
        self.game_over = False
        self.ai_enabled = False
        self.ai_mode = None  # "basic" or "minimax"
        self.turn = 'X'
        self.default_color = tk.Button(self.root).cget("bg")
        self.player_x_name = ""
        self.player_o_name = ""

        self.label = tk.Label(root, text="Select mode and press Start", font=("Arial", 14))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(9):
            btn = tk.Button(root, text=str(i), font=("Arial", 20), width=5, height=2,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.mode_frame = tk.Frame(root)
        self.mode_frame.grid(row=4, column=0, columnspan=3)
        tk.Button(self.mode_frame, text="Manual", font=("Arial", 12),
                  command=self.set_manual_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(self.mode_frame, text="Basic AI", font=("Arial", 12),
                  command=self.set_basic_ai_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(self.mode_frame, text="Minimax AI", font=("Arial", 12),
                  command=self.set_minimax_mode).pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 14),
                                      command=self.start_game)
        self.start_button.grid(row=5, column=0, columnspan=3, pady=10)

        self.reset_button = tk.Button(root, text="Replay", font=("Arial", 14),
                                      command=self.reset_game, state=tk.DISABLED)
        self.reset_button.grid(row=6, column=0, columnspan=3, pady=10)

    def set_manual_mode(self):
        self.ai_enabled = False
        self.ai_mode = None
        self.label.config(text="Manual Mode selected")
        speak("Manual mode selected")

    def set_basic_ai_mode(self):
        self.ai_enabled = True
        self.ai_mode = "basic"
        self.label.config(text="Basic AI Mode selected")
        speak("Basic AI mode selected")

    def set_minimax_mode(self):
        self.ai_enabled = True
        self.ai_mode = "minimax"
        self.label.config(text="Minimax AI Mode selected")
        speak("Minimax AI mode selected")

    def start_game(self):
        if self.ai_enabled:
            if not self.player_x_name:
                self.player_x_name = simpledialog.askstring("Name", "Enter your name:")
                if not self.player_x_name:
                    self.player_x_name = "Player"
            self.player_o_name = "AI"
        else:
            if not self.player_x_name:
                self.player_x_name = simpledialog.askstring("Name", "Enter name for Player X:")
                if not self.player_x_name:
                    self.player_x_name = "Player X"
            if not self.player_o_name:
                self.player_o_name = simpledialog.askstring("Name", "Enter name for Player O:")
                if not self.player_o_name:
                    self.player_o_name = "Player O"

        speak("Game started. Your turn.")
        self.label.config(text="Your turn!")
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

    def make_move(self, index):
        if self.board[index] == '' and not self.game_over:
            self.board[index] = self.turn
            self.buttons[index].config(text=self.turn, bg='green' if self.turn == 'X' else 'orange')
            self.drop_token(index, self.turn)
            self.label.config(text=f"{self.turn} moved at tile {index}")
            speak(f"{self.turn} moved at tile {index}")

            if self.check_winner(self.turn):
                winner = self.player_x_name if self.turn == 'X' else self.player_o_name
                self.label.config(text=f"{winner} wins!")
                speak(f"Congratulations {winner}, you win!")
                self.game_over = True
                self.reset_button.config(state=tk.NORMAL)
                return
            elif '' not in self.board:
                self.label.config(text="It's a draw!")
                speak("It's a draw!")
                self.game_over = True
                self.reset_button.config(state=tk.NORMAL)
                return

            self.turn = 'O' if self.turn == 'X' else 'X'

            if self.ai_enabled and self.turn == 'O':
                self.label.config(text="AI is thinking...")
                speak("AI is thinking. Please wait.")
                threading.Thread(target=self.ai_move).start()

    def drop_token(self, index, symbol):
        global x_index, o_index
        try:
            tile_pos = sim.getObjectPosition(tile_handles[index], -1)
            drop_pos = [tile_pos[0], tile_pos[1], 0.2]
            if symbol == 'X' and x_index < len(token_x_handles):
                sim.setObjectPosition(token_x_handles[x_index], -1, drop_pos)
                x_index += 1
            elif symbol == 'O' and o_index < len(token_o_handles):
                sim.setObjectPosition(token_o_handles[o_index], -1, drop_pos)
                o_index += 1
        except Exception as e:
            print("CoppeliaSim drop error:", e)

    def ai_move(self):
        time.sleep(1)
        move = self.find_best_move_minimax() if self.ai_mode == "minimax" else self.find_best_move_basic()
        if move != -1:
            self.board[move] = 'O'
            self.buttons[move].config(text='O', bg='orange')
            self.drop_token(move, 'O')
            self.label.config(text=f"AI moved at tile {move}")
            speak(f"AI moved at tile {move}")
            if self.check_winner('O'):
                self.label.config(text=f"{self.player_o_name} wins!")
                speak(f"{self.player_o_name} wins!")
                self.game_over = True
                self.reset_button.config(state=tk.NORMAL)
            elif '' not in self.board:
                self.label.config(text="It's a draw!")
                speak("It's a draw!")
                self.game_over = True
                self.reset_button.config(state=tk.NORMAL)
            else:
                self.turn = 'X'
                self.label.config(text="Your turn!")

    def find_best_move_basic(self):
        for i in range(9):
            if self.board[i] == '':
                return i
        return -1

    def find_best_move_minimax(self):
        def minimax(b, depth, is_max):
            if self.check_win_symbol(b, 'O'):
                return 1
            if self.check_win_symbol(b, 'X'):
                return -1
            if '' not in b:
                return 0
            if is_max:
                best = -math.inf
                for i in range(9):
                    if b[i] == '':
                        b[i] = 'O'
                        best = max(best, minimax(b, depth + 1, False))
                        b[i] = ''
                return best
            else:
                best = math.inf
                for i in range(9):
                    if b[i] == '':
                        b[i] = 'X'
                        best = min(best, minimax(b, depth + 1, True))
                        b[i] = ''
                return best

        best_val = -math.inf
        best_move = -1
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                move_val = minimax(self.board, 0, False)
                self.board[i] = ''
                if move_val > best_val:
                    best_val = move_val
                    best_move = i
        return best_move

    def check_win_symbol(self, b, symbol):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for cond in win_conditions:
            if b[cond[0]] == b[cond[1]] == b[cond[2]] == symbol:
                return True
        return False

    def check_winner(self, symbol):
        return self.check_win_symbol(self.board, symbol)

    def reset_game(self):
        global x_index, o_index
        self.board = [''] * 9
        for i, btn in enumerate(self.buttons):
            btn.config(text=str(i), bg=self.default_color)
        self.label.config(text="Game reset. Press Start.")
        speak("Game reset. Press Start to play.")
        self.turn = 'X'
        self.game_over = False
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        x_index = 0
        o_index = 0
        try:
            sim.stopSimulation()
            time.sleep(0.5)
            sim.startSimulation()
        except Exception as e:
            print("Simulation restart failed:", e)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
