#Carlo Colizzi
#27.06.2019

#This file requires python3, numpy

import sys
import numpy
import os

#First File
#Read and Extract contents of files, specifically the coordinates of points on a point cloud.

path = input('Drag point cloud file here: ')
pointCloud = open(path, "rt")       #path to file here
contents = pointCloud.read()        #create a variable that holds the text

countertwo = 0                                          #counts the number of different points there are
coordinates = [""] * contents.count("\n")               #initialize array that will hold coordinates with correct length

#the following wouldn't be needed if python were able to identify lines in this type of file
for counter in range(0, len(contents)):
    #print(contents[counter])       #DEBUG
    if contents[counter] != '\n':                       #separate
        coordinates[countertwo] = coordinates[countertwo] + contents[counter]
    else:
        countertwo += 1
#print(coordinates)                  #print array            #DEBUG
pointCloud.close()                  #close connection with file

#############################################################################
#############################################################################

#Second File
#Multiply matrices, specifically from homogenous coordinates of a point cloud with a roto-translation matrix

#Convert regular coordinates into homogenous coordinates
homogenousCoordinates = []
for index in range(0, len(coordinates)):
    countertwo = 0
    temporaryCoordinates = [""] * 3
    for counter in range(0, len(coordinates[index])):

        if coordinates[index][counter] != " ":
            temporaryCoordinates[countertwo] = temporaryCoordinates[countertwo] + coordinates[index][counter]
        else:
            countertwo += 1

    x = temporaryCoordinates[0]
    y = temporaryCoordinates[1]
    z = temporaryCoordinates[2]
    homogenousCoordinates.append(numpy.array([[x], [y], [z], [1]]))

print(*homogenousCoordinates, sep=', \n')       #DEBUG

#Obtain
#########
#JUST FOR DEV PURPOSES - NEED TO FIGURE OUT HOT TO CONVERT .MAT TO .PY
positionone = [[ 0.02338846,  0.55960668, -0.89716775],
            [-0.63092591, -0.82383616,  0.11799638],
            [ 0.77549179,  0.09019791, -0.42563812],
            [-0.03063223,  0.05854423,  0.07523607]]

position = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]]
#########

#Multiply HC By roto-translation matrix to obtain new coordinates
position = numpy.array(position, dtype=float)
homogenousCoordinates = numpy.array(homogenousCoordinates, dtype=float)
translatedCoordinates = [""] * len(homogenousCoordinates)
for index in range(0, len(homogenousCoordinates)):
    translatedCoordinates[index] = numpy.dot(position, homogenousCoordinates[index])

#Convert new coordinates into type of file (.XYZ?)  .obf   #code actually can also use .txt file
    #Create .txt file
finalPath = "newfile.txt"
os.system("touch " + finalPath)        #may not be needed
finalFile = open(finalPath, "w")

    #write to file
finalFile.writelines(str(translatedCoordinates))
finalFile.close()

#Use Superquadric Algorith to Create Superquadric from translated translatedCoordinates
os.system("Superquadric-Pipeline-Single " + finalPath)
