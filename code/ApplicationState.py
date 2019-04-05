class ApplicationState:
    # state variables
    command_to_execute = None # command line to be executed after confirming
    requested_command = None # command extracted fom SystemCommand intent
    requested_time_of_execution = 0 # minutes before eexecution of commend
    last_spoken_text = None   # last text send to user. Used on replay-Intent
    command_confirmed= False # has the user confirmed the command


    @classmethod
    def  resetCommandState(cls):
        cls.command_to_execute = None # command line to be executed after confirming
        cls.requested_command = None # command extracted fom SystemCommand intent
        cls.requested_time_of_execution = 0 # minutes before eexecution of commend
        cls.last_spoken_text = None   # last text send to user. Used on replay-Intent
        cls.command_confirmed= False # has the user confirmed the command

    @classmethod
    def confirmCommand(cls):
        cls.command_confirmed = True

    @classmethod
    def getCommandConfirmed(cls):
        return cls.command_confirmed

    @classmethod
    def setlastSpokenText(cls,text):
        cls.last_spoken_text = text

    @classmethod
    def setCommandToExecute(cls,command):
        cls.command_to_execute = command

    @classmethod
    def setRequestedCommand(cls,command):
        cls.requested_command = command

    @classmethod
    def setRequestedTimeOfExecution(cls, executionTime):
        cls.requested_time_of_execution = executionTime

    @classmethod
    def getlastSpokenText(cls):
        return cls.last_spoken_text

    @classmethod
    def getCommandToExecute(cls):
        return cls.command_to_execute

    @classmethod
    def getRequestedCommand(cls):
        return cls.requested_command

    @classmethod
    def getRequestedTimeOfExecution(cls):
        return cls.requested_time_of_execution

    @classmethod
    def getWaitingTimeText(cls):
        if(cls.requested_time_of_execution == 0):
            return "immediately"
        if(cls.requested_time_of_execution == 1):
            return "in one minute".format(cls.requested_time_of_execution)
        return "in {} minutes".format(cls.requested_time_of_execution)

