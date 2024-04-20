import face_api
# image = face_api.load_image_file("/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/Maneger_Known_Faces/ke.jpg")
# face_landmarks_list = face_api.face_landmarks(image)
# print()
# encoding = face_api.face_encodings(image)[0]
# print(encoding)


image = face_api.load_image_file("/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/Maneger_Known_Faces/ke.jpg")
face_landmarks_lis = face_api.face_landmarks(image)
print(face_landmarks_lis)