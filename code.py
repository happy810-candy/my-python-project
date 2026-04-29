# Báo cáo doanh thu

# Danh sách sản phẩm
san_pham = [
    ["Laptop Gaming Dell G15", 25000000, 1],
    ["Chuột Logitech B100", 100000, 50],
    ["Màn hình LG UltraWide", 8000000, 3],
    ["Cáp chuyển đổi USB-C", 150000, 10],
    ["Server HP ProLiant", 60000000, 1],
    ["Bàn phím cơ Keychron", 2000000, 5],
    ["Tai nghe Sony WH-1000XM5", 7000000, 4],
    ["Ổ cứng HDD WD Red 4TB", 3000000, 10],
    ["Lót chuột khổ lớn", 50000, 20],
    ["Macbook Pro M3", 45000000, 2],
    ["USB Kingston 64GB", 200000, 15],
    ["Máy chiếu Epson 4K", 35000000, 1],
    ["Ghế công thái học", 5000000, 6],
    ["Webcam Logitech C930", 2500000, 2],
    ["Tủ mạng Rack 42U", 15000000, 2]
]

# Tính toán
tong_doanh_thu = 0
so_don_vip = 0
so_don_pho_thong = 0
doanh_thu_vip = 0
doanh_thu_pho_thong = 0

# Lưu dữ liệu để ghi file
du_lieu_bao_cao = []

# In ra màn hình
print("\n" + "="*100)
print(" " * 35 + "BÁO CÁO DOANH THU")
print("="*100)
print()

# In tiêu đề bảng
print(f"{'STT':<5} {'Tên Sản Phẩm':<35} {'Đơn Giá':>15} {'Số Lượng':>12} {'Doanh Thu':>18} {'Loại':>15}")
print("-"*100)

# Xử lý từng sản phẩm
for i in range(len(san_pham)):
    ten = san_pham[i][0]
    don_gia = san_pham[i][1]
    so_luong = san_pham[i][2]
    doanh_thu_sp = don_gia * so_luong  # Doanh thu của sản phẩm
    
    # Phân loại đơn hàng
    if doanh_thu_sp >= 20000000:
        loai = "Đơn hàng VIP"
        so_don_vip += 1
        doanh_thu_vip += doanh_thu_sp
    else:
        loai = "Đơn hàng Phổ thông"
        so_don_pho_thong += 1
        doanh_thu_pho_thong += doanh_thu_sp
    
    tong_doanh_thu += doanh_thu_sp
    
    # Lưu dữ liệu
    du_lieu_bao_cao.append([i+1, ten, don_gia, so_luong, doanh_thu_sp, loai])
    
    # In dòng dữ liệu
    print(f"{i+1:<5} {ten:<35} {don_gia:>15,} {so_luong:>12} {doanh_thu_sp:>18,} {loai:>15}")

print("-"*100)
print(f"{'TỔNG DOANH THU:':<70} {tong_doanh_thu:>18,} VNĐ")
print("="*100)

# Thống kê
print("\n" + "="*100)
print(" " * 35 + "THỐNG KÊ")
print("="*100)
print(f"Tổng doanh thu: {tong_doanh_thu:>20,} VNĐ")
print(f"Số đơn hàng VIP: {so_don_vip:>20}")
print(f"Số đơn hàng Phổ thông: {so_don_pho_thong:>20}")
print(f"Doanh thu từ đơn VIP: {doanh_thu_vip:>20,} VNĐ")
print(f"Doanh thu từ đơn Phổ thông: {doanh_thu_pho_thong:>20,} VNĐ")
print("="*100)

# Chi tiết doanh thu từng sản phẩm
print("\n" + "="*100)
print(" " * 30 + "DOANH THU TỪNG SẢN PHẨM")
print("="*100)
print(f"{'STT':<5} {'Tên Sản Phẩm':<40} {'Doanh Thu (VNĐ)':>20}")
print("-"*100)
for du_lieu in du_lieu_bao_cao:
    print(f"{du_lieu[0]:<5} {du_lieu[1]:<40} {du_lieu[4]:>20,}")
