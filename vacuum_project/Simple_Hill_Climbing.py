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
            possible_moves.append(child) # Hill climbing không cần lưu cost riêng biệt
            
    # 2. Hành động Hút rác (Chỉ thực hiện khi ô hiện tại có rác)
    if curr.matrix[r][c] == 1:
        new_mat = [row[:] for row in curr.matrix]
        new_mat[r][c] = 0
        child = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
        possible_moves.append(child)
        
    return possible_moves

def Simple_Hill_Climbing(self):
    """
    Thuật toán Simple Hill Climbing tuân thủ chính xác theo ảnh bài giảng.
    """
    # 1. Current_State = Start
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    curr_node = root_node
    
    # Lưu lại đường đi thực tế để trả về cho UI vẽ hoạt ảnh
    path = [curr_node]
    
    # Giới hạn số vòng lặp tối đa để tránh trường hợp vòng lặp vô hạn ngoài ý muốn
    max_loops = 1000 
    loop_count = 0
    
    # 2. TRONG KHI (đúng):
    while loop_count < max_loops:
        loop_count += 1
        
        # Nếu Current_State == Goal (Không còn ô sai / rác nào nữa)
        if curr_node.is_goal() or get_misplaced_count(self, curr_node.matrix) == 0:
            # TRẢ VỀ Current_State (dưới dạng chuỗi đường đi từ Start đến đích)
            return path
            
        # Sinh các trạng thái lân cận của Current_State
        neighbors = get_vacuum_neighbors(self, curr_node)
        
        found_better = False
        curr_h = get_misplaced_count(self, curr_node.matrix)
        
        # Tìm thấy Next_State ĐẦU TIÊN có Value(Next_State) > Value(Current_State)
        # Tương đương với việc h(Next_State) < h(Current_State)
        for next_node in neighbors:
            next_h = get_misplaced_count(self, next_node.matrix)
            
            if next_h < curr_h:
                # Thiết lập mối quan hệ cha-con để phục vụ cấu trúc Node của bạn
                next_node.parent = curr_node 
                
                # Current_State = Next_State
                curr_node = next_node
                path.append(curr_node)
                
                # Đánh dấu đã tìm thấy và LẬP TỨC ngắt vòng lặp duyệt lân cận
                found_better = True
                break 
                
        # Nếu ĐÃ DUYỆT HẾT lân cận mà không có ai tốt hơn:
        if not found_better:
            # TRẢ VỀ Current_State (Dừng vì đạt cực đại cục bộ)
            return path

    return path