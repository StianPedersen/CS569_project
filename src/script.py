import bpy 
from sys import path
path.append('/home/stian/repos/Blender_project/src')
from functions import *
from settings import *

for variations in range(0,nr_different_scenes):
    # Reset all created objects in the scene
    reset_object_collection(bpy.data.collections.get(Collection_Name))

    # Create collection
    myCollection = bpy.data.collections.new(Collection_Name)
    bpy.context.scene.collection.children.link(myCollection)

    x = y = -24 # Start in uppermost corner
    for curr_row in range(0,4,1):
        x = x + (curr_row+8)

        for curr_col in range(0,4,1):
            y = y + (curr_col+8)
            bpy.ops.mesh.primitive_cube_add(size=3, location=(x,y,1.5))
            obj = bpy.context.active_object     
            apply_random_transformation(obj)
            obj.name ='Cube_{}-{}'.format(curr_row,curr_col)
            obj.data.materials.clear()  
            obj.data.materials.append(generate_random_material()) 
            bpy.ops.collection.objects_remove_all()
            bpy.data.collections[Collection_Name].objects.link(obj)
        y = -24 # New row
        
    # Set one to be red aa 1stk farlig object
    positive_object = set_positive_object()

    # Light source
    set_lighting()

    # Camera
    cam = set_camera()

    # Render
    render_image(cam,variations, positive_object)


