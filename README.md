# 📌 Introduction to Artificial Intelligence  - AI vacuum cleaner project & visual interface

---

## 👤 Thông tin sinh viên
- **Họ và tên:** Nguyễn Xuân Nhật
- **Mã số sinh viên (MSSV):** 24110293
- **Môn học:** Introduction to AI (Nhập môn Trí tuệ Nhân tạo)

---

## 📌 Tổng quan dự án
Dự án này lưu trữ toàn bộ các bài tập thực hành, đồ án và mã nguồn được xây dựng cho môn học **Nhập môn Trí tuệ Nhân tạo (Introduction to AI)**. 

Dự án bao gồm:
1. **Tác nhân phản xạ (Reflex Agents):** Các mô hình tác nhân phản xạ đơn giản và tác nhân có mô hình bộ nhớ giải quyết bài toán robot hút bụi và 8-puzzle.
2. **Trực quan hóa Thuật toán Tìm kiếm (Search Algorithms Visualizer):** Giao diện đồ họa viết bằng thư viện **Tkinter (Python)** minh họa hoạt động của hơn 15 thuật toán tìm kiếm trên bản đồ robot hút bụi (từ tìm kiếm mù, tìm kiếm heuristic đến tìm kiếm cục bộ và tìm kiếm trong môi trường phức tạp).
3. **Đồ án Tô màu bản đồ (CSP - Constraint Satisfaction Problems):** Trực quan hóa và giải quyết bài toán tô màu bản đồ sử dụng các thuật toán thỏa mãn ràng buộc tối ưu như AC-3, Backtracking, Forward Checking, và Min-Conflicts.

---

## 📂 Cấu trúc thư mục dự án
```text
trí tuệ nhân tạo/
├── simple reflex agent/             # Các mô hình Agent phản xạ đơn giản
│   └── 8puzzle                      # File giải bài toán 8-Puzzle bằng Agent phản xạ
├── map_cloring/                     # Đồ án Tô màu bản đồ (Constraint Satisfaction Problems)
│   ├── algorithms/                  # Thuật toán giải CSP
│   │   ├── AC3.py                   # Thuật toán Arc Consistency 3
│   │   ├── back_tracking.py         # Thuật toán Quay lui Backtracking
│   │   ├── forward_checking.py      # Thuật toán Kiểm tra trước Forward Checking
│   │   └── min_conflicts.py         # Thuật toán Cực tiểu hóa xung đột Min-Conflicts
│   └── main_ui.py                   # Giao diện chính đồ án Tô màu bản đồ (Tkinter)
├── vacuum_project/                  # Đồ án Robot hút bụi thông minh (Search Algorithms & GUI)
│   ├── algorithms/                  # Thuật toán tìm kiếm cốt lõi
│   │   ├── And_Or_Search.py         # Tìm kiếm đồ thị AND-OR
│   │   ├── Astar.py                 # Tìm kiếm A*
│   │   ├── BFS_1.py                 # BFS tiếp cận 1 (Đích muộn)
│   │   ├── BFS_2.py                 # BFS tiếp cận 2 (Đích sớm)
│   │   ├── DFS_1.py                 # DFS tiếp cận 1 (Đích muộn)
│   │   ├── DFS_2.py                 # DFS tiếp cận 2 (Đích sớm)
│   │   ├── DFS_Searching_With_No_Observation.py          # Tìm kiếm không cảm biến (Sensorless)
│   │   ├── DFS_Searching_for_partially_observable_problems.py # Tìm kiếm quan sát bộ phận
│   │   ├── GS.py                    # Greedy Best-First Search
│   │   ├── IDAstar.py               # Tìm kiếm IDA*
│   │   ├── IDS_1.py                 # IDS tiếp cận 1 (Đích muộn)
│   │   ├── IDS_2.py                 # IDS tiếp cận 2 (Đích sớm)
│   │   ├── Local_Beam_Search.py     # Tìm kiếm chùm tia cục bộ
│   │   ├── Random_Restart_Hill_Climbing.py               # Leo đồi khởi động lại ngẫu nhiên
│   │   ├── Simple_Hill_Climbing.py  # Leo đồi đơn giản
│   │   ├── Simulated_Annealing.py   # Luyện kim giả lập
│   │   ├── Steepest_Ascent_Hill_Climbing.py              # Leo đồi dốc nhất
│   │   ├── Stochastic_Hill_Climbing.py                   # Leo đồi ngẫu nhiên
│   │   └── UCS.py                   # Tìm kiếm chi phí đồng nhất Uniform Cost
│   ├── visualizer/                  # Giao diện đồ họa (GUI) trực quan hóa Robot hút bụi
│   │   ├── main_UI.ipynb            # Notebook thử nghiệm giao diện
│   │   ├── matrix.txt               # Bản đồ ma trận đầu vào mặc định
│   │   ├── test_main.py             # File chạy giao diện Tkinter chính
│   │   └── vacuum.png               # Asset ảnh của robot hút bụi
│   └── node.py                      # Lớp định nghĩa cấu trúc nút (Node) tìm kiếm
├── 8puzzle.ipynb                    # Notebook thực hành 8-Puzzle
├── mayhutbui.ipynb                  # Notebook thực hành Robot hút bụi cơ bản
└── README.md                        # Tài liệu giới thiệu dự án (File này)
```

