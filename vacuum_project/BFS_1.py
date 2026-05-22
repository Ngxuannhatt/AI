from collections import deque
from node import Node
def bfs_1(self):
        root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
        frontier = deque([root_node])
        reached = set()
        
        steps_limit = 0

        while frontier:
            curr = frontier.popleft()
            steps_limit += 1
            
            # 1. KIỂM TRA ĐÍCH MUỘN (Late Test)
            if curr.is_goal():
                # Xây dựng đường đi (Path)
                path = []
                temp = curr
                while temp is not None:
                    path.append(temp)
                    temp = temp.parent
                path.reverse() # Trả về từ Start -> Goal
                return path
            
            # 2. KIỂM TRA TRÙNG LẶP & ĐƯA VÀO REACHED
            state_key = curr.get_state_key()
            if state_key in reached:
                continue
            reached.add(state_key)

            r, c = curr.x, curr.y
            
            # Lập kế hoạch sinh Node con:
            # Hành động HÚT (nếu chỗ đó đang dơ)
            if curr.matrix[r][c] == 1:
                new_mat = [row[:] for row in curr.matrix]
                new_mat[r][c] = 0
                frontier.append(Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})"))
            
            # Hành động DI CHUYỂN
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.n and 0 <= nc < self.n:
                    frontier.append(Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})"))
            
            # Chống treo máy nếu chạy quá lâu
            if steps_limit > 5000000:
                print("Quá thời hạn xử lý đồ thị.")
                return None
                
        return None