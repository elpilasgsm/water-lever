import smtplib, os
import ssl
from smtplib import SMTPException
from time import sleep

import RPi.GPIO as GPIO

print(GPIO.VERSION)
context = ssl.create_default_context()

receivers = ["elpilasgsm@gmail.com",
             "daria.zaruba@gmail.com",
             "duzaporozhets@sfedu.ru",
             "dvzaruba@sfedu.ru"]

sender = os.environ["SMTP_USERNAME"]
password = os.environ["SMTP_PASSWORD"]
server = os.environ["SMTP_SERVER"]
port = os.environ["SMTP_PORT"]

def sendEmail(text):
    try:
        smtpObj = smtplib.SMTP(server, port)
        smtpObj.ehlo()  # Can be omitted
        smtpObj.starttls(context=context)  # Secure the connection
        smtpObj.ehlo()  # Can be omitted
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, text)
        print("Successfully sent email")
    except SMTPException:
        print("Can't Send Email")

FIRST_WATER_LEVEL_DETECTOR = {
    "name": "Yellow: 2/3 of Water Tank",
    "pinId": 17,
    "currentState": 0
}
SECOND_WATER_LEVEL_DETECTOR = {
    "name": "Orange: 1/3 of Water Tank",
    "pinId": 27,
    "currentState": 0
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(FIRST_WATER_LEVEL_DETECTOR["pinId"], FIRST_WATER_LEVEL_DETECTOR["currentState"])
GPIO.setup(SECOND_WATER_LEVEL_DETECTOR["pinId"], SECOND_WATER_LEVEL_DETECTOR["currentState"])


def onDetectorListen(detector):
    curVal = detector["currentState"]
    val = GPIO.input(detector["pinId"])

    if val != curVal:
        detector["currentState"] = val
        text = ""
        if val == 0:
            text = format("""\
Subject: Home Water level DECREASING: %s

The Lever is gone BELOW the detector Level: %s
Please decrease the usage of water.
""" % (detector['name'], detector['name']))
        else:
            text = format("""\
Subject: Home Water level INCREASING: %s

The Lever is gone Above the detector Level: %s
This is Good Sign.
""" % (detector['name'], detector['name']))
        print(text)
        sendEmail(text)


try:
    while True:
        onDetectorListen(FIRST_WATER_LEVEL_DETECTOR)
        onDetectorListen(SECOND_WATER_LEVEL_DETECTOR)
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
