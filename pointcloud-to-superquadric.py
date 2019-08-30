#Carlo Colizzi
#27.06.2019

#This file requires python3, numpy, scipy, superquadric-lib
#Doesnt use VTK.  Go to scripts folder for visualizer


import sys                      #needs to be UNIX-based
import numpy
import os
import scipy.io as sio
import glob
#import ipdb; ipdb.set_trace()                          #to trace algorithm and debugging


path = input("Drag Folder Here:")
#path = "/Users/Carlo/Desktop/IIT/YCB_Video_Dataset/data/0000"
frames = []                                                             ##
for name in sorted(glob.glob(path + "/??????-box.txt")):                ##Stores name of each frame (Ex. 000001)
    frames.append(name[-14:-8])                                         ##

pointPath = input('Drag YCB models folder here: ')
#pointPath = "./models"

progressCounter = 0

for filename in frames:                           #repeat the whole process for each

    #understand the number of objects present in the scene
    numOfObjects = sum(1 for line in open(path + '/'+ filename + '-box.txt'))       #stores the number of objects in the scene
    objects = []                                                                    #stores the names of the objects
    for line in open(path + '/'+ filename + '-box.txt'):
        objects.append(line.split(None, 1)[0])                                      #appends names of objects to list
    #print(objects)          #DEBUG

    #store contents of mat file
    matpath = path + '/'+ filename + '-meta.mat'
    mat_contents = sio.loadmat(matpath)

    #store the point clouds for each object in the scene
    contents = [""] * numOfObjects
    coordinates = [""] * numOfObjects

    for index in range(0, numOfObjects):                    #for each object
        #Load Point Cloud and read its contents
        pointClouds = open(pointPath + "/" + objects[index] + "/points.xyz", "rt")
        contents[index] = pointClouds.read()                            #create a variable that holds the text
        #print("OLD COORDINATES" + str(index))      #DEBUG
        #print(contents[index])                     #DEBUG

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

        #Convert regular coordinates into homogenous coordinates
        homogenousCoordinates = [""] * numOfObjects
        homogenousCoordinates[index] = []

        for indextwo in range(0, len(coordinates[index])):      #repeats itself ~2600 times (each point cloud has 2621 points)
            countertwo = 0
            temporaryCoordinates = [""] * numOfObjects
            temporaryCoordinates[index] = [""] * 3
            for counter in range(0, len(coordinates[index][indextwo])):         #repeats itself 25 times (number of characters in the coordinates of a point)
                #print(coordinates[index][indextwo][counter])
                if coordinates[index][indextwo][counter] != " ":
                    temporaryCoordinates[index][countertwo] = temporaryCoordinates[index][countertwo] + coordinates[index][indextwo][counter]
                else:
                    countertwo += 1

            x = temporaryCoordinates[index][0]
            y = temporaryCoordinates[index][1]
            z = temporaryCoordinates[index][2]
            homogenousCoordinates[index].append(numpy.array([[x], [y], [z], [1]]))
        #print(homogenousCoordinates[index])
        #print(*homogenousCoordinates, sep=', \n')       #DEBUG
        #print(*homogenousCoordinates)


        positionIdentity = [[1, 0, 0, 0],           #to verify correct multiplication
                            [0, 1, 0, 0],           #not used
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]]


        positionone = mat_contents.get('poses')
        #print(positionone)            #DEBUG

        position = [""] * numOfObjects   #THIS IS WRONG
        for indextwo in range(0, numOfObjects):
            position[indextwo] = numpy.array([[positionone[0][0][indextwo], positionone[0][1][indextwo], positionone[0][2][indextwo], positionone[0][3][indextwo]],
                                             [positionone[1][0][indextwo], positionone[1][1][indextwo], positionone[1][2][indextwo], positionone[1][3][indextwo]],
                                             [positionone[2][0][indextwo], positionone[2][1][indextwo], positionone[2][2][indextwo], positionone[2][3][indextwo]],
                                             [           0              ,              0              ,                0           ,                 1         ]])

        #print(position)             #DEBUG
        #print(positionone)

        #Convert new coordinates into type of file (.XYZ?)  .obf   #code actually can also use .txt file
        #Create .xyz file
        finalPath = path + "/" + filename + "-" + objects[index] + "-rototranslated.xyz"        #one per frame
        os.system("touch " + finalPath)
        finalFile = open(finalPath, "w")


        position = numpy.array(position, dtype=float)
        homogenousCoordinatesTest = numpy.array(homogenousCoordinates[index], dtype=float)
        #translatedCoordinates = [0] * numOfObjects
        #translatedCoordinates[index] = []

        #Multiply HC By roto-translation matrix to obtain new coordinates
        for indexthree in range(0, homogenousCoordinatesTest.shape[0]):
            translatedCoordinates= numpy.dot(position[index], homogenousCoordinatesTest[indexthree])
            #print(*translatedCoordinates)
            #write to file
            finalFile.write((str(*translatedCoordinates[0])+" "))
            finalFile.write((str(*translatedCoordinates[1])+" "))
            finalFile.write((str(*translatedCoordinates[2])+"\n"))
            #finalFile.write((str(*translatedCoordinates[index][3])+"\n"))  #this is to reprint the coordinates in homogenous format



        finalFile.close()
        #Show Progress
        print( str(int((int(frames[progressCounter]) / int(frames[-1]))*100)) + "% Completed")
        progressCounter += 1

    #Use Superquadric Algorith to Create Superquadric from translated translatedCoordinates
    #os.system("Superquadric-Pipeline-Single " + finalPath)             #this works only with icub installed
