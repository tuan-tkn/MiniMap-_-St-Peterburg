import tkinter
import tkintermapview
import math

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
root.geometry("900x700")
root.title("Hệ thống tìm đường Sankt-Peterburg")

# --- 2. TẠO BẢN ĐỒ VÀ ĐẶT VÀO CỬA SỔ ---
map_widget = tkintermapview.TkinterMapView(root, width=900, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# --- 3. THIẾT LẬP TỌA ĐỘ VÀ DẤU GHIM ---
hermitage = [59.9398, 30.3146]
church_on_blood = [59.9401, 30.3286]

# Đưa camera đến vị trí trung tâm giữa 2 điểm
map_widget.set_position(59.9400, 30.3200)
map_widget.set_zoom(14)

# Cắm ghim trực tiếp lên map_widget
map_widget.set_marker(hermitage[0], hermitage[1], text="Bảo tàng Hermitage")
map_widget.set_marker(church_on_blood[0], church_on_blood[1], text="Nhà thờ Chúa Cứu Thế")

# --- 4. TÍNH KHOẢNG CÁCH VÀ CHẠY ỨNG DỤNG ---
dist = calculate_distance(hermitage[0], hermitage[1], church_on_blood[0], church_on_blood[1])
print(f"Khoảng cách giữa hai điểm là: {dist:.2f} mét")

root.mainloop()