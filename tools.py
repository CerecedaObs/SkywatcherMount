import ntplib
import time
import subprocess, os, sys

def GetNPTtime():
  ''' Sync time with the internet '''
  c = ntplib.NTPClient()
  response = c.request('europe.pool.ntp.org', version=3)
  return response.tx_time

def ExecSubprocess(cmd, communicate=False, verbose=False):
  ''' Function to execute cmd in the background '''
  if verbose:
    print('Executing subprocess: ', cmd)
  process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if communicate:
    return process.communicate()
  else:
    return process

def CheckIDprocesses(string, verbose=False):
  ''' Return a list of IDs of processes containing string '''
  pid1, err1 = ExecSubprocess('pgrep -f "%s"'%string, True, verbose)
  pid2, err2 = ExecSubprocess('pgrep -f "%s"'%string, True)
  pid1 = pid1.splitlines()
  pid2 = pid2.splitlines()
  processes = [x for x in pid1 if x in pid2]
  return processes

def KillProcess(string):
  ''' Kill processes containing the string '''
  pids = CheckIDprocesses(string)
  for pid in pids:
    os.system(f'kill -9 {int(pid)}')

def KillKStars():
  ''' Kills kstars if found '''
  KillProcess('kstars')
  
def KillIndiServer():
  ''' Kills indiserver if found '''
  KillProcess('indiserver')

def StartEQmod():
  ''' Start indisever with eqmod driver '''
  print('Starting indiserver indi_eqmod_telescope...')
  ExecSubprocess('indiserver indi_eqmod_telescope') 

def CheckIndiEQmod(activate=False):
  ''' Check if the indi server for indi_eqmod_telescope is running 
      If activate: runs a script on the background to activate indi server
  '''
  running = CheckIDprocesses('indi_eqmod_telescope')
  if len(running) == 0 and activate:
    print('EQMod is not active!')
    StartEQmod()
    running = CheckIDprocesses('indi_eqmod_telescope')
  return len(running) > 0

def CheckStartMountControl(activate=False):
  ''' Check if the SkywatcherMount script is running.
      If not and activate is True, it runs the script on the background.
      # Note: should we change the query string by something like "python */StartMountControl.py"?
  '''
  running = CheckIDprocesses('StartMountControl.py')
  if len(running) == 0 and activate:
    print('StartMountControl is not running!')
    path = os.getcwd()
    cmd = f'python {path}/StartMountControl.py'
    ExecSubprocess(cmd, verbose=1)
    running = CheckIDprocesses('StartMountControl.py')
  return len(running) > 0
