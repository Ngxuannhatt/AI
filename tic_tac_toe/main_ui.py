import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import sys
import os

# Ensure robust imports regardless of how the script is run
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from algorithms import minimax, alpha_beta, expectimax
except ImportError:
    try:
        from tic_tac_toe.algorithms import minimax, alpha_beta, expectimax
    except ImportError as e:
        print("Import error. Please check path structure:", e)

# Color Scheme for premium look
COLOR_BG_MAIN = "#f5f6fa"
COLOR_BG_PANEL = "#ffffff"
COLOR_TEXT_MAIN = "#2f3640"
COLOR_ACCENT = "#3498db"

# Player Colors
COLOR_X_BG = "#f5cdcb"       # Soft Red/Pink for AI (X)
COLOR_X_FG = "#c0392b"
COLOR_O_BG = "#d4e6f1"       # Soft Blue for Player (O)
COLOR_O_FG = "#2980b9"
COLOR_WIN_BG = "#d4efdf"     # Soft Green for Winning Line
COLOR_WIN_FG = "#27ae60"

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trực quan hóa Thuật toán Tic Tac Toe 3x3 (Caro)")
        
        # Center application window
        self.width = 1120
        self.height = 680
        self.center_window(self.width, self.height)
        
        # Configure overall layout background
        self.root.configure(bg=COLOR_BG_MAIN)
        
        # State management
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'O'  # 'O' (Player) or 'X' (AI)
        self.game_over = False
        self.ai_thinking = False
        
        # UI controls vars
        self.algo_var = tk.StringVar(value="Alpha-Beta Pruning")
        self.starter_var = tk.StringVar(value="Player (O)")
        
        # Performance Statistics
        self.stat_explored = tk.StringVar(value="0")
        self.stat_time = tk.StringVar(value="0.00 ms")
        self.stat_score = tk.StringVar(value="0")
        
        # Setup UI Components
        self.setup_styles()
        self.setup_ui()
        self.reset_game()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Frame styles
        self.style.configure("TFrame", background=COLOR_BG_MAIN)
        self.style.configure("Panel.TFrame", background=COLOR_BG_PANEL, relief=tk.SOLID, borderwidth=1)
        
        # Label styles
        self.style.configure("TLabel", background=COLOR_BG_MAIN, foreground=COLOR_TEXT_MAIN, font=("Arial", 10))
        self.style.configure("PanelTitle.TLabel", background=COLOR_BG_PANEL, foreground=COLOR_TEXT_MAIN, font=("Arial", 12, "bold"))
        self.style.configure("Header.TLabel", background=COLOR_ACCENT, foreground="white", font=("Arial", 16, "bold"), padding=10)
        self.style.configure("Status.TLabel", background=COLOR_BG_MAIN, foreground=COLOR_ACCENT, font=("Arial", 11, "bold"))
        self.style.configure("StatVal.TLabel", background=COLOR_BG_PANEL, foreground="#2f3640", font=("Arial", 10, "bold"))
        
        # Combobox styles
        self.style.configure("TCombobox", font=("Arial", 10))
        self.style.map("TCombobox", fieldbackground=[("readonly", "white")], background=[("readonly", "white")])

    def setup_ui(self):
        # 1. HEADER BANNER
        header = ttk.Label(self.root, text="TRỰC QUAN HÓA THUẬT TOÁN TIỂU LUẬN: TIC TAC TOE 3x3", style="Header.TLabel", anchor="center")
        header.pack(fill=tk.X)
        
        # Container for columns
        container = ttk.Frame(self.root, padding=15)
        container.pack(fill=tk.BOTH, expand=True)
        
        # --- CỘT TRÁI: ĐIỀU KHIỂN & THÔNG SỐ (Rộng: 320) ---
        left_column = ttk.Frame(container, style="Panel.TFrame", padding=15)
        left_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_column.pack_propagate(False)
        left_column.config(width=320)
        
        ttk.Label(left_column, text="CẤU HÌNH TRÒ CHƠI", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Algorithm selection
        ttk.Label(left_column, text="Thuật toán AI (X):", background=COLOR_BG_PANEL).pack(anchor="w", pady=(5, 2))
        self.algo_combo = ttk.Combobox(left_column, textvariable=self.algo_var, values=["Minimax", "Alpha-Beta Pruning", "Expectimax"], state="readonly")
        self.algo_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Starting player
        ttk.Label(left_column, text="Lượt đi đầu tiên:", background=COLOR_BG_PANEL).pack(anchor="w", pady=(5, 2))
        self.starter_combo = ttk.Combobox(left_column, textvariable=self.starter_var, values=["Player (O)", "AI (X)"], state="readonly")
        self.starter_combo.pack(fill=tk.X, pady=(0, 20))
        
        # Control buttons
        self.btn_reset = tk.Button(left_column, text="🔄 Thiết lập lại (Reset)", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", bd=0, pady=8, command=self.reset_game)
        self.btn_reset.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Separator(left_column, orient="horizontal").pack(fill=tk.X, pady=10)
        
        # AI Performance statistics
        ttk.Label(left_column, text="THÔNG SỐ LƯỢT ĐI AI", style="PanelTitle.TLabel").pack(anchor="w", pady=(10, 15))
        
        stat_frame = tk.Frame(left_column, bg=COLOR_BG_PANEL)
        stat_frame.pack(fill=tk.X)
        
        stats = [
            ("Số trạng thái duyệt:", self.stat_explored, "nút"),
            ("Thời gian tính toán:", self.stat_time, ""),
            ("Điểm đánh giá tốt nhất:", self.stat_score, "động")
        ]
        for label_text, var, unit in stats:
            f = tk.Frame(stat_frame, bg=COLOR_BG_PANEL, pady=5)
            f.pack(fill=tk.X)
            tk.Label(f, text=label_text, font=("Arial", 9), bg=COLOR_BG_PANEL, fg="#7f8c8d").pack(side=tk.LEFT)
            tk.Label(f, text=unit, font=("Arial", 9), bg=COLOR_BG_PANEL, fg="#7f8c8d").pack(side=tk.RIGHT)
            ttk.Label(f, textvariable=var, style="StatVal.TLabel").pack(side=tk.RIGHT, padx=5)
            
        ttk.Separator(left_column, orient="horizontal").pack(fill=tk.X, pady=15)
        
        # Educational info/guideline panel
        info_frame = tk.Frame(left_column, bg="#fcfcfc", bd=1, relief=tk.GROOVE, padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(info_frame, text="💡 Ghi chú thuật toán:", font=("Arial", 9, "bold"), bg="#fcfcfc", fg="#e67e22").pack(anchor="w")
        
        self.info_text = tk.Label(info_frame, text="", font=("Arial", 9), bg="#fcfcfc", fg="#7f8c8d", justify=tk.LEFT, wraplength=260)
        self.info_text.pack(anchor="w", pady=5)
        self.update_info_panel()
        self.algo_combo.bind("<<ComboboxSelected>>", lambda e: self.update_info_panel())
        
        # --- CỘT GIỮA: BÀN CỜ TICTACTOE (Rộng: 420) ---
        middle_column = ttk.Frame(container, style="TFrame")
        middle_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Title of board
        self.lbl_board_status = ttk.Label(middle_column, text="Lượt đi của Player (O)", style="Status.TLabel", anchor="center")
        self.lbl_board_status.pack(pady=(0, 10))
        
        # 3x3 Board Frame
        board_panel = ttk.Frame(middle_column, style="Panel.TFrame", padding=15)
        board_panel.pack(expand=True)
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(board_panel, text="", font=("Helvetica", 36, "bold"), bg="#ffffff",
                                activebackground="#ecf0f1", relief=tk.GROOVE, bd=1, width=4, height=1,
                                command=lambda row=r, col=c: self.player_move(row, col))
                btn.grid(row=r, column=c, padx=5, pady=5)
                # Bind hover events
                btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b))
                btn.bind("<Leave>", lambda e, b=btn: self.on_button_leave(b))
                self.buttons[r][c] = btn
                
        # --- CỘT PHẢI: NHẬT KÝ CHI TIẾT (Rộng: 340) ---
        right_column = ttk.Frame(container, style="Panel.TFrame", padding=15)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_column.pack_propagate(False)
        right_column.config(width=340)
        
        ttk.Label(right_column, text="NHẬT KÝ PHÂN TÍCH", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(right_column, height=25, font=("Courier New", 9), wrap=tk.WORD, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def on_button_hover(self, btn):
        if btn["text"] == "" and not self.game_over and not self.ai_thinking:
            btn.config(bg="#f1f2f6")

    def on_button_leave(self, btn):
        if btn["text"] == "" and not self.game_over and not self.ai_thinking:
            btn.config(bg="#ffffff")

    def update_info_panel(self):
        algo = self.algo_var.get()
        if algo == "Minimax":
            text = ("- Minimax duyệt qua TẤT CẢ các nhánh nước đi có thể.\n"
                    "- X đóng vai trò tối đa hóa điểm (X thắng = +10).\n"
                    "- O đóng vai trò tối thiểu hóa điểm (O thắng = -10).\n"
                    "- Số nút duyệt thường rất cao (tới 549,946 trạng thái ở nước đầu tiên).")
        elif algo == "Alpha-Beta Pruning":
            text = ("- Alpha-Beta hoạt động như Minimax nhưng tích hợp cơ chế CẮT TỈA nhánh con.\n"
                    "- Nhánh kém hơn giá trị alpha/beta đã biết sẽ bị bỏ qua lập tức.\n"
                    "- Giảm lượng trạng thái cần duyệt cực lớn (xuống còn ~18,000 ở nước đầu tiên), giúp tính toán nhanh gấp hàng chục lần nhưng vẫn đảm bảo nước đi tối ưu hoàn hảo.")
        else:
            text = ("- Expectimax được sử dụng khi đối thủ không chơi tối ưu hoàn toàn (ví dụ: chơi ngẫu nhiên).\n"
                    "- Lượt của AI (Max) tối đa hóa giá trị.\n"
                    "- Lượt của đối thủ (Chance) tính toán giá trị KỲ VỌNG (trung bình cộng điểm số).\n"
                    "- AI sẽ ưu tiên các nước đi an toàn hơn thay vì chỉ giả định đối thủ đi tối ưu nhất.")
        self.info_text.config(text=text)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.ai_thinking = False
        
        # Reset stats
        self.stat_explored.set("0")
        self.stat_time.set("0.00 ms")
        self.stat_score.set("0")
        
        # Enable starter combo during configuration
        self.starter_combo.config(state="readonly")
        
        # Reset grid buttons
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", bg="#ffffff", fg="#2f3640", state=tk.NORMAL)
                
        # Clear log text
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        
        # Determine who starts
        starter = self.starter_var.get()
        self.log(f"=== Bắt đầu trận đấu mới ===")
        self.log(f"Thuật toán AI lựa chọn: {self.algo_var.get()}")
        self.log(f"Đi trước: {starter}")
        
        if starter == "AI (X)":
            self.current_turn = 'X'
            self.lbl_board_status.config(text="AI (X) đang suy nghĩ...", foreground=COLOR_X_FG)
            self.trigger_ai_move()
        else:
            self.current_turn = 'O'
            self.lbl_board_status.config(text="Lượt đi của Player (O)", foreground=COLOR_O_FG)

    def player_move(self, row, col):
        if self.game_over or self.ai_thinking or self.current_turn != 'O':
            return
            
        if self.board[row][col] != '':
            return
            
        # Player makes a move
        self.board[row][col] = 'O'
        self.buttons[row][col].config(text="O", bg=COLOR_O_BG, fg=COLOR_O_FG, state=tk.DISABLED)
        
        # Lock configuration once the game has started
        self.starter_combo.config(state=tk.DISABLED)
        
        self.log(f"Người chơi (O) đi tại ô ({row}, {col})")
        
        # Check game status
        if self.check_game_end():
            return
            
        # Switch turn
        self.current_turn = 'X'
        self.lbl_board_status.config(text="AI (X) đang suy nghĩ...", foreground=COLOR_X_FG)
        self.trigger_ai_move()

    def trigger_ai_move(self):
        self.ai_thinking = True
        # Disable all board buttons to prevent user interactions
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    self.buttons[r][c].config(state=tk.DISABLED)
                    
        # Launch AI processing thread to keep GUI responsive and allow smooth logs
        threading.Thread(target=self.process_ai_move, daemon=True).start()

    def process_ai_move(self):
        algo = self.algo_var.get()
        start_time = time.perf_counter()
        
        # Call the selected search algorithm
        if algo == "Minimax":
            move, score, explored, evaluations = minimax.get_best_move(self.board)
        elif algo == "Alpha-Beta Pruning":
            move, score, explored, evaluations = alpha_beta.get_best_move(self.board)
        else:
            move, score, explored, evaluations = expectimax.get_best_move(self.board)
            
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        
        # Return result back to main GUI Thread
        self.root.after(0, lambda: self.apply_ai_move(move, score, explored, elapsed_ms, evaluations, algo))

    def apply_ai_move(self, move, score, explored, elapsed_ms, evaluations, algo):
        if self.game_over:
            return
            
        # Execute AI move on board
        if move:
            r, c = move
            self.board[r][c] = 'X'
            self.buttons[r][c].config(text="X", bg=COLOR_X_BG, fg=COLOR_X_FG, state=tk.DISABLED)
            
            # Print detailed logs in the panel
            self.log(f"\n--- AI phân tích ({algo}) ---")
            self.log(f"Thời gian tính toán: {elapsed_ms:.2f} ms")
            self.log(f"Số trạng thái đã duyệt: {explored:,}")
            self.log(f"Điểm số gán cho các nước khả thi:")
            
            # Sort move evaluations for tidy logging
            for pos, val in sorted(evaluations.items()):
                self.log(f"  └─ Ô {pos}: Điểm = {val:.2f}")
                
            self.log(f"▶ AI quyết định đi tại ô ({r}, {c}) với điểm tối ưu: {score:.2f}")
            
            # Update left statistics widgets
            self.stat_explored.set(f"{explored:,}")
            self.stat_time.set(f"{elapsed_ms:.2f} ms")
            self.stat_score.set(f"{score:.2f}")
        
        self.ai_thinking = False
        
        # Check game status
        if self.check_game_end():
            return
            
        # Switch turn back to Player
        self.current_turn = 'O'
        self.lbl_board_status.config(text="Lượt đi của Player (O)", foreground=COLOR_O_FG)
        
        # Re-enable empty buttons for player interaction
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '':
                    self.buttons[r][c].config(state=tk.NORMAL)

    def check_game_end(self):
        # We can import check_winner from minimax
        winner = minimax.check_winner(self.board)
        if winner is None:
            return False
            
        self.game_over = True
        
        # Highlight winning cells if there is a winner
        if winner in ['X', 'O']:
            winning_cells = self.get_winning_cells(winner)
            for r, c in winning_cells:
                self.buttons[r][c].config(bg=COLOR_WIN_BG, fg=COLOR_WIN_FG)
                
            if winner == 'X':
                msg = "AI (X) giành chiến thắng!"
                self.lbl_board_status.config(text=msg, foreground=COLOR_X_FG)
                self.log(f"\n🏆 KẾT QUẢ: {msg}")
                messagebox.showinfo("Kết quả", "AI (X) thắng cuộc! Hãy cố gắng hơn ở lượt sau.")
            else:
                msg = "Chúc mừng! Bạn (O) đã chiến thắng!"
                self.lbl_board_status.config(text=msg, foreground=COLOR_O_FG)
                self.log(f"\n🏆 KẾT QUẢ: {msg}")
                messagebox.showinfo("Kết quả", "Bạn (O) đã chiến thắng!")
        else:
            msg = "Trận đấu hòa!"
            self.lbl_board_status.config(text=msg, foreground="#7f8c8d")
            self.log(f"\n🤝 KẾT QUẢ: {msg}")
            messagebox.showinfo("Kết quả", "Trận đấu hòa!")
            
        # Disable all board buttons
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state=tk.DISABLED)
                
        return True

    def get_winning_cells(self, player):
        # Rows
        for r in range(3):
            if self.board[r][0] == self.board[r][1] == self.board[r][2] == player:
                return [(r, 0), (r, 1), (r, 2)]
        # Columns
        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] == player:
                return [(0, c), (1, c), (2, c)]
        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return [(0, 2), (1, 1), (2, 0)]
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
