tien = 10000000
lai_suat= 0.5/100

for i in range(1, 13, 1):
    tien = tien+ tien*lai_suat

    print("số tiền sau tháng ", i, "là:", tien)