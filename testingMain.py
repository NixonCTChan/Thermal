import time
import board
import busio
import adafruit_mlx90640
import os
import testingFunc as testing

PRINT_TEMPERATURES = False
PRINT_ASCIIART = True

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

location, sensitivity = testing.get_location_sensitivity()

minTemp, maxTemp, distribution, baseFrame = testing.extract_data(location)
keypress=" "
while keypress!="x":
    print("Press anykey to take a picture, press x to stop taking pictures.")
    keypress=input()
    if keypress=="x":
        break
    deltaDistribution, deltaFrame, outsideDistribution, takenFrame= testing.compute_distributions_data(mlx,minTemp,maxTemp,baseFrame,distribution)
    anomaly = testing.compute_final_score(sensitivity, deltaDistribution, deltaFrame, outsideDistribution)
    if anomaly:
        print("ANOMALY")
        testing.print_save_anomalous(takenFrame, location)
    else:
        print("NOT ANOMALOUS")
        max = -1
        min = 100
        for i in range(768):
            if takenFrame[i] > max:
                max = takenFrame[i]
            if takenFrame[i] < min:
                min = takenFrame[i]
        for i in range(768):
            takenFrame[i] = (takenFrame[i]-min)/(max-min)
        for h in range(24):
            for w in range(32):
                t = takenFrame[h * 32 + w]
                c = "&"
                if t < 0.1:
                    c = " "
                elif t < 0.2:
                    c = "."
                elif t < 0.3:
                    c = "-"
                elif t < 0.4:
                    c = "*"
                elif t < 0.5:
                    c = "+"
                elif t < 0.6:
                    c = "x"
                elif t < 0.7:
                    c = "%"
                elif t < 0.8:
                    c = "#"
                elif t < 0.9:
                    c = "X"
                print(c, end="")

            print()

        print()

