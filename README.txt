# Mount control

### Init indi server

First, you must have an indi server running 'indi_eqmod_telescope'. You can do it by hand or through kstars/EKOS.
You can do it by hand by executing:

    indiserver indi_eqmod_telescope

Start the control script by executing:

    python StartMountControl.py

It has to be running on the background. Now you are ready to send commands to the mount.

### How to send commands

Commands are sent by writing lines into a txt file that is by default located in '/tmp/mountcommands.txt'
Commands have the form [axis  direction  speed  (n seconds)] as in this example, that would move the DEC axis to the right with a speed of 8 for 5 seconds.

    echo "DEC right 8 5" > ~/python/.commands.txt

### Automatic start

# Sensors and wachdog
