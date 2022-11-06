import cv2 as cv
import mediapipe as mp 

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

i = 0

cap = cv.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    static_image_mode = False,
    max_num_faces = 1,
    refine_landmarks = True,
    min_detection_confidence = 0.1,
    min_tracking_confidence = 0.1) as face_mesh:

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            continue

        smallImg = cv.resize(img, (int(img.shape[1]*0.03), int(img.shape[0]*0.03)), interpolation = cv.INTER_AREA)

        smallImg = cv.resize(smallImg, (int(smallImg.shape[1]/0.03), int(smallImg.shape[0]/0.03)), interpolation = cv.INTER_NEAREST)

        cv.imwrite("./originBigFrame/{}.png".format(i), cv.flip(img, 1))
        cv.imwrite("./originSmallFrame/{}.png".format(i), cv.flip(smallImg, 1))

        # interpolation = cv2.INTER_NEAREST

        smallImg = cv.cvtColor(smallImg, cv.COLOR_BGR2RGB)

        results = face_mesh.process(smallImg)

        smallImg = cv.cvtColor(smallImg, cv.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=smallImg,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=smallImg,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=smallImg,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
        

        cv.imwrite("./SmallFrames/{}.png".format(i), cv.flip(smallImg, 1))

        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        results = face_mesh.process(img)

        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
        

        cv.imwrite("./BigFrames/{}.png".format(i), cv.flip(img, 1))
        i += 1

        if cv.waitKey(5) & 0xFF == 27:
            break
        