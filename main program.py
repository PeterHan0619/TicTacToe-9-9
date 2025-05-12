import tkinter as tk
from tkinter import messagebox
import random

BOARD_SIZE = 9  # 棋盘边长
WINNING_LENGTH = 5  # 获胜所需连续棋子数

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(BOARD_SIZE * BOARD_SIZE)]  # 9x9 棋盘
        self.current_winner = None

    def available_moves(self):
        """返回所有可用的格子索引"""
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        """检查棋盘是否还有空位"""
        return " " in self.board

    def num_empty_squares(self):
        """返回空余格子的数量"""
        return self.board.count(" ")

    def make_move(self, square, letter):
        """在指定位置下棋"""
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        """检查是否有玩家获胜"""
        row = square // BOARD_SIZE
        col = square % BOARD_SIZE

        # 检查行
        start_col = max(0, col - WINNING_LENGTH + 1)
        end_col = min(BOARD_SIZE - WINNING_LENGTH + 1, col)
        for c in range(start_col, end_col + 1):
            if all(self.board[row * BOARD_SIZE + i] == letter for i in range(c, c + WINNING_LENGTH)):
                return True

        # 检查列
        start_row = max(0, row - WINNING_LENGTH + 1)
        end_row = min(BOARD_SIZE - WINNING_LENGTH + 1, row)
        for r in range(start_row, end_row + 1):
            if all(self.board[i * BOARD_SIZE + col] == letter for i in range(r, r + WINNING_LENGTH)):
                return True

        # 检查正对角线
        start = min(row, col)
        end = min(BOARD_SIZE - row, BOARD_SIZE - col)
        for offset in range(-min(start, WINNING_LENGTH - 1), min(end, BOARD_SIZE - WINNING_LENGTH + 1)):
            indices = [(row + i - offset) * BOARD_SIZE + col + i - offset for i in range(WINNING_LENGTH)]
            # 确保所有索引都在有效范围内
            if all(0 <= idx < BOARD_SIZE * BOARD_SIZE and self.board[idx] == letter for idx in indices):
                return True

        # 检查反对角线
        start = min(row, BOARD_SIZE - col - 1)
        end = min(BOARD_SIZE - row, col + 1)
        for offset in range(-min(start, WINNING_LENGTH - 1), min(end, BOARD_SIZE - WINNING_LENGTH + 1)):
            indices = [(row + i - offset) * BOARD_SIZE + col - i + offset for i in range(WINNING_LENGTH)]
            # 确保所有索引都在有效范围内
            if all(0 <= idx < BOARD_SIZE * BOARD_SIZE and self.board[idx] == letter for idx in indices):
                return True

        return False

    def minimax(self, state, player, maximizing_player_is_o):
        # 由于 9x9 棋盘使用 minimax 算法复杂度太高，这里简单随机选择
        max_player = 'O' if maximizing_player_is_o else 'X'
        other_player = 'X' if player == 'O' else 'O'

        temp_board_state = TicTacToe()
        temp_board_state.board = state

        if any(temp_board_state.winner(i, max_player) for i in range(BOARD_SIZE * BOARD_SIZE) if state[i] == max_player):
            return {'score': 1 * (temp_board_state.num_empty_squares() + 1)}
        elif any(temp_board_state.winner(i, other_player) for i in range(BOARD_SIZE * BOARD_SIZE) if state[i] == other_player):
            return {'score': -1 * (temp_board_state.num_empty_squares() + 1)}
        elif not temp_board_state.empty_squares():
            return {'score': 0}

        moves = temp_board_state.available_moves()
        move = random.choice(moves)
        return {'score': 0, 'position': move}

    def get_computer_move(self):
        """获取电脑的下棋位置"""
        if self.num_empty_squares() == BOARD_SIZE * BOARD_SIZE:
            return random.choice([i for i in range(BOARD_SIZE * BOARD_SIZE)])
        else:
            move = self.minimax(self.board, 'O', True)
            return move['position']

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("9x9 成五棋")
        master.resizable(False, False)

        self.game = TicTacToe()
        self.buttons = []
        self.human_player = "X"
        self.computer_player = "O"
        self.current_player = self.human_player

        self.status_label = tk.Label(master, text="轮到你了 (X)", font=('Arial', 16))
        self.status_label.grid(row=BOARD_SIZE, column=0, columnspan=BOARD_SIZE, pady=10)

        for i in range(BOARD_SIZE * BOARD_SIZE):
            row, col = divmod(i, BOARD_SIZE)
            button = tk.Button(master, text=" ", font=('Arial', 20, 'bold'),
                               width=2, height=1,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self.buttons.append(button)

        for i in range(BOARD_SIZE):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

        self.restart_button = tk.Button(master, text="重新开始", font=('Arial', 14), command=self.restart_game)
        self.restart_button.grid(row=BOARD_SIZE + 1, column=0, columnspan=BOARD_SIZE, pady=10, sticky="ew")

    def on_button_click(self, index):
        if self.game.board[index] == " " and not self.game.current_winner and self.current_player == self.human_player:
            if self.game.make_move(index, self.human_player):
                self.buttons[index].config(text=self.human_player, state=tk.DISABLED, disabledforeground="black")
                if self.game.current_winner:
                    self.end_game(f"恭喜你 ({self.human_player}) 获胜!")
                elif not self.game.empty_squares():
                    self.end_game("平局!")
                else:
                    self.current_player = self.computer_player
                    self.status_label.config(text=f"电脑思考中 ({self.computer_player})...")
                    self.master.after(500, self.computer_turn)
            else:
                messagebox.showerror("错误", "无效的移动。")

    def computer_turn(self):
        if not self.game.current_winner and self.game.empty_squares():
            computer_move = self.game.get_computer_move()
            if computer_move is not None and self.game.make_move(computer_move, self.computer_player):
                self.buttons[computer_move].config(text=self.computer_player, state=tk.DISABLED,
                                                   disabledforeground="red")
                if self.game.current_winner:
                    self.end_game(f"电脑 ({self.computer_player}) 获胜!")
                elif not self.game.empty_squares():
                    self.end_game("平局!")
                else:
                    self.current_player = self.human_player
                    self.status_label.config(text=f"轮到你了 ({self.human_player})")

    def end_game(self, message):
        self.status_label.config(text=message)
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        messagebox.showinfo("游戏结束", message)

    def restart_game(self):
        self.game = TicTacToe()
        self.current_player = self.human_player
        self.status_label.config(text=f"轮到你了 ({self.human_player})")
        for i in range(BOARD_SIZE * BOARD_SIZE):
            self.buttons[i].config(text=" ", state=tk.NORMAL)

def main():
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()