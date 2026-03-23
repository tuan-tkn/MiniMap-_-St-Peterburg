from collections import deque

def bfs(graph, start_node):
    """
    Hàm thực hiện thuật toán BFS.
    :param graph: Đồ thị được biểu diễn dưới dạng Dictionary (Danh sách kề).
    :param start_node: Đỉnh bắt đầu duyệt.
    """
    # Bước 1: Khởi tạo tập hợp các đỉnh đã thăm và thêm đỉnh bắt đầu vào
    visited = set()
    visited.add(start_node)
    
    # Bước 2: Khởi tạo hàng đợi và đưa đỉnh bắt đầu vào hàng đợi
    queue = deque([start_node])
    
    print(f"Thứ tự duyệt BFS bắt đầu từ đỉnh '{start_node}':")

    # Bước 3: Lặp trong khi hàng đợi vẫn còn phần tử
    while queue:
        # Lấy đỉnh ở đầu hàng đợi ra để xử lý
        current_node = queue.popleft()
        print(current_node, end=" -> ") # In ra đỉnh đang thăm

        # Bước 4: Kiểm tra tất cả các "hàng xóm" của đỉnh hiện tại
        for neighbor in graph[current_node]:
            # Nếu hàng xóm này chưa từng được ghé thăm
            if neighbor not in visited:
                visited.add(neighbor)      # Đánh dấu là đã thăm ngay lập tức
                queue.append(neighbor)     # Đưa vào cuối hàng đợi để xử lý sau

    print("Hoàn tất!")

# ==========================================
# HƯỚNG DẪN SỬ DỤNG (VÍ DỤ THỰC TẾ)
# ==========================================

# Biểu diễn đồ thị bằng Dictionary (Danh sách kề)
# Tưởng tượng đây là bản đồ các thành phố kết nối với nhau:
# A nối với B và C
# B nối với A, D, và E ...
my_graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Chạy thử thuật toán
bfs(my_graph, 'A')