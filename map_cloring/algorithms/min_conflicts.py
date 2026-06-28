import random
import copy

def min_conflicts_coloring(neighbors, num_colors, max_steps=100, callback=None):
    """
    Giải bài toán tô màu bản đồ bằng thuật toán Min-Conflicts (Local Search).
    
    :param neighbors: Đồ thị kề dạng dict { node: [list_of_neighbors] }
    :param num_colors: Số lượng màu tối đa được phép dùng
    :param max_steps: Số bước tối đa để sửa đổi trước khi bỏ cuộc (tránh vòng lặp vô tận)
    :param callback: Hàm lưu lại trạng thái từng bước để hiển thị lên UI
    :return: Lời giải dạng dict { node: color_id } hoặc None nếu thất bại
    """
    # BƯỚC 1: Khởi tạo trạng thái ban đầu - Gán NGẪU NHIÊN màu cho tất cả các quận
    assignment = {}
    for region in neighbors:
        assignment[region] = random.randint(1, num_colors)
        
    # Tạo biến domains giả lập để UI hiển thị (mỗi quận đã gán thì hiển thị màu đó)
    def get_current_domains(current_assign):
        return {r: [current_assign[r]] for r in neighbors}

    # Gọi callback cho trạng thái khởi tạo ngẫu nhiên ban đầu
    if callback:
        callback(None, None, 'INITIAL', assignment.copy(), get_current_domains(assignment))

    # BƯỚC 2: Vòng lặp sửa đổi các quận bị xung đột
    for step in range(max_steps):
        # Tìm danh sách các quận đang bị xung đột (trùng màu với hàng xóm)
        conflicted_regions = []
        for region in neighbors:
            if count_conflicts(region, assignment[region], assignment, neighbors) > 0:
                conflicted_regions.append(region)
                
        # Nếu không còn quận nào bị xung đột -> Đã tìm thấy lời giải hợp lệ!
        if not conflicted_regions:
            return assignment

        # Chọn ngẫu nhiên một quận đang bị xung đột để tiến hành sửa đổi
        region_to_fix = random.choice(conflicted_regions)

        # Tìm màu tối ưu nhất cho quận này (màu sinh ra ít xung đột nhất)
        min_conflicts_count = float('inf')
        best_colors = []

        for color in range(1, num_colors + 1):
            conflicts = count_conflicts(region_to_fix, color, assignment, neighbors)
            if conflicts < min_conflicts_count:
                min_conflicts_count = conflicts
                best_colors = [color]
            elif conflicts == min_conflicts_count:
                best_colors.append(color)

        # Nếu có nhiều màu tốt ngang nhau, chọn ngẫu nhiên một màu
        chosen_color = random.choice(best_colors)
        
        # Tiến hành cập nhật màu mới cho quận
        assignment[region_to_fix] = chosen_color

        # Gọi callback cập nhật sự kiện "ASSIGN" lên giao diện để vẽ lại đồ thị
        if callback:
            # Gửi sự kiện ASSIGN thông thường
            callback(region_to_fix, chosen_color, 'ASSIGN', assignment.copy(), get_current_domains(assignment))

    # Nếu hết số bước max_steps mà vẫn chưa sửa hết xung đột -> Thất bại
    return None

def count_conflicts(region, color, assignment, neighbors):
    """
    Đếm số lượng vị trí xung đột (trùng màu) nếu quận 'region' mang màu 'color'
    """
    count = 0
    for neighbor in neighbors[region]:
        # Nếu hàng xóm đã có màu và màu đó trùng với màu đang thử nghiệm
        if neighbor in assignment and assignment[neighbor] == color:
            count += 1
    return count