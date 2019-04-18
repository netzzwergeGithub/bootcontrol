#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
        import RPi.GPIO as GPIO
except RuntimeError:
        print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io
import os
import sys
import datetime
import time


from code.ApplicationState import ApplicationState
from code.GPIOInputThread import GPIOInputThread
from code.BootControlHelp import BootControlHelp

from  timeconvert import  getMinutesToShutdown

CONFIGURATION_ENCODING_FORMAT = "utf-8"

# the used intents
BOOTCONTROL_INTENT = "mardeh:SystemCommand"
BOOTCONTROL_HELP_INTENT = "mardeh:help"
CONFIRM_INTENT = "mardeh:confirm"
REPLAY_INTENT = "mardeh:replay"
CANCEL_INTENT = "mardeh:cancel"
PASSWORD_INTENT = "mardeh:password"
follow_up_intents = [CONFIRM_INTENT,REPLAY_INTENT,CANCEL_INTENT, PASSWORD_INTENT, BOOTCONTROL_HELP_INTENT ]
# String-Template for command to execute
SHUTDOWN_STRING = "sudo shutdown {} +{}"
SHUTDOWN_STRING_CANCEL = "sudo shutdown {} "
TO_CONFIRM_TEXT = "Confirm with 'yes', abort with 'no', repeat question with 'repeat'."

# GPIO-Pin of Buttopn on respeaker 2 Mic
RESPEAKER_BUTTON = 17


def session_started(hermes, intentMessage):
    # print("Session started\n")
    #clear state on session start (for savety sake)
    ApplicationState.resetCommandState()

def session_ended(hermes, intentMessage):
    '''
    We execute the requested command after the session ended because the 'Ok'-message of the dialog would not be spoken on an immediately executed shutdown.
    '''
    # print("Session Ended\n")

    confirmed = ApplicationState.getCommandConfirmed()
    # only execute confirmed commands
    if confirmed:
        command = ApplicationState.getCommandToExecute()
        if command != None:
            print(command)
            os.system(command)
    #clear state on session end
    ApplicationState.resetCommandState()

def replay_intent_callback(hermes, intentMessage):
    hermes.publish_continue_session(intentMessage.session_id, ApplicationState.getlastSpokenText(), follow_up_intents)

def help_intent_callback(hermes, intentMessage):
    #clear state on help intent
    ApplicationState.resetCommandState()
    hermes.publish_continue_session(intentMessage.session_id, BootControlHelp.getText(),  [BOOTCONTROL_INTENT, BOOTCONTROL_HELP_INTENT ])

def cancel_intent_callback(hermes, intentMessage):
    hermes.publish_end_session(intentMessage.session_id, "{} canceld".format(ApplicationState.getRequestedCommand() ))
    #clear state on cancelling command
    ApplicationState.resetCommandState()

def confirm_intent_callback(hermes, intentMessage):
    #saving the confirmation of the user
    ApplicationState.confirmCommand()
    if ApplicationState.getRequestedCommand() == "stop shutdown":
        sentence =  "Ok, system will stop the shutdown"
    else:
        sentence = "Ok, system will {} {}.".format(ApplicationState.getRequestedCommand(),ApplicationState.getWaitingTimeText())
    # feedback to user and end session. Requested command will be executed after session ended.
    hermes.publish_end_session(intentMessage.session_id,  sentence)

def bootcontrol_intent_callback(hermes, intentMessage):
    """
    react on the different commands of the bootcontrol intentMessage
    """
    session_id = intentMessage.session_id
    ApplicationState.setRequestedCommand(intentMessage.slots.registeredCommand.first().value)
    # get the minutes to wait before shutdown etc.
    if intentMessage.slots.timeToExcecute:
        timeToExecute =intentMessage.slots.timeToExcecute.first().value
        ApplicationState.setRequestedTimeOfExecution(getMinutesToShutdown(timeToExecute))
    else:
        ApplicationState.setRequestedTimeOfExecution(0)

    # decide the switch to use for the shutdiwn command
    if ApplicationState.getRequestedCommand() == "reboot":
        shortCommand = "-r"
    elif ApplicationState.getRequestedCommand() == "halt":
        shortCommand = "-H"
    elif ApplicationState.getRequestedCommand() == "shutdown":
        shortCommand = "-P"
    elif ApplicationState.getRequestedCommand() == "stop shutdown":
        shortCommand = "-c"
    else:
        '''
         handle unknown command requests
        '''
        hermes.publish_end_session(intentMessage.session_id, "Wrong command {}".format(ApplicationState.getRequestedCommand() ))

    if ApplicationState.getRequestedCommand() == "stop shutdown":
        # sentence for canceling shutdown
        sentence =  "The system shutdown will be canceld. {}".format(TO_CONFIRM_TEXT)
        # Save command to execute after confirmation
        ApplicationState.setCommandToExecute(SHUTDOWN_STRING_CANCEL.format(shortCommand))

    else:
        #sentence for shutdown resetCommands
        sentence =  "The system will {} {}. {}".format(ApplicationState.getRequestedCommand(), ApplicationState.getWaitingTimeText(),TO_CONFIRM_TEXT)
        # Save command to execute after confirmation
        ApplicationState.setCommandToExecute(SHUTDOWN_STRING.format(shortCommand, ApplicationState.getRequestedTimeOfExecution()))

    hermes.publish_continue_session(intentMessage.session_id, sentence, follow_up_intents)
    # save the last spoken sentence. Used if the usere requests an reprtition of the spoken words.
    ApplicationState.setlastSpokenText(sentence)


def onPin17High( ):
    '''
      callback function called on rising edge
    '''
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.publish_start_session_action(None,
            "Boot control activated. You say 'shutdown', 'reboot' or 'halt'. Or you can get help, saying 'help'",
            [BOOTCONTROL_INTENT, BOOTCONTROL_HELP_INTENT ],
            True, False, None)

if __name__ == "__main__":
    try:
        # Start the background thread, which is polling the GPIO-Pin (BCM-Layout)
        # GPIOInputThread(RESPEAKER_BUTTON, onPinState, check_interval=1 )
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RESPEAKER_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(RESPEAKER_BUTTON, GPIO.RISING, callback = onPin17High, bouncetime = 200)
        # Register on intents and state changes
        mqtt_opts = MqttOptions()
        with Hermes(mqtt_options=mqtt_opts) as h:
            h.subscribe_intent(BOOTCONTROL_INTENT, bootcontrol_intent_callback) \
             .subscribe_intent(BOOTCONTROL_HELP_INTENT, help_intent_callback) \
             .subscribe_intent(CONFIRM_INTENT, confirm_intent_callback) \
             .subscribe_intent(REPLAY_INTENT, replay_intent_callback) \
             .subscribe_intent(CANCEL_INTENT, cancel_intent_callback) \
             .subscribe_session_started( session_started) \
             .subscribe_session_ended( session_ended) \
             .start()
    finally:
         GPIO.cleanup()
