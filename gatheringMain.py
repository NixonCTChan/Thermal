import time
import board
import busio
import adafruit_mlx90640
import gatheringFunc as gathering
import os
import shutil

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

location = gathering.getting_location()

keyPress = "0"
name = 0
if os.path.exists("Calibration/%s" %location):
    shutil.rmtree("Calibration/%s"%location)
while keyPress != "x":
    print("Press x to stop taking pictures, press any key to continue taking pictures.")
    keyPress = input()
    gathering.take_and_save(mlx,location,name)
    name += 1

print("Computing bins and averages for %s...\n" % location)
gathering.compute_bins_averages(location)
