#Carlo Colizzi
#27.06.2019

#This file requires python3, numpy, scipy, superquadric-lib
from __future__ import print_function
import sys                      #needs to be UNIX-based
import numpy
import os
import scipy.io as sio
import glob
import vtk
import math
from scipy.spatial.transform import Rotation as R
#import ipdb; ipdb.set_trace()                          #to trace algorithm and debugging


#visualizes superquadrics given an array with parameters
def visualizeSuperquadric(parameters, fn):
    colors = vtk.vtkNamedColors()

    colors.SetColor('light_cyan', [100, 255, 255, 255])
    colors.SetColor('light_magenta', [255, 100, 255, 255])

    #  Verify input arguments
    if fn:
        # Read the image
        jpeg_reader = vtk.vtkPNGReader()
        if not jpeg_reader.CanReadFile(fn):
            print("Error reading file:", fn)
            return

        jpeg_reader.SetFileName(fn)
        jpeg_reader.Update()
        image_data = jpeg_reader.GetOutput()
    else:
        canvas_source = vtk.vtkImageCanvasSource2D()
        canvas_source.SetExtent(0, 100, 0, 100, 0, 0)
        canvas_source.SetScalarTypeToUnsignedChar()
        canvas_source.SetNumberOfScalarComponents(3)
        canvas_source.SetDrawColor(colors.GetColor4ub('warm_grey'))
        canvas_source.FillBox(0, 100, 0, 100)
        canvas_source.SetDrawColor(colors.GetColor4ub('light_cyan'))
        canvas_source.FillTriangle(10, 10, 25, 10, 25, 25)
        canvas_source.SetDrawColor(colors.GetColor4ub('light_magenta'))
        canvas_source.FillTube(75, 75, 0, 75, 5.0)
        canvas_source.Update()
        image_data = canvas_source.GetOutput()

    # Create an image actor to display the image
    image_actor = vtk.vtkImageActor()
    image_actor.SetInputData(image_data)

    # Create a renderer to display the image in the background
    background_renderer = vtk.vtkRenderer()
    scene_renderer = vtk.vtkRenderer()


    for index in range(0,len(parameters)):
    # Create a superquadric
        superquadric_actor = vtk.vtkActor()
        superquadric_source = vtk.vtkSuperquadricSource()
        superquadric_source.SetPhiRoundness(parameters[index][3])
        superquadric_source.SetThetaRoundness(parameters[index][4])
        superquadric_source.SetScale(parameters[index][0], parameters[index][1], parameters[index][2])
        #superquadric_source.SetModelBounds(-parameters[index][0], parameters[index][0],-parameters[index][1],parameters[index][1],-parameters[index][2],parameters[index][2])
        # Create a mapper and actor
        superquadric_mapper = vtk.vtkPolyDataMapper()
        superquadric_mapper.SetInputConnection(superquadric_source.GetOutputPort())

        superquadric_actor.SetMapper(superquadric_mapper)
        vtk_transform = vtk.vtkTransform()
        vtk_transform.Translate(parameters[index][5], parameters[index][6], parameters[index][7])
        vtk_transform.RotateWXYZ((180.0/math.pi)*parameters[index][11], parameters[index][8], parameters[index][9], parameters[index][10])
        vtk_transform.RotateX(-90.0)
        superquadric_actor.SetUserTransform(vtk_transform)
        superquadric_actor.GetProperty().SetColor(0.0,0.3,0.1+(index/len(parameters)))
        superquadric_source.SetSize(1)
        superquadric_source.SetCenter(0.0, 0.0, 0.0)

        scene_renderer.AddActor(superquadric_actor)

        print(parameters[index])
        print(index)


    render_window = vtk.vtkRenderWindow()

    # Set up the render window and renderers such that there is
    # a background layer and a foreground layer
    background_renderer.SetLayer(0)
    background_renderer.InteractiveOff()
    scene_renderer.SetLayer(1)
    render_window.SetNumberOfLayers(2)
    render_window.AddRenderer(background_renderer)
    render_window.AddRenderer(scene_renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Add actors to the renderers
    #scene_renderer.AddActor(superquadric_actor)
    background_renderer.AddActor(image_actor)

    # Render once to figure out where the background camera will be
    render_window.Render()

    # Set up the background camera to fill the renderer with the image
    origin = image_data.GetOrigin()
    spacing = image_data.GetSpacing()
    extent = image_data.GetExtent()

    camera = vtk.vtkCamera()

    #camera = background_renderer.GetActiveCamera()
    camera.ParallelProjectionOn()




    xc = origin[0] + 0.5 * (extent[0] + extent[1]) * spacing[0]
    yc = origin[1] + 0.5 * (extent[2] + extent[3]) * spacing[1]
    # xd = (extent[1] - extent[0] + 1) * spacing[0]
    yd = (extent[3] - extent[2] + 1) * spacing[1]
    d = camera.GetDistance()
    camera.SetParallelScale(0.5 * yd)
    camera.SetFocalPoint(xc, yc, 0.0)
    camera.SetPosition(xc, yc, d)
    print(xc, yc, d)
    scene_renderer.SetActiveCamera(camera)
    # Render again to set the correct view
    render_window.Render()

    # Interact with the window
    render_window_interactor.Start()

# Calculates Rotation Matrix given euler angles.  Theta is a list
def eulertoangle(roll, pitch, yaw):
    yawMatrix = numpy.matrix([
    [math.cos(yaw), -math.sin(yaw), 0],
    [math.sin(yaw), math.cos(yaw), 0],
    [0, 0, 1]
    ])

    pitchMatrix = numpy.matrix([
    [math.cos(pitch), 0, math.sin(pitch)],
    [0, 1, 0],
    [-math.sin(pitch), 0, math.cos(pitch)]
    ])

    rollMatrix = numpy.matrix([
    [1, 0, 0],
    [0, math.cos(roll), -math.sin(roll)],
    [0, math.sin(roll), math.cos(roll)]
    ])

    R = yawMatrix * pitchMatrix * rollMatrix

    theta = math.acos(((R[0, 0] + R[1, 1] + R[2, 2]) - 1) / 2)
    multi = 1 / (2 * math.sin(theta))

    rx = multi * (R[2, 1] - R[1, 2])
    ry = multi * (R[0, 2] - R[2, 0])
    rz = multi * (R[1, 0] - R[0, 1])
    angleAxis = []
    angleAxis.append(rx)
    angleAxis.append(ry)
    angleAxis.append(rz)
    angleAxis.append(theta)
    angleAxis = numpy.array(angleAxis)

    return angleAxis

path = input("Drag Folder Here:")
#path = "/Users/Carlo/Desktop/IIT/YCB_Video_Dataset/data/0000"

frames = []                                                             ##
for name in sorted(glob.glob(path + "/??????-box.txt")):                ##Stores name of each frame (Ex. 000001)
    frames.append(name[-14:-8])                                         ##

#pointPath = input('Drag YCB models folder here: ')
pointPath = "../models"

progressCounter = 0
superquadricPar = [""] * len(frames)



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
    superquadricPar[progressCounter] = [""] * numOfObjects
    superquadric = [""] * numOfObjects
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

        #print(*homogenousCoordinates, sep=', \n')       #DEBUG

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
        finalPath = path + "/" + filename + "-" + objects[index] + "-rototranslated.xyz"      #one per frame
        os.system("touch " + finalPath)
        os.system("touch " + finalPath[0:-19] + "-superquadric.txt")
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

        #Use Superquadric Algorith to Create Superquadric from translated translatedCoordinates
        #os.system("Superquadric-Pipeline-Single " + finalPath + " | grep 'Superquadric estimated' >> " + finalPath[0:-19] + "-superquadric.txt")             #this works only with icub installed              #save to file
        tempParameters = os.popen("Superquadric-Pipeline-Single " + finalPath + " | grep 'Superquadric estimated'").read()          #save to variable
        #print(superquadricPar[progressCounter][index])      #DEBUG
        print(tempParameters)
        tempParameters = tempParameters[61:-2].split(", ")
        superquadricPar[progressCounter][index] = numpy.array(list(map(float, tempParameters)))

        AngleAxis[0] = R.from_euler("z", superquadricPar[progressCounter][index][8], degrees=True)
        AngleAxis[1] = R.from_euler("y", superquadricPar[progressCounter][index][9], degrees=True)
        AngleAxis[2] = R.from_euler("z", superquadricPar[progressCounter][index][10], degrees=True)
        #need to figure out how to get theta (angleAxis[3])

        #angleAxis = eulertoangle(superquadricPar[progressCounter][index][8], superquadricPar[progressCounter][index][9], superquadricPar[progressCounter][index][10])
        superquadric[index] = numpy.array([superquadricPar[progressCounter][index][0],
                                 superquadricPar[progressCounter][index][1],
                                 superquadricPar[progressCounter][index][2],
                                 superquadricPar[progressCounter][index][3],
                                 superquadricPar[progressCounter][index][4],
                                 superquadricPar[progressCounter][index][5],
                                 superquadricPar[progressCounter][index][6],
                                 superquadricPar[progressCounter][index][7],
                                 angleAxis[0],
                                 angleAxis[1],
                                 angleAxis[2],
                                 angleAxis[3]])


    visualizeSuperquadric(superquadric, fn=(path + "/" + filename + "-color.png"))

        #Show Progress
    print( str(int((int(frames[progressCounter]) / int(frames[-1]))*100)) + "% Completed")
    progressCounter += 1
