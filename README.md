# FaceTrack: AI-Powered Attendance Monitoring System

FaceTrack is a streamlined AI-driven system that simplifies attendance tracking through facial recognition technology. With features like real-time attendance marking, student registration, and attendance record viewing, it offers a modern solution for educational institutions.

---

## Features
1. **Student Registration**: Register a student's face with their enrollment number using a webcam or upload an image file.
2. **Real-Time Attendance**: Detect and recognize faces through a live webcam feed to mark attendance automatically, displaying the name and enrollment number on the video feed.
3. **Attendance Records**: View and manage attendance logs with details like enrollment number, name, date, and time.

---

## How It Works
1. **Register Student**: Capture the student's face using a webcam or upload an image file, and save it with their enrollment number in the `students_images` directory.
2. **Mark Attendance**: Compare live webcam feeds with stored images to detect faces, display the name and enrollment number on the feed, and log attendance.
3. **View Attendance**: Access attendance records in a structured, tabular format.

---

## Prerequisites
- Python 3.7 or above
- Libraries: `opencv-python`, `face_recognition`, `numpy`, `pandas`, `streamlit`

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/facetrack.git
   cd facetrack
   ```

2. **Install Dependencies**:
   ```bash
   pip install opencv-python face_recognition numpy pandas streamlit
   ```

3. **Setup Files and Folders**:
   - Create a folder named `students_images` in the project directory.
   - Ensure `attendance.csv` exists in the project folder (it will be auto-created if missing).

4. **Run the Application**:
   ```bash
   streamlit run attendance_management.py
   ```

5. **Access the Interface**:
   Open your browser and navigate to `http://localhost:8501`.

---

## File Overview
### `attendance_management.py`
This single Python script serves as the backbone of the project. It contains:
- **Student Registration**: A module to capture or upload and save student faces with their details.
- **Real-Time Attendance Marking**: Uses facial recognition to match, display names and enrollment numbers, and log attendance.
- **Attendance Viewing**: Displays a detailed table of attendance records.

### Example Structure:
```
FaceTrack/
├── attendance_management.py    # Main script
├── students_images/            # Stores registered student images
├── attendance.csv              # Logs attendance data
└── README.md                   # Documentation
```

---

## Usage
### 1. **Register a Student**:
- Enter the student's enrollment number and name in the Streamlit interface.
- Capture the face using the webcam or upload an image file.
- The image will be stored in the `students_images` directory.

### 2. **Mark Attendance**:
- Choose the "Mark Attendance" option.
- The system detects faces from the webcam feed, displays the name and enrollment number, and matches them with registered students.
- Attendance is logged automatically in the `attendance.csv` file.

### 3. **View Attendance**:
- Select the "View Attendance" option.
- The attendance records are displayed in a table format, with options to export them.

---

## Future Enhancements
- Add email notifications for attendance status.
- Integrate cloud storage for better scalability.
- Support multiple cameras for larger institutions.
- Introduce facial expression detection for added analytics.

---

## Contributors
- **Giridhar Chennuru** - Developer

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Example Attendance Log
| Enrollment | Name      | Date       | Time     |
|------------|-----------|------------|----------|
| 12345      | John Doe  | 2024-11-23 | 10:15:32 |
| 67890      | Jane Smith| 2024-11-23 | 10:20:45 |

---

Happy Coding! 😊
