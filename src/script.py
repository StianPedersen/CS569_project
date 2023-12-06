import bpy 
import bmesh
import math
import random
from mathutils import Vector
from random import uniform

from sys import path
path.append('/home/stian/repos/Blender_project/src')
from transformation import rotate
from boundingbox import camera_view_bounds_2d

# Variables ########################
Collection_Name = "Created_Collection"
nr_different_scenes = 4
nr_of_squares = 16
change_factor = 3

####################################

for variations in range(0,nr_different_scenes):
    coll = bpy.data.collections.get(Collection_Name)
    if coll:
        obs = [o for o in coll.objects if o.users == 1]
        while obs:
            bpy.data.objects.remove(obs.pop())

        bpy.data.collections.remove(coll)
    myCollection = bpy.data.collections.new(Collection_Name)
    bpy.context.scene.collection.children.link(myCollection)

    # Object SQUARE
    mat = bpy.data.materials.new(name='Material')

    mat.use_nodes=True
    x = -24
    for curr_row in range(0,4,1):
        x = x + (curr_row+8) # random.randint(-18, 18)
        y = -24

        for curr_col in range(0,4,1):
            y = y + (curr_col+8) #random.randint(-18, 18)
            bpy.ops.mesh.primitive_cube_add(size=3, location=(x,y,1.5))

        
            # Random apply transformation
            context = bpy.context
            # obj = context.edit_object
            obj = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            mesh = obj.data
            # get a bmesh
            bm = bmesh.from_edit_mesh(mesh)
            for v in bm.verts:
                if not v.select:
                    continue
                v.co.xy += Vector([uniform(-change_factor, change_factor) for axis in "xy"])
            #update.
            bmesh.update_edit_mesh(mesh)
            bpy.ops.object.mode_set(mode='OBJECT')



            obj.name ='Cube_{}-{}'.format(curr_row,curr_col)
            obj.data.materials.append(mat)
            bpy.ops.collection.objects_remove_all()
            bpy.data.collections[Collection_Name].objects.link(obj)
        
        

    # Set one to be red aa 1stk farlig object
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
    cube_red = bpy.data.collections[Collection_Name].objects.get("Cube_{}-{}".format(select_random_col,select_random_row))
    cube_red.data.materials[0] = mat_find


    # Light source
    light_data = bpy.data.lights.new('light', type='POINT')
    light = bpy.data.objects.new('light', light_data)
    bpy.data.collections[Collection_Name].objects.link(light)
    light.location = (0, 0, 20)  
    light.data.energy=12000.0

    mat_nodes = mat.node_tree.nodes
    mat_nodes['Principled BSDF'].inputs['Metallic'].default_value=0.0
    mat_nodes['Principled BSDF'].inputs['Roughness'].default_value=0.9
    mat_nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.05, 0.0185, 0.8, 1.0)
    mat_nodes['Principled BSDF'].inputs['Roughness'].default_value=0.167

    # Camera
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

    # Render
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
            camera_view_bounds_2d(scene, camera_object, cube_red,file_name)


