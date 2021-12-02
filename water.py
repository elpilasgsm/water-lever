import os
import ssl
from time import sleep

import RPi.GPIO as GPIO
from telegram.bot import Bot, Update

print(GPIO.VERSION)
context = ssl.create_default_context()
accessToken = os.environ["BOT_ACCESS_TOKEN"]
bot = Bot(token=accessToken)

snowflake = u'\U00002744'
decreasing = u'\U0001F621'
increasing = u'\U0001F60A'
yellowLevelDecr = u'\U0001F625'
yellowLevelIncr = u'\U0001F60F'
redLevelDecr = u'\U0001F631'
redLevelIncr = u'\U0001F630'


def sendEmail(text):
    # chatIds = set()
    # updates = bot.get_updates()
    # update: Update
    # if updates:
    #     for update in updates:
    #         chatIds.add(update.effective_chat.id)
    #
    # print(chatIds)
    # for chatId in chatIds:
    bot.send_message(text=text, chat_id="-1001600345896", )


FIRST_WATER_LEVEL_DETECTOR = {
    "name": "2/3 of Water Tank",
    "pinId": 17,
    "decreasingLabel": yellowLevelDecr,
    "increasingLabel": yellowLevelIncr,
    "currentState": 0
}
SECOND_WATER_LEVEL_DETECTOR = {
    "name": "1/3 of Water Tank",
    "pinId": 27,
    "decreasingLabel": redLevelDecr,
    "increasingLabel": redLevelIncr,
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
        if val == 0:
            text = format("""
%s %s The Lever is BELOW the detector Level: %s
Please decrease the usage of water.
""" % (decreasing, detector["decreasingLabel"], detector['name']))
        else:
            text = format("""
%s %s The Lever is ABOVE the detector Level: %s.
""" % (increasing, detector["increasingLabel"], detector['name']))
        print(text)
        sendEmail(text)


try:
    while True:
        onDetectorListen(FIRST_WATER_LEVEL_DETECTOR)
        onDetectorListen(SECOND_WATER_LEVEL_DETECTOR)
        sleep(60.0)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
