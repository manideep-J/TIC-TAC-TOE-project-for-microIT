import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    def _init_(self):
        self.window = tk.Tk()
        self.window.title("⭕ Tic-Tac-Toe Game")
        self.window.geometry("600x700")
        self.window.configure(bg="#0f3460")
        self.window.resizable(False, False)
        
        # Game variables
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.player_x_score = 0
        self.player_o_score = 0
        self.game_mode = "PvP"  # Player vs Player or Player vs Computer
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.window,
            text="⭕ TIC-TAC-TOE ❌",
            font=("Arial", 28, "bold"),
            bg="#0f3460",
            fg="#00d4aa"
        )
        title_label.pack(pady=20)
        
        # Game mode selector
        mode_frame = tk.Frame(self.window, bg="#0f3460")
        mode_frame.pack(pady=10)
        
        tk.Label(
            mode_frame,
            text="Game Mode:",
            font=("Arial", 14, "bold"),
            bg="#0f3460",
            fg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        
        self.mode_var = tk.StringVar(value="PvP")
        
        pvp_radio = tk.Radiobutton(
            mode_frame,
            text="Player vs Player",
            variable=self.mode_var,
            value="PvP",
            font=("Arial", 12),
            bg="#0f3460",
            fg="#ffffff",
            selectcolor="#16213e",
            activebackground="#0f3460",
            activeforeground="#ffffff",
            command=self.change_mode
        )
        pvp_radio.pack(side=tk.LEFT, padx=10)
        
        pvc_radio = tk.Radiobutton(
            mode_frame,
            text="vs Computer",
            variable=self.mode_var,
            value="PvC",
            font=("Arial", 12),
            bg="#0f3460",
            fg="#ffffff",
            selectcolor="#16213e",
            activebackground="#0f3460",
            activeforeground="#ffffff",
            command=self.change_mode
        )
        pvc_radio.pack(side=tk.LEFT, padx=10)
        
        # Score display
        score_frame = tk.Frame(self.window, bg="#0f3460")
        score_frame.pack(pady=15)
        
        self.score_label = tk.Label(
            score_frame,
            text=f"Player X: {self.player_x_score}  |  Player O: {self.player_o_score}",
            font=("Arial", 16, "bold"),
            bg="#0f3460",
            fg="#feca57"
        )
        self.score_label.pack()
        
        # Current player display
        self.current_player_label = tk.Label(
            self.window,
            text=f"Current Player: {self.current_player}",
            font=("Arial", 18, "bold"),
            bg="#0f3460",
            fg="#4ecdc4"
        )
        self.current_player_label.pack(pady=10)
        
        # Game board
        self.board_frame = tk.Frame(self.window, bg="#0f3460")
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            button_row = []
            for j in range(3):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 36, "bold"),
                    width=4,
                    height=2,
                    bg="#16213e",
                    fg="#ffffff",
                    activebackground="#1e3a8a",
                    activeforeground="#ffffff",
                    relief="raised",
                    bd=3,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                button_row.append(button)
            self.buttons.append(button_row)
            
        # Control buttons
        control_frame = tk.Frame(self.window, bg="#0f3460")
        control_frame.pack(pady=30)
        
        new_game_button = tk.Button(
            control_frame,
            text="🔄 NEW GAME",
            font=("Arial", 14, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#ff5252",
            activeforeground="#ffffff",
            relief="flat",
            width=12,
            height=2,
            command=self.new_game
        )
        new_game_button.pack(side=tk.LEFT, padx=10)
        
        reset_scores_button = tk.Button(
            control_frame,
            text="📊 RESET SCORES",
            font=("Arial", 14, "bold"),
            bg="#6c5ce7",
            fg="#ffffff",
            activebackground="#5f3dc4",
            activeforeground="#ffffff",
            relief="flat",
            width=15,
            height=2,
            command=self.reset_scores
        )
        reset_scores_button.pack(side=tk.LEFT, padx=10)
        
        quit_button = tk.Button(
            control_frame,
            text="❌ QUIT",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="#ffffff",
            activebackground="#c0392b",
            activeforeground="#ffffff",
            relief="flat",
            width=12,
            height=2,
            command=self.window.quit
        )
        quit_button.pack(side=tk.LEFT, padx=10)
        
    def change_mode(self):
        self.game_mode = self.mode_var.get()
        self.new_game()
        
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != "":
            return
            
        # Make player move
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg="#ff6b6b" if self.current_player == "X" else "#4ecdc4",
            state="disabled"
        )
        
        # Check for win or draw
        if self.check_winner():
            self.end_game(f"🎉 Player {self.current_player} Wins! 🎉")
            if self.current_player == "X":
                self.player_x_score += 1
            else:
                self.player_o_score += 1
            self.update_score_display()
            return
        elif self.is_board_full():
            self.end_game("🤝 It's a Draw! 🤝")
            return
            
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.current_player_label.config(text=f"Current Player: {self.current_player}")
        
        # Computer move if in PvC mode and it's O's turn
        if self.game_mode == "PvC" and self.current_player == "O":
            self.window.after(500, self.computer_move)  # Delay for better UX
            
    def computer_move(self):
        if self.game_over:
            return
            
        # Simple AI: Try to win, then block, then random
        move = self.get_best_move()
        if move:
            row, col = move
            self.make_move(row, col)
            
    def get_best_move(self):
        # Try to win
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    if self.check_winner():
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
                    
        # Try to block player from winning
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    if self.check_winner():
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
                    
        # Take center if available
        if self.board[1][1] == "":
            return (1, 1)
            
        # Take corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [(r, c) for r, c in corners if self.board[r][c] == ""]
        if available_corners:
            return random.choice(available_corners)
            
        # Take any available spot
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    return (i, j)
                    
        return None
        
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True
                
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
            
        return False
        
    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True
        
    def end_game(self, message):
        self.game_over = True
        self.current_player_label.config(
            text=message,
            fg="#00d4aa" if "Wins" in message else "#feca57"
        )
        
        # Disable all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")
                
        # Highlight winning combination
        self.highlight_winner()
        
    def highlight_winner(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                for j in range(3):
                    self.buttons[i][j].config(bg="#2ecc71")
                return
                
        # Check columns  
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != "":
                for i in range(3):
                    self.buttons[i][j].config(bg="#2ecc71")
                return
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            for i in range(3):
                self.buttons[i][i].config(bg="#2ecc71")
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.buttons[0][2].config(bg="#2ecc71")
            self.buttons[1][1].config(bg="#2ecc71")
            self.buttons[2][0].config(bg="#2ecc71")
            
    def new_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        
        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text="",
                    state="normal",
                    bg="#16213e",
                    fg="#ffffff"
                )
                
        self.current_player_label.config(
            text=f"Current Player: {self.current_player}",
            fg="#4ecdc4"
        )
        
    def reset_scores(self):
        self.player_x_score = 0
        self.player_o_score = 0
        self.update_score_display()
        
    def update_score_display(self):
        self.score_label.config(
            text=f"Player X: {self.player_x_score}  |  Player O: {self.player_o_score}"
        )
        
    def run(self):
        self.window.mainloop()

if _name_ == "_main_":
    game = TicTacToeGame()
    game.run()