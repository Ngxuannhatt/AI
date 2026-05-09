# Đích đến để so sánh độ chính xác
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def print_board(state):
    for i in range(0, 9, 3):
        print(f"{state[i]} {state[i+1]} {state[i+2]}")
    print("-" * 10)

# 1. Hàm đếm xem có bao nhiêu số đang đứng đúng vị trí
def count_correct_positions(state):
    count = 0
    for i in range(9):
        # Không đếm số 0 (ô trống) vì ta chỉ cần các số từ 1-8 đúng vị trí
        if state[i] != 0 and state[i] == GOAL[i]:
            count += 1
    return count

# 2. Hàm tìm các trạng thái có thể đi tiếp
def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Lên, Xuống, Trái, Phải

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], new_state[zero_index]
            neighbors.append(tuple(new_state))
    return neighbors

# --- CHƯƠNG TRÌNH CHÍNH ---

# Nhập dữ liệu từ bàn phím
print("Nhap day so (9 so tu 0-8, cach nhau bang dau cach):")
# Ví dụ nhập: 1 2 3 0 4 6 7 5 8
input_data = input().split()
start_state = tuple(int(x) for x in input_data)

current_state = start_state
history = [current_state] # Lưu lịch sử các bước đã đi

print("\nBat dau qua trinh di chuyen tham lam:")
print_board(current_state)

while True:
    neighbors = get_neighbors(current_state)
    
    best_neighbor = None
    max_correct = -1
    
    # Tìm trong các hàng xóm, cái nào có nhiều số đúng vị trí nhất
    for neighbor in neighbors:
        correct_count = count_correct_positions(neighbor)
        if correct_count > max_correct:
            max_correct = correct_count
            best_neighbor = neighbor
            
    # Nếu di chuyển tốt nhất dẫn đến một trạng thái đã từng đi qua -> Thoát
    if best_neighbor in history:
        print("PHAT HIEN LAP LAI TRANG THAI CU. DUNG CHUONG TRINH.")
        print(f"Trang thai bi lap: {best_neighbor}")
        break
    
    # Cập nhật trạng thái hiện tại
    current_state = best_neighbor
    history.append(current_state)
    
    print(f"Buoc tiep theo (Co {max_correct} so dung vi tri):")
    print_board(current_state)

    # Nếu đã đạt đến đích thì cũng dừng
    if current_state == GOAL:
        print("DA DAT DEN TRANG THAI DICH!")
        break