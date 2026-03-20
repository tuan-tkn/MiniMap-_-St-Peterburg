import tkinter
import tkintermapview

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
root_tk.mainloop()