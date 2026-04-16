import tkinter
import customtkinter
import tkintermapview
import math
import osmnx as ox
from queue import Queue, PriorityQueue

# Danh sách đen chứa ID các ngã tư bị chặn
obstacles = set()

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
    def __init__(self): pass
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
        global obstacles # Lấy danh sách đen
        open_set = Queue()
        open_set.put(start)
        came_from = {start: None}
        closed = set([start])
        count_node = 0
        
        while not open_set.empty():
            current = open_set.get()
            count_node += 1
            if current == goal: 
                path = self.reconstruct_path(start, goal, came_from)
                total_dist = sum(calculate_distance(graph.nodes[path[i]]['y'], graph.nodes[path[i]]['x'], 
                                                    graph.nodes[path[i+1]]['y'], graph.nodes[path[i+1]]['x']) 
                                 for i in range(len(path)-1))
                return count_node, path, total_dist
                
            for neighbor in graph.neighbors(current):
                # SỰ THÔNG MINH Ở ĐÂY: NẾU LÀ VẬT CẢN THÌ BỎ QUA!
                if neighbor in obstacles:
                    continue
                    
                if neighbor not in closed:
                    closed.add(neighbor)
                    came_from[neighbor] = current
                    open_set.put(neighbor)
        return count_node, None, 0.0

class AStar(Algorithm):
    def run(self, start, goal, graph):
        global obstacles # Lấy danh sách đen
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
                # SỰ THÔNG MINH Ở ĐÂY: NẾU LÀ VẬT CẢN THÌ BỎ QUA!
                if neighbor in obstacles:
                    continue
                    
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
# PHẦN 2: THIẾT LẬP GIAO DIỆN & TƯƠNG TÁC
# ==========================================
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("1000x700")
root.title("Hệ thống tìm đường Sankt-Peterburg - AI HUST")

frame_left = customtkinter.CTkFrame(root)
frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

frame_right = customtkinter.CTkFrame(root, width=300)
frame_right.pack(side="right", fill="y", padx=10, pady=10)

map_widget = tkintermapview.TkinterMapView(frame_left, corner_radius=10)
map_widget.pack(fill="both", expand=True)

# BIẾN TOÀN CỤC CHO BẢN ĐỒ
start_marker = goal_marker = current_path = None
start_coords = goal_coords = None
obstacle_markers = [] # Chứa các ghim vật cản để lát xóa

# --- CÁC HÀM CHUỘT PHẢI ---
def set_start(coords):
    global start_marker, start_coords
    if start_marker: start_marker.delete()
    start_marker = map_widget.set_marker(coords[0], coords[1], text="A (Bắt đầu)")
    start_coords = coords

def set_goal(coords):
    global goal_marker, goal_coords
    if goal_marker: goal_marker.delete()
    goal_marker = map_widget.set_marker(coords[0], coords[1], text="B (Đích)")
    goal_coords = coords

def set_obstacle(coords):
    global obstacles, obstacle_markers
    obs_node = ox.distance.nearest_nodes(G, X=coords[1], Y=coords[0])
    obstacles.add(obs_node)
    m = map_widget.set_marker(coords[0], coords[1], text="✖ CẤM ĐI")
    obstacle_markers.append(m)

map_widget.add_right_click_menu_command(label="Đặt Điểm Đầu", command=set_start, pass_coords=True)
map_widget.add_right_click_menu_command(label="Đặt Điểm Đích", command=set_goal, pass_coords=True)
map_widget.add_right_click_menu_command(label="Đặt Vật Cản", command=set_obstacle, pass_coords=True)

# --- CÁC HÀM NÚT BẤM ---
def find_path():
    global current_path
    if start_coords is None or goal_coords is None:
        label_result.configure(text="Lỗi: Vui lòng cắm đủ\nĐiểm Đầu và Đích!")
        return
    label_result.configure(text="Đang tính toán AI...")
    root.update()
    
    if current_path: current_path.delete()
    start_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
    goal_node = ox.distance.nearest_nodes(G, X=goal_coords[1], Y=goal_coords[0])
    
    selected_algo = algo_var.get()
    algo = AStar() if selected_algo == "A*" else BFS()
    path_color = "red" if selected_algo == "A*" else "blue"
    
    nodes_searched, path_nodes, total_distance = algo.run(start_node, goal_node, G)
    
    if path_nodes is not None:
        path_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path_nodes]
        current_path = map_widget.set_path(path_coords, color=path_color, width=4)
        label_result.configure(text=f"Thuật toán: {selected_algo}\nQuãng đường: {total_distance:.0f} m\nSố ngã rẽ: {len(path_nodes)}\nĐã duyệt: {nodes_searched} nút")
    else:
        label_result.configure(text="Không tìm thấy đường!\n(Bị chặn kín rồi)")

