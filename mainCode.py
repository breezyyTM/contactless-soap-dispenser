import RPi.GPIO as GPIO
import time
import requests

import I2C_LCD_driver


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)    # GPIO24 - LED
GPIO.setup(18, GPIO.OUT)    # GPIO18 - Buzzer

GPIO.setup(26, GPIO.OUT)    # GPIO26 - Servo
Servo_PWM = GPIO.PWM(26, 50) # Servo setup

GPIO.setup(25, GPIO.OUT)    # GPIO25 - Ultrasonic Trig
GPIO.setup(27, GPIO.IN)     # GPIO27 - Ultrasonic Echo



def distance():
    # produce 10us pulse at Trig
    GPIO.output(25, 1)
    time.sleep(0.0001)
    GPIO.output(25, 0)


    # measure pulse width (i.e. time of flight) at Echo
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(27) == 0:   # When sensor is NOT activated...
        StartTime = time.time()


    while GPIO.input(27) == 1:   # When sensor is activated...
        StopTime = time.time()


    ElapsedTime = StopTime - StartTime

    # Compute distance in cm, from time of flight
    Distance = (ElapsedTime * 34300) / 2

    if Distance < 7.0:
        active = 1
        return active, Distance
    
    else:
        active = 0
        return active, Distance





# <<<<<<<<<<<<<<< MAIN PROGRAM >>>>>>>>>>>>>>>

# Validate user input of the amount of liquid in bottle
while True:
    userValue = input("Please enter the amount of ml your bottle of liquid has. (in ml - min 500, max 600)\n>> ")


    # If user-entered value IS empty
    if userValue.strip() == "":
        userValue = input("Error! Please enter a valid amount. (min 500ml, max 600ml)\n>> ")

        if userValue.strip() != "" and userValue.strip().isnumeric() == True and int(userValue.strip()) >= 500 and int(userValue.strip()) <= 600:
            soapAmount = int(userValue.strip())
            originalAmt = soapAmount
            break



    # If user-entered value is NOT a number... (e.g. string)
    elif userValue.strip() != "" and userValue.strip().isnumeric() == False:
        userValue = input("Error! Please enter a valid amount. (min 500ml, max 600ml)\n>> ")

        if userValue.strip() != "" and userValue.strip().isnumeric() == True and int(userValue.strip()) >= 500 and int(userValue.strip()) <= 600:
            soapAmount = int(userValue.strip())
            originalAmt = soapAmount
            break



    # If user-entered value is a number...
    elif userValue.strip() != "" and userValue.strip().isnumeric() == True:
        if int(userValue.strip()) >= 500 and int(userValue.strip()) <= 600:
            soapAmount = int(userValue.strip())
            originalAmt = soapAmount
            break

        else:
            userValue = input("Error! Please enter a valid amount. (min 500ml, max 600ml)\n>> ")

            if userValue.strip() != "" and userValue.strip().isnumeric() == True and int(userValue) >= 500 and int(userValue) <= 600:
                soapAmount = int(userValue.strip())
                originalAmt = soapAmount
                break



# Saves the 'originalAmt' value into a .txt file
with open("originalAmt.txt", "w") as f:
	f.write(str(originalAmt))


# Records the number of times liquid is dispensed by the bottle
liquidDispensedTimes = 0

# Helps record the current sample number the program is at
i = 0

# Used to count up to 20, to substitute 20 seconds of delay when uploading sensor data to the cloud
count = 0

# Ensures that the interval timer is only started once.
start = 0

# Checks if user has been tweeted of the remaining amount of liquid left in the bottle
informed25 = 0
informed50 = 0


