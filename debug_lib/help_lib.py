import pprint

def getFormattedIntentMessage(intent_message):
  message = "\n\n"
  message +=  "\n" + "SessionID: {}".format(intent_message.session_id)
  message +=  "\n" + "CustomData: {}".format(intent_message.custom_data)
  message +=  "\n" + "SiteID: {}".format(intent_message.site_id)
  message +=  "\n" + "input: {}".format(intent_message.input)
  message +=  "\n" + 'Intent.name: {}'.format(intent_message.intent.intent_name)
  message +=  "\n" + 'Intent.confidence: {}'.format(intent_message.intent.confidence_score)

  if  intent_message.slots:
    for (slot_value, slot) in intent_message.slots.items():
          message +=  "\n" + 'Slot {} -> \n\tRaw: {} \tValue: {}'.format(slot_value, slot[0].raw_value, slot[0].slot_value.value.value)
  message +=  "\n" +  "\n\n"
  return message

def print_intentMessage(intent_message):
  print(getFormattedIntentMessage(intent_message))

def save_intentMessage(intent_message, file_path):
  with open(file_path, 'w') as file:
    file.write(getFormattedIntentMessage(intent_message))

