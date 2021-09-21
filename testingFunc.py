import time
import board
import busio
import adafruit_mlx90640
import os
import math
import shutil
import datetime

BASE_SENSITIVITY = 100
#set location and sensitivity function

def get_location_sensitivity():
    print("Please enter a location.")
    location = str(input())
    sensitivity = 100
    return location, sensitivity

#compute distributions and data
def compute_distributions_data(mlx, minCal, maxCal, calFrame, calDistribution):
    frame = [0] * 768
    try: 
        mlx.getFrame(frame)
        print("Picture taken!")
    except:
        print("mlx failed to take a picture\n")
        return
    tempRange = maxCal-minCal
    distribution = [0] * tempRange
    outsideDistribution = 0

    for i in range(768):
        temperature = frame[i]
        temperatureDifference = int(math.floor(temperature))-int(minCal)
        if temperatureDifference>=tempRange or temperatureDifference<0:
            outsideDistribution+=1
        else:
            distribution[int(math.floor(temperature))-int(minCal)]+=1
    
    deltaDistribution = [0]*tempRange
    for i in range(tempRange):
        deltaDistribution[i] = abs(distribution[i]-calDistribution[i])

    deltaFrame = [0] * 768
    for i in range(768):
        deltaFrame[i] = abs(frame[i]-calFrame[i])
    
    return deltaDistribution, deltaFrame, outsideDistribution, frame
        
#extract data from location file
def extract_data(location):
    try:
        dataFile = open("Data/%s.txt"%location,"r+")
    except:
        print("That location does not exist/has not been calibrated!")
        return
    
    minTemp = int(dataFile.readline().strip("\n"))
    maxTemp = int(dataFile.readline().strip("\n"))
    
    tempRange = maxTemp-minTemp


    distribution = [0] * tempRange
    for i in range(tempRange):
        distribution[i] = int(dataFile.readline().strip("\n"))
    
    frame = [0] * 768
    for i in range(768):
        frame[i] = float(dataFile.readline().strip("\n"))
    return minTemp, maxTemp, distribution, frame

#compute final score
def compute_final_score(sensitivity, deltaDistribution, deltaFrame, outsideDistribution):
    maxDeltaDistribution = -1.0
    maxDeltaFrame = 0.0
    totalSensitivity = (100-sensitivity)/100

    for i in range(len(deltaDistribution)):
        if maxDeltaDistribution<deltaDistribution[i]:
            maxDeltaDistribution=deltaDistribution[i]
    
    for i in range(len(deltaFrame)):
        if maxDeltaFrame<deltaFrame[i]:
            maxDeltaFrame = deltaFrame[i]
    deltaAnomalous = 0.0
    distributionAnomalous = 0.0
    if maxDeltaFrame>7:
        deltaAnomalous=float((maxDeltaFrame-7)/7)
    if maxDeltaDistribution>(0.2*768):
        distributionAnomalous=(maxDeltaDistribution+outsideDistribution/10-(0.2*768))/(0.2*768)
    totalScore = float(1000.0*deltaAnomalous+10.0*distributionAnomalous)
    print ("Total Score is :%s" %totalScore)
    if totalScore>totalSensitivity:
        return True
    else: 
        return False

#output picture
def print_save_anomalous(totalFrames,location):
    max = -1
    min = 100
    if not os.path.exists("Anomalous/%s" %location):
        os.mkdir("Anomalous/%s"%location)
    imageFile = open("Anomalous/%s/%s.txt"%(location,datetime.datetime.now().date()),"w+")
    for i in range(768):
        if totalFrames[i] > max:
            max = totalFrames[i]
        if totalFrames[i] < min:
            min = totalFrames[i]
    for i in range(768):
        totalFrames[i] = (totalFrames[i]-min)/(max-min)
    for h in range(24):
        for w in range(32):
            t = totalFrames[h * 32 + w]
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
            imageFile.write(c+" ")
        print()
        imageFile.write("\n")
    print()
    imageFile.write("\n")
    imageFile.close()