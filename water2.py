import os
import ssl

import RPi.GPIO as GPIO
from telegram.bot import Bot, Update

print(GPIO.VERSION)
context = ssl.create_default_context()

receivers = ["elpilasgsm@gmail.com",
             "daria.zaruba@gmail.com"]

accessToken = os.environ["BOT_ACCESS_TOKEN"]
chatIds = set()
bot = Bot(token=accessToken)


def sendEmail(text):
    updates = bot.get_updates()
    update: Update
    if updates:
        for update in updates:
            chatIds.add(update.effective_chat.id)

    print(chatIds)
    for chatId in chatIds:
        bot.send_message(text=text, chat_id=chatId, )


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


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(FIRST_WATER_LEVEL_DETECTOR["pinId"], FIRST_WATER_LEVEL_DETECTOR["currentState"])
# GPIO.setup(SECOND_WATER_LEVEL_DETECTOR["pinId"], SECOND_WATER_LEVEL_DETECTOR["currentState"])


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


sendEmail("pert the 21st")
GPIO.cleanup()
