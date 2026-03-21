import tkinter
import customtkinter
import tkintermapview
import math
import osmnx as ox
from queue import Queue, PriorityQueue

# ==========================================
# PHẦN 1: CÁC HÀM VÀ THUẬT TOÁN TÌM ĐƯỜNG
# ==========================================
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class Algorithm:
    def __init__(self):
        pass
    def reconstruct_path(self, start, goal, came_from):
        path = []
        current = goal
        while current != start:
            path.append(current)
            if came_from.get(current) is None: return None
            current = came_from[current]
        path.append(start)
        return path[::-1]

class BFS(Algorithm):
    def run(self, start, goal, graph):
        open_set = Queue()
        open_set.put(start)
        came_from = {start: None}
        closed = set([start])
        count_node = 0
        while not open_set.empty():
            current = open_set.get()
            count_node += 1
            if current == goal: 
                return count_node, self.reconstruct_path(start, goal, came_from)
            for neighbor in graph.neighbors(current):
                if neighbor not in closed:
                    closed.add(neighbor)
                    came_from[neighbor] = current
                    open_set.put(neighbor)
        return count_node, None

class AStar(Algorithm):
    def run(self, start, goal, graph):
        open_queue = PriorityQueue()
        open_queue.put((0, start))
        came_from = {start: None}
        g_score = {start: 0}
        count_node = 0
        goal_lat, goal_lon = graph.nodes[goal]['y'], graph.nodes[goal]['x']

        while not open_queue.empty():
            current_f, current = open_queue.get()
            count_node += 1
            if current == goal: 
                return count_node, self.reconstruct_path(start, goal, came_from), g_score[current]
            for neighbor in graph.neighbors(current):
                lat1, lon1 = graph.nodes[current]['y'], graph.nodes[current]['x']
                lat2, lon2 = graph.nodes[neighbor]['y'], graph.nodes[neighbor]['x']
                step_cost = calculate_distance(lat1, lon1, lat2, lon2)
                tentative_g_score = g_score[current] + step_cost
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    h_score = calculate_distance(lat2, lon2, goal_lat, goal_lon)
                    open_queue.put((tentative_g_score + h_score, neighbor))
        return count_node, None, 0.0

# ==========================================
# PHẦN 2: THIẾT LẬP GIAO DIỆN NGƯỜI DÙNG
# ==========================================
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Chỉ gọi 1 cửa sổ duy nhất ở đây!
root = customtkinter.CTk()
root.geometry("1000x700")
root.title("Hệ thống tìm đường Sankt-Peterburg")

# Khung chứa bản đồ (Bên trái)
frame_left = customtkinter.CTkFrame(root)
frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Khung chứa bảng điều khiển (Bên phải)
frame_right = customtkinter.CTkFrame(root, width=300)
frame_right.pack(side="right", fill="y", padx=10, pady=10)

# Cài đặt bản đồ vào khung trái
map_widget = tkintermapview.TkinterMapView(frame_left, corner_radius=10)
map_widget.pack(fill="both", expand=True)

center_point = (59.9400, 30.3200)
map_widget.set_position(center_point[0], center_point[1])
map_widget.set_zoom(14)

# --- TÍNH NĂNG MỚI: TƯƠNG TÁC CHUỘT PHẢI ---
# 1. Các biến toàn cục để lưu trữ tọa độ và dấu ghim
start_marker = None
goal_marker = None
start_coords = None
goal_coords = None

# 2. Hàm xử lý khi chọn "Đặt Điểm Đầu"
def set_start(coords):
    global start_marker, start_coords
    # Nếu đã có ghim cũ thì xóa đi
    if start_marker:
        start_marker.delete()
    # Cắm ghim mới màu xanh lá
    start_marker = map_widget.set_marker(coords[0], coords[1], text="Điểm Đầu")
    start_coords = coords
    print(f"Đã cắm Điểm Đầu tại: {coords}")

# 3. Hàm xử lý khi chọn "Đặt Điểm Đích"
def set_goal(coords):
    global goal_marker, goal_coords
    if goal_marker:
        goal_marker.delete()
    # Cắm ghim mới màu đỏ
    goal_marker = map_widget.set_marker(coords[0], coords[1], text="Điểm Đích")
    goal_coords = coords
    print(f"Đã cắm Điểm Đích tại: {coords}")

