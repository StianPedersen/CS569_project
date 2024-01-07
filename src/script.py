import bpy 
from sys import path
path.append('/home/stian/repos/CS569_project/src')
from functions import *
from settings import *
import os
import shutil
import glob

if CLEAN:
    # Remove all contents of the files in object_detection/test
    detection_test_images = '/home/stian/repos/CS569_project/object_detection/test/images/*'
    detection_test_labels= '/home/stian/repos/CS569_project/object_detection/test/labels/*'
    for ti in glob.glob(detection_test_images):
        os.remove(ti)
    for  tl in glob.glob(detection_test_labels):
        os.remove(tl)
    

    # Remove all contents of the files in object_detection/valid
    detection_valid_images = '/home/stian/repos/CS569_project/object_detection/valid/images/*'
    detection_valid_labels= '/home/stian/repos/CS569_project/object_detection/valid/labels/*'
    for vi in glob.glob(detection_valid_images):
        os.remove(vi)
    for  vl in  glob.glob(detection_valid_labels):
        os.remove(vl)

    # Remove all contents of the files in object_detection/train
    detection_train_images = '/home/stian/repos/CS569_project/object_detection/train/images/*'
    detection_train_labels= '/home/stian/repos/CS569_project/object_detection/train/labels/*'
    for ti in glob.glob(detection_train_images):
        os.remove(ti)
    for tl in glob.glob(detection_train_labels):
        os.remove(tl)
    
    # Remove all contents of the files in files/
    files_img = '/home/stian/repos/CS569_project/files/img/*'    
    files_txt_files = '/home/stian/repos/CS569_project/files/txt_files/*'
    files_bb = '/home/stian/repos/CS569_project/files/bb/*'
    for i in glob.glob(files_img):
         os.remove(i)
    for t in glob.glob(files_txt_files):
        os.remove(t)
    for b in glob.glob(files_bb):
        os.remove(b)

for variations in range(0,DIFFERENT_SCENES):
    # Reset all created objects in the scene
    reset_blender_collection(bpy.data.collections.get(COLLECTION_NAME))

    # Create collection
    bpy.context.scene.collection.children.link(bpy.data.collections.new(COLLECTION_NAME))
    
    # Start in uppermost corner and fill objects in a grid 
    x = y = -24 

    for curr_row in range(0, ROWS,1):
        x = x + curr_row + 8

        for curr_col in range(0,COLS,1):
            y = y + curr_col + 8
            bpy.ops.mesh.primitive_cube_add(size=3, location=(x,y,1.5))
            active_obj = bpy.context.active_object     
            apply_random_transformation(active_obj)
            active_obj.name ='Cube_{}-{}'.format(curr_row,curr_col)
            active_obj.data.materials.clear()  
            active_obj.data.materials.append(generate_random_material()) 
            bpy.ops.collection.objects_remove_all()
            bpy.data.collections[COLLECTION_NAME].objects.link(active_obj)
        y = -24 # New row    
    # Set one random positive object for the object detection system to detect
    positive_object = set_positive_object()

    # Set a random light
    set_lighting()

    # Camera
    cam = set_camera()

    # Render
    render_image(cam, variations, positive_object)

# Move images to object_detection folder
src = "/home/stian/repos/CS569_project/files/img"
allFileNames = os.listdir(src)
np.random.shuffle(allFileNames)
train_FileNames, val_FileNames, test_FileNames = np.split(np.array(allFileNames),
                                                          [int(len(allFileNames)*0.7), int(len(allFileNames)*0.85)])

txt_train_FileNames = train_FileNames
txt_val_FileNames   = val_FileNames
txt_test_FileNames  = test_FileNames

train_FileNames = [src+'/'+ name for name in train_FileNames.tolist()]
val_FileNames = [src+'/' + name for name in val_FileNames.tolist()]
test_FileNames = [src+'/' + name for name in test_FileNames.tolist()]

txt_src = "/home/stian/repos/CS569_project/files/txt_files"

txt_train_FileNames = [txt_src+'/'+ name for name in txt_train_FileNames.tolist()]
txt_val_FileNames = [txt_src+'/' + name for name in txt_val_FileNames.tolist()]
txt_test_FileNames = [txt_src+'/' + name for name in txt_test_FileNames.tolist()]

txt_train_FileNames = [w.replace('.png', '.txt') for w in txt_train_FileNames]
txt_val_FileNames = [w.replace('.png', '.txt') for w in txt_val_FileNames]
txt_test_FileNames = [w.replace('.png', '.txt') for w in txt_test_FileNames]



print('Total images: ', len(allFileNames))
print('Training: ', len(train_FileNames))
print('Validation: ', len(val_FileNames))
print('Testing: ', len(test_FileNames))

# Copy-pasting images
for name in train_FileNames:
    shutil.copy(name, "/home/stian/repos/CS569_project/object_detection/train/images")

for name in val_FileNames:
    shutil.copy(name, "/home/stian/repos/CS569_project/object_detection/valid/images")

for name in test_FileNames:
    shutil.copy(name, "/home/stian/repos/CS569_project/object_detection/test/images")

# Copy-pasting images
for name in txt_train_FileNames:
    shutil.copy(name, "/home/stian/repos/CS569_project/object_detection/train/labels")

for name in txt_val_FileNames:
    shutil.copy(name, "/home/stian/repos/CS569_project/object_detection/valid/labels")

for name in txt_test_FileNames:
    shutil.copy(name, "/home/stian/repos/CS569_project/object_detection/test/labels")