import os
from tkinter import messagebox
import dlib
import cv2
import face_api
from scipy.spatial import distance as dist

# 初始化dlib的面部检测器和预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/shape_predictor_68_face_landmarks.dat")


# 眼睛
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# 嘴巴
def mouth_aspect_ratio(mouth):
    # 对于嘴巴关键点子集，正确的索引应该是：
    # 上嘴唇外侧中点 - 索引 2
    # 下嘴唇外侧中点 - 索引 6
    # 嘴角 - 索引 0 和 4
    # 因此，根据68个关键点的标注，对于仅包含嘴巴的列表（0到19），需要使用这些索引：
    A = dist.euclidean(mouth[2], mouth[6])  # 垂直距离
    C = dist.euclidean(mouth[0], mouth[4])  # 水平距离

    mar = A / C
    return mar


# 加载文件夹中的已知人物照片和生成面部编码
def load_known_faces(folder_path):
    known_faces = []
    known_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = face_api.load_image_file(image_path)
            encoding = face_api.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(filename[:-4])  # Assume filename without extension is the person's name
    return known_faces, known_names


# 检查最后一帧中的人脸是否与已知人脸匹配
def check_face_match(frame, known_faces, known_names):
    face_locations = face_api.face_locations(frame)
    face_encodings = face_api.face_encodings(frame, face_locations)
    for encoding in face_encodings:
        # 第二个返回值是每个已知面部编码与当前面部编码的比较结果（True/False列表）
        matches = face_api.compare_faces(known_faces, encoding)
        name = "Unknown"  # 如果没有找到匹配，默认为"Unknown"

        # 如果有匹配，找到匹配的第一个索引
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]  # 通过索引获取匹配的姓名
            return True, name  # 返回True和匹配的姓名

    return False, None  # 如果没有找到匹配，返回False和None


# 检测是否存在人脸（需要改成，是否只存在一个人脸）
def face_detected(frame):
    # 将BGR图像转换为RGB图像，因为face_recognition库使用RGB格式
    rgb_frame = frame[:, :, ::-1]

    # 使用face_recognition来检测图像中的所有人脸
    face_locations = face_api.face_locations(rgb_frame)

    # 如果face_locations非空，说明至少检测到一个人脸
    return len(face_locations) > 0


# 识别人脸
def capture(folder_path):
    # 加载已知人脸
    known_faces, known_names = load_known_faces(folder_path)

    # 定义状态检测和计数变量
    EYE_AR_THRESH = 0.3
    MOUTH_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 0.1
    MOUTH_AR_CONSEC_FRAMES = 2
    blink_counter = 0
    mouth_open_counter = 0
    blink_total = 0
    mouth_open_total = 0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open the camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)

            for rect in rects:
                x1, y1, x2, y2 = rect.left(), rect.top(), rect.right(), rect.bottom()
                # 绘制人脸头像框
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                landmarks = predictor(gray, rect)

                # 计算眼睛和嘴巴的纵横比
                leftEAR = eye_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
                rightEAR = eye_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
                ear = (leftEAR + rightEAR) / 2.0
                mar = mouth_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(60, 68)])

                # 检测眨眼
                if ear < EYE_AR_THRESH:
                    blink_counter += 1
                else:
                    if blink_counter >= EYE_AR_CONSEC_FRAMES:
                        blink_total += 1
                    blink_counter = 0

                # 检测张嘴
                if mar > MOUTH_AR_THRESH:
                    mouth_open_counter += 1
                else:
                    if mouth_open_counter >= MOUTH_AR_CONSEC_FRAMES:
                        mouth_open_total += 1
                    mouth_open_counter = 0

            cv2.putText(frame, f"Please Open Mouth and Blink with 3 times:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2)

            # 在视频帧上显示统计信息
            cv2.putText(frame, "Blinks: {}".format(blink_total), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 在视频帧上显示张嘴次数
            cv2.putText(frame, f"Mouth Opens: {mouth_open_total}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255),
                        2)

            if mouth_open_total >= 3 & blink_total >= 3:
                # 调用函数，同时获取匹配结果和姓名
                match_found, match_name = check_face_match(frame, known_faces, known_names)
                if match_found:
                    messagebox.showinfo("登录成功", f"欢迎{match_name}进入系统!")
                    return match_name  # 退出函数，避免继续执行摄像头读取代码
                else:
                    messagebox.showinfo("登录失败", "人脸未识别成功!")
                    return False

            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


# 识别人脸并存入文件夹
def capture_and_save_face(folder_path, name):
    # 加载已知人脸
    known_faces, known_names = load_known_faces(folder_path)
    # 定义状态检测和计数变量
    EYE_AR_THRESH = 0.3
    MOUTH_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 0.05
    MOUTH_AR_CONSEC_FRAMES = 2
    blink_counter = 0
    mouth_open_counter = 0
    blink_total = 0
    mouth_open_total = 0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open the camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)

            for rect in rects:
                landmarks = predictor(gray, rect)

                # 计算眼睛和嘴巴的纵横比
                leftEAR = eye_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
                rightEAR = eye_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
                ear = (leftEAR + rightEAR) / 2.0
                mar = mouth_aspect_ratio([(landmarks.part(i).x, landmarks.part(i).y) for i in range(60, 68)])

                # 检测眨眼
                if ear < EYE_AR_THRESH:
                    blink_counter += 1
                else:
                    if blink_counter >= EYE_AR_CONSEC_FRAMES:
                        blink_total += 1
                    blink_counter = 0

                # 检测张嘴
                if mar > MOUTH_AR_THRESH:
                    mouth_open_counter += 1
                else:
                    if mouth_open_counter >= MOUTH_AR_CONSEC_FRAMES:
                        mouth_open_total += 1
                    mouth_open_counter = 0

            cv2.putText(frame, f"Please Open Mouth and Blink with 3 times:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255),
                        2)

            # 在视频帧上显示统计信息
            cv2.putText(frame, "Blinks: {}".format(blink_total), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 在视频帧上显示张嘴次数
            cv2.putText(frame, f"Mouth Opens: {mouth_open_total}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        2)

            if mouth_open_total >= 3 & blink_total >= 3:
                match_found, match_name = check_face_match(frame, known_faces, known_names)
                # 人脸检测逻辑
                if face_detected(frame) & match_found is False:
                    cv2.imwrite(os.path.join(folder_path, f"{name}.jpg"), frame)
                    return True
                elif match_found:
                    return match_name

            cv2.imshow("人脸识别中，可点按Q键退出", frame)
            # 按Q键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()