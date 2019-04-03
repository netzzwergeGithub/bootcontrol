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

from  timeconvert import  getMinutesToShutdown

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

BOOTCONTROL_INTENT = "mardeh:SystemCommand"
CONFIRM_INTENT = "mardeh:confirm"
REPLAY_INTENT = "mardeh:replay"
CANCEL_INTENT = "mardeh:cancel"
follow_up_intents = [CONFIRM_INTENT,REPLAY_INTENT,CANCEL_INTENT]
# String-Template for command to execute
SUDO_STRING = "sudo shutdown {} +{}"
class ApplicationState:
    # state variables
    command_to_execute = None # command line to be executed after confirming
    requested_command = None # command extracted fom SystemCommand intent
    requested_time_of_execution = 0 # minutes before eexecution of commend
    last_spoken_text = None   # last text send to user. Used on replay-Intent


def  reset_command_state():
    ApplicationState.command_to_execute = None # command line to be executed after confirming
    ApplicationState.requested_command = None # command extracted fom SystemCommand intent
    ApplicationState.requested_time_of_execution = 0 # minutes before eexecution of commend
    ApplicationState.last_spoken_text = None   # last text send to user. Used on replay-Intent

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
    reset_command_state()

def subscribe_session_ended(hermes, intentMessage):
    print("Session Ended\n")
    if ApplicationState.command_to_execute != None:
        print(ApplicationState.command_to_execute)
        os.system(ApplicationState.command_to_execute)
    reset_command_state()

def subscribe_replay_intent_callback(hermes, intentMessage):
    hermes.publish_continue_session(intentMessage.session_id, ApplicationState.last_spoken_text, follow_up_intents)

def subscribe_cancel_intent_callback(hermes, intentMessage):
    #print(ApplicationState.requested_command)
    hermes.publish_end_session(intentMessage.session_id, "{} canceld".format(ApplicationState.requested_command ))
    reset_command_state()

def subscribe_confirm_intent_callback(hermes, intentMessage):
    #print(ApplicationState.requested_command)
    confirm =  intentMessage.slots.confirm.first().value

    hermes.publish_end_session(intentMessage.session_id, "System will {} in {} minutes".format(ApplicationState.requested_command,ApplicationState.requested_time_of_execution))
    # os.system(ApplicationState.command_to_execute)

def subscribe_bootcontrol_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    session_id = intentMessage.session_id
    ApplicationState.requested_command =  intentMessage.slots.registeredCommand.first().value
    if intentMessage.slots.timeToExcecute:
        timeToExecute =intentMessage.slots.timeToExcecute.first().value
        ApplicationState.requested_time_of_execution = getMinutesToShutdown(timeToExecute)
        #print (ApplicationState.requested_time_of_execution)
    else:
        ApplicationState.requested_time_of_execution = 0

    if ApplicationState.requested_command == "reboot":
        shortCommand = "-r"
    elif ApplicationState.requested_command == "halt":
        shortCommand = "-H"
    elif ApplicationState.requested_command == "shutdown":
        shortCommand = "-P"
    else:
        hermes.publish_end_session(intentMessage.session_id, "Wrong command {}".format(ApplicationState.requested_command ))


    sentence =  "The system will {} in {} minutes. Confirm with 'yes', abort with 'no', replay with 'repeat' ".format(ApplicationState.requested_command, ApplicationState.requested_time_of_execution)
    hermes.publish_continue_session(intentMessage.session_id, sentence, follow_up_intents)

    ApplicationState.command_to_execute = SUDO_STRING.format(shortCommand, ApplicationState.requested_time_of_execution)
    #print(ApplicationState.command_to_execute )

    ApplicationState.last_spoken_text = sentence 


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