---

## 🧠 Phân loại và Chi tiết 6 nhóm thuật toán lớn

---

### 1. Nhóm Tác nhân Phản xạ (Reflex Agent)
Các tác nhân phản xạ tương tác trực tiếp với môi trường theo chu kỳ cảm nhận - hành động thông qua các tập quy tắc định sẵn (Condition-Action Rules).

#### 1.1. Simple Reflex Agent (Tác nhân phản xạ đơn giản)
* **Khái niệm:** Đưa ra quyết định hành động chỉ dựa trên cảm nhận ở trạng thái hiện tại, bỏ qua lịch sử hoạt động.
* **Mã giả (Pseudo-code):**
  ```python
  def Simple_Reflex_Agent(percept):
      state = Interpret_Input(percept)
      rule = Rule_Match(state, rules)
      action = rule.action
      return action
  ```
* **Ưu điểm:** Cấu trúc cực kỳ đơn giản, thời gian tính toán rất nhanh, tốn ít tài nguyên phần cứng.
* **Độ phức tạp thời gian:** $O(1)$ cho mỗi lượt chọn hành động.
* **Độ phức tạp không gian:** $O(1)$ vì không cần bộ nhớ lưu giữ lịch sử thế giới.

#### 1.2. Model-Based Reflex Agent (Tác nhân phản xạ dựa trên mô hình)
* **Khái niệm:** Duy trì một trạng thái bên trong để ghi nhớ thông tin về môi trường trước đó, hữu dụng khi môi trường không thể quan sát toàn phần.
* **Mã giả (Pseudo-code):**
  ```python
  def Model_Based_Reflex_Agent(percept):
      state = Update_State(state, action, percept, model)
      rule = Rule_Match(state, rules)
      action = rule.action
      return action
  ```
* **Ưu điểm:** Khắc phục nhược điểm mất dấu thông tin trong môi trường quan sát bộ phận bằng cách theo dõi lịch sử và mô phỏng sự biến đổi của thế giới.
* **Độ phức tạp thời gian:** $O(1)$
* **Độ phức tạp không gian:** $O(S)$ với $S$ là kích thước mô hình trạng thái trong cần duy trì.

---

### 2. Nhóm Tìm kiếm Mù (Uninformed Search)
Các thuật toán duyệt qua không gian trạng thái một cách hệ thống mà không có thêm thông tin định hướng về khoảng cách đến đích ngoại trừ mô hình định nghĩa bài toán.

#### 2.1. BFS (Breadth-First Search)
* **Khái niệm:** Mở rộng các nút gần gốc nhất trước, sử dụng hàng đợi FIFO.
* **Mã giả (Pseudo-code):**
  ```python
  def BFS(problem):
      node = Node(state=problem.initial_state)
      if problem.is_goal(node.state): return node
      frontier = Queue([node]) # FIFO Queue
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  if problem.is_goal(child.state): return child
                  frontier.push(child)
      return None
  ```
