from collections import deque
from node import Node

def ids_2(self):
    """
    Hàm chính của Iterative Deepening Search (IDS)
    Tăng giới hạn độ sâu (limit) từ 0 cho đến khi tìm thấy đích hoặc thất bại hoàn toàn.
    """
    limit = 0
    while True:
        # Gọi hàm tìm kiếm giới hạn độ sâu với giới hạn tầng hiện tại
        result, status = self.depth_limited_search(limit)
        
        if status == "SUCCESS":
            return result      # Tìm thấy đường đi thành công
        elif status == "FAIL":
            return None        # Đã duyệt hết toàn bộ không gian trạng thái mà không có đích
        
        # Nếu status == "CUTOFF": Tức là chạm giới hạn độ sâu mà chưa có đích -> Tăng độ sâu làm lại từ đầu
        limit += 1

def depth_limited_search(self, limit):
    """
    Hàm tìm kiếm theo chiều sâu giới hạn (DLS) với cơ chế Late Test
    """
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    if root_node.is_goal():
        return [root_node],"SUCCESS"  
    frontier = [root_node]
    root_node.depth = 0 
    reached_at_depth = {root_node.get_state_key(): 0} 
    temporary = []
    cutoff_occurred = False
    steps_limit = 0

    while frontier:
        curr = frontier.pop()  # LẤY RA TỪ CUỐI STACK (DFS)
        steps_limit += 1
    
        
        # KIỂM TRA GIỚI HẠN ĐỘ SÂU
        # Nếu node hiện tại đã chạm giới hạn tầng, không sinh con của nó nữa và đánh dấu cutoff
        if curr.depth >= limit:
            cutoff_occurred = True
            continue  # Bỏ qua không phát triển node con, chuyển sang node khác trong frontier
            
        

        r, c = curr.x, curr.y
        
        # --- SINH CÁC NODE CON ---
        # Lưu ý: Khi tạo node con, gán độ sâu của con = độ sâu cha + 1
        
        # Hành động DI CHUYỂN (Thêm vào Stack)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                child_node = Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})")
                child_node.depth = curr.depth + 1 # Cập nhật độ sâu node con
                temporary.append(child_node)
                
        # Hành động HÚT (Thêm vào Stack sau để được ưu tiên POP ra trước)
        if curr.matrix[r][c] == 1:
            new_mat = [row[:] for row in curr.matrix]
            new_mat[r][c] = 0
            child_node = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
            child_node.depth = curr.depth + 1 # Cập nhật độ sâu node con
            temporary.append(child_node)
             
        for node in temporary:
            if node.is_goal():
                path = []
                temp = node
                while temp is not None:
                    path.append(temp)
                    temp = temp.parent
                path.reverse()
                return path, "SUCCESS"
            # 3. KIỂM TRA TRÙNG LẶP VÀ CHU TRÌNH
            state_key = node.get_state_key()
            if state_key in reached_at_depth and reached_at_depth[state_key] <= node.depth:
                continue
            reached_at_depth[state_key] = node.depth
            frontier.append(node)
        # Chống treo máy nếu vòng lặp quá lớn
        if steps_limit > 5000000:
            print("Quá thời hạn xử lý đồ thị.")
            return None, "FAIL"
            
    # Hết vòng lặp frontier mà chưa return SUCCESS:
    if cutoff_occurred:
        return None, "CUTOFF" # Chạm giới hạn độ sâu -> Ra ngoài tăng tầng
    else:
        return None, "FAIL"   # Duyệt sạch bản đồ rồi mà không có đích thực sự