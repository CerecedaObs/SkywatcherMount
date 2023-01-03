'''
  This script should be always running on the background.
  It prevents the mount to be outside of the limits.
  In order to have control of the mount:
  - The indi server for eqmod must be running
  - The StartMountControl.py script must be running

  The watchdog can be running with no requirements in order to check for warnings, but the aforementioned steps must be running before taking control of the mount.

'''

from tools import CheckStartMountControl, CheckIndiEQmod
from SkywatcherMount import SkywatcherMount, MountSensors
import time

class Skywatchdog:

  def __init__(self, verbose=2):
    self.verbose = verbose
    self.sensor = MountSensors()
    self.mount = SkywatcherMount(verbose=verbose)
    self.mount.report("Starting watchdog", verbose)
    self.watching = False
    self.halted = False

  def report(self, txt, verbose=None):
    if verbose is None: verbose = self.verbose
    txt = '[watchdog] ' +txt
    self.mount.report(txt, verbose)

  def Watch(self, step=0.5):
    ''' Check each "step" seconds '''
    error = False
    while not error:
      self.watching = True
      error = self.sensor.CheckLimits()
      time.sleep(step)

    if error:
      self.watching = False
      self.report("Hg sensors report error position...")
      if self.sensor.DEClim():
        self.report("Hg sensor reports DEC out of limits!!")
      if self.sensor.RAlim():
        self.report("Hg sensor reports RA out of limits!!")
      self.Halt()

  ######################################################
  ### Functions to check indi server and mount control
  def CheckIndiServer(self):
    indi = CheckIndiEQmod(False)
    if not indi:
      self.report("Indi server is not running... forcing")
      ntries = 0; nmaxtries = 10
      while not indi:
        indi = CheckIndiEQmod(True)
        ntries += 1
        time.sleep(0.1)
        if ntries >= nmaxtries:
          break
    if indi:
      self.report("Indi server is running")
      return 1
    return 0

  def CheckMountControl(self):
    control = CheckStartMountControl(False)
    if not control:
      self.report("Mount control is not started... forcing")
      ntries = 0; nmaxtries = 10
      while not contol:
        control = CheckStartMountControl(True)
        ntries += 1
        time.sleep(0.1)
        if ntries >= nmaxtries:
          break
    if control:
      self.report("Control is running")
      return 1
    return 0

  def CheckMount(self):
    return self.CheckIndiServer() and self.CheckMountControl()
    

  ###############################################################
  ### Function to stop the mount and report

  def StopMount(self):
    self.mount.Stop()

  def Halt(self, gohome=False):
    error = self.sensor.CheckLimits()
    if not error:
      self.report("Halt funtion is called but sensors do not report error... I stop here")
      return 1
    self.halted = True
    control = self.CheckControl()
    if not control: self.report("Cannot take control of the mount!")
      return 0
    self.StopMount()
    if gohome: self.mount.Park()
    self.halted = False
    return 1

if __name__=="__main__":
  swd = Skywatchdog()
  while 1:
    if swd.halted:
      swd.StopMount()
    else:
      if not swd.watching:
        self.Watch()
      time.sleep(0.5)