def clear_obstacles():
    global obstacles, obstacle_markers
    obstacles.clear()
    for m in obstacle_markers: m.delete()
    obstacle_markers.clear()

def clear_map():
    global start_marker, goal_marker, start_coords, goal_coords, current_path
    if start_marker: start_marker.delete()
    if goal_marker: goal_marker.delete()
    if current_path: current_path.delete()
    start_marker = goal_marker = current_path = None
    start_coords = goal_coords = None
    clear_obstacles() # Xóa luôn vật cản
    label_result.configure(text="Khoảng cách: N/A\nSố ngã rẽ: N/A")

# --- GIAO DIỆN KHUNG PHẢI ---
label_title = customtkinter.CTkLabel(frame_right, text="TÌM ĐƯỜNG ĐI", font=("Arial", 20, "bold"))
label_title.pack(pady=20)

label_guide = customtkinter.CTkLabel(frame_right, text="Click chuột phải để:\n- Đặt Đầu/Đích\n- Đặt Vật Cản", text_color="gray")
label_guide.pack(pady=10)

algo_var = customtkinter.StringVar(value="A*")
dropdown_algo = customtkinter.CTkOptionMenu(frame_right, values=["A*", "BFS"], variable=algo_var)
dropdown_algo.pack(pady=10)

btn_find = customtkinter.CTkButton(frame_right, text="Bắt Đầu Tìm!", command=find_path)
btn_find.pack(pady=10)

btn_clear_obs = customtkinter.CTkButton(frame_right, text="Xóa Vật Cản", fg_color="orange", hover_color="darkorange", command=clear_obstacles)
btn_clear_obs.pack(pady=5)

btn_clear = customtkinter.CTkButton(frame_right, text="Xóa Toàn Bộ", fg_color="red", hover_color="darkred", command=clear_map)
btn_clear.pack(pady=5)

label_result = customtkinter.CTkLabel(frame_right, text="Khoảng cách: N/A\nSố ngã rẽ: N/A", justify="left", font=("Arial", 14))
label_result.pack(side="bottom", pady=30)

# ==========================================
# PHẦN 3: TẢI DỮ LIỆU ĐƯỜNG PHỐ VÀ GA TÀU
# ==========================================
print("Đang tải mạng lưới đường phố Sankt-Peterburg...")
center_point = (59.9400, 30.3200)

# Tải mạng lưới đường bộ cho thuật toán
G = ox.graph_from_point(center_point, dist=2000, network_type='drive')
print("Đã tải xong bản đồ đường phố!")

# --- TÍNH NĂNG MỚI: TẢI VÀ HIỂN THỊ GA TÀU ---
print("Đang quét các ga tàu điện/tàu hỏa trong khu vực...")
try:
    # Lọc các địa điểm có nhãn là ga tàu hoặc ga tàu điện ngầm
    tags = {'railway': 'station', 'station': 'subway'}
    stations = ox.features_from_point(center_point, tags=tags, dist=2000)
    
    # Lặp qua từng ga tàu tìm được để cắm ghim
    count_stations = 0
    for idx, row in stations.iterrows():
        # Dữ liệu đôi khi là một vùng (polygon), ta lấy điểm tâm (centroid) của nó
        centroid = row.geometry.centroid
        lat, lon = centroid.y, centroid.x
        
        # Lấy tên của ga tàu (nếu trên bản đồ không có tên thì để trống)
        station_name = row.get('name', 'Ga Tàu')
        if not isinstance(station_name, str): 
            station_name = 'Ga Tàu'
            
        # Cắm ghim lên bản đồ. Chỉnh màu xanh tím (purple) để khác với ghim Start/Goal
        map_widget.set_marker(lat, lon, text=f"🚇 {station_name}", 
                              marker_color_outside="purple", 
                              marker_color_circle="white")
        count_stations += 1
        
    print(f"Tuyệt vời! Đã tìm thấy và cắm ghim {count_stations} ga tàu.")
except Exception as e:
    print("Không tìm thấy ga tàu nào hoặc có lỗi tải dữ liệu:", e)
# ---------------------------------------------

# Thiết lập camera
map_widget.set_position(center_point[0], center_point[1])
map_widget.set_zoom(14)

print("Ứng dụng đã sẵn sàng.")
root.mainloop()