* **Ưu điểm:** Đầy đủ (Complete) và luôn tìm thấy đường đi ngắn nhất (Optimal) khi chi phí các bước bằng nhau.
* **Độ phức tạp thời gian:** $O(b^d)$ (với $b$ là hệ số nhánh, $d$ là độ sâu của lời giải).
* **Độ phức tạp không gian:** $O(b^d)$ do phải giữ toàn bộ các nút trong bộ nhớ hàng đợi.

#### 2.2. DFS (Depth-First Search)
* **Khái niệm:** Mở rộng các nút ở sâu nhất trên cây tìm kiếm trước, sử dụng ngăn xếp LIFO.
* **Mã giả (Pseudo-code):**
  ```python
  def DFS(problem):
      frontier = Stack([Node(state=problem.initial_state)]) # LIFO Stack
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          if node.state not in explored:
              explored.add(node.state)
              for action in problem.actions(node.state):
                  frontier.push(child_node(problem, node, action))
      return None
  ```
* **Ưu điểm:** Tiết kiệm không gian bộ nhớ hơn BFS đáng kể nếu cây tìm kiếm sâu nhưng hẹp.
* **Độ phức tạp thời gian:** $O(b^m)$ (với $m$ là độ sâu tối đa của không gian trạng thái).
* **Độ phức tạp không gian:** $O(b \cdot m)$ tuyến tính theo độ sâu.

#### 2.3. UCS (Uniform Cost Search)
* **Khái niệm:** Mở rộng nút có chi phí đường đi tích lũy $g(n)$ nhỏ nhất trước, sử dụng hàng đợi ưu tiên (Priority Queue).
* **Mã giả (Pseudo-code):**
  ```python
  def UCS(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: n.path_cost) # Min-Priority Queue
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
              elif child.state in frontier với chi phí cao hơn:
                  thay thế nút trong frontier bằng child
      return None
  ```
* **Ưu điểm:** Đầy đủ và luôn đảm bảo tối ưu hóa chi phí tích lũy ngay cả khi các bước đi có trọng số/chi phí khác nhau.
* **Độ phức tạp thời gian:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$ (với $C^*$ là chi phí tối ưu, $\epsilon$ là chi phí tối thiểu của một bước).
* **Độ phức tạp không gian:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$.

#### 2.4. IDS (Iterative Deepening Search)
* **Khái niệm:** Thực hiện DFS lặp lại nhiều lần với giới hạn độ sâu (depth-limit) tăng dần từ 0 đến vô hạn.
* **Mã giả (Pseudo-code):**
  ```python
  def IDS(problem):
      for depth in range(0, infinity):
          result = Depth_Limited_Search(problem, depth)
          if result != cutoff: return result
  ```
* **Ưu điểm:** Kết hợp hoàn hảo tính tối ưu, đầy đủ của BFS và tính tiết kiệm bộ nhớ tuyến tính của DFS.
* **Độ phức tạp thời gian:** $O(b^d)$
* **Độ phức tạp không gian:** $O(b \cdot d)$

---

### 3. Nhóm Tìm kiếm Thông tin (Informed / Heuristic Search)
Sử dụng tri thức bổ sung dưới dạng hàm heuristic $h(n)$ để ước lượng khoảng cách từ trạng thái hiện tại đến đích nhằm tăng tốc độ tìm kiếm.

#### 3.1. Greedy Best-First Search (Tìm kiếm tham lam)
* **Khái niệm:** Mở rộng nút được ước lượng là gần đích nhất dựa theo hàm heuristic $h(n)$.
* **Mã giả (Pseudo-code):**
  ```python
  def Greedy_Best_First(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: heuristic(n.state))
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
      return None
  ```
