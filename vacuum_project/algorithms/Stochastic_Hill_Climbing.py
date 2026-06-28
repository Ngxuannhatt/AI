import random # Cần import thêm thư viện random ở đầu file
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

def Stochastic_Hill_Climbing(self):
    """
    Biến thể Leo đồi ngẫu nhiên (Stochastic Hill Climbing):
    Tìm tất cả các node con tốt hơn và chọn ngẫu nhiên một node để đi.
    """
    # 1. Current_State = Start
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    curr_node = root_node
    
    # Lưu lại đường đi thực tế để trả về cho UI vẽ hoạt ảnh
    path = [curr_node]
    
    max_loops = 1000 
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
        
        # Tạo danh sách chứa tất cả các node con "tốt hơn" node hiện tại
        better_neighbors = []
        
        for next_node in neighbors:
            next_h = get_misplaced_count(self, next_node.matrix)
            
            # Nếu node con có số ô sai ít hơn node hiện tại -> Cho vào danh sách ứng viên
            if next_h < curr_h:
                better_neighbors.append(next_node)
                
        # Nếu tìm được ít nhất một ứng viên tốt hơn
        if better_neighbors:
            # CHỌN NGẪU NHIÊN một node trong danh sách ứng viên tốt hơn
            chosen_node = random.choice(better_neighbors)
            
            # Thiết lập quan hệ cha-con
            chosen_node.parent = curr_node
            
            # Current_State = Trạng thái ngẫu nhiên vừa chọn
            curr_node = chosen_node
            path.append(curr_node)
        else:
            # Nếu ĐÃ DUYỆT HẾT lân cận mà không có ai tốt hơn giá trị hiện tại:
            # TRẢ VỀ Current_State (Dừng vì đạt cực đại cục bộ)
            return path

    return path