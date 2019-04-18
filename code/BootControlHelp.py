
class BootControlHelp:
    def getText():
        return '''Bootcontrol allows you to shutdown or reboot the underlying raspberry system.
                  You can use the commands 'shutdown' , 'reboot', 'halt'.
                  To execute a command later you can add an time to the command like:
                  'shutdown in five minutes'.
                  If a shutdown command is scheduled you can cancel it, saying 'stop shutdown'.

                  Which command shoud I execute?
                '''
