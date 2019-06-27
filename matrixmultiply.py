#Carlo Colizzi
#27.06.2019

#Multiply matrices, specifically from homogenous coordinates of a point cloud with a roto-translation matrix

import numpy
from readfile import coordinates            #problem importing the file.  In the meantime, the correct file is YCB-Complete.py

#Convert Into homogenous coordinates
for index in len(coordinates):
    countertwo = 0

    for counter in range(0, len(coordinates[index])):

        if coordinates[index][counter] != " ":
            temporaryCoordinates[countertwo] = temporaryCoordinates[countertwo] + coordinates[index][counter]
        else:
            countertwo += 1

    x = temporaryCoordinates[0]
    y = temporaryCoordinates[1]
    z = temporaryCoordinates[2]
    homogenousCoordinates.append(numpy.array([[x], [y], [z], [1]]))

    print(homogenousCoordinates)

#########
#JUST FOR DEV PURPOSES - NEED TO FIGURE OUT HOT TO CONVERT .MAT TO .PY