* **Ưu điểm:** Thường có tốc độ tìm đường đi rất nhanh trong thực tế nếu xây dựng được hàm heuristic sát thực tế.
* **Độ phức tạp thời gian:** $O(b^m)$ (trường hợp xấu nhất tương tự DFS).
* **Độ phức tạp không gian:** $O(b^m)$ để lưu trữ biên tìm kiếm.

#### 3.2. A\* Search (Tìm kiếm A-sao)
* **Khái niệm:** Chọn nút mở rộng dựa trên hàm đánh giá tổng hợp $f(n) = g(n) + h(n)$ (chi phí thực tế cộng chi phí ước lượng đến đích).
* **Mã giả (Pseudo-code):**
  ```python
  def A_Star(problem):
      node = Node(state=problem.initial_state)
      frontier = PriorityQueue(node, key=lambda n: n.path_cost + heuristic(n.state))
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(node.state)
          for action in problem.actions(node.state):
              child = child_node(problem, node, action)
              if child.state not in explored and child.state not in frontier:
                  frontier.push(child)
              elif child.state in frontier với f(n) lớn hơn:
                  thay thế nút trong frontier bằng child
      return None
  ```
* **Ưu điểm:** Là thuật toán tìm kiếm tối ưu nhất (nếu heuristic chấp nhận được - admissible và nhất quán - consistent).
* **Độ phức tạp thời gian:** Hàm mũ $O(b^d)$ phụ thuộc vào độ lệch của hàm ước lượng.
* **Độ phức tạp không gian:** $O(b^d)$ lưu toàn bộ các nút sinh ra.

#### 3.3. IDA\* (Iterative Deepening A\*)
* **Khái niệm:** Tương tự IDS nhưng thay thế giới hạn độ sâu bằng giới hạn chi phí $f(n) = g(n) + h(n)$.
* **Mã giả (Pseudo-code):**
  ```python
  def IDA_Star(problem):
      limit = heuristic(problem.initial_state)
      while True:
          temp_limit, result = DLS_A_Star(problem.initial_state, 0, limit)
          if result == goal: return result
          if temp_limit == infinity: return None
          limit = temp_limit
  ```
* **Ưu điểm:** Giảm thiểu tối đa không gian lưu trữ của A* (chỉ tốn dung lượng tuyến tính như DFS) nhưng giữ nguyên tính tối ưu.
* **Độ phức tạp thời gian:** $O(b^d)$
* **Độ phức tạp không gian:** $O(b \cdot d)$

---

### 4. Nhóm Tìm kiếm Cục bộ (Local Search)
Tập trung vào việc cải thiện trạng thái hiện tại thay vì ghi nhớ toàn bộ đường đi từ nguồn. Cực kỳ thích hợp cho các bài toán tối ưu hóa.

#### 4.1. Hill Climbing (Leo đồi) & Các biến thể
* **Khái niệm:** Di chuyển liên tục từ trạng thái hiện tại sang trạng thái lân cận có giá trị tốt hơn.
  - **Simple Hill Climbing:** Chọn ngay lân cận tốt hơn đầu tiên tìm thấy.
  - **Steepest-Ascent Hill Climbing:** Đánh giá mọi lân cận và chọn lân cận tốt nhất.
  - **Stochastic Hill Climbing:** Chọn ngẫu nhiên giữa các lân cận tốt hơn dựa trên xác suất.
  - **Random-Restart Hill Climbing:** Khởi chạy leo đồi nhiều lần từ các điểm xuất phát ngẫu nhiên.
* **Mã giả (Steepest-Ascent):**
  ```python
  def Hill_Climbing(problem):
      current = problem.initial_state
      while True:
          neighbors = problem.neighbors(current)
          best_neighbor = max(neighbors, key=lambda n: value(n))
          if value(best_neighbor) <= value(current):
              return current
          current = best_neighbor
  ```
* **Ưu điểm:** Tiêu tốn bộ nhớ ở mức tối thiểu hằng số $O(1)$.
* **Độ phức tạp thời gian:** Phụ thuộc vào địa hình của không gian trạng thái; dễ bị kẹt ở cực trị địa phương (local maxima) hoặc cao nguyên phẳng.
* **Độ phức tạp không gian:** $O(1)$.

