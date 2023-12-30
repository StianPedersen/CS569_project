from settings import *
import bpy 
import bmesh
from mathutils import Vector
from random import uniform
import random
import math
from transformation import rotate, camera_view_bounds_2d
import numpy as np

def reset_blender_collection(coll):
    """ Removes all objects from a collection.

    Arguments:
    coll -- The collection to remove all objects from

    """

    if coll:
        obs = [o for o in coll.objects if o.users == 1]
        while obs:
            bpy.data.objects.remove(obs.pop())
        bpy.data.collections.remove(coll)
 

def apply_random_transformation(object):
    """ Applies a random transformation to a blender object.

    Arguments:
    object -- The object to apply the transformations on

    """

    # First set object to edit mode 
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select current mesh 
    mesh = object.data

    # select bmesh: Unified way of enabling to select vertices, faces etc.
    bm = bmesh.from_edit_mesh(mesh)

    # Apply random transformation defined by TRANSFORMATION_FACTOR in settings.
    # Applied to the XY coordinates of the selected bmesh
    for v in bm.verts:
        if not v.select:
            continue
        v.co.xy += Vector([uniform(-TRANSFORMATION_FACTOR, TRANSFORMATION_FACTOR) for axis in "xy"])

    # Update the mesh
    bmesh.update_edit_mesh(mesh)

    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

def generate_random_material():
    """ Creates a random material.
    
    Creates three nodes: BSDFDiffuse, BSDFGlossy and MIXshader. Random values on between 0-1
    are set on each of these node. Further the nodes are connected to an OutputNode. This
    new material is returned.

    Arguments: 
    None

    Returns:
    A new BSDF material with random set values.  

    """    

    mat = bpy.data.materials.new(name="Material") 
    mat.use_nodes = True 
    nodes = mat.node_tree.nodes 
    nodes.clear()

    # Create output node
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )

    # Add diffuse node 
    diffuse = nodes.new(type="ShaderNodeBsdfDiffuse") 
    diffuse.inputs[0].default_value = (random.random(), random.random(), random.random(), 1) 
 
    # Add glossy node 
    glossy = nodes.new(type="ShaderNodeBsdfGlossy") 
    glossy.inputs[0].default_value = (random.random(), random.random(), random.random(), 1) 
 
    # Add mix node 
    mix = nodes.new(type="ShaderNodeMixShader") 
    mix.inputs['Fac'].default_value = random.random() 
 
    # Connect diffuse, glossy and mix to output node
    links = mat.node_tree.links 
    links.new(diffuse.outputs[0], mix.inputs[1]) 
    links.new(glossy.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0],output.inputs[0])
 
    return mat 

def set_positive_object():
    """ Sets one random object to the material intended for object detection.

    Selects one random object based on the amount of COLS and ROWS. This object gets a specific
    color and material 

    Arguments:
    none

    Returns:
    The positive object
    
    """

    # Define the name of the material
    mat_find = bpy.data.materials.new(name='Positive_Material')
    mat_find.use_nodes=True

    # Create node tree with specific values
    mat_2 = mat_find.node_tree.nodes
    mat_2['Principled BSDF'].inputs['Metallic'].default_value=0.0
    mat_2['Principled BSDF'].inputs['Roughness'].default_value=0.5
    mat_2['Principled BSDF'].inputs['Base Color'].default_value=(1.0, 0.0, 0.0, 1.0)
    mat_2['Principled BSDF'].inputs['Roughness'].default_value=0.167

    # Select a random object in the COLS and ROWS
    select_random_col = random.randint(0,COLS-1)
    select_random_row = random.randint(0,ROWS-1)
    positive_object = bpy.data.collections[COLLECTION_NAME].objects.get("Cube_{}-{}".format(select_random_col,select_random_row))
    
    # Apply the material
    positive_object.data.materials[0] = mat_find
    return positive_object

