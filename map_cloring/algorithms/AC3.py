import copy

def ac3_checking_coloring(neighbors, num_colors, callback=None):
    """
    Giải bài toán tô màu bản đồ bằng thuật toán Backtracking kết hợp với AC-3 (Arc-Consistency).
    
    :param neighbors: Đồ thị kề dạng dict { node: [list_of_neighbors] }
    :param num_colors: Số lượng màu tối đa được phép dùng (int)
    :param callback: Hàm lưu lại trạng thái từng bước để hiển thị lên UI
    :return: Lời giải dạng dict { node: color_id } hoặc None nếu thất bại
    """
    # Khởi tạo miền giá trị ban đầu cho tất cả các quận
    domains = {region: list(range(1, num_colors + 1)) for region in neighbors}
    assignment = {}

    # Chạy hàm đệ quy tìm kiếm kèm lọc AC-3
    return backtrack_ac3(assignment, domains, neighbors, callback)

def backtrack_ac3(assignment, domains, neighbors, callback):
    # Nếu đã gán màu cho tất cả các quận -> Hoàn thành
    if len(assignment) == len(neighbors):
        return assignment

    # Chọn quận tiếp theo chưa được gán màu (Sử dụng cơ chế MRV đơn giản: chọn quận còn ít màu nhất)
    unassigned = [v for v in neighbors if v not in assignment]
    region = min(unassigned, key=lambda v: len(domains[v]))

    # Duyệt qua các màu có thể gán cho quận này
    for color in list(domains[region]):
        # Tạo bản sao sâu để tránh ghi đè dữ liệu khi quay lui
        domains_copy = copy.deepcopy(domains)
        domains_copy[region] = [color]  # Gán thử màu bằng cách thu hẹp miền giá trị về 1 phần tử

        # Gọi callback cập nhật sự kiện "ASSIGN" (Gán màu thử nghiệm) lên giao diện
        if callback:
            assignment_copy = assignment.copy()
            assignment_copy[region] = color
            callback(region, color, 'ASSIGN', assignment_copy, domains_copy)

        # Tiến hành chạy thuật toán AC-3 để thiết lập tính nhất quán cung (Arc Consistency)
        if ac3(domains_copy, neighbors):
            # Nếu AC-3 thành công (không có miền giá trị của quận nào bị rỗng)
            assignment[region] = color
            
            # Tiếp tục đệ quy gán cho quận tiếp theo
            result = backtrack_ac3(assignment, domains_copy, neighbors, callback)
            if result is not None:
                return result
            
            # Quay lui nếu nhánh đệ quy dưới thất bại
            del assignment[region]
        else:
            # Nếu AC-3 thất bại (lọc sạch màu của một quận lân cận nào đó)
            if callback:
                # Gửi sự kiện FAIL_FC lên giao diện để chuyển nút sang màu Đỏ cảnh báo
                assignment_copy = assignment.copy()
                assignment_copy[region] = color
                callback(region, color, 'FAIL_FC', assignment_copy, domains_copy)

        # Gọi callback thông báo quay lui (Hủy gán màu)
        if callback:
            callback(region, color, 'BACKTRACK', assignment.copy(), domains)

    return None

def ac3(domains, neighbors):
    """
    Thuật toán AC-3 kiểm tra và duy trì tính nhất quán cung.
    """
    # Khởi tạo hàng đợi chứa tất cả các cung (arc) có trong đồ thị
    queue = []
    for node in neighbors:
        for neighbor in neighbors[node]:
            queue.append((node, neighbor))

    while queue:
        xi, xj = queue.pop(0)
        
        # Nếu miền giá trị của xi bị chỉnh sửa để nhất quán với xj
        if revise(domains, xi, xj):
            # Nếu miền giá trị của xi trống rỗng -> AC-3 thất bại
            if len(domains[xi]) == 0:
                return False
            
            # Thêm lại các cung lân cận của xi (trừ xj) vào hàng đợi để kiểm tra lại
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    """
    Sửa đổi miền giá trị của xi sao cho nhất quán với xj.
    Trả về True nếu miền giá trị của xi có sự thay đổi, ngược lại False.
    """
    revised = False
    # Duyệt qua từng màu trong miền giá trị của xi
    for x in list(domains[xi]):
        # Tìm xem có ít nhất một màu 'y' khác 'x' trong miền giá trị của xj hay không
        has_allowed_value = any(y != x for y in domains[xj])
        
        # Nếu không có màu nào thỏa mãn (xung đột hoàn toàn), xóa x khỏi miền giá trị của xi
        if not has_allowed_value:
            domains[xi].remove(x)
            revised = True
            
    return revised