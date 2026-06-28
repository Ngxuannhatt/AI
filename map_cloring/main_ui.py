import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import copy

# Add current folder to path to ensure correct imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from back_tracking import map_coloring_backtracking
from forward_checking import forward_checking_coloring
from AC3 import ac3_checking_coloring
from min_conflicts import min_conflicts_coloring
# --- CẤU HÌNH ĐỒ THỊ 7 QUẬN TP.HCM ---
NEIGHBORS = {
    'Quận 1': ['Quận 3', 'Quận 10'],
    'Quận 3': ['Quận 1', 'Quận Bình Thạnh', 'Quận Phú Nhuận'],
    'Quận Bình Thạnh': ['Quận 3'],
    'Quận Phú Nhuận': ['Quận 3'],
    'Quận 10': ['Quận 1', 'Quận 5', 'Quận 11'],
    'Quận 5': ['Quận 10'],
    'Quận 11': ['Quận 10']
}

NODE_POSITIONS = {
    'Quận 1': (120, 225),
    'Quận 3': (280, 100),
    'Quận Bình Thạnh': (480, 100),
    'Quận Phú Nhuận': (340, 225),
    'Quận 10': (280, 350),
    'Quận 5': (450, 290),
    'Quận 11': (450, 400)
}

DISPLAY_NAMES = {
    'Quận 1': 'Quận 1\n(Start Node)',
    'Quận 3': 'Quận 3',
    'Quận Bình Thạnh': 'Bình Thạnh',
    'Quận Phú Nhuận': 'Phú Nhuận',
    'Quận 10': 'Quận 10',
    'Quận 5': 'Quận 5',
    'Quận 11': 'Quận 11\n(Success Node)'
}

COLOR_INFO = {
    1: {"name": "Xanh Dương", "hex": "#3498db", "text": "white"},
    2: {"name": "Xanh Lá", "hex": "#2ecc71", "text": "white"},
    3: {"name": "Đỏ", "hex": "#e74c3c", "text": "white"},
    4: {"name": "Vàng", "hex": "#f1c40f", "text": "black"},
    5: {"name": "Tím", "hex": "#9b59b6", "text": "white"},
    6: {"name": "Cam", "hex": "#e67e22", "text": "white"},
    7: {"name": "Màu Lơ", "hex": "#1abc9c", "text": "white"}
}

class MapColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Thuật toán Tô màu Bản đồ - 7 Quận TP.HCM")
        
        # Căn giữa cửa sổ ứng dụng
        self.width = 1150
        self.height = 680
        self.center_window(self.width, self.height)
        
        self.neighbors = NEIGHBORS
        self.node_positions = NODE_POSITIONS
        
        # Quản lý các bước mô phỏng
        self.steps = []
        self.current_step_idx = -1
        self.is_playing = False
        self.delay = 600  # ms
        
        # Biến điều khiển giao diện
        self.algo_var = tk.StringVar(value="Backtracking")
        self.color_mode_var = tk.StringVar(value="2")
        
        self.setup_ui()
        self.reset_ui()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Định nghĩa kiểu giao diện hiện đại (ttk Style)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#ecf0f1", foreground="#2c3e50")
        self.style.configure("Treeview", font=("Arial", 9), rowheight=25)
        self.style.map("Treeview", background=[("selected", "#3498db")])

        # --- FRAME TRÁI: ĐIỀU KHIỂN ---
        left_frame = tk.Frame(self.root, bg="#f8f9fa", width=280, padx=15, pady=15, bd=1, relief=tk.SOLID)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="CẤU HÌNH thuật toán", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 15))
        
        # Chọn thuật toán
        tk.Label(left_frame, text="Chọn Thuật Toán:", font=("Arial", 10), bg="#f8f9fa").pack(anchor="w")
        algo_combo = ttk.Combobox(left_frame, textvariable=self.algo_var, values=["Backtracking", "Forward Checking","AC3", "Min_conflicts"], state="readonly", font=("Arial", 10))
        algo_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Chọn số màu
        tk.Label(left_frame, text="Số màu cho phép tối đa:", font=("Arial", 10), bg="#f8f9fa").pack(anchor="w")
        color_combo = ttk.Combobox(left_frame, textvariable=self.color_mode_var, values=["2", "3", "4", "Auto (Tự động tìm tối thiểu)"], state="readonly", font=("Arial", 10))
        color_combo.pack(fill=tk.X, pady=(0, 20))

        # Nút khởi chạy
        btn_run = tk.Button(left_frame, text="Khởi Chạy", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white", bd=0, pady=8, command=self.run_search)
        btn_run.pack(fill=tk.X, pady=(0, 20))

        # Kháng hiệu ứng ngăn cản tương tác
        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        # Điều khiển Playback
        tk.Label(left_frame, text="ĐIỀU KHIỂN MÔ PHỎNG", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 10))

        # Nút Tua / Chạy tự động
        btn_control_frame = tk.Frame(left_frame, bg="#f8f9fa")
        btn_control_frame.pack(fill=tk.X, pady=5)

        self.btn_prev = tk.Button(btn_control_frame, text="⏮ Trước", font=("Arial", 9), width=7, command=self.prev_step)
        self.btn_prev.pack(side=tk.LEFT, padx=2)

        self.btn_play = tk.Button(btn_control_frame, text="▶ Chạy tự động", font=("Arial", 9, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white", command=self.toggle_play)
        self.btn_play.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_next = tk.Button(btn_control_frame, text="Sau ⏭", font=("Arial", 9), width=7, command=self.next_step)
        self.btn_next.pack(side=tk.LEFT, padx=2)

        # Thanh trượt các bước
        tk.Label(left_frame, text="Thanh trượt bước mô phỏng:", font=("Arial", 9), bg="#f8f9fa").pack(anchor="w", pady=(15, 2))
        self.step_scale = tk.Scale(left_frame, from_=0, to=0, orient=tk.HORIZONTAL, bg="#f8f9fa", length=240, command=self.on_slider_move)
        self.step_scale.pack(fill=tk.X, pady=(0, 15))

        # Thanh trượt tốc độ (Speed Slider)
        tk.Label(left_frame, text="Tốc độ chạy tự động (ms):", font=("Arial", 9), bg="#f8f9fa").pack(anchor="w", pady=(5, 2))
        self.speed_scale = tk.Scale(left_frame, from_=200, to=2000, resolution=100, orient=tk.HORIZONTAL, bg="#f8f9fa", length=240, command=self.update_speed)
        self.speed_scale.set(self.delay)
        self.speed_scale.pack(fill=tk.X, pady=(0, 15))

        # Nút Reset
        btn_reset = tk.Button(left_frame, text="🔄 Đặt lại (Reset)", font=("Arial", 10), bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", bd=0, pady=5, command=self.reset_ui)
        btn_reset.pack(fill=tk.X, pady=10)

        # Thông tin bước hiện tại
        self.lbl_step_info = tk.Label(left_frame, text="Bước: 0 / 0", font=("Arial", 10, "bold"), bg="#f8f9fa", fg="#7f8c8d")
        self.lbl_step_info.pack(side=tk.BOTTOM, pady=10)

        # --- FRAME GIỮA: SƠ ĐỒ ĐỒ THỊ ---
        center_frame = tk.Frame(self.root, bg="white", bd=1, relief=tk.SOLID)
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Tiêu đề sơ đồ
        self.lbl_canvas_title = tk.Label(center_frame, text="SƠ ĐỒ PHÂN BỐ VÀ LIÊN KẾT 7 QUẬN TP.HCM", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50", pady=10)
        self.lbl_canvas_title.pack(anchor="center")

        # Canvas vẽ sơ đồ
        self.canvas = tk.Canvas(center_frame, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # --- FRAME PHẢI: NHẬT KÝ & MIỀN GIÁ TRỊ ---
        right_frame = tk.Frame(self.root, bg="#f8f9fa", width=340, padx=15, pady=15, bd=1, relief=tk.SOLID)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)

        # Nhật ký
        tk.Label(right_frame, text="NHẬT KÝ QUÁ TRÌNH CHẠY", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        self.log_text = scrolledtext.ScrolledText(right_frame, height=14, font=("Courier New", 9), state="disabled", wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Miền giá trị (Domains)
        tk.Label(right_frame, text="MIỀN GIÁ TRỊ CỦA CÁC QUẬN", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        
        # Bảng hiển thị thông tin miền giá trị
        self.tree = ttk.Treeview(right_frame, columns=("District", "Assignment", "Domain"), show="headings", height=8)
        self.tree.heading("District", text="Quận")
        self.tree.heading("Assignment", text="Màu Đã Gán")
        self.tree.heading("Domain", text="Miền Giá Trị")
        
        self.tree.column("District", width=100, anchor="center")
        self.tree.column("Assignment", width=105, anchor="center")
        self.tree.column("Domain", width=95, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def update_speed(self, val):
        self.delay = int(val)

    def toggle_play(self):
        if not self.steps:
            messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Khởi Chạy' thuật toán trước!")
            return
            
        if self.is_playing:
            self.pause_animation()
        else:
            self.is_playing = True
            self.btn_play.config(text="⏸ Tạm Dừng", bg="#e67e22")
            self.play_animation()

    def pause_animation(self):
        self.is_playing = False
        self.btn_play.config(text="▶ Chạy tự động", bg="#3498db")

    def play_animation(self):
        if not self.is_playing:
            return
            
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.step_scale.set(self.current_step_idx)  # Tự động gọi on_slider_move để vẽ lại UI
            self.root.after(self.delay, self.play_animation)
        else:
            self.pause_animation()
            messagebox.showinfo("Hoàn tất", "Đã chạy hết các bước mô phỏng!")

    def next_step(self):
        self.pause_animation()
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.step_scale.set(self.current_step_idx)

    def prev_step(self):
        self.pause_animation()
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.step_scale.set(self.current_step_idx)

    def on_slider_move(self, val):
        idx = int(val)
        if 0 <= idx < len(self.steps):
            self.current_step_idx = idx
            self.update_ui_to_step(idx)

    def reset_ui(self):
        self.pause_animation()
        self.steps = []
        self.current_step_idx = -1
        self.step_scale.config(from_=0, to=0)
        self.step_scale.set(0)
        
        self.lbl_step_info.config(text="Bước: 0 / 0")
        
        # Xóa nhật ký
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        
        # Xóa bảng miền giá trị
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Vẽ đồ thị trắng
        self.draw_graph()

    def run_search(self):
        self.reset_ui()
        
        algo = self.algo_var.get()
        color_mode_str = self.color_mode_var.get()
        
        is_fc = (algo == "Forward Checking")
        
        # Xác định số lượng màu thử nghiệm
        if "Auto" in color_mode_str:
            colors_range = range(1, len(self.neighbors) + 1)
            is_auto = True
        else:
            colors_range = [int(color_mode_str)]
            is_auto = False

        # Callback dùng để ghi lại từng sự kiện khi thuật toán chạy
        def make_callback(n_cols):
            def callback(region, color, action_type, assignment, domains):
                # Đồng bộ hóa miền giá trị cho dễ hiển thị ở UI
                if domains is None:
                    # Đối với Backtracking thuần túy, miền giá trị của quận chưa gán là toàn bộ số màu
                    current_domains = {}
                    for r in self.neighbors:
                        if r in assignment:
                            current_domains[r] = [assignment[r]]
                        else:
                            current_domains[r] = list(range(1, n_cols + 1))
                else:
                    current_domains = copy.deepcopy(domains)
                    for r in assignment:
                        current_domains[r] = [assignment[r]]
                        
                self.steps.append({
                    'step_num': len(self.steps) + 1,
                    'region': region,
                    'color': color,
                    'action_type': action_type,
                    'assignment': assignment.copy(),
                    'domains': current_domains,
                    'num_colors': n_cols
                })
            return callback

        solution = None
        final_colors_used = 0
        
        # Vòng lặp giải thuật
        if is_auto:
            # Ghi nhận trạng thái khởi động đầu tiên
            self.steps.append({
                'step_num': 0,
                'region': None,
                'color': None,
                'action_type': 'INITIAL',
                'assignment': {},
                'domains': {r: [1] for r in self.neighbors},
                'num_colors': 1
            })
            
            for c in colors_range:
                if c > 1:
                    # Ghi nhận chuyển giao số lượng màu
                    self.steps.append({
                        'step_num': len(self.steps),
                        'region': None,
                        'color': None,
                        'action_type': 'START_TRIAL',
                        'assignment': {},
                        'domains': {r: list(range(1, c + 1)) for r in self.neighbors},
                        'num_colors': c
                    })
                    
                if algo == "Backtracking":
                    sol = map_coloring_backtracking(self.neighbors, c, callback=make_callback(c))
                elif algo == "Forward Checking":
                    sol = forward_checking_coloring(self.neighbors, c, callback=make_callback(c))
                elif algo == "AC3":
                    sol = ac3_checking_coloring(self.neighbors, c, callback=make_callback(c))
                elif algo == "Min_conflicts":
                    sol = min_conflicts_coloring(self.neighbors, c, callback=make_callback(c)) 
                
                if sol is not None:
                    solution = sol
                    final_colors_used = c
                    break
        else:
            c = colors_range[0]
            # Trạng thái khởi tạo
            self.steps.append({
                'step_num': 0,
                'region': None,
                'color': None,
                'action_type': 'INITIAL',
                'assignment': {},
                'domains': {r: list(range(1, c + 1)) for r in self.neighbors},
                'num_colors': c
            })
            
            if algo == "Backtracking":
                sol = map_coloring_backtracking(self.neighbors, c, callback=make_callback(c))
            elif algo == "Forward Checking":
                sol = forward_checking_coloring(self.neighbors, c, callback=make_callback(c))
            elif algo == "AC3":
                sol = ac3_checking_coloring(self.neighbors, c, callback=make_callback(c))
            elif algo == "Min_conflicts":
                sol = min_conflicts_coloring(self.neighbors, c, callback=make_callback(c))
            
            solution = sol
            if solution is not None:
                final_colors_used = c

        # Thêm bước báo cáo kết quả cuối cùng
        last_step = self.steps[-1]
        success = (solution is not None)
        self.steps.append({
            'step_num': len(self.steps),
            'region': None,
            'color': None,
            'action_type': 'SUCCESS' if success else 'FAILURE',
            'assignment': last_step['assignment'].copy(),
            'domains': last_step['domains'],
            'num_colors': final_colors_used if success else last_step['num_colors']
        })

        # Cấu hình thanh trượt
        self.step_scale.config(from_=0, to=len(self.steps) - 1)
        self.step_scale.set(0)
        self.current_step_idx = 0
        self.update_ui_to_step(0)
        
        # Hỏi người dùng xem có muốn chạy tự động luôn không
        if success:
            msg = f"Đã tìm thấy lời giải với {final_colors_used} màu ({len(self.steps)-2} bước trung gian).\nBấm 'Chạy tự động' để xem chi tiết."
            messagebox.showinfo("Tìm thấy lời giải", msg)
        else:
            msg = f"Không tìm thấy phương án hợp lệ sau {len(self.steps)-2} bước thử nghiệm."
            messagebox.showwarning("Không có lời giải", msg)

    def update_ui_to_step(self, idx):
        self.draw_graph()
        self.update_logs_and_table(idx)
        self.lbl_step_info.config(text=f"Bước: {idx} / {len(self.steps) - 1}")

    def draw_graph(self):
        self.canvas.delete("all")
        
        # 1. Vẽ các đường nối (Cạnh đồ thị)
        drawn_edges = set()
        for node, adjacent in self.neighbors.items():
            x1, y1 = self.node_positions[node]
            for adj in adjacent:
                edge_key = tuple(sorted([node, adj]))
                if edge_key not in drawn_edges:
                    x2, y2 = self.node_positions[adj]
                    self.canvas.create_line(x1, y1, x2, y2, fill="#bdc3c7", width=3)
                    drawn_edges.add(edge_key)
                    
        # 2. Xác định trạng thái của bước hiện tại để tô màu
        current_step = self.steps[self.current_step_idx] if (0 <= self.current_step_idx < len(self.steps)) else None
        current_assignment = current_step['assignment'] if current_step else {}
        current_region = current_step['region'] if current_step else None
        action_type = current_step['action_type'] if current_step else None
        
        # 3. Vẽ các nút (Quận)
        radius = 35
        for node, (x, y) in self.node_positions.items():
            color_id = current_assignment.get(node)
            if color_id in COLOR_INFO:
                fill_color = COLOR_INFO[color_id]["hex"]
                text_color = COLOR_INFO[color_id]["text"]
            else:
                fill_color = "#ffffff"
                text_color = "#2c3e50"
                
            # Đánh dấu nút đang hoạt động
            is_active = (node == current_region)
            if is_active:
                if action_type == "FAIL_FC":
                    outline_color = "#e74c3c"  # Màu đỏ nếu bước lọc Forward Checking thất bại
                    outline_width = 4
                else:
                    outline_color = "#e67e22"  # Màu cam nếu đang thử gán màu thông thường
                    outline_width = 4
            else:
                outline_color = "#2c3e50"
                outline_width = 2
                
            # Vẽ hình tròn của quận
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=fill_color, outline=outline_color, width=outline_width
            )
            
            # Vẽ văn bản hiển thị tên quận
            disp_name = DISPLAY_NAMES.get(node, node)
            self.canvas.create_text(
                x, y, text=disp_name, fill=text_color,
                font=("Arial", 9, "bold"), justify=tk.CENTER
            )
            
            # Vẽ thông tin miền giá trị ngay bên dưới mỗi nút
            if current_step and current_step.get('domains'):
                doms = current_step['domains'].get(node, [])
                if node in current_assignment:
                    dom_str = f"[{current_assignment[node]}]"
                else:
                    dom_str = str(doms)
                
                self.canvas.create_text(
                    x, y + radius + 15, text=f"D: {dom_str}",
                    fill="#34495e", font=("Courier", 9, "bold")
                )

    def update_logs_and_table(self, idx):
        # --- CẬP NHẬT NHẬT KÝ (LOGS) ---
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        
        for i in range(idx + 1):
            step = self.steps[i]
            step_num = step.get('step_num', i)
            action_type = step['action_type']
            region = step['region']
            color = step['color']
            num_cols = step['num_colors']
            
            color_name = COLOR_INFO.get(color, {}).get("name", f"Màu {color}") if color else ""
            
            if action_type == 'INITIAL':
                log_msg = f"[BƯỚC {step_num}] Khởi tạo: Số màu tối đa = {num_cols}.\n"
            elif action_type == 'START_TRIAL':
                log_msg = f"\n--- Thử nghiệm tiếp tục với tối đa {num_cols} màu ---\n"
            elif action_type == 'ASSIGN':
                log_msg = f"[BƯỚC {step_num}] Gán: {region} = {color_name} (Màu {color})\n"
            elif action_type == 'FAIL_FC':
                log_msg = f"[BƯỚC {step_num}] Thử gán: {region} = {color_name} -> THẤT BẠI (Miền giá trị lân cận bị rỗng!)\n"
            elif action_type == 'BACKTRACK':
                log_msg = f"[BƯỚC {step_num}] Quay lui: Hủy gán màu cho {region}\n"
            elif action_type == 'SUCCESS':
                log_msg = f"\n>>> THÀNH CÔNG: Đã tô màu xong với tối đa {num_cols} màu!\n"
            elif action_type == 'FAILURE':
                log_msg = f"\n>>> THẤT BẠI: Không tìm thấy phương án hợp lệ!\n"
            else:
                log_msg = f"[BƯỚC {step_num}] Sự kiện khác.\n"
                
            self.log_text.insert(tk.END, log_msg)
            
        # Đánh dấu và highlight dòng cuối cùng đang hoạt động
        self.log_text.tag_remove("current_line", "1.0", tk.END)
        last_line_start = self.log_text.index("end-2c linestart")
        last_line_end = self.log_text.index("end-2c lineend")
        self.log_text.tag_add("current_line", last_line_start, last_line_end)
        self.log_text.tag_config("current_line", background="#ffeaa7", foreground="#d35400", font=("Courier New", 9, "bold"))
        
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
        # --- CẬP NHẬT BẢNG MIỀN GIÁ TRỊ (DOMAINS TABLE) ---
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        current_step = self.steps[idx]
        assignment = current_step['assignment']
        domains = current_step.get('domains', {})
        
        for node in self.neighbors.keys():
            assigned_val = assignment.get(node)
            if assigned_val is not None:
                color_name = COLOR_INFO.get(assigned_val, {}).get("name", f"Màu {assigned_val}")
                assign_str = f"Màu {assigned_val} ({color_name})"
                dom_list = [assigned_val]
            else:
                assign_str = "Chưa gán"
                dom_list = domains.get(node, [])
                
            dom_str = ", ".join(str(c) for c in dom_list)
            dom_display = f"{{{dom_str}}}"
            
            self.tree.insert("", tk.END, values=(node, assign_str, dom_display))

if __name__ == "__main__":
    root = tk.Tk()
    app = MapColoringApp(root)
    root.mainloop()
