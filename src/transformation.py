import numpy as np
import math
import bpy
import numpy as np
from PIL import Image, ImageDraw
from settings import *
import fnmatch
import os

    
def rotation_matrix(axis, theta):
    """ Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotate(point, angle_degrees, axis=(0,1,0)):
    theta_degrees = angle_degrees
    theta_radians = math.radians(theta_degrees)
    rotated_point = np.dot(rotation_matrix(axis, theta_radians), point)
    return rotated_point



def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, cam_ob, me_ob, file_name):
    """ Adds boundingbox lines based on the view angle of the camera.
    
    Arguments:
    scene -- The whole scene
    cam_ob -- Camera object
    me_ob -- Mesh object to be encapsulated 
    file_name -- File name of current scene
    
    """
    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)

            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    
    x = round(min_x * dim_x)
    y = round(dim_y - max_y * dim_y)
    width = round((max_x - min_x) * dim_x)
    height = round((max_y - min_y) * dim_y)
    
    # Needed for YOLO Format TODO -> not static
    imwidth = SIZE_X
    imheight = SIZE_Y 
    
    # Create .txt file
    with open(SAVE_PATH + "txt_files/" + file_name + '.txt', 'a') as f:
        x_center = x + (width / 2)
        x_cen_norm = x_center / imwidth

        width_norm = width/imwidth 

        y_center = y + (height / 2)
        y_cen_norm = y_center / imheight
        height_norm = (height) / imheight 

        f.write('0 {} {} {} {} '.format(x_cen_norm,y_cen_norm, width_norm, height_norm))

    # Create BB image
    if len(fnmatch.filter(os.listdir("/home/stian/repos/CS569_project/files/bb"), '*.*')) < BB_AMOUNT:
        x = x_center-(width / 2)
        y = y_center- (height/2)
        im = Image.open(SAVE_PATH + "img/" + file_name + ".png") 
        line1 = [(x, y), (x + width, y)] 
        line2 = [(x, y), (x, y+height)] 
        line3 = [(x, y+height), (x + width, y+height)] 
        line4 = [(x+width, y), (x+width,y+height)] 
        img1 = ImageDraw.Draw(im) 
        img1.line(line1, fill ="Green", width = 1) 
        img1.line(line2, fill ="Green", width = 1) 
        img1.line(line3, fill ="Green", width = 1) 
        img1.line(line4, fill ="Green", width = 1) 
        im.save(SAVE_PATH + "bb/" + file_name + "_bb.png")  
