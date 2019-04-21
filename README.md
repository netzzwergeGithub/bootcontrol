# Bootcontrol  Snips skill

Skill to shutdown or reboot the underlying raspberry pi system via voice control.
It's a case study for executing system commands as voice commands.

The dialog can be started using the push-button on Seeds respeaker 2 Mic hat.
It's just an example how to initiate an snips dialog via an external event.


## Possible commands
Some commands have a optional time-parameter. If you add no time-paramter the command is excuted immediately.

```
   reboot [time to reboot]
       Shedule a a reboot of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'.
       Examples:
       reboot
       reboot in ten minutes
```
```
shutdown  [time to shutdown]
Shedule a a shutdown of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'. Examples:
shutdown
shutdown at ten o clock
```
```
halt  [time to shutdown]
Shedule a a halt of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'. Examples:
halt
halt at tomorrow at 10 am
```
```
stop shutdown
Stop a sheduled reboot, shutdown or halt.
```
```
help
Get a short help what commands the app understands.
```


Additionally the commands reboot, shutdown and halt can be timed, like 'shutdown in ten minutes', 'reboot tomorrow at noon".


snips.toml

user/groups

visudo

GPIO (BCM) PIN 17
snips.toml => 30 Sekunden.

## Setup

# GPIO access
# sudoers

Please read the app description.
