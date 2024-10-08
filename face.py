import face_recognition
import pyttsx3
import cv2
import numpy as np
import csv
import os
from datetime import datetime

engine = pyttsx3.init()
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

path = "photos"
sys = os.listdir(path)

known_face_encoding = []

for i in sys:
    known_face_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file('photos/' + i))[0])


known_faces_names = sys

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)
count = 0
cooldown = 50

face_names = []
while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    if (count % 15 == 0):

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding, tolerance=0.6)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
        
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
                face_names.append(name)

                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2

                cv2.putText(frame, name.split('.')[0] + ' Present',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)
                engine.say(name.split('.')[0] + " marked present")
                engine.runAndWait()

                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name.split('.')[0], current_time])
                else:
                    engine.say("Already marked Present")
                
            flag = 0
            for values in matches:
                if values == True:
                    flag+=1
            if flag ==0:
                print("Not a part of this class")
                engine.say(name.split('.')[0] + "Not a part of this class")
                engine.runAndWait()

    count += 1
    cv2.imshow("attendence system", frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
