import tkinter
import tkintermapview
import math
import osmnx as ox

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

path_1 = map_widget.set_path([hermitage, church_on_blood], color="red", width=3)

# --- 4. TÍNH KHOẢNG CÁCH ---
dist = calculate_distance(hermitage[0], hermitage[1], church_on_blood[0], church_on_blood[1])
print(f"Khoảng cách đường chim bay là: {dist:.2f} mét")

# --- 5. TẢI MẠNG LƯỚI ĐƯỜNG PHỐ THỰC TẾ ---
print("Đang tải mạng lưới đường phố Sankt-Peterburg, vui lòng đợi một chút...")
# Tải các đường dành cho xe cộ ('drive') trong bán kính 2000 mét từ tâm
G = ox.graph_from_point(center_point, dist=2000, network_type='drive')
print(f"Tuyệt vời! Đã tải xong bản đồ với {len(G.nodes)} điểm giao cắt và {len(G.edges)} đoạn đường.")

# Lệnh này luôn nằm ở cuối cùng để giữ cửa sổ mở
root.mainloop()