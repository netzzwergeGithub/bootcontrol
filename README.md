# Bootcontrol  Snips skill

Skill to shutdown or reboot the underlying raspberry pi system via voice control.
It's a case study for executing system commands as voice commands.

The dialog can be started using the push-button on Seeds respeaker 2 Mic hat.
It's just an example how to initiate an snips dialog via an external event.


## Possible commands
Some commands have a optional time-parameter. If you add no time-parameter the command is executed immediately.

```
   reboot [time to reboot]
       Schedule a a reboot of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'.
       Examples:
       reboot
       reboot in ten minutes
```

```
shutdown  [time to shutdown]
Schedule a a shutdown of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'. Examples:
shutdown
shutdown at ten o clock
```
```
halt  [time to shutdown]
Schedule a a halt of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'. Examples:
halt
halt at tomorrow at 10 am
```
```
stop shutdown
Stop a scheduled reboot, shutdown or halt.
```
```
help
Get a short help which commands the app understands.
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
