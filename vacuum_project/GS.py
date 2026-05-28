import heapq
from node import Node

def gs(self): 
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")

    initial_h = get_manhattan_count(self,root_node.x, root_node.y,root_node.matrix)
    
    # Priority Queue lưu: (h_value, counter, node)
    frontier = []
    counter = 0
    heapq.heappush(frontier, (initial_h, counter, root_node))
     
    reached = set()
    steps_limit = 0

    while frontier:
        curr_h, _, curr = heapq.heappop(frontier)
        
        # Kiểm tra trùng lặp sau khi POP
        state_key = curr.get_state_key()
        if state_key in reached:
            continue
        reached.add(state_key)
        
        # Kiểm tra đích
        if curr.is_goal():
            path = []
            temp = curr
            while temp is not None:
                path.append(temp)
                temp = temp.parent
            path.reverse()
            return path
            
        steps_limit += 1
        if steps_limit > 500000: # Giảm giới hạn để tránh treo UI
            return None

        # Sinh node con
        r, c = curr.x, curr.y
        possible_moves = []
        
        # 1. Di chuyển
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                possible_moves.append(Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})"))
                
        # 2. Hút rác
        if curr.matrix[r][c] == 1:
            new_mat = [row[:] for row in curr.matrix]
            new_mat[r][c] = 0
            possible_moves.append(Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})"))
    
        # Push tất cả vào Heap
        for child in possible_moves:
            if child.get_state_key() not in reached:
                counter += 1
                h_val = get_manhattan_count(self,child.x, child.y, child.matrix)
                heapq.heappush(frontier, (h_val, counter, child))
    return None

def get_manhattan_count(self, agent_x, agent_y, matrix):
    min_distance = float('inf')
    has_dirt = False
    
    # Duyệt toàn bộ ma trận để tìm các ô có rác (giá trị = 1)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                has_dirt = True
                # Tính khoảng cách Manhattan từ robot tới ô rác này
                distance = abs(agent_x - i) + abs(agent_y - j)
                if distance < min_distance:
                    min_distance = distance
                    
    # Nếu bản đồ còn rác, trả về khoảng cách ngắn nhất; nếu hết rác trả về 0
    return min_distance if has_dirt else 0
            
