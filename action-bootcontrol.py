#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from  timeconvert import  getMinutesToShutdown

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

BOOTCONTROL_INTENT = "mardeh:SystemCommand"
CONFIRM_INTENT = "mardeh:confirm"
REPLAY_INTENT = "mardeh:replay"
CANCEL_INTENT = "mardeh:cancel"
PASSWORD_INTENT = "mardeh:password"
follow_up_intents = [CONFIRM_INTENT,REPLAY_INTENT,CANCEL_INTENT, PASSWORD_INTENT]
# String-Template for command to execute
SHUTDOWN_STRING = "sudo shutdown {} +{}"
SHUTDOWN_STRING_CANCEL = "sudo shutdown {} "
TO_CONFIRM_TEXT = "Confirm with 'yes', abort with 'no', repeat question with 'repeat'."

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_session_started(hermes, intentMessage):
    print("Session started\n")
    ApplicationState.resetCommandState()

def subscribe_session_ended(hermes, intentMessage):
    print("Session Ended\n")
    confirmed = ApplicationState.getCommandConfirmed()
    if confirmed:
        command = ApplicationState.getCommandToExecute()
        if command != None:
            print(command)
            os.system(command)
    ApplicationState.resetCommandState()

def subscribe_replay_intent_callback(hermes, intentMessage):
    hermes.publish_continue_session(intentMessage.session_id, ApplicationState.getlastSpokenText(), follow_up_intents)

def subscribe_cancel_intent_callback(hermes, intentMessage):
    hermes.publish_end_session(intentMessage.session_id, "{} canceld".format(ApplicationState.getRequestedCommand() ))
    ApplicationState.resetCommandState()

def subscribe_confirm_intent_callback(hermes, intentMessage):
    ApplicationState.confirmCommand()

    if ApplicationState.getRequestedCommand() == "stop shutdown":
        sentence =  "Ok, system will stop the shutdown"
    else:
        sentence = "Ok, system will {} {}.".format(ApplicationState.getRequestedCommand(),ApplicationState.getWaitingTimeText())
    hermes.publish_end_session(intentMessage.session_id,  sentence)

def subscribe_bootcontrol_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    session_id = intentMessage.session_id
    ApplicationState.setRequestedCommand(intentMessage.slots.registeredCommand.first().value)
    if intentMessage.slots.timeToExcecute:
        timeToExecute =intentMessage.slots.timeToExcecute.first().value
        ApplicationState.setRequestedTimeOfExecution(getMinutesToShutdown(timeToExecute))
    else:
        ApplicationState.setRequestedTimeOfExecution(0)

    if ApplicationState.getRequestedCommand() == "reboot":
        shortCommand = "-r"
    elif ApplicationState.getRequestedCommand() == "halt":
        shortCommand = "-H"
    elif ApplicationState.getRequestedCommand() == "shutdown":
        shortCommand = "-P"
    elif ApplicationState.getRequestedCommand() == "stop shutdown":
        shortCommand = "-c"
    else:
        hermes.publish_end_session(intentMessage.session_id, "Wrong command {}".format(ApplicationState.getRequestedCommand() ))

    if ApplicationState.getRequestedCommand() == "stop shutdown":
        sentence =  "The system shutdown will be canceld. {}".format(TO_CONFIRM_TEXT)
        ApplicationState.setCommandToExecute(SHUTDOWN_STRING_CANCEL.format(shortCommand))

    else:
        sentence =  "The system will {} {}. {}".format(ApplicationState.getRequestedCommand(), ApplicationState.getWaitingTimeText(),TO_CONFIRM_TEXT)
        ApplicationState.setCommandToExecute(SHUTDOWN_STRING.format(shortCommand, ApplicationState.getRequestedTimeOfExecution()))

    hermes.publish_continue_session(intentMessage.session_id, sentence, follow_up_intents)


    ApplicationState.setlastSpokenText(sentence)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(BOOTCONTROL_INTENT, subscribe_bootcontrol_intent_callback) \
         .subscribe_intent(CONFIRM_INTENT, subscribe_confirm_intent_callback) \
         .subscribe_intent(REPLAY_INTENT, subscribe_replay_intent_callback) \
         .subscribe_intent(CANCEL_INTENT, subscribe_cancel_intent_callback) \
         .subscribe_session_started( subscribe_session_started) \
         .subscribe_session_ended( subscribe_session_ended) \
         .start()
