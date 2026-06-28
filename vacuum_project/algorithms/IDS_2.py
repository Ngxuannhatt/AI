from collections import deque
from node import Node  # Điều chỉnh lại path import nếu cần

def ids_2(self):
    """
    Hàm chính của Iterative Deepening Search (IDS)
    """
    limit = 0
    while True:
        result, status = depth_limited_search(self,limit)
        
        if status == "SUCCESS":
            return result      # Tìm thấy đường đi thành công
        elif status == "FAIL":
            return None        # Thất bại hoàn toàn
        
        # Nếu status == "CUTOFF": Tăng độ sâu làm lại từ đầu
        limit += 1

def depth_limited_search(self, limit):
    """
    Hàm DLS phối hợp KIỂM TRA SỚM (Early Test)
    """
    root_node = Node(self.agent_x, self.agent_y, self.matrix, parent=None, action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})")
    root_node.depth = 0 
    
    # 1. KIỂM TRA SỚM CHO NODE GỐC
    if root_node.is_goal():
        return [root_node], "SUCCESS"
        
    frontier = [root_node]
    
    # Khởi tạo reached lưu độ sâu nhỏ nhất của node gốc
    reached_at_depth = {root_node.get_state_key(): 0} 
    
    cutoff_occurred = False
    steps_limit = 0

    while frontier:
        curr = frontier.pop()  # LIFO (DFS Stack)
        steps_limit += 1
        
        # KIỂM TRA GIỚI HẠN ĐỘ SÂU
        # Vì ta kiểm tra sớm, nếu cha đã ở tầng `limit`, các con sinh ra sẽ ở tầng `limit + 1` (vượt mức)
        # Nên ta không sinh con từ node cha này nữa.
        if curr.depth >= limit:
            cutoff_occurred = True
            continue  
            
        r, c = curr.x, curr.y
        temporary = []  # RESET danh sách node con ở mỗi vòng lặp mới!
        
        # --- A. SINH CÁC NODE CON ---
        
        # Hành động DI CHUYỂN
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                child_node = Node(nr, nc, curr.matrix, parent=curr, action=f"Đi tới ({nr},{nc})")
                child_node.depth = curr.depth + 1
                temporary.append(child_node)
                
        # Hành động HÚT (Được append sau để POP ra trước)
        if curr.matrix[r][c] == 1:
            new_mat = [row[:] for row in curr.matrix]
            new_mat[r][c] = 0
            child_node = Node(r, c, new_mat, parent=curr, action=f"Hút rác tại ({r},{c})")
            child_node.depth = curr.depth + 1
            temporary.append(child_node)
        
        # --- B. XỬ LÝ NODE CON (Vòng lặp này phải nằm NGOÀI lệnh if của Hút) ---
        for node in temporary:
            # 2. KIỂM TRA SỚM CHO NODE CON
            if node.is_goal():
                path = []
                temp = node
                while temp is not None:
                    path.append(temp)
                    temp = temp.parent
                path.reverse()
                return path, "SUCCESS"  # Trả về đủ 2 tham số (path, status)
            
            # 3. KIỂM TRA TRÙNG LẶP / CHU TRÌNH
            state_key = node.get_state_key()
            if state_key in reached_at_depth and reached_at_depth[state_key] <= node.depth:
                continue
            
            # Đạt điều kiện: Cập nhật độ sâu tối ưu và đẩy vào frontier
            reached_at_depth[state_key] = node.depth
            frontier.append(node)

        # Chống treo máy
        if steps_limit > 5000000:
            print("Quá thời hạn xử lý đồ thị.")
            return None, "FAIL"
            
    if cutoff_occurred:
        return None, "CUTOFF"
    else:
        return None, "FAIL"