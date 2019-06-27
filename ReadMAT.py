#Carlo Colizzi
#27.06.2019

#CONVERT .MAT FILES TO .TXT

import os                           #to create .txt file
import scipy.io as sio              #to load .mat files

path = input("Drag .mat file here:")

mat_contents = sio.loadmat(path)            #store contents of mat file

finalPath = path[:-3] + "txt"
os.system("touch " + finalPath)             #create text file in the same position

finalFile = open(finalPath, "w")
finalFile.writelines(str(mat_contents))         #dump contents to text file
