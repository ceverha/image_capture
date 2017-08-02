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

        buf = 20
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x-buf, y-buf), (x+w+buf, y+h+buf), (0,255,0), 2)

        cv2.imwrite("found.jpg", frame)
        cv2.imwrite("found1.jpg", cv2.resize(frame, None, fx=0.75, fy=1.0, interpolation = cv2.INTER_NEAREST))
        cv2.imwrite("found2.jpg", cv2.resize(frame, None, fx=1.0, fy=0.75, interpolation = cv2.INTER_NEAREST))

        key = cv2.waitKey(20)
        if key == 27:
            break
except KeyboardInterrupt:
    print("hello")