#### 4.2. Local Beam Search (Tìm kiếm chùm tia cục bộ)
* **Khái niệm:** Theo dõi song song $k$ trạng thái tốt nhất. Tại mỗi bước lặp, sinh tất cả các lân cận của cả $k$ trạng thái và chỉ giữ lại $k$ trạng thái có đánh giá cao nhất.
* **Mã giả (Pseudo-code):**
  ```python
  def Beam_Search(problem, k):
      frontier = [problem.initial_state]
      while not goal_found:
          candidates = []
          for state in frontier:
              candidates.extend(problem.neighbors(state))
          frontier = select_best_k(candidates, k)
          if goal in frontier: return goal
      return None
  ```
* **Ưu điểm:** Chia sẻ thông tin giữa các luồng tìm kiếm song song, giúp thoát khỏi cực đại địa phương tốt hơn leo đồi đơn lẻ.
* **Độ phức tạp thời gian:** $O(k \cdot b \cdot m)$
* **Độ phức tạp không gian:** $O(k \cdot b)$

#### 4.3. Simulated Annealing (Luyện kim giả lập)
* **Khái niệm:** Cho phép thực hiện các bước đi làm giảm chất lượng giải thuật ở giai đoạn đầu với một xác suất được kiểm soát bởi nhiệt độ giảm dần $T$.
* **Mã giả (Pseudo-code):**
  ```python
  def Simulated_Annealing(problem, schedule):
      current = problem.initial_state
      for t in range(1, infinity):
          T = schedule(t)
          if T == 0: return current
          next_state = random_select(problem.neighbors(current))
          delta_E = value(next_state) - value(current)
          if delta_E > 0:
              current = next_state
          else:
              current = next_state với xác suất e^(delta_E / T)
  ```
* **Ưu điểm:** Đã được chứng minh toán học là có khả năng hội tụ về điểm tối ưu toàn cục nếu giảm nhiệt độ đủ chậm.
* **Độ phức tạp thời gian:** Phụ thuộc cooling schedule.
* **Độ phức tạp không gian:** $O(1)$.

---

### 5. Nhóm Tìm kiếm Trong Môi Trường Phức Tạp (Complex Environments Search)
Tìm kiếm khi môi trường không còn tính xác định (nondeterministic) hoặc không thể quan sát đầy đủ (partially observable).

#### 5.1. Sensorless Search (Tìm kiếm không cảm biến)
* **Khái niệm:** Tác nhân hoàn toàn mù (không cảm biến), phải duyệt qua không gian các trạng thái niềm tin (Belief States) để tìm chuỗi hành động đưa mọi trạng thái khởi đầu về đích.
* **Mã giả (Pseudo-code):**
  ```python
  def Sensorless_Search_BFS(problem):
      start_belief = problem.initial_belief_state
      frontier = Queue([Node(start_belief)])
      explored = Set()
      while not frontier.is_empty():
          node = frontier.pop()
          if problem.is_goal(node.state): return node
          explored.add(hash_belief(node.state))
          for action in problem.actions:
              next_belief = predict_belief(node.state, action)
              if hash_belief(next_belief) not in explored:
                  frontier.push(Node(next_belief, parent=node, action=action))
      return None
  ```
* **Ưu điểm:** Đưa ra giải pháp chắc chắn thành công ngay cả khi hệ thống không có bất kỳ khả năng cảm nhận vị trí hiện tại.
* **Độ phức tạp thời gian:** $O(b^P)$ với $P \le 2^N$ trạng thái niềm tin (với $N$ là số trạng thái vật lý).
* **Độ phức tạp không gian:** $O(2^N)$ lưu trữ.

#### 5.2. Partially Observable Search (Tìm kiếm quan sát bộ phận)
* **Khái niệm:** Cập nhật niềm tin động kết hợp từ hành động hành trình và phản hồi thực tế từ các cảm biến hạn chế.
* **Mã giả (Belief Update):**
  ```python
  # Trạng thái niềm tin mới được cập nhật sau hành động và cảm nhận:
  # Belief_Next = Update(Predict(Belief, Action), Percept)
  ```
