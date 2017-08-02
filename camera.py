import cv2
import distance as dist
import time
import requests
import sys
import base64
import json

deviceId = 'raspberry_pi'
def upload(filename):
    endpoint = "https://eai5udmepa.execute-api.us-east-1.amazonaws.com/latest/match"
    file = open(filename, 'rb')
    base64Image = base64.b64encode(file.read()).decode('UTF-8')
    payload = '{"numImages": 2,'
    payload = payload + '"images": ['
    payload = payload + '{"data": "' + base64Image + '"}'
    payload = payload + ', {"data": "' + base64Image + '"}'
    payload = payload + ', {"data": "' + base64Image + '"}'
    payload = payload + ', {"data": "' + base64Image + '"}'
    payload = payload + '],'
    payload = payload + '"deviceId": "' + deviceId + '"}'
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint, headers=headers, json=payload)

vc = cv2.VideoCapture(0)

# initiate distance sensor
dist.distanceInit()
THRESHOLD = 10  

# refractory period size in seconds
PERIOD_SIZE = 5

lastPeriodTime = time.time()
try:
    while True:
        distance = dist.getDistance()
        if (distance < THRESHOLD):
            currTime = time.time()
            if currTime > lastPeriodTime + PERIOD_SIZE:
                lastPeriodTime = currTime

                # capture and save image
                rval, frame = vc.read()
                filename = "capturedImages/capture" + str(lastPeriodTime) + ".jpg"
                cv2.imwrite(filename, frame)

                before = time.time()
                response = upload(filename)
                after = time.time()
                print("request returned in " + str(after - before) + " seconds")

                print(response)
                print(response.text)
                
                key = cv2.waitKey(20)
                if key == 27:
                    break
        # don't overload rpio
        time.sleep(0.1)
except KeyboardInterrupt:
    dist.distanceClose()
    print("hello")
