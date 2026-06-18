import tkinter as tk
from tkinter import scrolledtext, messagebox
import random

# Giữ nguyên các import thuật toán của bạn
from BFS_1 import bfs_1
from BFS_2 import bfs_2
from DFS_1 import dfs_1
from DFS_2 import dfs_2
from IDS_1 import ids_1
from IDS_2 import ids_2
from UCS import ucs
from GS import gs
from Astar import A_Star
from IDAstar import IDAstar
from Simple_Hill_Climbing import Simple_Hill_Climbing
from Steepest_Ascent_Hill_Climbing import Steepest_Ascent_Hill_Climbing
from Stochastic_Hill_Climbing import Stochastic_Hill_Climbing
from Random_Restart_Hill_Climbing import Random_Restart_Hill_Climbing
from Local_Beam_Search import Local_Beam_Search
from Simulated_Annealing import SimulatedAnnealing
from DFS_Searching_With_No_Observation import dfs_no_observation
from DFS_Searching_for_partially_observable_problems import dfs_partially_observable
from And_Or_Search import and_or_graph_search

# ==========================================
# PHẦN 2: LỚP GIAO DIỆN (UI) CHÍNH
# ==========================================
class VacuumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng AI Máy Hút Bụi - Giao Diện Hoàn Chỉnh")
        self.root.geometry("1100x650")
        
        # Các biến trạng thái cơ bản
        self.n = 0
        self.matrix = []
        self.agent_x = 0
        self.agent_y = 0
        
        # Các biến trạng thái bổ sung cho thuật toán No Observation (2 trạng thái)
        self.matrix2 = []
        self.agent2_x = 0
        self.agent2_y = 0
        self.is_dual_state = False  # Cờ hiệu xác định có vẽ 2 ma trận hay không

        self.is_running = False  # Khóa nút bấm khi đang chạy animation
        
        # Tải ảnh máy hút bụi một lần duy nhất để tránh bị giải phóng bộ nhớ (garbage collection) làm mất hình ở ma trận bên trái
        try:
            self.img_vacuum = tk.PhotoImage(file='vacuum.png', master=self.root)
        except Exception:
            self.img_vacuum = None
            
        self.setup_ui()

    def setup_ui(self):
        # --- FRAME BÊN TRÁI CÓ THANH CUỘN --- 
        left_container = tk.Frame(self.root) 
        left_container.pack(side=tk.LEFT, fill=tk.Y) 
        # Scrollbar
        scrollbar = tk.Scrollbar(left_container, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
        # Canvas chứa nội dung cuộn 
        canvas = tk.Canvas(left_container, width=260, bg="#f0f0f0", highlightthickness=0, yscrollcommand=scrollbar.set) 
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
        scrollbar.config(command=canvas.yview) 
        # Frame thật sự chứa các widget
        left_frame = tk.Frame(canvas, bg="#f0f0f0", padx=10, pady=10) 
        canvas.create_window((0, 0), window=left_frame, anchor="nw") 
        
        # Cập nhật vùng cuộn 
        def configure_scroll_region(event): 
            canvas.configure(scrollregion=canvas.bbox("all")) 
        left_frame.bind("<Configure>", configure_scroll_region) 
        
        # Cuộn bằng bánh xe chuột 
        def on_mousewheel(event): 
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") 
        canvas.bind_all("<MouseWheel>", on_mousewheel) 

        # ========================== # CÁC WIDGET BÊN TRÁI # ========================== 
        tk.Label(left_frame, text="Kích thước ma trận (n):", bg="#f0f0f0").pack(anchor="w") 
        self.entry_n = tk.Entry(left_frame) 
        self.entry_n.insert(0, "3") 
        self.entry_n.pack(fill=tk.X, pady=(0, 15)) 
        tk.Button(left_frame, text="Tạo Mới / Reset", command=self.generate_map, bg="#ffcc00").pack(fill=tk.X, pady=(0, 20)) 
        tk.Label(left_frame, text="CHỌN THUẬT TOÁN:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # 4 Ô Thuật Toán (và các nút khác)
        tk.Button(left_frame, text="BFS Tiếp cận 1\n(Kiểm tra đích muộn)", command=lambda: self.run_algorithm("BFS1"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="BFS Tiếp cận 2\n(Kiểm tra đích sớm)", command=lambda: self.run_algorithm("BFS2"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="DFS Tiếp cận 1\n(Kiểm tra đích muộn)", command=lambda: self.run_algorithm("DFS1"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="DFS Tiếp cận 2\n(Kiểm tra đích sớm)", command=lambda: self.run_algorithm("DFS2"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="IDS Tiếp cận 1\n(Kiểm tra đích muộn)", command=lambda: self.run_algorithm("IDS1"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="IDS Tiếp cận 2\n(Kiểm tra đích sớm)", command=lambda: self.run_algorithm("IDS2"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="UCS", command=lambda: self.run_algorithm("UCS"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="GS", command=lambda: self.run_algorithm("GS"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Astar", command=lambda: self.run_algorithm("Astar"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="IDAstar", command=lambda: self.run_algorithm("IDAstar"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Simple_Hill_Climbing", command=lambda: self.run_algorithm("Simple_Hill_Climbing"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Steepest_Ascent_Hill_Climbing", command=lambda: self.run_algorithm("Steepest_Ascent_Hill_Climbing"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Stochastic_Hill_Climbing", command=lambda: self.run_algorithm("Stochastic_Hill_Climbing"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Random_Restart_Hill_Climbing", command=lambda: self.run_algorithm("Random_Restart_Hill_Climbing"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="Local_Beam_Search", command=lambda: self.run_algorithm("Local_Beam_Search"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="SimulatedAnnealing", command=lambda: self.run_algorithm("SimulatedAnnealing"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="dfs_no_observation", command=lambda: self.run_algorithm("dfs_no_observation"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="and_or_graph_search", command=lambda: self.run_algorithm("and_or_graph_search"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="dfs_partially_observable", command=lambda: self.run_algorithm("dfs_partially_observable"), bg="#d9d9d9").pack(fill=tk.X, pady=5)
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

        # Đưa giao diện về trạng thái vẽ 1 ma trận mặc định khi reset
        self.is_dual_state = False
        
        with open("matrix.txt", "r") as f:
            self.matrix = []
            for line in f:
                row = list(map(int, line.strip().split()))
                self.matrix.append(row)

            self.n = len(self.matrix)
            # vị trí robot mặc định (đảm bảo nằm trong kích thước ma trận n x n)
            self.agent_x = min(1, self.n - 1) if self.n > 0 else 0
            self.agent_y = min(2, self.n - 1) if self.n > 0 else 0

            self.clear_logs()
            self.write_log("Đã tạo map từ file txt.", "log")
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        if self.n == 0: return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if self.is_dual_state:
            # Chế độ 2 ma trận: Chia đôi chiều rộng Canvas
            self._draw_single_grid(0, 0, w/2, h, self.matrix, self.agent_x, self.agent_y, "Trạng thái 1")
            self._draw_single_grid(w/2, 0, w, h, self.matrix2, self.agent2_x, self.agent2_y, "Trạng thái 2")
        else:
            # Chế độ 1 ma trận: Vẽ full Canvas
            self._draw_single_grid(0, 0, w, h, self.matrix, self.agent_x, self.agent_y, "")

    def _draw_single_grid(self, start_x, start_y, end_x, end_y, matrix, agent_x, agent_y, title):
        if not matrix: return
        
        box_w = end_x - start_x
        box_h = end_y - start_y
        
        # Tính kích thước của 1 ô vuông (nhân 0.8 để có khoảng trống lề)
        cell_size = min(box_w, box_h) * 0.8 / self.n
        
        # Căn giữa bàn cờ trong khu vực được cấp
        offset_x = start_x + (box_w - (cell_size * self.n)) / 2
        offset_y = start_y + (box_h - (cell_size * self.n)) / 2

        # Vẽ tiêu đề nếu có (dành cho chế độ 2 ma trận)
        if title:
            self.canvas.create_text(start_x + box_w/2, offset_y - 20, text=title, font=("Arial", 12, "bold"), fill="blue")

        # Vẽ các ô Caro
        for r in range(self.n):
            for c in range(self.n):
                x1 = offset_x + c * cell_size
                y1 = offset_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # 1 = Dơ (Trắng/Xám), 0 = Sạch (Xanh)
                color = "gray" if matrix[r][c] == 1 else "lightgreen"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Vẽ máy hút bụi
                if r == agent_x and c == agent_y:
                    self.draw_agent(x1, y1, x2, y2)

    def draw_agent(self, x1, y1, x2, y2):
        if self.img_vacuum is not None:
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            self.canvas.create_image(center_x, center_y, image=self.img_vacuum)
        else:
            # Fallback nếu không có ảnh: vẽ hình tròn đỏ
            self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="red")

    # ==========================================
    # PHẦN 3: ĐIỀU HƯỚNG THUẬT TOÁN & ANIMATION
    # ==========================================
    def run_algorithm(self, algo_type):
        if self.is_running:
            messagebox.showwarning("Cảnh báo", "Đang chạy mô phỏng, vui lòng đợi!")
            return
        
        self.clear_logs()
        self.is_running = True
        
        # --- THIẾT LẬP CỜ HIỆU ĐỂ UI BIẾT CẦN VẼ 2 MA TRẬN KHÔNG ---
        self.is_dual_state = (algo_type == "dfs_no_observation" or algo_type =="dfs_partially_observable" )

        self.write_log(f"Đang chạy thuật toán: {algo_type}...", "log")
        self.root.update()
 
        path = None
        if algo_type == "BFS1": path = bfs_1(self)
        elif algo_type == "BFS2": path = bfs_2(self)
        elif algo_type == "DFS1": path = dfs_1(self)
        elif algo_type == "DFS2": path = dfs_2(self)
        elif algo_type == "IDS1": path = ids_1(self)
        elif algo_type == "IDS2": path = ids_2(self)
        elif algo_type == "UCS": path = ucs(self)
        elif algo_type == "GS": path = gs(self)
        elif algo_type == "Astar": path = A_Star(self)
        elif algo_type == "IDAstar": path = IDAstar(self)
        elif algo_type == "Simple_Hill_Climbing": path = Simple_Hill_Climbing(self)
        elif algo_type == "Stochastic_Hill_Climbing": path = Stochastic_Hill_Climbing(self)
        elif algo_type == "Steepest_Ascent_Hill_Climbing": path = Steepest_Ascent_Hill_Climbing(self)
        elif algo_type == "Random_Restart_Hill_Climbing": path = Random_Restart_Hill_Climbing(self)
        elif algo_type == "Local_Beam_Search": path = Local_Beam_Search(self)
        elif algo_type == "SimulatedAnnealing": path = SimulatedAnnealing(self)
        elif algo_type == "dfs_no_observation": path = dfs_no_observation(self)
        elif algo_type == "and_or_graph_search":path = and_or_graph_search(self)
        elif algo_type == "dfs_partially_observable":path = dfs_partially_observable(self)

        if path:
            
            self.write_log(f"Tìm thấy lời giải ({len(path)-1} bước)", "log")

            for i, node in enumerate(path):
                self.write_log(f"Bước {i}: {node.action}", "log")
                
                # In log phân biệt giữa 2 ma trận hoặc 1 ma trận để tránh lỗi
                if self.is_dual_state and hasattr(node, 'state1'):
                    self.write_log(f"State1: ({node.state1.x},{node.state1.y})", "log")
                    for row in node.state1.matrix:
                        self.write_log(str(row), "log")
                    self.write_log("----------------", "log")

                    self.write_log(f"State2: ({node.state2.x},{node.state2.y})", "log")
                    for row in node.state2.matrix:
                        self.write_log(str(row), "log")
                    self.write_log("================", "log")
                else:
                    # Thuật toán 1 ma trận
                    self.write_log(f"State: ({node.x},{node.y})", "log")
                    for row in node.matrix:
                        self.write_log(str(row), "log")
                    self.write_log("================", "log")

            # Gọi UI bắt đầu chạy mô phỏng di chuyển (animation)
            self.animate_path(path, 0)

        else:
            self.write_log("Không tìm thấy lời giải", "log")
            self.is_running = False

    def animate_path(self, path, step_idx):
        if step_idx < len(path):
            node = path[step_idx]
            
            # Cập nhật trạng thái cho UI tùy theo loại thuật toán
            if self.is_dual_state and hasattr(node, 'state1'):
                self.agent_x = node.state1.x
                self.agent_y = node.state1.y
                self.matrix = node.state1.matrix
                
                self.agent2_x = node.state2.x
                self.agent2_y = node.state2.y
                self.matrix2 = node.state2.matrix
            else:
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
            
            if self.is_dual_state:
                coord_list = [f"[({n.state1.x},{n.state1.y})&({n.state2.x},{n.state2.y})]" for n in path]
            else:
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