
class BootControlHelp:
    def getText():
        return '''Boot control allows you to shutdown or reboot the underlying raspberry system.
                  You can use the commands 'shutdown' , 'reboot', 'halt'.

                  To execute a command later you can add an time to the command, like:
                  'shutdown in five minutes'.

                  If a shutdown command is scheduled you can cancel it, saying
                  'stop shutdown'.

                  Which command you want to execute?
                '''