def set_lighting():
    """ Chooses a random light sources and places it randomly in a circle which is encapsulated by the bottom plane.

    Randomly selects a int between 0-3 which represents the four different light sources SPOT, SUN, AREA and POINT.
    Every light is places randomly within a circle that follows the size of the bottom plane. In other words, the 
    diameter of the circle and the plane is equal. Following, each light source has randomized parameters specific 
    for the light source. Specific randomization is needed because the different lightsources vary differently. In
    example, the sun light source cannot use energy 6k to 13k (As the spot) and uses values between 0.5 to 1.5. 

    Arguments:
    None
    
    """

    # Randomly select a number between 0.3
    light_type_select = random.randint(0,3) 
    
    # Select a random angle and radius in the circle
    angle = random.randint(0,360)
    radius = random.randint(0,20) # Bottom plate is -20 -> 20

    # Calculate x,y coordinates using the random radius and angle
    x = radius * np.sin(np.pi * 2 * (angle/360))
    y = radius * np.cos(np.pi * 2 * (angle/360))

    # Spotlight
    if light_type_select == 0:
        light_data = bpy.data.lights.new('light', type='SPOT')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[COLLECTION_NAME].objects.link(light)
        light.location = (x, y, 20)  

        # Random spot_size
        light.data.spot_size = random.randint(157,314) / 100
        
        # Random energy
        light.data.energy= random.randint(6000,13000)

    # Sunlight
    elif light_type_select == 1:
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[COLLECTION_NAME].objects.link(light)
        light.location = (x, y, 20)  

        # Set random light
        light.data.energy = random.randint(5,15) / 10

    # Arealight
    elif light_type_select == 2:
        light_data = bpy.data.lights.new('light', type='AREA')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[COLLECTION_NAME].objects.link(light)
        light.location = (x, y, 20)  

        # Set random light
        light.data.energy = random.randint(2000,6000)

        # Set random size
        light.data.size = random.randint(20,60)

    # Pointlight
    else:
        light_data = bpy.data.lights.new('light', type='POINT')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[COLLECTION_NAME].objects.link(light)
        light.location = (x, y, 20)  

        # Set random light
        light.data.energy=8000.0

def set_camera():
    """ Adds a camera for rendering.

    This function does not have any randomization as it only creates the camera and its respective 
    attributes. The randomization of camera position is applied in the render_image function

    Arguments:
    None
    
    """
    # Create camera and link to collection
    cam_data = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_data)
    bpy.data.collections[COLLECTION_NAME].objects.link(cam)
    
    # Set attributes 
    scene = bpy.context.scene
    scene.camera=cam
    cam.location=(20, -30, 40)
    cam.data.lens_unit = 'FOV'
    cam.data.angle = math.radians(110)
    
    # Tracks the camera to the plane
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target=bpy.data.collections['Static_Collection'].objects.get("Plane")
    return cam

def render_image(cam, variations, positive_cube):
    """ Renders a image, image with boundingbox and creates the .txt file.

    This functions takes the created camera in set_camera() and rotates it stepwise by ANGLE (see settings)
    and caputres the image in each step of ANGLE that fits into 360 degrees. Furthermore, a bb image is created
    so a visual representation can be seen of the created images (mainly for debug purposes). When the bb iamge
    is created a .txt file is also created needed for the Yolov8 model in further steps
    
    Arguments
    cam -- Camera object
    variations -- the current variation (needed for naming purposes)
    positive_cube -- The positive cube needed for creating the bb
    """
    
    # Set rendering paramters
    scene = bpy.context.scene
    scene.render.image_settings.file_format='PNG'
    scene = bpy.data.scenes['Scene']
    camera_object = bpy.data.collections[COLLECTION_NAME].objects['camera']

    # Create an image for each angle able to fit into 360 degrees 
    for angle in range(0, 360, ANGLE):
            
            # Rotate the camera around the Z axis
            cam.location = rotate(cam.location, 60, axis=(0, 0, 1))
            
            # Create the filename
            file_name = "scrap_" + str(variations) + "_" + str(angle)

            # Save image
            scene.render.filepath= SAVE_PATH + "img/" + file_name
            bpy.ops.render.render(write_still=1)

            # Create the bb image and .txt file
            camera_view_bounds_2d(scene, camera_object, positive_cube, file_name)