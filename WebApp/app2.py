import subprocess
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19, GPIO.IN)
GPIO.setup(27, GPIO.OUT)

while(True):
    if GPIO.input(19):
        GPIO.output(27,1)
        print("Taking a photo...")
        subprocess.run(["fswebcam", "static/photo.jpg"])
        sleep(2)

    else:
        GPIO.output(27,0)

        
