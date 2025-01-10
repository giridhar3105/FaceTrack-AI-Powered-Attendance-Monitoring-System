import os
import streamlit as st
from datetime import datetime
from file_handler_module import create_attendance_file, save_attendance, load_attendance
from face_recognition_module import load_known_faces, find_encodings, recognize_faces

# File paths
attendance_file = "attendance.csv"
images_folder = "students_images"

# Ensure necessary files and folders exist
if not os.path.exists(images_folder):
    os.makedirs(images_folder)
create_attendance_file(attendance_file)

# Streamlit interface
st.title("Attendance Monitoring System")

option = st.radio("Select an option:", ("Register Student", "Mark Attendance", "View Attendance"))

if option == "Register Student":
    enrollment_number = st.text_input("Enrollment Number")
    name = st.text_input("Student Name")
    capture_method = st.radio("How do you want to register?", ("Use Webcam", "Upload Image"))

    if st.button("Register Student"):
        if enrollment_number and name:
            if capture_method == "Use Webcam":
                import cv2
                cap = cv2.VideoCapture(0)
                st.write("Capturing face... Press 'q' to save and stop.")
                temp_image_path = f"{images_folder}/{enrollment_number}.jpg"

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
            elif capture_method == "Upload Image":
                uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
                if uploaded_file:
                    temp_image_path = f"{images_folder}/{enrollment_number}.jpg"
                    with open(temp_image_path, "wb") as f:
                        f.write(uploaded_file.read())
                    st.success(f"Image uploaded and saved as {enrollment_number}.jpg")
        else:
            st.error("Please fill in all fields.")

elif option == "Mark Attendance":
    images, classNames = load_known_faces(images_folder)
    encode_list_known = find_encodings(images)
    st.write("Starting attendance...")
    recognize_faces(encode_list_known, classNames, save_attendance)

elif option == "View Attendance":
    attendance_data = load_attendance(attendance_file)
    if not attendance_data.empty:
        st.dataframe(attendance_data)
    else:
        st.error("No attendance records found.")
