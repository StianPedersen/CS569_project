# Synthetic image creation using Blender and computer Graphics

This project contains code to create and evaluate synthetic data created using a Computer Graphics engine. The data is split into a 70-15-15 train/test/valid. 

### Running this project on your own computer
- Download blender. https://www.blender.org/download/
- pip install *requirements.txt* into blenders own python3 (NB! Important, this step may vary for OS)
- Run the following command: blender layout.blend --background --python src/script.py
- Then run Object_Detection: python3 object_detection/model.py

## Macro values
src/settings.py contain all the folder paths needed to save/remove images. Furthermore, settings contains all macro values used throughout the project.
- *COLLECTION_NAME*: Name of the collection that the objects are placed in Blender.
- *DIFFERENT_SCENES*: Number of different scenes with different objects.
- *TRANSFORMATION_FACTOR*: How much the objects shall vary randomly in shape.
- *ROWS*: How many rows the objects should be placed in.
- *COLS*: How many cols the objects should be placed in.
- *ANGLE*: How much the camera angle should rotate between each image.
- *SIZE_Y*: Size of the image size Y.
- *SIZE_X*: Size of the image size X.
- *CLEAN*: If you should delete the images in all folders containing images


## files/
This folder is where the script will initially store all images created. 
- *bb/* contains BB_AMOUNT of images, defined in *src/settings.py*.
- *img/* contains all the images rendered by Blender. Images are of size SIZE_X and SIZE_Y defined in *src/settings.py*.
- *txt_files/* contains text files with the correct  label format for Yolov8.

## src/
Main folder for the synthetic data creation files. Contains the following files:
- *functions.py*: Functions for creating and rendering images. 
- *script.py*: Main overview script file. Also saves and deletes images.    
- *settings.py*: See **settings** headline.
- *transformations.py*: Contains functions for transforming rotations and images.    


## object_detection/
Contains the file structure for the yolov8 object detection model. The file contains one python file *model.py* which contains simple debug prints and one line that initiates a model. The model requires the following structure within the folder:

- test
  - images
  - labels
- train
  - images
  - labels
- valid
  - images
  - labels

The model is downloaded from the web if no model in the *.pt* format is found. *data.yaml* contains the pathings for the yolo model to find.