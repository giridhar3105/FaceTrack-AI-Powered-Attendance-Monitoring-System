import cv2
import face_recognition
import os
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

# Path to the folder with known faces
path = r'C:\Users\girid\Desktop\Attendence project\students_images'
attendance_file = 'attendance.csv'

# Create attendance file if it doesn't exist
if not os.path.exists(attendance_file):
    with open(attendance_file, 'w') as f:
        f.write('Enrollment,Name,Date,Time\n')

# Function to save attendance
def save_attendance(enrollment, name):
    with open(attendance_file, 'a') as f:
        f.write(f"{enrollment},{name},{datetime.now().date()},{datetime.now().strftime('%H:%M:%S')}\n")

# Function to load known faces
def load_known_faces():
    images = []
    classNames = []
    myList = os.listdir(path)

    for cls in myList:
        current_img = cv2.imread(f'{path}/{cls}')
        if current_img is not None:
            images.append(current_img)
            classNames.append(os.path.splitext(cls)[0])  # Assuming the filename is the enrollment number
    return images, classNames

# Function to find encodings
def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode) > 0:
            encode_list.append(encode[0])
    return encode_list

# Function for real-time face recognition for attendance
def recognize_faces(encode_list_known, classNames):
    cap = cv2.VideoCapture(0)
    recognized_students = set()  # To track already marked students

    st.write("Press 'q' to stop the attendance marking.")
    while True:
        success, img = cap.read()
        if not success:
            st.error("Failed to access webcam.")
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

                if enrollment not in recognized_students:  # Check if the enrollment number is already marked
                    save_attendance(enrollment, name)
                    recognized_students.add(enrollment)
                    st.success(f"Attendance marked for: {name}")

        # Display the video feed
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Streamlit interface
st.title("Attendance Monitoring System")

option = st.radio("Select an option:", ("Register Student", "Mark Attendance", "View Attendance"))

if option == "Register Student":
    enrollment_number = st.text_input("Enrollment Number")
    name = st.text_input("Student Name")

    if st.button("Capture Face for Registration"):
        if enrollment_number and name:
            cap = cv2.VideoCapture(0)
            st.write("Capturing face... Press 'q' to stop.")
            temp_image_path = os.path.join(path, f"{enrollment_number}.jpg")

            while True:
                success, img = cap.read()
                if not success:
                    st.error("Failed to access webcam.")
                    break

                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.imwrite(temp_image_path, img)
                    st.success(f"Face captured and saved as {enrollment_number}.jpg")
                    break

            cap.release()
            cv2.destroyAllWindows()
        else:
            st.error("Please fill in all fields.")

elif option == "Mark Attendance":
    images, classNames = load_known_faces()
    encode_list_known = find_encodings(images)
    st.write("Starting attendance...")
    recognize_faces(encode_list_known, classNames)

elif option == "View Attendance":
    if os.path.exists(attendance_file):
        df = pd.read_csv(attendance_file)
        st.dataframe(df)
    else:
        st.error("No attendance records found.")