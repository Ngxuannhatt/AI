
import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
from BFS_1 import bfs_1
from BFS_2 import bfs_2
from DFS_1 import dfs_1
from DFS_2 import dfs_2
from IDS_1 import ids_1
from IDS_2 import ids_2
from UCS import ucs
from GS import gs
from Astar import A_Star


# ==========================================
# PHẦN 2: LỚP GIAO DIỆN (UI) CHÍNH
# ==========================================
class VacuumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng AI Máy Hút Bụi - Giao Diện Hoàn Chỉnh")
        self.root.geometry("1100x650")
        
        # Các biến trạng thái
        self.n = 0
        self.matrix = []
        self.agent_x = 0
        self.agent_y = 0
        self.is_running = False  # Khóa nút bấm khi đang chạy animation

        self.setup_ui()

    def setup_ui(self):
        # --- FRAME BÊN TRÁI: ĐIỀU KHIỂN & CHỌN THUẬT TOÁN ---
        left_frame = tk.Frame(self.root, width=200, bg="#f0f0f0", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_frame, text="Kích thước ma trận (n):", bg="#f0f0f0").pack(anchor="w")
        self.entry_n = tk.Entry(left_frame)
        self.entry_n.insert(0, "3") # Mặc định n=3
        self.entry_n.pack(fill=tk.X, pady=(0, 15))

        tk.Button(left_frame, text="Tạo Mới / Reset", command=self.generate_map, bg="#ffcc00").pack(fill=tk.X, pady=(0, 20))

        tk.Label(left_frame, text="CHỌN THUẬT TOÁN:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # 4 Ô Thuật Toán
        tk.Button(left_frame, text="BFS Tiếp cận 1\n(Kiểm tra đích muộn)", command=lambda: self.run_algorithm("BFS1"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="BFS Tiếp cận 2\n(Kiểm tra đích sớm)", command=lambda: self.run_algorithm("BFS2"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="DFS Tiếp cận 1\n(Kiểm tra đích muộn)", command=lambda: self.run_algorithm("DFS1"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="DFS Tiếp cận 2\n(Kiểm tra đích sớm)", command=lambda: self.run_algorithm("DFS2"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="IDS Tiếp cận 1\n(Kiểm tra đích muộn)", command=lambda: self.run_algorithm("IDS1"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="IDS Tiếp cận 2\n(Kiểm tra đích sớm)", command=lambda: self.run_algorithm("IDS2"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="UCS", command=lambda: self.run_algorithm("UCS"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="GS", command=lambda: self.run_algorithm("GS"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Astar", command=lambda: self.run_algorithm("Astar"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        # --- FRAME Ở GIỮA: BÀN CỜ CARO ---
        center_frame = tk.Frame(self.root, bg="white")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.canvas = tk.Canvas(center_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Bắt sự kiện thay đổi kích thước cửa sổ để vẽ lại bàn cờ cho khớp
        self.canvas.bind("<Configure>", lambda e: self.draw_grid())

        # --- FRAME BÊN PHẢI: NHẬT KÝ & TRUY VẾT ---
        right_frame = tk.Frame(self.root, width=300, bg="#f0f0f0", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(right_frame, text="Nhật ký quá trình đi:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(right_frame, width=35, height=20, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        tk.Label(right_frame, text="Truy vết ngược (Đích -> Nguồn):", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.trace_text = scrolledtext.ScrolledText(right_frame, width=35, height=10, state="disabled")
        self.trace_text.pack(fill=tk.BOTH, expand=True)

        # Khởi tạo bản đồ lần đầu
        self.generate_map()

    def write_log(self, text, widget="log"):
        # Hàm hỗ trợ ghi text vào khung bên phải
        target = self.log_text if widget == "log" else self.trace_text
        target.config(state="normal")
        target.insert(tk.END, text + "\n")
        target.see(tk.END)
        target.config(state="disabled")

    def clear_logs(self):
        for target in (self.log_text, self.trace_text):
            target.config(state="normal")
            target.delete(1.0, tk.END)
            target.config(state="disabled")

    def generate_map(self):
        if self.is_running:
            return

        with open("matrix.txt", "r") as f:
            self.matrix = []

            for line in f:
                row = list(map(int, line.strip().split()))
                self.matrix.append(row)

            self.n = len(self.matrix)

            # vị trí robot random
            self.agent_x = 1
            self.agent_y = 2

            self.clear_logs()
            self.write_log("Đã tạo map từ file txt.", "log")
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        if self.n == 0: return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # Tính kích thước của 1 ô vuông
        cell_size = min(w, h) / self.n
        
        # Tính khoảng lề để căn giữa bàn cờ
        offset_x = (w - (cell_size * self.n)) / 2
        offset_y = (h - (cell_size * self.n)) / 2

        # Vẽ các ô Caro
        for r in range(self.n):
            for c in range(self.n):
                x1 = offset_x + c * cell_size
                y1 = offset_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # 1 = Dơ (Trắng), 0 = Sạch (Xanh)
                color = "gray" if self.matrix[r][c] == 1 else "lightgreen"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Nếu là vị trí của máy hút bụi thì vẽ đè lên
                if r == self.agent_x and c == self.agent_y:
                    self.draw_agent(x1, y1, x2, y2)

    def draw_agent(self, x1, y1, x2, y2):
        self.img = tk.PhotoImage(file='vacuum.png', master=self.root)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        self.canvas.create_image(center_x, center_y, image=self.img)
  
   


    # ==========================================
    # PHẦN 3: ĐIỀU HƯỚNG THUẬT TOÁN & ANIMATION
    # ==========================================
    def run_algorithm(self, algo_type):
        if self.is_running:
            messagebox.showwarning("Cảnh báo", "Đang chạy mô phỏng, vui lòng đợi!")
            return
        
        self.clear_logs()
        self.is_running = True
        self.write_log(f"Đang chạy thuật toán: {algo_type}...", "log")
        self.root.update()
 
        path = None
        if algo_type == "BFS1":
            path = bfs_1(self)
        elif algo_type=="BFS2":
            path = bfs_2(self)
        elif algo_type=="DFS1":
            path = dfs_1(self)
        elif algo_type=="DFS2":
            path = dfs_2(self)
        elif algo_type =="IDS1":
            path = ids_1(self)
        elif algo_type == "IDS2":
            path = ids_2(self)
        elif algo_type == "UCS":
            path = ucs(self)
        elif algo_type == "GS":
            path = gs(self)
        elif algo_type == "Astar":
            path = A_Star(self)
        if path:
            self.write_log(f"-> Tìm thấy đường đi! (Số bước: {len(path)-1})", "log")
            self.animate_path(path, 0)
        else:
            self.write_log("-> KHÔNG tìm thấy giải pháp hoặc bị quá hạn.", "log")
            self.is_running = False

    def animate_path(self, path, step_idx):
        if step_idx < len(path):
            node = path[step_idx]
            # Cập nhật trạng thái cho UI
            self.agent_x = node.x
            self.agent_y = node.y
            self.matrix = node.matrix
            self.draw_grid()
            
            # Ghi nhật ký từng bước tiến tới
            self.write_log(f"Bước {step_idx}: {node.action}", "log")
            
            # Đặt hẹn giờ chạy bước tiếp theo (Delay 400ms mỗi bước)
            self.root.after(400, self.animate_path, path, step_idx + 1)
        else:
            # Khi chạy xong, in truy vết ngược ở ô dưới
            self.write_log("=== TRUY VẾT NGƯỢC (TỪ NGUỒN VỀ ĐÍCH) ===", "trace")
            

            coord_list = [f"({node.x},{node.y})" for node in path]
            
            # Nối chúng lại bằng dấu " -> "

            trace_string = " -> ".join(coord_list)
            self.write_log(trace_string, "trace")
            
            self.is_running = False
            messagebox.showinfo("Hoàn tất", "Đã mô phỏng xong!")



# ==========================================
# KHỞI CHẠY ỨNG DỤNG
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumApp(root)
    root.mainloop()