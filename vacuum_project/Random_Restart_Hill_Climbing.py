import random
from node import Node

def get_misplaced_count(self, matrix):
    """Hàm h(n): Tính số ô còn rác trên ma trận hiện tại."""
    return sum(row.count(1) for row in matrix)

def get_vacuum_neighbors(self, curr):
    """Hàm sinh các node con (trạng thái lân cận) từ node hiện tại."""
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

def generate_random_state(self):
    """
    Hàm bổ trợ để tạo một trạng thái ngẫu nhiên (Khởi tạo lại vị trí robot).
    Giữ nguyên ma trận hiện tại (hoặc cấu hình rác tùy theo logic bài toán của bạn).
    """
    # Ngẫu nhiên vị trí mới cho robot trong không gian ma trận n x n
    rand_x = random.randint(0, self.n - 1)
    rand_y = random.randint(0, self.n - 1)
    
    # Tạo node xuất phát ngẫu nhiên
    return Node(rand_x, rand_y, self.matrix, parent=None, action=f"Khởi tạo lại tại ({rand_x},{rand_y})")


def Random_Restart_Hill_Climbing(self, MAX_RESTART=20):
    """
    Thuật toán Random Restart Hill Climbing tuân thủ chính xác theo ảnh bài giảng.
    """
    # Để UI có thể vẽ toàn bộ hành trình qua các lượt restart, 
    # chúng ta dùng một danh sách tổng để lưu vết.
    total_path = []
    
    # 1. Khởi tạo: MAX_RESTART được truyền qua tham số (mặc định là 10)
    
    # 2. CHO i = 1 đến MAX_RESTART:
    for i in range(1, MAX_RESTART + 1):
        
        # Current_State = Start 
        # (Lần đầu tiên dùng vị trí ban đầu của agent, các lần sau restart ngẫu nhiên)
        if i == 1:
            curr_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
        else:
            curr_node = generate_random_state(self)
            
        total_path.append(curr_node)
        
        # TRONG KHI (đúng):
        while True:
            # NẾU Current_State == Goal (Số ô rác bằng 0)
            if curr_node.is_goal() or get_misplaced_count(self, curr_node.matrix) == 0:
                # TRẢ VỀ Current_State (Đường đi thành công)
                return total_path
            
            # Sinh tất cả các trạng thái lân cận của Current_State
            neighbors = get_vacuum_neighbors(self, curr_node)
            curr_h = get_misplaced_count(self, curr_node.matrix)
            
            # Lọc ra tập Better_Neighbors = {Neighbor | Value(Neighbor) tốt hơn Value(Current_State)}
            # Ở đây tốt hơn nghĩa là số rác ít hơn (next_h < curr_h)
            better_neighbors = []
            for next_node in neighbors:
                next_h = get_misplaced_count(self, next_node.matrix)
                if next_h < curr_h:
                    better_neighbors.append(next_node)
            
            # NẾU Better_Neighbors RỖNG:
            if not better_neighbors:
                # Thoát vòng lặp TRONG KHI // Lượt này bị kẹt, nhảy sang lượt i tiếp theo
                break
                
            # NGƯỢC LẠI:
            else:
                # Next_State = Chọn trạng thái tốt nhất từ tập Better_Neighbors
                # (Tìm node có số rác h(n) nhỏ nhất trong tập better)
                next_state = min(better_neighbors, key=lambda node: get_misplaced_count(self, node.matrix))
                
                # Cập nhật liên kết cha-con
                next_state.parent = curr_node
                
                # Current_State = Next_State
                curr_node = next_state
                total_path.append(curr_node)
                
    # 3. TRẢ VỀ "Thất bại" // Chạy hết sạch MAX_RESTART lượt mà không chạm được Goal
    # Ở đây trả về chuỗi danh sách đường đi đã đi kèm thông báo hoặc trả về total_path rỗng tùy bạn.
    # Để an toàn cho UI không bị lỗi vẽ, ta vẫn trả về hành trình đã thử nghiệm của các lượt.
    print("Thất bại: Đã thử hết số lượt restart nhưng không tìm thấy Goal.")
    return total_path