# 4. Gắn lệnh vào Menu Chuột Phải của bản đồ
map_widget.add_right_click_menu_command(label="Đặt Điểm Đầu", command=set_start, pass_coords=True)
map_widget.add_right_click_menu_command(label="Đặt Điểm Đích", command=set_goal, pass_coords=True)
# ------------------------------------------

# ==========================================
# 5. CÁC HÀM XỬ LÝ NÚT BẤM (NỐI ĐIỆN CHO NÚT)
# ==========================================
current_path = None # Biến để nhớ đường đi hiện tại (để sau này xóa đi)

def find_path():
    global current_path
    
    # Kiểm tra xem đã cắm đủ 2 ghim chưa
    if start_coords is None or goal_coords is None:
        label_result.configure(text="Lỗi:\nVui lòng cắm đủ\nĐiểm Đầu và Đích!")
        return
        
    label_result.configure(text="Đang tìm đường...")
    root.update() # Cập nhật chữ trên màn hình ngay lập tức
    
    # Xóa đường đi cũ nếu có
    if current_path is not None:
        current_path.delete()
        
    # Tìm điểm giao cắt gần nhất với 2 cái ghim
    start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
    goal_node = ox.distance.nearest_nodes(G, X=goal_coords[1], Y=goal_coords[0])
    
    # Chạy thuật toán A*
    astar_algo = AStar()
    nodes_searched, path_nodes, total_distance = astar_algo.run(start_node, goal_node, G)
    
    # Nếu tìm thấy đường, vẽ lên bản đồ và in kết quả
    if path_nodes is not None:
        path_coords = []
        for node_id in path_nodes:
            lat = G.nodes[node_id]['y']
            lon = G.nodes[node_id]['x']
            path_coords.append((lat, lon))
            
        current_path = map_widget.set_path(path_coords, color="red", width=4)
        label_result.configure(text=f"Khoảng cách: {total_distance:.2f} m\nSố ngã rẽ: {len(path_nodes)}\nĐã duyệt: {nodes_searched} nút")
    else:
        label_result.configure(text="Không tìm thấy\nđường đi!")

def clear_map():
    global start_marker, goal_marker, start_coords, goal_coords, current_path
    
    # Xóa ghim và đường đi trên bản đồ
    if start_marker: start_marker.delete()
    if goal_marker: goal_marker.delete()
    if current_path: current_path.delete()
    
    # Đưa các biến về trạng thái trống
    start_marker = goal_marker = current_path = None
    start_coords = goal_coords = None
    
    # Trả lại dòng chữ mặc định
    label_result.configure(text="Khoảng cách: N/A\nSố ngã rẽ: N/A")


# ==========================================
# 6. GẮN HÀM VÀO GIAO DIỆN KHUNG PHẢI
# ==========================================
label_title = customtkinter.CTkLabel(frame_right, text="TÌM ĐƯỜNG ĐI", font=("Arial", 20, "bold"))
label_title.pack(pady=20)

label_guide = customtkinter.CTkLabel(frame_right, text="Click chuột phải để\nchọn Điểm Đầu/Đích", text_color="gray")
label_guide.pack(pady=10)

# LƯU Ý: Đã thêm tham số command=find_path và command=clear_map
btn_find = customtkinter.CTkButton(frame_right, text="Tìm Đường (A*)", command=find_path)
btn_find.pack(pady=10)

btn_clear = customtkinter.CTkButton(frame_right, text="Xóa Bản Đồ", fg_color="red", hover_color="darkred", command=clear_map)
btn_clear.pack(pady=10)

label_result = customtkinter.CTkLabel(frame_right, text="Khoảng cách: N/A\nSố ngã rẽ: N/A", justify="left", font=("Arial", 14))
label_result.pack(side="bottom", pady=30)

# ==========================================
# PHẦN 3: TẢI DỮ LIỆU ĐƯỜNG PHỐ
# ==========================================
print("Đang tải mạng lưới đường phố Sankt-Peterburg...")
G = ox.graph_from_point(center_point, dist=2000, network_type='drive')
print("Đã tải xong bản đồ! Ứng dụng đã sẵn sàng.")

root.mainloop()