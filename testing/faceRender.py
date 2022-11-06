import cv2
import mediapipe as mp  # pip install mediapipe
import matplotlib.pyplot as plt
import numpy as np
import open3d
import random

import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

import platform
isMacOS = (platform.system() == "Darwin")

gui.Application.instance.initialize()


# def vis_matplotlib_3d(points_x,points_y,points_z):
#     fig = plt.figure()
#     ax = plt.axes(projection="3d")
#     height,width = img.shape[0],img.shape[1]
#     points_x = points_x*width
#     points_y = points_y*height
#     points_z = points_z*width
#     ax.scatter(points_x, points_y, points_z) 
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')
#     ax.view_init(elev=0, azim=90)
#     plt.show()

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
# mp_drawing_utils = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# drawing_spec = mp_drawing_utils.DrawingSpec(color=(50,50,50), thickness=1, circle_radius=3)

# img = cv2.imread('f.png')
# if img is None:
#     print('Failed to read image, check image path')
#     exit(-1)

# img.flags.writeable = False
# img_RGB = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
# results = face_mesh.process(img_RGB)
# img.flags.writeable = True

# if results.multi_face_landmarks:
#     for face_landmarks in results.multi_face_landmarks: 
#         coords = np.array(face_landmarks.landmark)
#         points_x = np.array([c.x for c in coords])
#         points_y = np.array([c.y for c in coords])
#         points_z = np.array([c.z for c in coords])
#         # vis_matplotlib_3d(points_x,points_y,points_z)
#         points = np.vstack([points_x,points_y,points_z]).T.astype(np.float64)


#         # construct point cloud
#         pcd = open3d.geometry.PointCloud()
#         pcd.points = open3d.utility.Vector3dVector(points)
#         # pcd.colors = open3d.utility.Vector3dVector(colors)
#         # estimate normals
#         pcd.estimate_normals()
#         pcd.orient_normals_to_align_with_direction()

#         # surface reconstruction
#         mesh = open3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=10, n_threads=1)[0]
#         mesh.compute_vertex_normals()

#         # remove weird artefacts
#         mesh.remove_degenerate_triangles()
#         mesh.remove_duplicated_triangles()
#         mesh.remove_duplicated_vertices()
#         mesh.remove_non_manifold_edges()

#         mesh.paint_uniform_color([1, 0.706, 0])  # [R, G, B]

#         # save mesh
#         # open3d.io.write_triangle_mesh('mesh.obj', mesh)
#         window = gui.Application.instance.create_window(
#             "Add Spheres Example", 1024, 768)
#         scene = gui.SceneWidget()
#         scene.scene = rendering.Open3DScene(window.renderer)
#         scene.scene.set_background([1, 1, 1, 1])
#         scene.scene.scene.set_sun_light(
#             [-1, -1, -1],  # direction
#             [1, 1, 1],  # color
#             100000)  # intensity
#         scene.scene.scene.enable_sun_light(True)
#         bbox = open3d.geometry.AxisAlignedBoundingBox([-10, -10, -10],
#                                                    [10, 10, 10])
#         scene.setup_camera(60, bbox, [0, 0, 0])


#         mat = rendering.MaterialRecord()
#         mat.base_color = [
#             random.random(),
#             random.random(),
#             random.random(), 1.0
#         ]
#         mat.shader = "defaultLit"
#         # sphere = open3d.geometry.TriangleMesh.create_sphere(0.5)
#         # sphere.compute_vertex_normals()
#         # sphere.translate([
#         #     10.0 * random.uniform(-1.0, 1.0), 10.0 * random.uniform(-1.0, 1.0),
#         #     10.0 * random.uniform(-1.0, 1.0)
#         # ])
#         scene.scene.add_geometry("sphere", mesh, mat)

#         # faceObject = open3d.visualization.rendering.Renderer

#         # vis = open3d.visualization.rendering.Open3DScene
#         # scene.scene.add_geometry(mesh)
#         # vis.add_geometry(mesh)
#         # ctr = vis.get_view_control()
#         # print("Field of view (before changing) %.2f" % ctr.get_field_of_view())
#         # ctr.change_field_of_view(step=10)
#         # print("Field of view (after changing) %.2f" % ctr.get_field_of_view())
#         # vis.run()


#         # open3d.visualization.draw_geometries([pcd])

#         # open3d.visualization.draw_geometries([mesh])
#         window.add_child(scene)