while True:
    if start == 0:
        intervalStart = time.time()     # Start the interval timer
        start = 1

    activeOrNo, distanceFloat = distance()
    print("Measured Distance = {0:0.1f} cm".format(distanceFloat))
    time.sleep(1)   # 1 second delay before dispensing liquid (if sensor is activated)


    if activeOrNo == 1 and distanceFloat < 7.0:    # Sensor activates if distance of hand from ultrasonic ranger sensor is between 0cm to 12.0cm
        GPIO.output(24, 1)   # LED turns on
        time.sleep(0.5)
        
        GPIO.output(24, 0)   # LED turns off
        time.sleep(0.5)
        
        # GPIO.output(18, 1)   # Buzzer active
        print("Buzzer active")
        time.sleep(0.5)
        
        # GPIO.output(18, 0)   # Buzzer silent
        print("Buzzer silent")
        time.sleep(0.5)


        # No. of times liquid is dispensed. Increments by 1 whenever ultrasonic ranger sensor is activated
        liquidDispensedTimes += 1


        # ******Servo movement here******

        Servo_PWM.start(6)   # 90 degrees (?)
        time.sleep(2)

        Servo_PWM.start(12)   # back to original position
        time.sleep(2)


        deducted = 5
        soapAmount -= deducted      # Current amount of liquid is deducted, each time the sensor is activated and liquid is dispensed

        with open("soapAmount.txt", "w") as f:
            f.write(str(soapAmount))

        soapAmountInStr = str(soapAmount)   # Current amount of liquid left, to be displayed on the LCD screen


        # LCD Screen Setup
        LCD = I2C_LCD_driver.lcd()
        time.sleep(0.5)
        LCD.backlight(0)
        time.sleep(0.5)
        LCD.backlight(1)
        LCD.lcd_display_string("   Soap Left:", 1)
        LCD.lcd_display_string("    "+ soapAmountInStr + "ml", 2, 2)

        time.sleep(2)
        LCD.lcd_clear()



    else:        
        # If the ultrasonic ranger sensor is not activated, check for other things...
        # e.g. time elapsed since start of interval, amount of liquid left in bottle, whether set interval has ended, etc.
        intervalEnd = time.time()
        elapsedInterval = intervalEnd - intervalStart
        print("Elapsed Time: ", elapsedInterval)

        # Uploading sensor data to ThingSpeak channel
        if elapsedInterval >= 20:    # If elapsed time interval is more than or equal to 24 hours...
            print("No. of times liquid is dispensed...", liquidDispensedTimes)
            count = 0   # Reset count value
            start = 0   # Reset 'start' value, so that the interval timer will be reset

            i += 1
            print("Uploading sample number", i)
            resp = requests.get("https://api.thingspeak.com/update?api_key=OI1N9PBFHJZOL8R8&field1=%s" %(liquidDispensedTimes))

            liquidDispensedTimes = 0    # Reset no. of times liquid has been dispensed, after the 24-hour set interval and uploading the data to cloud

            while count < 20:
                print(count)    # Debugging purposes
                # LED turns on and off for 20 seconds, to indicate that data is being uploaded to the cloud
                GPIO.output(24, 1)   # LED turns on
                time.sleep(0.5)
                GPIO.output(24, 0)   # LED turns off
                time.sleep(0.5)

                count += 1      # 20-second delay in between uploads, due to limit for free ThingSpeak channel



        elif soapAmount <= 0:       # Empty / 0ml left in bottle
            resp = requests.post("https://api.thingspeak.com/apps/thingtweet/1/statuses/update", json = {"api_key":"KJB8LLA1FEVNWRUE", "status":"Your bottle of liquid is empty! (0ml)"})
            print("LED turns on for 15 seconds, when notifying user through ThingTweet.")
            print("Program is shutting down, because bottle is empty. ")
            GPIO.output(24, 1)   # LED turns on
            print("Goodbye! ")
            time.sleep(15)
            GPIO.output(24, 0)   # LED turns off
            
            break



        elif (informed25 == 0) and (soapAmount <= originalAmt / 4):      # 25% or less amount of liquid left in bottle
            resp = requests.post("https://api.thingspeak.com/apps/thingtweet/1/statuses/update", json = {"api_key":"KJB8LLA1FEVNWRUE", "status":"The remaining amount of liquid in the bottle is at 25% or below! "})
            GPIO.output(24, 1)   # LED turns on
            print("LED turns on for 20 seconds, when notifying user through ThingTweet.")
            time.sleep(20)
            GPIO.output(24, 0)   # LED turns off
            
            informed25 = 1



        elif (informed50 == 0) and (soapAmount <= originalAmt / 2):      # 50% or less amount of liquid left in bottle
            resp = requests.post("https://api.thingspeak.com/apps/thingtweet/1/statuses/update", json = {"api_key":"KJB8LLA1FEVNWRUE", "status":"The remaining amount of liquid in the bottle is at 50% or below! "})
            print("LED turns on for 20 seconds, when notifying user through ThingTweet.")
            time.sleep(20)
            GPIO.output(24, 0)   # LED turns off
            
            informed50 = 1


    
