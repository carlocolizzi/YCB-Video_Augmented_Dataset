# YCB-Video Augmented Dataset

The goal of this project is to create a file that, given the correct input, is able to:
- analyse the scene
- identify objects in the scene
- roto-translate the point cloud of each object to match their position in the scene
- compute a superquadric for each new point cloud

The script works with all UNIX-based systems.  However, in order to minimize changes by the user, a separate script for macOS was created.
### Requirements
In order to function fully and correctly, `YCB-Video Augmented Dataset` requires: 
- `superquadric-lib` - found [here](https://github.com/robotology/superquadric-lib)
- `python3`
- `scipy`
- `numpy`
- `vtk` - found [here](https://gitlab.kitware.com/vtk/vtk)

### Installation
 The python script works instantly, however, the use of a virtual environment is reccomended.  The following commands create a virtual environment with the required dependencies installed.
 ```
 $ virtualenv $NAME_OF_ENV 
 $ source $NAME_OF_ENV/bin/activate
 $ pip3 install -r requirements.txt
 ```

### How to use

Once all requirements are installed, it is sufficient to run the script using
``` 
$ python3 pointcloud-to-superquadric.py
```
\*\* If used on MacOS, use the `pointcould-to-superquadric-macos.py` file instead.

When the file asks for the path to a folder, it is sufficient to drag & drop on the terminal the YCB-Video folder that contains the scene to be analysed.  An example of the input folder can be found at `Example_Scenes/0001`.

The script will then identify the objects in the scene, find the corresponding point clouds, and roto-translate them to match the input frames.  The resulting point cloud will be saved in the same folder under the name `$FRAME_NUMBER-$OBJECT-rototranslated.xyz`.  An example of the output can be found at `Example_Scenes/0000`.

<img src="/Example-Scenes/0000/000001-color.png" height="250" width="350"> <img src="/misc/snapshot02.png" height="250" width="350">

The script will also calculate an adeguate superquadric for each object in the scene, and save its parameters in the file `[frame]-[object]-superquadric.txt` under the format [a <sub>1</sub>, a <sub>2</sub>, a <sub>3</sub>, &epsilon; <sub>1</sub>, &epsilon; <sub>2</sub>, dx, dy, dz, &theta;, &phi;, &psi;]

<img src="https://github.com/robotology/superquadric-model/blob/master/misc/superq-eq.jpg" width="400">

***currently not working***

Once calculated the parameters for the superquadric, the script will proceed to render the superquadric using `vtk` and saving it in the appropriate folder.  

