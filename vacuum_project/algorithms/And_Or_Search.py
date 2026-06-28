import random
from node import Node

def and_or_graph_search(self):
    """
    Hàm khởi chạy thuật toán AND-OR Graph Search
    """
    initial_state = Node(
        self.agent_x, 
        self.agent_y, 
        self.matrix, 
        parent=None, 
        action=f"Bắt đầu tại ({self.agent_x},{self.agent_y})"
    )
    
    # 1. Tìm cây kế hoạch phân nhánh
    # Trước tiên thử tìm kế hoạch có tính đến trượt chân (non-deterministic)
    memo = {}
    plan, _ = or_search(self, initial_state, [], memo, allow_slipping=True)
    actual_slipping = True
    
    if plan == "failure":
        # Nếu không có kế hoạch bảo đảm (do trượt chân tạo chu trình vô tận),
        # thử tìm kế hoạch dưới mô hình không trượt chân (deterministic fallback)
        memo = {}
        plan, _ = or_search(self, initial_state, [], memo, allow_slipping=False)
        actual_slipping = False
        
    if plan == "failure":
        return None
        
    # 2. CHUYỂN ĐỔI CÂY KẾ HOẠCH THÀNH ĐƯỜNG ĐI TUYẾN TÍNH ĐỂ CHẠY ĐƯỢC TRÊN UI
    linear_path = []
    curr_node = initial_state
    linear_path.append(curr_node)
    
    curr_plan = plan
    steps_limit = 0
    
    while curr_plan and curr_plan != "failure" and steps_limit < 50:
        steps_limit += 1
        action, next_contingencies = curr_plan
        
        # Lấy danh sách các kết quả có thể xảy ra từ Node hiện tại
        possible_results = _get_results(self, curr_node, action, allow_slipping=actual_slipping)
        if not possible_results:
            break
            
        # Chọn ngẫu nhiên 1 trạng thái thực tế xảy ra
        chosen_node = random.choice(possible_results)
        chosen_node.parent = curr_node
        
        action_type, details = action
        action_desc = f"Định đi {details}" if action_type == "DI_CHUYEN" else "Hút rác"
        chosen_node.action = f"{action_desc} -> Thực tế tới ({chosen_node.x},{chosen_node.y})"
        
        linear_path.append(chosen_node)
        curr_node = chosen_node
        
        if curr_node.is_goal():
            break
            
        # Tìm kế hoạch ứng phó tiếp theo dựa trên trạng thái thực tế vừa rơi vào
        state_key = curr_node.get_state_key()
        if isinstance(next_contingencies, dict) and state_key in next_contingencies:
            curr_plan = next_contingencies[state_key]
        else:
            if isinstance(next_contingencies, dict) and next_contingencies:
                curr_plan = list(next_contingencies.values())[0]
            else:
                break
                
    return linear_path


def _get_actions(self, state):
    r, c = state.x, state.y
    # Nếu ô hiện tại dơ, CHỈ thực hiện hút rác để tối ưu không gian tìm kiếm
    if state.matrix[r][c] == 1:
        return [("HUT_RAC", None)]
        
    actions = []
    # Chỉ di chuyển khi vị trí hiện tại đã sạch
    for direction in ["LÊN", "XUỐNG", "TRÁI", "PHẢI"]:
        actions.append(("DI_CHUYEN", direction))
        
    return actions


def _get_results(self, state, action, allow_slipping=True):
    """
    Hàm sinh các trạng thái kết quả được tinh chỉnh để tối ưu không gian tìm kiếm
    """
    action_type, details = action
    results = []
    r, c = state.x, state.y
    
    if action_type == "DI_CHUYEN":
        direction = details
        move_map = {"LÊN": (-1, 0), "XUỐNG": (1, 0), "TRÁI": (0, -1), "PHẢI": (0, 1)}
        dr, dc = move_map[direction]
        target_r, target_c = r + dr, c + dc
        
        # 1. Kết quả mong muốn: Đi đúng hướng dự định
        if 0 <= target_r < self.n and 0 <= target_c < self.n:
            results.append(Node(target_r, target_c, state.matrix, parent=state, action=f"Di chuyển {direction}"))
        else:
            # Nếu đi đụng tường, giữ nguyên vị trí cũ (không bị mất trạng thái)
            results.append(Node(r, c, state.matrix, parent=state, action=f"Di chuyển {direction} (Đụng tường)"))
            
        # 2. Kết quả ngẫu nhiên (Trượt chân vuông góc): 
        if allow_slipping:
            if direction in ["LÊN", "XUỐNG"]:
                sides = [(0, -1), (0, 1)]  # Trượt sang Trái / Phải
            else:
                sides = [(-1, 0), (1, 0)]  # Trượt lên Trên / Xuống dưới
                
            for sr, sc in sides:
                side_r, side_c = r + sr, c + sc
                if 0 <= side_r < self.n and 0 <= side_c < self.n:
                    # Chỉ thêm vào nút AND nếu ô trượt này khác với ô mục tiêu ban đầu
                    if (side_r, side_c) != (target_r, target_c):
                        results.append(Node(side_r, side_c, state.matrix, parent=state, action=f"Trượt chân sang ({side_r},{side_c})"))

    elif action_type == "HUT_RAC":
        new_mat = [row[:] for row in state.matrix]
        new_mat[r][c] = 0
        results.append(Node(r, c, new_mat, parent=state, action="Hút rác"))
        
    # Loại bỏ các Node bị trùng tọa độ trong danh sách kết quả của nút AND
    unique_results = []
    seen_coords = set()
    for node in results:
        coord = (node.x, node.y, tuple(tuple(row) for row in node.matrix))
        if coord not in seen_coords:
            seen_coords.add(coord)
            unique_results.append(node)
            
    return unique_results


def or_search(self, state, path, memo, allow_slipping=True):
    if state.is_goal():
        return [], set()
    # Giới hạn chiều sâu lớn hơn để tìm được kế hoạch dài
    if len(path) > 100:
        return "failure", set()
        
    state_key = state.get_state_key()
    if state_key in path:
        return "failure", {state_key}
        
    # Tái sử dụng kết quả đã lưu trong Cache nếu an toàn với chu trình
    if state_key in memo:
        cached_plan, cached_hits = memo[state_key]
        if cached_hits.isdisjoint(path):
            return cached_plan, cached_hits
            
    accumulated_hits = set()
    
    for action in _get_actions(self, state):
        result_states = _get_results(self, state, action, allow_slipping)
        if not result_states:
            continue
            
        plan, and_hits = and_search(self, result_states, path + [state_key], memo, allow_slipping)
        accumulated_hits.update(and_hits)
        
        if plan != "failure":
            resolved_hits = accumulated_hits - {state_key}
            memo[state_key] = ([action, plan], resolved_hits)
            return [action, plan], resolved_hits
            
    resolved_hits = accumulated_hits - {state_key}
    memo[state_key] = ("failure", resolved_hits)
    return "failure", resolved_hits


def and_search(self, states, path, memo, allow_slipping=True):
    plans = {}
    accumulated_hits = set()
    for s in states:
        plan_s, or_hits = or_search(self, s, path, memo, allow_slipping)
        accumulated_hits.update(or_hits)
        if plan_s == "failure":
            return "failure", accumulated_hits
        plans[s.get_state_key()] = plan_s
    return plans, accumulated_hits