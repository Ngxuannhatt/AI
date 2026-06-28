from node import Node

def get_misplaced_count(self, matrix):
    """Hàm h(n): Tính số ô còn rác trên ma trận hiện tại."""
    return sum(row.count(1) for row in matrix)

def get_vacuum_neighbors(self, curr):
    """
    Hàm sinh các node con (trạng thái lân cận) từ node hiện tại.
    """
    possible_moves = []
    r, c = curr.x, curr.y
    
    # 1. Hành động Di chuyển (Lên, Xuống, Trái, Phải)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.n and 0 <= nc < self.n:
            child = Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})")
            possible_moves.append(child)
            
    # 2. Hành động Hút rác (Chỉ thực hiện khi ô hiện tại có rác)
    if curr.matrix[r][c] == 1:
        new_mat = [row[:] for row in curr.matrix]
        new_mat[r][c] = 0
        child = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
        possible_moves.append(child)
        
    return possible_moves

def Steepest_Ascent_Hill_Climbing(self):
    """
    Biến thể Leo đồi dốc nhất (Steepest-Ascent Hill Climbing):
    Liệt kê tất cả các node con và chọn node có h(n) nhỏ nhất.
    """
    # 1. Current_State = Start
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    curr_node = root_node
    
    # Lưu lại đường đi thực tế để trả về cho UI vẽ hoạt ảnh
    path = [curr_node]
    
    max_loops = 50000
    loop_count = 0
    
    # 2. TRONG KHI (đúng):
    while loop_count < max_loops:
        loop_count += 1
        
        # Nếu Current_State == Goal (Không còn ô sai / rác nào nữa)
        if curr_node.is_goal() or get_misplaced_count(self, curr_node.matrix) == 0:
            return path
            
        # Sinh các trạng thái lân cận của Current_State
        neighbors = get_vacuum_neighbors(self, curr_node)
        
        curr_h = get_misplaced_count(self, curr_node.matrix)
        
        best_node = None
        min_h = curr_h # Ban đầu đặt mốc tối ưu là giá trị hiện tại
        
        # DUYỆT HẾT tất cả các lân cận để tìm ra trạng thái có h(n) nhỏ nhất
        for next_node in neighbors:
            next_h = get_misplaced_count(self, next_node.matrix)
            
            # Nếu tìm thấy một node có h(n) nhỏ hơn mức min_h hiện tại
            if next_h < min_h:
                min_h = next_h
                best_node = next_node
                
        # Sau khi đã duyệt hết lân cận, kiểm tra xem có tìm được ai tốt hơn không
        if best_node is not None:
            # Thiết lập quan hệ cha-con
            best_node.parent = curr_node
            
            # Current_State = Next_State (Node tốt nhất vừa tìm được)
            curr_node = best_node
            path.append(curr_node)
        else:
            # Nếu ĐÃ DUYỆT HẾT lân cận mà không có ai tốt hơn giá trị hiện tại:
            # TRẢ VỀ Current_State (Dừng vì đạt cực đại cục bộ)
            return path

    return path