import cv2
import distance as dist
import time
import requests
import sys
import base64
import json
import datetime

deviceId = 'raspberry_pi'
def upload(filenames):
    endpoint = "https://eai5udmepa.execute-api.us-east-1.amazonaws.com/latest/match"
    payload = '{"numImages": ' + str(len(filenames)) + ','
    payload = payload + '"images": ['

    for filename in filenames:
        file = open(filename, 'rb')
        base64Image = base64.b64encode(file.read()).decode('UTF-8')
        payload = payload + '{"data": "' + base64Image + '"},'

    # remove trailing comma
    payload = payload[0:len(payload)-1]
    payload = payload + '],'
    payload = payload + '"deviceId": "' + deviceId + '"}'
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint, headers=headers, json=payload)

def saveResizedImages(filename, srcImage):
    image1 = srcImage
    image2 = cv2.resize(frame, None, fx=0.75, fy=1.0, interpolation = cv2.INTER_NEAREST)
    image3 = cv2.resize(frame, None, fx=1.0, fy=0.75, interpolation = cv2.INTER_NEAREST)
    cv2.imwrite(filename+'_1.jpg', image1)
    cv2.imwrite(filename+'_2.jpg', image2)
    cv2.imwrite(filename+'_3.jpg', image3)
    filenames = [filename+'_1.jpg', filename+'_2.jpg', filename+'_3.jpg']
    return filenames
    
vc = cv2.VideoCapture(0)

# initiate distance sensor
dist.distanceInit()
THRESHOLD = 30

# refractory period size in seconds
PERIOD_SIZE = 5

lastPeriodTime = time.time()
try:
    while True:
        # don't overload rpio
        time.sleep(0.25)
        print(str(datetime.datetime.now()))
        distance = dist.getDistance()
        if (distance < THRESHOLD):
            currTime = time.time()
            if currTime > lastPeriodTime + PERIOD_SIZE:
                lastPeriodTime = currTime

                # capture and save image
                rval, frame = vc.read()
                filename = "webcam_capture"
                filenames = saveResizedImages(filename, frame)

                before = time.time()
                response = upload(filenames)
                after = time.time()
                print("request returned in " + str(after - before) + " seconds")

                print(response)
                print(response.text)
                
                key = cv2.waitKey(20)
                if key == 27:
                    break
except KeyboardInterrupt:
    dist.distanceClose()
    print("hello")
