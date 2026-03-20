import tkinter
import tkintermapview
import math

# 1. Tạo cửa sổ chính của ứng dụng
root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{600}") # Kích thước cửa sổ 800x600
root_tk.title("Bản đồ Sankt-Peterburg - Tìm đường đi")

# 2. Tạo thành phần hiển thị bản đồ
# Chúng ta đặt nó vào cửa sổ 'root_tk'
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# 3. Đặt vị trí trung tâm là Sankt-Peterburg
# Tọa độ: Vĩ độ 59.9311, Kinh độ 30.3609
map_widget.set_position(59.9311, 30.3609) 
map_widget.set_zoom(12) # Mức độ phóng to (từ 0 đến 19)

# 4. Chạy ứng dụng

# --- HÀM TÍNH KHOẢNG CÁCH (Công thức Haversine) ---
def calculate_distance(lat1, lon1, lat2, lon2):
    # Bán kính Trái Đất tính bằng mét
    R = 6371000 
    
    # Chuyển đổi độ sang radian
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    # Công thức Haversine
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c # Kết quả trả về tính bằng mét

# --- THIẾT LẬP GIAO DIỆN ---
root = tkinter.Tk()
root.geometry("900x700")
root.title("Hệ thống tìm đường Sankt-Peterburg")

map_widget = tkintermapview.TkinterMapView(root, width=900, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# Tọa độ các điểm
hermitage = [59.9398, 30.3146]
church_on_blood = [59.9401, 30.3286]

# Tập trung bản đồ vào khu vực trung tâm
map_widget.set_position(59.9400, 30.3200)
map_widget.set_zoom(15)

# 1. Thêm dấu ghim (Markers)
map_widget.set_marker(hermitage[0], hermitage[1], text="Bảo tàng Hermitage")
map_widget.set_marker(church_on_blood[0], church_on_blood[1], text="Nhà thờ Chúa Cứu Thế")

# 2. Tính toán và in kết quả ra Terminal
dist = calculate_distance(hermitage[0], hermitage[1], church_on_blood[0], church_on_blood[1])
print(f"Khoảng cách giữa hai điểm là: {dist:.2f} mét")

root_tk.mainloop()