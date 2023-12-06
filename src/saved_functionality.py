# /snap/blender/4228/4.0/python/bin/python3.10 -m pip install pillow

# Moving a object
#cube = bpy.data.collections[Collection_Name].objects.get("Cube")
#cube.location[0]+=10

# Plane
#bpy.ops.mesh.primitive_plane_add(size=40)
#obj = bpy.context.active_object
#bpy.ops.collection.objects_remove_all()
#bpy.data.collections[Collection_Name].objects.link(obj)

# create material
#mat = bpy.data.materials.new(name='AnotherMaterial')
#assign material to plane
#plane = bpy.data.collections[Collection_Name].objects.get("Plane")
#plane.data.materials.append(mat)
#mat.use_nodes=True
# let's create a variable to store our list of nodes
#mat_nodes = mat.node_tree.nodes
#mat_nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.50, 0., 0.6, 1.0)
#mat_nodes['Principled BSDF'].inputs['Roughness'].default_value=0.0/*

# def camera_view_bounds_2d(scene, camera_object, mesh_object):
#     """
#     Returns camera space bounding box of the mesh object.

#     Gets the camera frame bounding box, which by default is returned without any transformations applied.
#     Create a new mesh object based on mesh_object and undo any transformations so that it is in the same space as the
#     camera frame. Find the min/max vertex coordinates of the mesh visible in the frame, or None if the mesh is not in view.

#     :param scene:
#     :param camera_object:
#     :param mesh_object:
#     :return:
#     """

#     """ Get the inverse transformation matrix. """
#     matrix = camera_object.matrix_world.normalized().inverted()
#     """ Create a new mesh data block, using the inverse transform matrix to undo any transformations. """
#     mesh = mesh_object.to_mesh()
#     mesh.transform(mesh_object.matrix_world)
#     mesh.transform(matrix)

#     """ Get the world coordinates for the camera frame bounding box, before any transformations. """
#     frame = [-v for v in camera_object.data.view_frame(scene=scene)[:3]]

#     lx = []
#     ly = []

#     for v in mesh.vertices:
#         co_local = v.co
#         z = -co_local.z

#         if z <= 0.0:
#             """ Vertex is behind the camera; ignore it. """
#             continue
#         else:
#             """ Perspective division """
#             frame = [(v / (v.z / z)) for v in frame]

#         min_x, max_x = frame[1].x, frame[2].x
#         min_y, max_y = frame[0].y, frame[1].y

#         x = (co_local.x - min_x) / (max_x - min_x)
#         y = (co_local.y - min_y) / (max_y - min_y)

#         lx.append(x)
#         ly.append(y)

#     # bpy.data.meshes.remove(mesh)
#     mesh_object.to_mesh_clear()
#     """ Image is not in view if all the mesh verts were ignored """
#     if not lx or not ly:
#         return None

#     min_x = np.clip(min(lx), 0.0, 1.0)
#     min_y = np.clip(min(ly), 0.0, 1.0)
#     max_x = np.clip(max(lx), 0.0, 1.0)
#     max_y = np.clip(max(ly), 0.0, 1.0)

#     """ Image is not in view if both bounding points exist on the same side """
#     if min_x == max_x or min_y == max_y:
#         return None

#     """ Figure out the rendered image size """
#     render = scene.render
#     fac = render.resolution_percentage * 0.01
#     dim_x = render.resolution_x * fac
#     dim_y = render.resolution_y * fac

#     return (min_x, min_y), (max_x, max_y)


