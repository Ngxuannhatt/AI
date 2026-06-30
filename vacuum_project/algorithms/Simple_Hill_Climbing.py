from node import Node

def get_heuristic(self, node):
    """
    h(n) = số ô còn rác + khoảng cách Manhattan tới đống rác gần nhất
    """
    dirt_positions = []
    n = len(node.matrix)

    for i in range(n):
        for j in range(n):
            if node.matrix[i][j] == 1:
                dirt_positions.append((i, j))

    # Goal
    if not dirt_positions:
        return 0

    # Tính khoảng cách Manhattan từ vị trí hiện tại của agent tới cục rác gần nhất
    nearest = min(
        abs(node.x - r) + abs(node.y - c)
        for r, c in dirt_positions
    )

    return len(dirt_positions) + nearest

def get_vacuum_neighbors(self, curr):
    """
    Hàm sinh các node con (trạng thái lân cận) từ node hiện tại.
    """
    possible_moves = []
    r, c = curr.x, curr.y
    n = len(curr.matrix)
    
    # 1. Hành động Di chuyển (Lên, Xuống, Trái, Phải)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            child = Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})")
            possible_moves.append(child)
            
    # 2. Hành động Hút rác (Chỉ thực hiện khi ô hiện tại có rác)
    if curr.matrix[r][c] == 1:
        new_mat = [row[:] for row in curr.matrix]
        new_mat[r][c] = 0
        child = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
        possible_moves.append(child)
        
    return possible_moves

def Simple_Hill_Climbing(self):
    """
    Thuật toán Simple Hill Climbing chuẩn hóa
    """
    # 1. Khởi tạo trạng thái bắt đầu
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    curr_node = root_node
    
    # Lưu lại đường đi thực tế
    path = [curr_node]
    
    max_loops = 1000 
    loop_count = 0
    
    # 2. Vòng lặp tìm kiếm
    while loop_count < max_loops:
        loop_count += 1
        
        # ĐIỀU KIỆN DỪNG 1: Đã sạch rác (Goal)
        # Sửa lỗi truyền tham số: truyền trực tiếp curr_node thay vì curr_node.matrix
        if curr_node.is_goal() or get_heuristic(self, curr_node) == 0:
            return path
            
        # Sinh các trạng thái lân cận
        # Sửa lỗi truyền tham số: truyền curr_node
        neighbors = get_vacuum_neighbors(self, curr_node)
        
        found_better = False
        curr_h = get_heuristic(self, curr_node)
        
        # Tìm trạng thái đầu tiên tốt hơn
        for next_node in neighbors:
            # Sửa lỗi truyền tham số: truyền next_node
            next_h = get_heuristic(self, next_node)
            
            if next_h < curr_h:
                next_node.parent = curr_node 
                curr_node = next_node
                path.append(curr_node)
                
                found_better = True
                break  # Ngắt ngay lập tức theo đúng tính chất Simple Hill Climbing
                
        # ĐIỀU KIỆN DỪNG 2: Kẹt ở cực đại cục bộ (Local Maximum / Flat Local Maximum)
        if not found_better:
            return path

    return path