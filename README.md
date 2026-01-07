# 👤 AI-Based Face Recognition & Attendance System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red)
![FaceRecognition](https://img.shields.io/badge/Library-Face_Recognition-green)

## 📖 Project Overview
This project is an automated **Attendance Management System** that uses facial recognition technology to log entries. It detects faces in real-time via webcam, identifies registered users, and logs their arrival time into a CSV/Excel file.

It eliminates the need for manual checks or ID cards, providing a contactless and efficient solution for offices or schools.

---

## ✨ Key Features
* **High Accuracy:** Uses HOG (Histogram of Oriented Gradients) algorithm for precise face detection.
* **Real-Time Processing:** Instantly recognizes faces from the video stream.
* **Duplicate Prevention:** Prevents multiple logs for the same person on the same day.
* **Auto-Logging:** Automatically creates and updates an `Attendance.csv` file with Name, Date, and Time.
* **Visual Interface:** Displays the user's name and bounding box on the screen.

---

## 🛠️ Output Example
The system generates a clean CSV log file automatically:

| Name | Date | Time |
| :--- | :--- | :--- |
| AHMET_YILMAZ | 07/01/2026 | 09:15:22 |
| ELON_MUSK | 07/01/2026 | 09:16:05 |

---

## 🚀 How to Run

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/han5858/Face-Recognition-Attendance.git](https://github.com/han5858/Face-Recognition-Attendance.git)