* **Ưu điểm:** Cho phép robot tự định vị và thích nghi theo thời gian thực dựa trên các tín hiệu cảm biến thu được.
* **Độ phức tạp thời gian:** Lên đến lũy thừa $O(2^N)$ trong trường hợp tệ nhất.
* **Độ phức tạp không gian:** $O(2^N)$.

#### 5.3. And-Or Graph Search (Tìm kiếm đồ thị AND-OR)
* **Khái niệm:** Tìm kiếm cây giải pháp (contingency plan) trong môi trường ngẫu nhiên. Các nút OR đại diện cho các lựa chọn hành động của tác nhân, các nút AND đại diện cho các phản ứng ngẫu nhiên của môi trường.
* **Mã giả (Pseudo-code):**
  ```python
  def And_Or_Graph_Search(problem):
      return Or_Search(problem.initial_state, problem, [])

  def Or_Search(state, problem, path):
      if problem.is_goal(state): return empty_plan
      if state in path: return failure
      for action in problem.actions(state):
          plan = And_Search(Results(state, action), problem, [state] + path)
          if plan != failure: return [action, plan]
      return failure

  def And_Search(states, problem, path):
      plan = {}
      for s in states:
          p = Or_Search(s, problem, path)
          if p == failure: return failure
          plan[s] = p
      return plan
  ```
* **Ưu điểm:** Cung cấp giải thuật thích ứng đầy đủ cho mọi kết quả ngẫu nhiên có thể xảy ra trong môi trường.
* **Độ phức tạp thời gian:** Tỷ lệ thuận với kích thước không gian AND-OR.
* **Độ phức tạp không gian:** Tỷ lệ thuận với độ sâu tối đa của cây kế hoạch.

---

### 6. Nhóm Bài toán Thỏa mãn Ràng buộc (CSP - Constraint Satisfaction Problems)
Giải quyết các bài toán bằng cách phân bổ giá trị cho các biến sao cho thỏa mãn tập các ràng buộc đặt ra.

#### 6.1. Backtracking Search (CSP)
* **Khái niệm:** Giải thuật quay lui gán giá trị lần lượt cho từng biến và thực hiện quay lui ngay khi phát hiện vi phạm ràng buộc.
* **Mã giả (Pseudo-code):**
  ```python
  def Backtracking_Search(csp):
      return Backtrack({}, csp)

  def Backtrack(assignment, csp):
      if is_complete(assignment, csp): return assignment
      var = select_unassigned_variable(assignment, csp)
      for value in order_domain_values(var, assignment, csp):
          if is_consistent(var, value, assignment, csp):
              assignment.add(var, value)
              result = Backtrack(assignment, csp)
              if result != failure: return result
              assignment.remove(var, value)
      return failure
  ```
* **Ưu điểm:** Đơn giản, đảm bảo tìm thấy giải pháp nếu tồn tại.
* **Độ phức tạp thời gian:** $O(d^n)$ (với $n$ là số biến, $d$ là số lượng phần tử miền giá trị).
* **Độ phức tạp không gian:** $O(n)$ lưu trữ đệ quy.

#### 6.2. Forward Checking (Kiểm tra trước)
* **Khái niệm:** Mỗi khi gán một giá trị cho biến $X$, kiểm tra và loại bỏ các giá trị không tương thích khỏi miền giá trị của các biến chưa gán liên kề với $X$.
* **Mã giả (Pseudo-code):**
  ```python
  def Forward_Checking(assignment, csp, var, value):
      assignment.add(var, value)
      for neighbor in csp.neighbors(var):
          if neighbor not in assignment:
              remove value from neighbor.domain if it violates constraints
              if neighbor.domain is empty: return failure
      return success
  ```