# gui.Application.instance.run()


import open3d as o3d
import open3d.visualization.rendering as rendering
import numpy as np
import cv2 as cv

def main():
    render = rendering.OffscreenRenderer(640, 480)

    img = cv.imread("f.png")

    img = o3d.geometry.Image(img)

    color = np.ndarray(shape= (4,), buffer=np.array([1.0, 0.75, 0.0, 1.0]))

    # render.scene.set_background(color, img)

    yellow = rendering.MaterialRecord()
    yellow.base_color = [1.0, 0.75, 0.0, 1.0]
    yellow.shader = "defaultLit"

    green = rendering.MaterialRecord()
    green.base_color = [0.0, 0.5, 0.0, 1.0]
    green.shader = "defaultLit"

    grey = rendering.MaterialRecord()
    grey.base_color = [0.7, 0.7, 0.7, 1.0]
    grey.shader = "defaultLit"

    white = rendering.MaterialRecord()
    white.base_color = [1.0, 1.0, 1.0, 1.0]
    white.shader = "defaultLit"

    cyl = o3d.geometry.TriangleMesh.create_cylinder(.05, 3)
    cyl.compute_vertex_normals()
    cyl.translate([-2, 0, 1.5])
    sphere = o3d.geometry.TriangleMesh.create_sphere(.2)
    sphere.compute_vertex_normals()
    sphere.translate([-2, 0, 3])

    box = o3d.geometry.TriangleMesh.create_box(2, 2, 1)
    box.compute_vertex_normals()
    box.translate([-1, -1, 0])
    solid = o3d.geometry.TriangleMesh.create_icosahedron(0.5)
    solid.compute_triangle_normals()
    solid.compute_vertex_normals()
    solid.translate([0, 0, 1.75])




    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing_utils = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    drawing_spec = mp_drawing_utils.DrawingSpec(color=(50,50,50), thickness=1, circle_radius=3)

    img = cv2.imread('f.png')
    if img is None:
        print('Failed to read image, check image path')
        exit(-1)

    img.flags.writeable = False
    img_RGB = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    results = face_mesh.process(img_RGB)
    img.flags.writeable = True

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks: 
            coords = np.array(face_landmarks.landmark)
            points_x = np.array([c.x for c in coords])
            points_y = np.array([c.y for c in coords])
            points_z = np.array([c.z for c in coords])
            # vis_matplotlib_3d(points_x,points_y,points_z)
            points = np.vstack([points_x,points_y,points_z]).T.astype(np.float64)


            # construct point cloud
            pcd = open3d.geometry.PointCloud()
            pcd.points = open3d.utility.Vector3dVector(points)
            # pcd.colors = open3d.utility.Vector3dVector(colors)
            # estimate normals
            pcd.estimate_normals()
            pcd.orient_normals_to_align_with_direction()

            # surface reconstruction
            mesh = open3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=10, n_threads=1)[0]
            mesh.compute_vertex_normals()

            # remove weird artefacts
            mesh.remove_degenerate_triangles()
            mesh.remove_duplicated_triangles()
            mesh.remove_duplicated_vertices()
            mesh.remove_non_manifold_edges()

            # mesh.paint_uniform_color([1, 0.706, 0])  # [R, G, B]



            render.scene.add_geometry("face", pcd, green)
    # render.scene.add_geometry("sphere", sphere, yellow)
    # render.scene.add_geometry("box", box, grey)
    # render.scene.add_geometry("solid", solid, white)
    # render.setup_camera(60.0, [0, 0, 0], [0, 10, 0], [0, 0, 1])
    render.scene.scene.set_sun_light([0.707, 0.0, -.707], [1.0, 1.0, 1.0], 75000)
    render.scene.scene.enable_sun_light(True)
    render.scene.show_axes(True)

    img = render.render_to_image()
    print("Saving image at test.png")
    o3d.io.write_image("test.png", img, 9)

    for i in range(-100,101, 50):
        for j in range(-100,101, 50):
            for c in range(-100,101, 50):
                for d in range(100,201, 20):
                    render.setup_camera(d, [i, j, c], [0, 0, 0], [0, 1, 0])
                    img = render.render_to_image()
                    print("Saving image at test2.png")
                    o3d.io.write_image("test/{}{}{}{}.png".format(i,j,c,d), img, 9)


if __name__ == "__main__":
    main()