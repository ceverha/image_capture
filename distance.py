import RPi.GPIO as GPIO
import time
TRIG = 23 
ECHO = 24
  

def distanceInit():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)
  
  GPIO.output(TRIG, False)
  print ("Waiting For Sensor To Settle")
  time.sleep(2)

def getDistance():
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  
  while GPIO.input(ECHO)==0:
    pulse_start = time.time()
  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  return distance

def distanceClose():
  GPIO.cleanup()
