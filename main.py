import tkinter
import tkintermapview
import math
import osmnx as ox
from queue import Queue, PriorityQueue

# --- HÀM TÍNH KHOẢNG CÁCH ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Bán kính Trái Đất (mét)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- 1. TẠO MỘT CỬA SỔ DUY NHẤT ---
root = tkinter.Tk()
root.geometry("777x777")
root.title("Hệ thống tìm đường Sankt-Peterburg")

# --- 2. TẠO BẢN ĐỒ VÀ ĐẶT VÀO CỬA SỔ ---
map_widget = tkintermapview.TkinterMapView(root, width=777, height=777, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# --- 3. THIẾT LẬP TỌA ĐỘ VÀ DẤU GHIM ---
hermitage = [59.9398, 30.3146]
church_on_blood = [59.9401, 30.3286]
center_point = (59.9400, 30.3200) # Tọa độ trung tâm

map_widget.set_position(center_point[0], center_point[1])
map_widget.set_zoom(15)

map_widget.set_marker(hermitage[0], hermitage[1], text="Bảo tàng Hermitage")
map_widget.set_marker(church_on_blood[0], church_on_blood[1], text="Nhà thờ Chúa Cứu Thế")

#path_1 = map_widget.set_path([hermitage, church_on_blood], color="red", width=3)

# --- 4. TÍNH KHOẢNG CÁCH ---
dist = calculate_distance(hermitage[0], hermitage[1], church_on_blood[0], church_on_blood[1])
print(f"Khoảng cách đường chim bay là: {dist:.2f} mét")

# --- 5. TẢI MẠNG LƯỚI ĐƯỜNG PHỐ THỰC TẾ ---
print("Đang tải mạng lưới đường phố Sankt-Peterburg, vui lòng đợi một chút...")
# Tải các đường dành cho xe cộ ('drive') trong bán kính 2000 mét từ tâm
G = ox.graph_from_point(center_point, dist=2000, network_type='drive')
print(f"Tuyệt vời! Đã tải xong bản đồ với {len(G.nodes)} điểm giao cắt và {len(G.edges)} đoạn đường.")

# --- 6. TÌM ĐIỂM GIAO CẮT GẦN NHẤT TRÊN ĐƯỜNG ---
# Lưu ý: Thư viện osmnx nhận tham số theo thứ tự X (Kinh độ - lon), Y (Vĩ độ - lat)
start_node = ox.distance.nearest_nodes(G, X=hermitage[1], Y=hermitage[0])
goal_node = ox.distance.nearest_nodes(G, X=church_on_blood[1], Y=church_on_blood[0])

print(f"ID điểm xuất phát: {start_node}")
print(f"ID điểm đích: {goal_node}")


# --- 7. KHUÔN MẪU CHO CÁC THUẬT TOÁN TÌM ĐƯỜNG ---
class Algorithm:
    def __init__(self):
        pass

    def run(self, start, goal, graph):
        """Hàm này sẽ bị ghi đè bởi các thuật toán cụ thể (BFS, A*...)"""
        pass

    def reconstruct_path(self, start, goal, came_from):
        """Hàm truy vết đường đi từ điểm đích ngược về điểm xuất phát"""
        path = []
        current = goal
        while current != start:
            path.append(current)
            if came_from.get(current) is None:
                return None # Không tìm thấy đường
            current = came_from[current]
        
        path.append(start)
        return path[::-1] # Đảo ngược danh sách để có đường đi từ Start -> Goal
    
# --- 8. TRIỂN KHAI THUẬT TOÁN BFS ---
class BFS(Algorithm):
    def run(self, start, goal, graph):
        open_set = Queue() # Hàng đợi lưu các điểm cần kiểm tra
        open_set.put(start)
        
        came_from = {start: None} # Lưu vết đường đi (điểm này đến từ điểm nào)
        closed = set([start])     # Tập hợp các điểm đã kiểm tra để không đi lùi
        count_node = 0            # Đếm số lượng ngã rẽ đã duyệt

        while not open_set.empty():
            current = open_set.get() # Lấy điểm đầu tiên trong hàng đợi ra kiểm tra
            count_node += 1

            if current == goal:
                # Nếu tìm thấy đích, gọi hàm truy vết đường đi
                return count_node, self.reconstruct_path(start, goal, came_from)

            # Lấy tất cả các điểm giao cắt nối liền với điểm hiện tại
            for neighbor in graph.neighbors(current):
                if neighbor not in closed: # Nếu điểm này chưa từng đi qua
                    closed.add(neighbor)
                    came_from[neighbor] = current
                    open_set.put(neighbor) # Đưa vào hàng đợi để lát nữa kiểm tra

        return count_node, None # Trả về None nếu không tìm thấy đường


# # --- 9. CHẠY THUẬT TOÁN VÀ VẼ ĐƯỜNG LÊN BẢN ĐỒ ---
# print("\nĐang chạy thuật toán BFS...")
# bfs_algo = BFS()
# nodes_searched, path_nodes = bfs_algo.run(start_node, goal_node, G)

# if path_nodes is not None:
#     print(f"Hoàn thành! BFS đã duyệt {nodes_searched} ngã rẽ.")
#     print(f"Đường đi tìm được đi qua {len(path_nodes)} ngã rẽ.")
    
#     # Chuyển đổi danh sách ID thành danh sách Tọa độ (Vĩ độ, Kinh độ)
#     path_coords = []
#     for node_id in path_nodes:
#         lat = G.nodes[node_id]['y']
#         lon = G.nodes[node_id]['x']
#         path_coords.append((lat, lon))
        
#     # Vẽ tuyến đường lên bản đồ (Màu xanh dương)
#     real_path = map_widget.set_path(path_coords, color="blue", width=4)
# else:
#     print("Không tìm thấy đường đi nào nối hai điểm này!")

# --- 10. TRIỂN KHAI THUẬT TOÁN A* (A-SAO) ---
class AStar(Algorithm):
    def run(self, start, goal, graph):
        open_queue = PriorityQueue()
        # Đưa điểm xuất phát vào hàng đợi với chi phí f=0
        open_queue.put((0, start))
        
        came_from = {start: None}
        g_score = {start: 0} # Lưu khoảng cách thực tế từ điểm xuất phát
        count_node = 0
        
        # Lấy trước tọa độ của đích để lát tính Heuristic
        goal_lat = graph.nodes[goal]['y']
        goal_lon = graph.nodes[goal]['x']

        while not open_queue.empty():
            # Lấy ngã rẽ có tổng chi phí f(n) nhỏ nhất ra kiểm tra
            current_f, current = open_queue.get()
            count_node += 1

            if current == goal:
                return count_node, self.reconstruct_path(start, goal, came_from)

            for neighbor in graph.neighbors(current):
                # Lấy tọa độ của current và neighbor để tính chiều dài đoạn đường
                lat1, lon1 = graph.nodes[current]['y'], graph.nodes[current]['x']
                lat2, lon2 = graph.nodes[neighbor]['y'], graph.nodes[neighbor]['x']
                
                # Tính g(n): Chi phí đi đến neighbor
                step_cost = calculate_distance(lat1, lon1, lat2, lon2)
                tentative_g_score = g_score[current] + step_cost

                # Nếu tìm được đường đi ngắn hơn đến neighbor này
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    
                    # Tính h(n): Ước lượng khoảng cách từ neighbor đến đích
                    h_score = calculate_distance(lat2, lon2, goal_lat, goal_lon)
                    
                    # Tính f(n) = g(n) + h(n) và đưa vào hàng đợi
                    f_score = tentative_g_score + h_score
                    open_queue.put((f_score, neighbor))

        return count_node, None
    
# --- CHẠY THUẬT TOÁN ---
print("\nĐang chạy thuật toán A*...")
astar_algo = AStar()
nodes_searched, path_nodes = astar_algo.run(start_node, goal_node, G)

if path_nodes is not None:
    print(f"Hoàn thành! A* cực kỳ thông minh, chỉ cần duyệt {nodes_searched} ngã rẽ.")
    print(f"Đường đi tìm được đi qua {len(path_nodes)} ngã rẽ.")
    
    path_coords = []
    for node_id in path_nodes:
        lat = G.nodes[node_id]['y']
        lon = G.nodes[node_id]['x']
        path_coords.append((lat, lon))
        
    # Lần này ta vẽ đường màu đỏ tươi (red) cho A* nhé
    real_path = map_widget.set_path(path_coords, color="red", width=4)
else:
    print("Không tìm thấy đường!")

# Lệnh này luôn nằm ở cuối cùng để giữ cửa sổ mở
root.mainloop()