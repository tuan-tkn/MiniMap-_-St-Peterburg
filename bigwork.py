import math
from queue import PriorityQueue

# Danh sách vật cản (Toàn cục)
obs = ["Lang_Bac"] 

# ==========================================
# 1. HÀM TÍNH KHOẢNG CÁCH
# ==========================================
def dist(u, v, V):
    # V là Dictionary lưu tọa độ. V[u] trả về (vĩ độ, kinh độ)
    x1, y1 = V[u] 
    x2, y2 = V[v] 
    
    R = 6371000
    p1, p2 = math.radians(x1), math.radians(x2)
    dp = math.radians(x2 - x1)
    dl = math.radians(y2 - y1)
    
    a = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ==========================================
# 2. HÀM TRUY VẾT ĐƯỜNG ĐI
# ==========================================
def get_path(s, e, p):
    res = []
    u = e
    while u != s:
        res.append(u)
        if p.get(u) is None: return None
        u = p[u]
    res.append(s)
    return res[::-1] # Cắt mảng ngược để đảo chiều từ Nguồn -> Đích

# ==========================================
# 3. THUẬT TOÁN A* TỐI GIẢN
# ==========================================
def astar(s, e, V, E):
    global obs
    q = PriorityQueue()
    q.put((0, s))    # Push tuple (f_score, đỉnh u) vào hàng đợi
    
    p = {s: None}    # Mảng truy vết (parent)
    g = {s: 0}       # Chi phí thực tế (g_score)
    
    while not q.empty():
        f, u = q.get()
        
        # Nếu tìm thấy đích, kết thúc và truy vết
        if u == e: 
            return get_path(s, e, p), g[u]
            
        # Duyệt qua các đỉnh kề v của u trong tập cạnh E
        for v in E.get(u, []):
            if v in obs: continue # Gặp vật cản -> Bỏ qua
            
            w = dist(u, v, V) # Tính trọng số cạnh (chi phí bước đi u -> v)
            tg = g[u] + w     # Chi phí g_score tạm thời
            
            # Nếu v chưa được thăm HOẶC tìm được đường đi rẻ hơn tới v
            if v not in g or tg < g[v]:
                p[v] = u              # Lưu vết
                g[v] = tg             # Cập nhật chi phí thực tế
                h = dist(v, e, V)     # Tính Heuristic h(v)
                q.put((tg + h, v))    # Push vào hàng đợi tổng f(v) = g(v) + h(v)
                
    return None, 0.0

# ==========================================
# 4. CHẠY THỬ
# ==========================================
if __name__ == "__main__":
    # V: Tập các đỉnh (Đỉnh: (Vĩ độ, Kinh độ))
    V = {
        "Ho_Hoan_Kiem": (21.0285, 105.8542),
        "Van_Mieu": (21.0294, 105.8355),
        "Lang_Bac": (21.0368, 105.8346),
        "Ho_Tay": (21.0583, 105.8159),
        "Cong_Vien": (21.0173, 105.8455)
    }
    
    # E: Tập các cạnh (Danh sách kề)
    E = {
        "Ho_Hoan_Kiem": ["Van_Mieu"],
        "Van_Mieu": ["Ho_Hoan_Kiem", "Lang_Bac", "Cong_Vien"],
        "Lang_Bac": ["Van_Mieu", "Ho_Tay"],
        "Ho_Tay": ["Lang_Bac", "Cong_Vien"],
        "Cong_Vien": ["Van_Mieu", "Ho_Tay"]
    }
    
    path, total_dist = astar("Ho_Hoan_Kiem", "Ho_Tay", V, E)
    print("Đường đi:", " -> ".join(path) if path else "Không có đường")
    print(f"Tổng khoảng cách: {total_dist:.2f} mét")