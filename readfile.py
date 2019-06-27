#Carlo Colizzi
#26.06.2019

#Read and Extract contents of files, specifically the coordinates of points on a point cloud.


def read(path):                         #defined as a function so it can later be called in other files
    pointCloud = open(path, "rt")       #path to file here
    contents = pointCloud.read()        #create a variable that holds the text

    countertwo = 0                                          #counts the number of different points there are
    coordinates = [""] * contents.count("\n")               #initialize array that will hold coordinates with correct length

#the following wouldn't be needed if python were able to identify lines in this type of file
    for counter in range(0, len(contents)):
        #print(contents[counter])       #debug
        if contents[counter] != '\n':                       #separate
            coordinates[countertwo] = coordinates[countertwo] + contents[counter]
        else:
            countertwo += 1
        #coordinates.append(line)
    #coordinates = list(contents)
    print(coordinates)                  #print array
    #print(contents)
    pointCloud.close()                  #close connection with file


#read(input('Input path to point cloud, enclosed in inverted commas(""): '))
