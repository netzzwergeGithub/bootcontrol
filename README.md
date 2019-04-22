# Bootcontrol  Snips skill

Skill to shutdown or reboot the underlying raspberry pi system via voice control.
It's a case study for executing system commands as voice commands.

It uses the raspberry pi with raspian an the seeeds respeaker 2 Mic hat.
It expects having installed a snips system on a raspberry pi (e.g. https://docs.snips.ai/getting-started/quick-start-raspberry-pi) and the ReSpeaker 2-Mics Pi HAT ( http://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/#getting-started)

The dialog can be started using the push-button on respeaker 2 Mic hat.
It's an example how to initiate an snips dialog via an external event.

**Caution:** The project manipulates the underlying raspberry pi system. You should have experience in using the unix commandline unsing ssh.


## Possible commands
Some commands have a optional time-parameter. If you add no time-parameter the command is executed immediately.

**reboot [time to reboot]**

_Schedule a a reboot of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'.
       Examples:_
```
reboot
reboot in ten minutes
```

**shutdown  [time to shutdown]**

_Schedule a a shutdown of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'. Examples:_
```
shutdown
shutdown at ten o clock
```
**halt  [time to shutdown]**

_Schedule a a halt of the system. Optionally you can add a time value like 'in five minutes' or 'tommorow at noon'. Examples:_
```
halt
halt at tomorrow at 10 am
```
**stop shutdown**

_Stop a scheduled reboot, shutdown or halt. Usage:_
```
stop shutdown
```

**help**

_Get a short help which commands the app understands. Usage:_
```
help
```

## Adaption of the underlying system
The following changes have to be made directly on the raspberry pi.

**increase dialog timeout**

Because the respond text of the help command is a little bit longish you have to increase the timeout for the session to 25 seconds.
You have to add a line to the file *'/etc/snips.toml'* for the category '[snips-dialogue]' using the sudo command with your favorite editor:
```
[snips-dialogue]
session_timeout = 25

```

**add skills user to sudoers**

You have to configure the system to allow the _\_snips_skills_ user to execute the bootcontrol commands.
First open the sudoers file via the command **visudo** and add the following lines and save and exit the editor:
```
 Cmnd_Alias      SHUTDOWN = /sbin/shutdown
 # allow shutdown
_snips-skills  ALL=(ALL) NOPASSWD: SHUTDOWN

```  

**deactivate hotword detection**

To limit the activation of the bootcontrol app to the pushing of the button you have to disable the snips hotword detection with the command:
```
sudo systemctl disable snips-hotword.service
```
**Caution:** This command will deactivate the activation of the snips dialog via the hotword (e.g. hey snips) for the whole system. To reactivate it use the command: **sudo systemctl enable snips-hotword.service**

snips.toml

user/groups

visudo

GPIO (BCM) PIN 17
snips.toml => 30 Sekunden.

## Setup

## GPIO access

Please read the app description.
