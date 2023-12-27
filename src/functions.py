from settings import *
import bpy 
import bmesh
from mathutils import Vector
from random import uniform
import random
import math
from boundingbox import camera_view_bounds_2d
from transformation import rotate
import numpy as np



def reset_object_collection(coll):
    if coll:
        obs = [o for o in coll.objects if o.users == 1]
        while obs:
            bpy.data.objects.remove(obs.pop())
        bpy.data.collections.remove(coll)
 
def apply_random_transformation(current_object):
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = current_object.data
    bm = bmesh.from_edit_mesh(mesh)
    for v in bm.verts:
        if not v.select:
            continue
        v.co.xy += Vector([uniform(-change_factor, change_factor) for axis in "xy"])
    bmesh.update_edit_mesh(mesh)
    bpy.ops.object.mode_set(mode='OBJECT')

def generate_random_material():    
    mat = bpy.data.materials.new(name="Material") 
    mat.use_nodes = True 
    nodes = mat.node_tree.nodes 
    nodes.clear()

    # Add output node
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
 
    # Connect nodes 
    links = mat.node_tree.links 
    links.new(diffuse.outputs[0], mix.inputs[1]) 
    links.new(glossy.outputs[0], mix.inputs[2])
    links. new(mix.outputs[0],output.inputs[0])
 
    return mat 

def set_positive_object():
    mat_find = bpy.data.materials.new(name='Material_red')
    mat_find.use_nodes=True
    mat_2 = mat_find.node_tree.nodes
    mat_2['Principled BSDF'].inputs['Metallic'].default_value=0.0
    mat_2['Principled BSDF'].inputs['Roughness'].default_value=0.5
    mat_2['Principled BSDF'].inputs['Base Color'].default_value=(1.0, 0.0, 0.0, 1.0)
    mat_2['Principled BSDF'].inputs['Roughness'].default_value=0.167
    select_random_col = random.randint(0,4-1)
    select_random_row = random.randint(0,4-1)
    print(select_random_col," ***", select_random_row)
    positive_cube = bpy.data.collections[Collection_Name].objects.get("Cube_{}-{}".format(select_random_col,select_random_row))
    positive_cube.data.materials[0] = mat_find
    return positive_cube

def set_lighting():
    random_select = random.randint(0,3) 
    angle = random.randint(0,360)
    radius = random.randint(0,20) # Bottom plate is -20 -> 20
    x = radius * np.sin(np.pi * 2 * (angle/360))
    y = radius * np.cos(np.pi * 2 * (angle/360))

    if random_select == 0:
        light_data = bpy.data.lights.new('light', type='SPOT')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[Collection_Name].objects.link(light)
        light.location = (x, y, 20)  
        
        # Random spot_size
        light.data.spot_size = random.randint(157,314) / 100
        
        # Random energy
        light.data.energy= random.randint(6000,13000)

    elif random_select == 1:
        light_data = bpy.data.lights.new('light', type='SUN')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[Collection_Name].objects.link(light)
        light.location = (0, 0, 20)  

        # Set random light
        light.data.energy = random.randint(5,15) / 10

    elif random_select == 2:
        light_data = bpy.data.lights.new('light', type='AREA')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[Collection_Name].objects.link(light)
        # Set random location
        light.location = (0, 0, 20)  

        # Set random light
        light.data.energy = random.randint(2000,6000)
        light.data.size = random.randint(20,60)

    else:
        light_data = bpy.data.lights.new('light', type='POINT')
        light = bpy.data.objects.new('light', light_data)
        bpy.data.collections[Collection_Name].objects.link(light)
        # Set random location
        light.location = (0, 0, 20)  
        # Set random light
        light.data.energy=8000.0

def set_camera():
    cam_data = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_data)
    bpy.data.collections[Collection_Name].objects.link(cam)
    # add camera to scene
    scene = bpy.context.scene
    scene.camera=cam
    cam.location=(20, -30, 40)
    cam.data.lens_unit = 'FOV'
    cam.data.angle = math.radians(110)
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target=bpy.data.collections['Static_Collection'].objects.get("Plane")
    return cam

def render_image(cam,variations,positive_cube):
    scene = bpy.context.scene
    scene.render.image_settings.file_format='PNG'
    filename = f'/home/stian/repos/Blender_project/img/squares_{variations}'

    scene = bpy.data.scenes['Scene']
    camera_object = bpy.data.collections[Collection_Name].objects['camera']

    for angle in range(0, 360, 360):
            cam_location = cam.location
            cam.location = rotate(cam_location, 60, axis=(0, 0, 1))

            file_name = filename+"_"+str(angle)
            scene.render.filepath=file_name
            bpy.ops.render.render(write_still=1)
            camera_view_bounds_2d(scene, camera_object, positive_cube,file_name)