x = 5
y = 10.5
algorithm = "BFS"

if algorithm == "BFS":
    print("Su dung hang doi (Queue)")
elif algorithm == "DFS":
    print("Su dung hang doi (Stack)")
else:
    print("Thuat toan nhu cut")

print("Danh sach cac dinh:")
for i in range(x):
    print("Dinh thu", i)

count = 0
while count < 3:
    print("Dang dem:", count)
    count += 1

print("Hello World")