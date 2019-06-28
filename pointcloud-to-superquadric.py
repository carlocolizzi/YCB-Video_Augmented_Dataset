#Carlo Colizzi
#27.06.2019

#This file requires python3, numpy, scipy, superquadric-lib

import sys
import numpy
import os
import scipy.io as sio

path = input("Drag Folder Here:")

#understand the number of objects present in the scene
lines = sum(1 for line in open(path + '/000001-box.txt'))
objects = []
for line in open(path + '/000001-box.txt'):
    objects.append(line.split(None, 1)[0])              #stores names of objects

print(objects)          #DEBUG

#close(path + '/000001-box.txt')         #close connection to object file ??

#store contents of mat file
matpath = path + "/000001-meta.mat"
mat_contents = sio.loadmat(matpath)

#store the point clouds for each object in the scene
pointPath = input('Drag YCB models folder here: ')
contents = [""] * lines
coordinates = [""] * lines

for index in range(0, lines):
    pointClouds = open(pointPath + "/" + objects[index] + "/points.xyz", "rt")   ###CONTINUE HERE
    contents[index] = pointClouds.read()                            #create a variable that holds the text

    #the following wouldn't be needed if python were able to identify lines in this type of file
    coordinates[index] = [""] * contents[index].count("\n")               #initialize array that will hold coordinates with correct length
    countertwo = 0                                                        #counts the number of different points there are
    for counter in range(0, len(contents[index])):
        #print(contents[index][counter])       #DEBUG
        if contents[index][counter] != '\n':                       #separate
            coordinates[index][countertwo] = coordinates[index][countertwo] + contents[index][counter]
        else:
            countertwo += 1

    #print(coordinates[index])                  #print array            #DEBUG
    pointClouds.close()                  #close connection with file

    #############################################################################
    #########################   TESTED UNTIL HERE   #############################       #correct
    #############################################################################

    #Multiply matrices, specifically from homogenous coordinates of a point cloud with a roto-translation matrix

    #Convert regular coordinates into homogenous coordinates
    homogenousCoordinates = [""] * lines
    for indextwo in range(0, len(coordinates[index])):
        countertwo = 0
        temporaryCoordinates = [""] * lines
        temporaryCoordinates[index] = [""] * 3
        for counter in range(0, len(coordinates[index][indextwo])):
            if coordinates[index][indextwo][counter] != " ":
                temporaryCoordinates[index][countertwo] = temporaryCoordinates[index][countertwo] + coordinates[index][indextwo][counter]
            else:
                countertwo += 1

        x = temporaryCoordinates[index][0]
        y = temporaryCoordinates[index][1]
        z = temporaryCoordinates[index][2]
        homogenousCoordinates[index] = []
        homogenousCoordinates[index].append(numpy.array([[x], [y], [z], [1]]))

    print(*homogenousCoordinates, sep=', \n')       #DEBUG

    ################################################################
    ########TESTED UNTIL ABOVE BUT SHOULD WORK UNTIL HERE###########

    positionone = mat_contents['poses']
    #print(positionone)                  #DEBUG

    positionIdentity = [[1, 0, 0, 0],           #to verify correct multiplication
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]

    for indextwo in range(0, lines):
        position[indextwo] = numpy.array([[positionone[0][0][indextwo], positionone[0][1][indextwo], positionone[0][2][indextwo], positionone[0][3][indextwo]],
                                       [positionone[1][0][indextwo], positionone[1][1][indextwo], positionone[1][2][indextwo], positionone[1][3][indextwo]],
                                       [positionone[2][0][indextwo], positionone[2][1][indextwo], positionone[2][2][indextwo], positionone[2][3][indextwo]],
                                       [          0         ,         0           ,           0         ,          1         ]])

    #print(position)             #DEBUG
    #########

    #Convert new coordinates into type of file (.XYZ?)  .obf   #code actually can also use .txt file
        #Create .txt file
    finalPath = pointPath[:-3]+"xyz"
    os.system("touch " + finalPath)
    finalFile = open(finalPath, "w")

    #Multiply HC By roto-translation matrix to obtain new coordinates
    position = numpy.array(position, dtype=float)
    homogenousCoordinates = numpy.array(homogenousCoordinates, dtype=float)
    translatedCoordinates = [""] * len(homogenousCoordinates)
    for index in range(0, len(homogenousCoordinates)):
        translatedCoordinates[index] = numpy.dot(position, homogenousCoordinates[index])

        #write to file
        finalFile.write((str(*translatedCoordinates[index][0])+" "))
        finalFile.write((str(*translatedCoordinates[index][1])+" "))
        finalFile.write((str(*translatedCoordinates[index][2])+"\n"))
        #finalFile.write((str(*translatedCoordinates[index][3])+"\n"))  #this is to reprint the coordinates in homogenous format

    finalFile.close()

#Use Superquadric Algorith to Create Superquadric from translated translatedCoordinates
#os.system("Superquadric-Pipeline-Single " + finalPath)
