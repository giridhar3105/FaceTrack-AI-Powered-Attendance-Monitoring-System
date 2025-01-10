import os
import cv2
import face_recognition
import numpy as np

# Load known faces
def load_known_faces(images_folder):
    images = []
    classNames = []
    myList = os.listdir(images_folder)

    for cls in myList:
        current_img = cv2.imread(f'{images_folder}/{cls}')
        if current_img is not None:
            images.append(current_img)
            classNames.append(os.path.splitext(cls)[0])  # Assuming the filename is the enrollment number
    return images, classNames

# Find encodings for known faces
def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode) > 0:
            encode_list.append(encode[0])
    return encode_list

# Real-time face recognition for attendance
def recognize_faces(encode_list_known, classNames, save_attendance):
    cap = cv2.VideoCapture(0)
    recognized_students = set()  # To track already marked students

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encode_list_known, encodeFace)
            faceDist = face_recognition.face_distance(encode_list_known, encodeFace)

            matchIndex = np.argmin(faceDist)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                enrollment = classNames[matchIndex]  # Assuming the file name is the enrollment number

                if enrollment not in recognized_students:  # Check if already marked
                    save_attendance(enrollment, name)
                    recognized_students.add(enrollment)
                    print(f"Attendance marked for: {name}")

                # Display the name or enrollment number on the video feed
                y1, x2, y2, x1 = [i * 4 for i in faceLoc]  # Scale back to original size
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Show the video feed
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
