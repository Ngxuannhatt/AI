# vacuum_astar.py
from node import Node

def get_misplaced_count(self, matrix):
    """Hàm h(n): Tính số ô còn rác trên ma trận hiện tại."""
    return sum(row.count(1) for row in self.matrix)

def get_vacuum_neighbors(self,curr):
    """
    Hàm sinh các node con (trạng thái kề m) từ node hiện tại n.
    Trả về danh sách tuple: (child_node, cost_n_m)
    Mỗi hành động (Di chuyển hoặc Hút rác) mặc định có chi phí là 1.
    """
    possible_moves = []
    r, c = curr.x, curr.y
    
    # 1. Hành động Di chuyển (Lên, Xuống, Trái, Phải)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.n and 0 <= nc < self.n:
            child = Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})")
            possible_moves.append((child, 1))
            
    # 2. Hành động Hút rác (Chỉ thực hiện khi ô hiện tại có rác)
    if curr.matrix[r][c] == 1:
        new_mat = [row[:] for row in curr.matrix]
        new_mat[r][c] = 0
        child = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
        possible_moves.append((child, 1))
        
    return possible_moves

def A_Star(self):
    """
    Thuật toán A* cho máy hút bụi tuân thủ chính xác theo bố cục ảnh bài giảng.
    """
    # Khởi tạo node gốc từ thông tin ban đầu
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    start_key = root_node.get_state_key()
    
    # 1. Khởi tạo tập FRONTIER = {Start} với f(Start) = g(Start) + h(Start) = 0 + h(Start)
    # Cấu trúc lưu: FRONTIER = { state_key: f_value }
    h_start = get_misplaced_count(self,root_node.matrix)
    FRONTIER = {start_key: 0 + h_start}
    
    # Các từ điển phụ trợ theo dõi chi phí thực tế g và đối tượng Node cụ thể
    g_dict = {start_key: 0}
    node_registry = {start_key: root_node}
    
    # 2. Khởi tạo tập REACHED = {}
    # Cấu trúc lưu: REACHED = { state_key: g_value }
    REACHED = {}
    
    steps_limit = 0

    # 3. TRONG KHI (FRONTIER không rỗng):
    while FRONTIER:
        # Tối ưu tránh treo UI nếu không gian trạng thái quá lớn
        steps_limit += 1
        if steps_limit > 50000:
            return None
            
        # a. Chọn trạng thái n từ FRONTIER có giá trị f(n) nhỏ nhất
        n_key = min(FRONTIER, key=FRONTIER.get)
        curr_node = node_registry[n_key]
        
        # b. NẾU n == Goal: TRẢ VỀ "Thành công" và truy xuất lại đường đi từ Start đến n.
        # Điều kiện Đích: Hoàn toàn sạch rác (h_val == 0)
        if curr_node.is_goal() or get_misplaced_count(self,curr_node.matrix) == 0:
            path = []
            temp = curr_node
            while temp is not None:
                path.append(temp)
                temp = temp.parent
            path.reverse()
            return path
        
        # c. Loại bỏ n khỏi FRONTIER và thêm n vào REACHED
        del FRONTIER[n_key]
        REACHED[n_key] = g_dict[n_key]
        
        # d. Với mỗi trạng thái m kề với n:
        for child, cost_n_m in get_vacuum_neighbors(self,curr_node):
            m_key = child.get_state_key()
            
            # i. Tính toán chi phí thực tế mới:
            g_new_m = g_dict[n_key] + cost_n_m
            
            # ii. NẾU m đã nằm trong REACHED:
            if m_key in REACHED:
                # NẾU g_new(m) >= g(m) hiện tại: Bỏ qua trạng thái m (tệ hơn).
                if g_new_m >= REACHED[m_key]:
                    continue
                # NGƯỢC LẠI: Xóa m khỏi REACHED và cập nhật lại g(m) = g_new(m)
                else:
                    del REACHED[m_key]
                    g_dict[m_key] = g_new_m
                    node_registry[m_key] = child
                    # Tiếp tục rơi xuống nhánh xử lý để đưa lại m vào FRONTIER

            # iii. NẾU m đã nằm trong FRONTIER:
            elif m_key in FRONTIER:
                # NẾU g_new(m) < g(m) hiện tại:
                if g_new_m < g_dict[m_key]:
                    # Cập nhật lại g(m) = g_new(m) và f(m) = g(m) + h(m)
                    g_dict[m_key] = g_new_m
                    h_m = get_misplaced_count(self,child.matrix)
                    FRONTIER[m_key] = g_new_m + h_m
                    # Cập nhật lại đỉnh cha của m là n
                    child.parent = curr_node
                    node_registry[m_key] = child
                    
            # iv. NẾU m chưa có mặt trong FRONTIER và REACHED:
            else:
                # Gán g(m) = g_new(m). Tính f(m) = g(m) + h(m)
                g_dict[m_key] = g_new_m
                h_m = get_misplaced_count(self,child.matrix)
                FRONTIER[m_key] = g_new_m + h_m
                # Gán đỉnh cha của m là n. Thêm m vào FRONTIER.
                child.parent = curr_node
                node_registry[m_key] = child

    # 4. TRẢ VỀ "Thất bại"
    return None