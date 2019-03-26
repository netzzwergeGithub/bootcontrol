#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from debug_lib.help_lib import  print_intentMessage
from debug_lib.help_lib import  save_intentMessage
import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io
import os
import sys
import datetime
from  timeconvert import  getMinutesToShutdown

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

BOOTCONTROL_INTENT = "mardeh:SystemCommand"
CONFIRM_INTENT = "mardeh:confirm"
SUDO_STRING = "sudo shutdown {} +{}"

command_to_execute = None


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

def subscribe_confirm_intent_callback(hermes, intentMessage):
    confirm =  intentMessage.slots.confirm.first().value
    if confirm == "yes":
        pass
    else:
        pass

    hermes.publish_end_session(intentMessage.session_id, "You said '{}".format(confirm))

def subscribe_bootcontrol_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    session_id = intentMessage.session_id
    print("action_wrapper")
    print(sys.version_info)
    #print_intentMessage(intentMessage)
    tempDir = "tmp"
    if not os.path.isdir(tempDir):
        os.mkdir(tempDir)
    save_intentMessage(intentMessage, "{}/{}_messageInfo.txt".format(tempDir,session_id))
    command =  intentMessage.slots.registeredCommand.first().value
    if intentMessage.slots.timeToExcecute:
        timeToExecute =intentMessage.slots.timeToExcecute.first().value
        minutesToGo = getMinutesToShutdown(timeToExecute)
        print (minutesToGo)
    else:
        minutesToGo = 0

    if command == "reboot":
        shortCommand = "-r"
    if command == "halt":
        shortCommand = "-H"
    if command == "shutdown":
        shortCommand = "-P"

    sentence =  "The system will {} in {} minutes. Confirm with 'yes', abort with 'no'? ".format(command, minutesToGo)
    hermes.publish_continue_session(intentMessage.session_id, sentence, [CONFIRM_INTENT])

    command_to_execute = SUDO_STRING.format(shortCommand, minutesToGo)
    #os.system(SUDO_STRING.format(shortCommand, timeToExecute))


if __name__ == "__main__":
    print(sys.version_info)
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(BOOTCONTROL_INTENT, subscribe_bootcontrol_intent_callback) \
         .subscribe_intent(CONFIRM_INTENT, subscribe_confirm_intent_callback) \
         .start()
