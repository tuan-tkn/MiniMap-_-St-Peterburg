import math
from queue import Queue, PriorityQueue

# ==========================================
# PHẦN 0: DỮ LIỆU TOÀN CỤC VÀ ĐỒ THỊ
# ==========================================
# Danh sách đen các đỉnh không được đi qua
obstacles = ["Lang_Bac"] 

class Graph:
    """Class này giả lập lại cấu trúc đồ thị em đang sử dụng"""
    def __init__(self):
        self.nodes = {}  # Lưu tọa độ (VD: {'Ho_Hoan_Kiem': {'y': 21.0..., 'x': 105.8...}})
        self.edges = {}  # Lưu danh sách kề (VD: {'Ho_Hoan_Kiem': ['Van_Mieu', ...]})

    def add_node(self, name, lat, lon):
        self.nodes[name] = {'y': lat, 'x': lon}
        if name not in self.edges:
            self.edges[name] = []

    def add_edge(self, u, v):
        # Đồ thị vô hướng (đi được 2 chiều)
        self.edges[u].append(v)
        self.edges[v].append(u)

    def neighbors(self, node):
        return self.edges.get(node, [])

# ==========================================
# PHẦN 1: CÁC HÀM VÀ THUẬT TOÁN TÌM ĐƯỜNG (Nguyên bản của em)
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
        global obstacles 
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
                if neighbor in obstacles:
                    continue
                if neighbor not in closed:
                    closed.add(neighbor)
                    came_from[neighbor] = current
                    open_set.put(neighbor)
        return count_node, None, 0.0

class AStar(Algorithm):
    def run(self, start, goal, graph):
        global obstacles 
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
# PHẦN 2: CHẠY THỬ NGHIỆM
# ==========================================
if __name__ == "__main__":
    # 1. Khởi tạo bản đồ
    my_map = Graph()
    
    # 2. Thêm các địa điểm (Vĩ độ, Kinh độ)
    my_map.add_node("Ho_Hoan_Kiem", 21.0285, 105.8542)
    my_map.add_node("Van_Mieu", 21.0294, 105.8355)
    my_map.add_node("Lang_Bac", 21.0368, 105.8346) # Đây là vật cản!
    my_map.add_node("Ho_Tay", 21.0583, 105.8159)
    my_map.add_node("Cong_Vien_Thong_Nhat", 21.0173, 105.8455)
    
    # 3. Tạo các tuyến đường nối với nhau
    my_map.add_edge("Ho_Hoan_Kiem", "Van_Mieu")
    my_map.add_edge("Van_Mieu", "Lang_Bac")
    my_map.add_edge("Lang_Bac", "Ho_Tay")
    my_map.add_edge("Van_Mieu", "Cong_Vien_Thong_Nhat")
    my_map.add_edge("Cong_Vien_Thong_Nhat", "Ho_Tay") # Đường vòng để tránh Lăng Bác
    
    # 4. Chạy thuật toán
    diem_bat_dau = "Ho_Hoan_Kiem"
    diem_ket_thuc = "Ho_Tay"
    
    print(f"--- Đang tìm đường từ {diem_bat_dau} đến {diem_ket_thuc} ---")
    print(f"Danh sách vật cản: {obstacles}\n")

    # Thử với BFS
    bfs_algo = BFS()
    bfs_nodes, bfs_path, bfs_dist = bfs_algo.run(diem_bat_dau, diem_ket_thuc, my_map)
    print("=== Kết quả thuật toán BFS ===")
    print(f"Số đỉnh đã xét: {bfs_nodes}")
    print(f"Đường đi: {' -> '.join(bfs_path) if bfs_path else 'Không tìm thấy'}")
    print(f"Tổng quãng đường: {bfs_dist:.2f} mét\n")

    # Thử với A*
    astar_algo = AStar()
    astar_nodes, astar_path, astar_dist = astar_algo.run(diem_bat_dau, diem_ket_thuc, my_map)
    print("=== Kết quả thuật toán A* ===")
    print(f"Số đỉnh đã xét: {astar_nodes}")
    print(f"Đường đi: {' -> '.join(astar_path) if astar_path else 'Không tìm thấy'}")
    print(f"Tổng quãng đường: {astar_dist:.2f} mét")