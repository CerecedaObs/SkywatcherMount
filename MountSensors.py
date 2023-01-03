'''
  Requirements:
  - Indi server for eqmod must be running (indiserver indi_eqmod_telescope)
  - Mount control must be running (python StartMountControl.py)

  This module contrains 3 classes (MountSensors, SkywatcherMount, Skywatchdog).

  > MountSensors is a class that retrieves unbiased information about the position of the mount.
  It also gives 'WARNING' state when at least one of the limit sensors is ON.

  > SkywatcherMount is a class to control de mount: move and stop commands, unbiased auto-park...

  > Skywatchdog is a class meant to be always running on the background. It stops the mount when the limit sensors are activated.


'''

import RPi.GPIO as GPIO
import time, os, sys

GPIO.setmode(GPIO.BCM)

PIN_Hg_RA      = 17 # ?? 21??

PIN_Hg_DEC     = 24

PIN_Hg_RA_side = 18
PIN_phot_DEC = 22
PIN_phot_RA  = 23

GPIO.setup(PIN_Hg_DEC    , GPIO.IN)
GPIO.setup(PIN_Hg_RA     , GPIO.IN)
GPIO.setup(PIN_Hg_RA_side, GPIO.IN)
GPIO.setup(PIN_phot_DEC  , GPIO.IN)
GPIO.setup(PIN_phot_RA   , GPIO.IN)
GPIO.setup(21, GPIO.IN)

class MountSensors:
  ###############################################################
  ### Read the sensors

  def __init__(self):
    pass

  def DEClim(self):
    ''' Returns true if DEC beyond limit (by Hg sensor) '''
    return GPIO.input(PIN_Hg_DEC)

  def RAlim(self):
    ''' Returns true if RA beyond limit (by Hg sensor) '''
    pass
    return GPIO.input(PIN_Hg_RA)

  def DECpos(self):
    '''
      1 : it is looking to the left
      0 : it is looking to the right or to the front
    '''
    return GPIO.input(PIN_phot_DEC)

  def RApos(self):
    '''
        1 : is or was leaning to the left
        0 : is or was leaning to the left
    '''
    return GPIO.input(PIN_Hg_RA_side)

  def RAcenter(self):
    ''' Returns 1 if phot sensor is blocked so RA is centered '''
    return GPIO.input(PIN_phot_RA)

  def CheckLimits(self):
    return self.DEClim() or self.RAlim()

from tools import GetNPTtime
class SkywatcherMount:

  def __init__(self, calibration='.mount.calib', report='.mount.report', verbose=1):
    self.calib_file = calibration
    self.report_file = report  
    self.verbose = verbose
    self.npt = GetNPTtime()
    self.t0 = time.time()
    self.isHalted = False
    self.hadError = False

  def Halt(self):
    self.isHalted = True
    self.hadError = True
    self.report('HALTED')

  def Recover(self):
    self.isHaled = False
    self.report('RECOVERED')

  def Reset(self):
    self.isHalted = False
    self.hadError = False
    self.report('RESETTING...')

  def GetTimeNow(self):
    ''' Return current time object '''
    dt = time.time() - self.t0
    t = self.npt+t
    return t

  def GetTimeLabel(self):
    ''' Returns a string with time '''
    return str(time.ctime(self.GetTimeNot()))

  def report(self, txt, verbose=None):
    ''' Write to report file '''
    if verbose is not None: self.verbose=verbose
    report = '[Mount report (%s)] %s'%(self.GetTimeLabel(), txt)
    if verbose >= 2: print(report)
    with open(self.report_file, 'a') as f:
      f.write(txt + '\n')

  ######################################
  ## Telescope control

  def Stop(self):
    pass

  def MoveRA(self):
    pass

  def MoveDEC(self):
    pass

  def RAtoSensorLimit(self):
    ''' Moves RA to find the photosensor edge, close to the park position '''
    pass

  def DECtoSensorLimit(self):
    ''' Moves DEC to find the photosensor edge, close to the park position '''
    pass

  def Park(self):
    ''' First, find photosensor edge positions, then use calibration to go to park position '''
    self.RAtoSensorLimit()
    self.DECtoSensorLimit()
    pass


s = SkywatcherMount(verbose=2)

#while True:
#    print('[17, 18, 21, 24] = [%i, %i, %i, %i]'% (GPIO.input(17), GPIO.input(18), GPIO.input(21), GPIO.input(24)))
#    time.sleep(1.0)
