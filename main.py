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

# Cài đặt các nút bấm vào khung phải
label_title = customtkinter.CTkLabel(frame_right, text="TÌM ĐƯỜNG ĐI", font=("Arial", 20, "bold"))
label_title.pack(pady=20)

label_guide = customtkinter.CTkLabel(frame_right, text="Click chuột phải để chọn Điểm Đầu/Đích", text_color="gray")
label_guide.pack(pady=10)

btn_find = customtkinter.CTkButton(frame_right, text="Tìm Đường (A*)")
btn_find.pack(pady=10)

btn_clear = customtkinter.CTkButton(frame_right, text="Xóa Bản Đồ", fg_color="red", hover_color="darkred")
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