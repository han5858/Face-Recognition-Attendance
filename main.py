import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# --- CONFIGURATION ---
PATH = 'Images_Attendance'  # Path to the folder containing reference images
CSV_FILE = 'Attendance.csv' # File to save attendance logs

# 1. Image Loading & Database Creation
images = []
classNames = []
myList = os.listdir(PATH)

print(f"[INFO] Loading images from '{PATH}'...")

for cl in myList:
    # Read image using OpenCV
    curImg = cv2.imread(f'{PATH}/{cl}')
    images.append(curImg)
    # Remove file extension from name (e.g., 'Ahmet.jpg' -> 'Ahmet')
    classNames.append(os.path.splitext(cl)[0])

print(f"[INFO] Found {len(classNames)} people: {classNames}")

# 2. Encoding Function (The AI Brain)
def findEncodings(images):
    """
    Converts a list of images into 128-dimensional face encodings.
    """
    encodeList = []
    for img in images:
        try:
            # OpenCV uses BGR, face_recognition uses RGB. Convert it.
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print(f"[WARNING] No face found in one of the images. Skipping...")
            continue
    return encodeList

# 3. Attendance Logging Function
def markAttendance(name):
    """
    Logs the name and time into a CSV file if not already logged today.
    """
    # Create file if it doesn't exist
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write('Name,Date,Time\n')

    with open(CSV_FILE, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        
        # Determine logic: Only log if NOT in list (or modify for daily logic)
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%d/%m/%Y')
            timeString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{timeString}')
            print(f"[LOG] Attendance recorded for: {name}")

# --- MAIN EXECUTION ---
print("[INFO] Starting Encoding Process (This might take a moment)...")
encodeListKnown = findEncodings(images)
print(f"[INFO] Encoding Complete. System Ready.")

# Open Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("[ERROR] Failed to access webcam.")
        break

    # Optimization: Resize frame to 1/4th size for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Loop through all detected faces
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        # Compare current face with known faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        # Get the best match index
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            # --- VISUALS ---
            y1, x2, y2, x1 = faceLoc
            # Scale coordinates back up by 4 (since we resized down)
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            # Draw Green Rectangle & Name
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            # Log Attendance
            markAttendance(name)
        else:
            # Unknown Face Logic
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, "UNKNOWN", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('AI Attendance System', img)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()