print("="*100)

# Ghi file text
with open("bao_cao_doanh_thu.txt", "w", encoding="utf-8") as f:
    f.write("="*100 + "\n")
    f.write(" " * 35 + "BÁO CÁO DOANH THU\n")
    f.write("="*100 + "\n\n")
    f.write(f"{'STT':<5} {'Tên Sản Phẩm':<35} {'Đơn Giá':>15} {'Số Lượng':>12} {'Doanh Thu':>18} {'Loại':>15}\n")
    f.write("-"*100 + "\n")
    
    for du_lieu in du_lieu_bao_cao:
        f.write(f"{du_lieu[0]:<5} {du_lieu[1]:<35} {du_lieu[2]:>15,} {du_lieu[3]:>12} {du_lieu[4]:>18,} {du_lieu[5]:>15}\n")
    
    f.write("-"*100 + "\n")
    f.write(f"{'TỔNG DOANH THU:':<70} {tong_doanh_thu:>18,} VNĐ\n")
    f.write("="*100 + "\n\n")
    f.write("="*100 + "\n")
    f.write(" " * 35 + "THỐNG KÊ\n")
    f.write("="*100 + "\n")
    f.write(f"Tổng doanh thu: {tong_doanh_thu:>20,} VNĐ\n")
    f.write(f"Số đơn hàng VIP: {so_don_vip:>20}\n")
    f.write(f"Số đơn hàng Phổ thông: {so_don_pho_thong:>20}\n")
    f.write(f"Doanh thu từ đơn VIP: {doanh_thu_vip:>20,} VNĐ\n")
    f.write(f"Doanh thu từ đơn Phổ thông: {doanh_thu_pho_thong:>20,} VNĐ\n")
    f.write("="*100 + "\n\n")
    f.write("="*100 + "\n")
    f.write(" " * 30 + "DOANH THU TỪNG SẢN PHẨM\n")
    f.write("="*100 + "\n")
    f.write(f"{'STT':<5} {'Tên Sản Phẩm':<40} {'Doanh Thu (VNĐ)':>20}\n")
    f.write("-"*100 + "\n")
    for du_lieu in du_lieu_bao_cao:
        f.write(f"{du_lieu[0]:<5} {du_lieu[1]:<40} {du_lieu[4]:>20,}\n")
    f.write("="*100 + "\n")

# Ghi file CSV
import csv
with open("bao_cao_doanh_thu.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Số TT", "Tên Sản Phẩm", "Đơn Giá (VNĐ)", "Số Lượng", "Doanh Thu (VNĐ)", "Loại Đơn Hàng"])
    
    for du_lieu in du_lieu_bao_cao:
        writer.writerow(du_lieu)
    
    writer.writerow([])
    writer.writerow(["TỔNG DOANH THU", "", "", "", tong_doanh_thu, ""])
    writer.writerow([])
    writer.writerow(["THỐNG KÊ"])
    writer.writerow(["Tổng doanh thu", "", "", "", tong_doanh_thu, ""])
    writer.writerow(["Số đơn hàng VIP", "", "", "", so_don_vip, ""])
    writer.writerow(["Số đơn hàng Phổ thông", "", "", "", so_don_pho_thong, ""])
    writer.writerow(["Doanh thu từ đơn VIP", "", "", "", doanh_thu_vip, ""])
    writer.writerow(["Doanh thu từ đơn Phổ thông", "", "", "", doanh_thu_pho_thong, ""])
    writer.writerow([])
    writer.writerow(["DOANH THU TỪNG SẢN PHẨM"])
    writer.writerow(["Số TT", "Tên Sản Phẩm", "", "", "Doanh Thu (VNĐ)", ""])
    for du_lieu in du_lieu_bao_cao:
        writer.writerow([du_lieu[0], du_lieu[1], "", "", du_lieu[4], ""])

print("\n✅ Đã lưu báo cáo vào file:")
print("   - bao_cao_doanh_thu.txt")
print("   - bao_cao_doanh_thu.csv")
