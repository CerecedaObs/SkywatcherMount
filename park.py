'''
  Script to park the skywatecher mount
  In order to have control of the mount:
  - The indi server for eqmod must be running
  - The StartMountControl.py script must be running

  This script does not force to run the indi server or the StartMountControl script! 
'''

mount = SkywatcherMount(verbose=2)
mount.report("Parking script has been called!")
status = mount.Park()
print('Park status = ', status)
