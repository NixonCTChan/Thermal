import time
import board
import busio
import adafruit_mlx90640
import os
import math
import shutil

def getting_location():
    print("Please enter the name of this location.")
    location = input()
    return location

def take_and_save(mlx, location, name):
    frame = [0] * 768
    imageTaken = 0
    try: 
        mlx.getFrame(frame)
    except:
        print("mlx failed to take a picture\n")
        imageTaken = 1

    if imageTaken == 0:
        if not os.path.exists("Calibration/%s" %location):
            os.mkdir("Calibration/%s"%location)
        if os.path.exists("Calibration/%s/%s.txt" %(location,name)):
            os.remove("Calibration/%s/%s.txt" %(location,name))

        imageFile = open("Calibration/%s/%s.txt" %(location,name),"w+")
        for i in range(768):
            imageFile.write(str(round(frame[i],3))+"\n")
        print("Data saved for %s" %name)
        imageFile.close()

def compute_bins_averages(location):
    #extract all images in the calibration location into a frames array
    path, dirs, files = next(os.walk("Calibration/%s" %location))
    fileCount = len(files)
    totalFrames = [0] * 768
    for i in range(fileCount):
        imageFile = open("Calibration/%s/%s.txt" %(location, i))
        for line in range(768):
            totalFrames[line] += float(imageFile.readline().strip("\n"))
    
    #finding max, min, and range
    max = -1
    min = 100
    for line in range(768):
        totalFrames[line] = totalFrames[line]/fileCount
        if totalFrames[line] > max:
            max = totalFrames[line]
        if totalFrames[line] < min:
            min = totalFrames[line]
    
    tempRange = int(math.floor(max))-int(math.floor(min))

    #creating bins and adding up the pixels into the bins
    bins = [0] * tempRange

    for i in range(768):
        temperature = totalFrames[i]
        bins[int(math.floor(temperature))-int(math.floor(min))-1] += 1
    
    #creating file, printing min, max, and bins
    if os.path.exists("Data/%s.txt" %location):
        os.remove("Data/%s.txt" %location)
    dataFile = open("Data/%s.txt" %location, "w+")
    dataFile.write(str(int(math.floor(min)))+"\n")
    dataFile.write(str(int(math.floor(max)))+" \n")

    for i in range(tempRange):
        dataFile.write(str(bins[i]) + "\n")
    
    #writing average temperatures
    for i in range(768):
        dataFile.write(str(totalFrames[i])+ "\n")

    dataFile.close()

    
