import math
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


def SimulatedAnnealing(self, T0=100, Tmin=0.01, alpha=0.95):
    """
    Thuật toán Simulated Annealing tuân thủ chính xác theo ảnh bài giảng.
    """
    # Để UI có thể vẽ toàn bộ hành trình, dùng một danh sách lưu vết các node đã đi qua
    total_path = []
    
    # current state = start
    curr_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    total_path.append(curr_node)
    
    # T = T0
    T = T0
    
    # while T > Tmin:
    while T > Tmin:
        # if current state == goal: return current state
        if curr_node.is_goal() or get_misplaced_count(self, curr_node.matrix) == 0:
            return total_path
            
        # Sinh các trạng thái lân cận và chọn ngẫu nhiên một trạng thái
        neighbors = get_vacuum_neighbors(self, curr_node)
        if not neighbors:
            # Nếu không có trạng thái lân cận nào (ngõ cụt), thoát vòng lặp
            break
            
        # next state = RandomNeighbor(current state)
        next_node = random.choice(neighbors)
        
        # Δ = h(next state) - h(current state)
        curr_h = get_misplaced_count(self, curr_node.matrix)
        next_h = get_misplaced_count(self, next_node.matrix)
        delta = next_h - curr_h
        
        # if Δ < 0:
        if delta < 0:
            # current state = next state
            next_node.parent = curr_node
            curr_node = next_node
            total_path.append(curr_node)
        # else:
        else:
            # p = exp(-Δ / T)
            # Tránh lỗi chia cho 0 nếu T bằng 0 (dù điều kiện vòng lặp T > Tmin > 0 đã chặn)
            p = math.exp(-delta / T) if T != 0 else 0
            
            # if Random(0,1) < p:
            if random.uniform(0, 1) < p:
                # current state = next state
                next_node.parent = curr_node
                curr_node = next_node
                total_path.append(curr_node)
        
        # T = α * T
        T = alpha * T

    # return current state (Trả về trạng thái hiện tại kèm toàn bộ lịch sử để vẽ UI)
    print("Vòng lặp kết thúc (Nhiệt độ giảm quá Tmin hoặc bị kẹt). Trả về trạng thái cuối cùng đạt được.")
    return total_path