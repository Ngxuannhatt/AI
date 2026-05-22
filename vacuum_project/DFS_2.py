from collections import deque
from node import Node
def dfs_2(self):
        root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
        if root_node.is_goal():
            return [root_node]
        frontier = deque([root_node])
        reached = set()
        reached.add(root_node.get_state_key())
        steps_limit = 0

        while frontier:
            curr = frontier.pop()
            steps_limit += 1
         

            r, c = curr.x, curr.y
            temporary=[]
            # Lập kế hoạch sinh Node con:
        
            # Hành động DI CHUYỂN
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.n and 0 <= nc < self.n:
                    temporary.append(Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})"))

            if curr.matrix[r][c] == 1:
                new_mat = [row[:] for row in curr.matrix]
                new_mat[r][c] = 0
                temporary.append(Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})"))
 
            
            for node in temporary:
                if node.is_goal():
                    path = []
                    temp = node
                    while temp is not None:
                        path.append(temp)
                        temp = temp.parent
                    path.reverse()
                    return path
                
                # KIỂM TRA TRÙNG LẶP & ĐƯA VÀO REACHED/FRONTIER
                state_key = node.get_state_key()
                if state_key not in reached:
                    reached.add(state_key)
                    frontier.append(node)      
            # Chống treo máy nếu chạy quá lâu
            if steps_limit > 5000000:
                print("Quá thời hạn xử lý đồ thị.")
                return None
        return None
