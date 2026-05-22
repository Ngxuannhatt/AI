import heapq
from node import Node
def ucs(self):
    def get_misplaced_count(matrix):
        misplaced = 0
        for r in range(self.n):
            for c in range(self.n):
                if matrix[r][c] != 0:  # Đích là ma trận sạch rác (toàn số 0)
                    misplaced += 1
        return misplaced
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    
    # 1. KIỂM TRA ĐÍCH SỚM
    if root_node.is_goal():
        return [root_node]
        
    # Tính số lượng sai vị trí ban đầu của node gốc
    initial_h = self.count_misplaced_tiles(root_node.matrix)
    frontier = []
    counter = 0
    heapq.heappush(frontier, (initial_h, counter, root_node))
    
    # Tập đạt được để tránh lặp (đối với Best-First Search ta dùng set bình thường như BFS)
    reached = set()
    reached.add(root_node.get_state_key())
    
    steps_limit = 0

    while frontier:
        # Lấy node có giá trị h (sai vị trí) NHỎ NHẤT ra trước
        curr_h, _, curr = heapq.heappop(frontier)
        steps_limit += 1
        
        # Vì ta đã kiểm tra sớm lúc sinh con, curr lấy ra chắc chắn không phải là đích
        # (Trừ trường hợp node gốc, nhưng đã check ở trên)

        r, c = curr.x, curr.y
        temporary = []
        
        # --- SINH CÁC NODE CON ---
        # Hành động DI CHUYỂN
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                child_node = Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})")
                temporary.append(child_node)
                
        # Hành động HÚT
        if curr.matrix[r][c] == 1:
            new_mat = [row[:] for row in curr.matrix]
            new_mat[r][c] = 0
            child_node = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
            temporary.append(child_node)
            
        # --- KIỂM TRA VÀ ĐẨY VÀO PRIORITY QUEUE ---
        for node in temporary:
            # Kiểm tra đích sớm
            if node.is_goal():
                path = []
                temp = node
                while temp is not None:
                    path.append(temp)
                    temp = temp.parent
                path.reverse()
                return path
                
            state_key = node.get_state_key()
            if state_key not in reached:
                reached.add(state_key)
                
                # TÍNH HÀM HEURISTIC: Đếm số ô sai vị trí của node con này
                h_value = get_misplaced_count(node.matrix)
                
                # Đẩy vào heap kèm theo độ ưu tiên là h_value
                counter += 1
                heapq.heappush(frontier, (h_value, counter, node))
                
        if steps_limit > 100000:
            print("Quá giới hạn xử lý.")
            return None
            
    return None

