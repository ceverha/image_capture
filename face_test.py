import cv2
import time

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
print(face_cascade.empty())
vc = cv2.VideoCapture(0)

try: 
    while True:
        time.sleep(5)
        rval, frame = vc.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        before = time.time()
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        after = time.time()
        print("detect finished in " + str(after - before) + " seconds")
        print(faces)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        if len(faces) > 0:
            cv2.imwrite("found.jpg", frame)
        key = cv2.waitKey(20)
        if key == 27:
            break
except KeyboardInterrupt:
    print("hello")