* **Ưu điểm:** Phát hiện sớm các mâu thuẫn ràng buộc, cắt tỉa các nhánh lỗi sớm trước khi đi sâu đệ quy.
* **Độ phức tạp thời gian:** Giảm thiểu đáng kể so với quay lui thông thường.
* **Độ phức tạp không gian:** $O(n \cdot d)$.

#### 6.3. AC-3 (Arc Consistency 3)
* **Khái niệm:** Thuật toán lọc miền giá trị bằng cách thực thi tính nhất quán cung (arc consistency) giữa mọi cặp biến trong CSP.
* **Mã giả (Pseudo-code):**
  ```python
  def AC_3(csp):
      queue = Queue(all_arcs_in_csp)
      while not queue.is_empty():
          (Xi, Xj) = queue.pop()
          if Revise(csp, Xi, Xj):
              if len(Xi.domain) == 0: return False
              for Xk in csp.neighbors(Xi) - {Xj}:
                  queue.push((Xk, Xi))
      return True

  def Revise(csp, Xi, Xj):
      revised = False
      for x in Xi.domain:
          if no y in Xj.domain satisfies constraint between Xi and Xj:
              remove x from Xi.domain
              revised = True
      return revised
  ```
* **Ưu điểm:** Triệt tiêu sớm rất nhiều giá trị không hợp lệ trước khi quá trình gán giá trị bắt đầu.
* **Độ phức tạp thời gian:** $O(c \cdot d^3)$ (với $c$ là số lượng cung liên kết).
* **Độ phức tạp không gian:** $O(c)$.

#### 6.4. Min-Conflicts (Cực tiểu hóa xung đột)
* **Khái niệm:** Thuật toán tìm kiếm cục bộ gán giá trị đầy đủ ngẫu nhiên cho các biến, sau đó chọn biến có xung đột ràng buộc và gán giá trị mới tối thiểu hóa xung đột.
* **Mã giả (Pseudo-code):**
  ```python
  def Min_Conflicts(csp, max_steps):
      current = complete_random_assignment(csp)
      for i in range(max_steps):
          if is_solution(current, csp): return current
          var = random_select(conflicted_variables(current, csp))
          value = argmin(csp.domain(var), key=lambda val: conflicts(var, val, current, csp))
          current[var] = value
      return failure
  ```
* **Ưu điểm:** Khả năng giải quyết các CSP khổng lồ cực kỳ nhanh (hàng triệu biến) trong thời gian gần như tuyến tính.
* **Độ phức tạp thời gian:** Gần như tuyến tính trong thực nghiệm.
* **Độ phức tạp không gian:** $O(n)$ lưu giữ lời giải hiện tại.

---

## 🚀 Hướng dẫn chạy chương trình

### 🧹 1. Ứng dụng mô phỏng Robot hút bụi (vacuum_project)
Để khởi chạy ứng dụng trực quan hóa robot hút bụi bằng Tkinter:

1. Di chuyển vào thư mục dự án:
   ```bash
   cd "vacuum_project/visualizer"
   ```
2. Chạy ứng dụng Python:
   ```bash
   python test_main.py
   ```
3. **Các tính năng trên giao diện:**
   - Chọn thuật toán tìm kiếm từ thanh menu bên trái (BFS, DFS, IDS, UCS, A*, v.v.).
   - Nhấn nút **Tạo Mới / Reset** để làm mới bản đồ dựa theo file cấu hình ma trận `matrix.txt`.
   - Xem nhật ký di chuyển thời gian thực bên phải và quá trình truy vết ngược sau khi hoàn tất.

### 🎨 2. Ứng dụng tô màu bản đồ (map_cloring)
Để chạy chương trình trực quan hóa bài toán CSP tô màu bản đồ:

1. Di chuyển vào thư mục tô màu bản đồ:
   ```bash
   cd "map_cloring"
   ```
2. Chạy file giao diện chính:
   ```bash
   python main_ui.py
   ```
3. **Các tính năng:**
   - Chọn các thuật toán CSP (Backtracking, Forward Checking, Min-Conflicts, AC-3) để xem cách phân bổ màu sắc cho các tỉnh/bang sao cho không có 2 vùng kề nhau trùng màu.
