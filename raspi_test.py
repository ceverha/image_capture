import picamera
import time
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
camera = picamera.PiCamera()

# camera.resolution = (1024, 768)
width = camera.resolution[0]
height = camera.resolution[1] + 8

print('warming up')
time.sleep(2)

image = np.empty((height*width*3,), dtype=np.uint8) 
camera.capture(image, 'bgr')
image = image.reshape((height, width, 3))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
before = time.time()
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5)
after = time.time()
print("detect finished in " + str(after - before) + " seconds")
print(faces)

buf = 20
for (x,y,w,h) in faces:
    cv2.rectangle(image, (x-buf, y-buf), (x+w+buf, y+h+buf), (0,255,0), 2)

cv2.imwrite('iot.jpg', image)
