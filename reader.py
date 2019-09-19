import pyautogui
import json

data = {}

def lookfor(action):
  if(pyautogui.locateOnScreen(action['img'], region=(getbox(action['area'])))):
    execaction(data['triggerable'][action['trigger']])

def click(action):
  pyautogui.click(getpoint(action['point']))

def getbox(area):
  return area['x'], area['y'], area['w'], area['h']

def getpoint(point):
  return point['x'], point['y']

def execaction(a):
  actions[a['type']](a)
  pyautogui.sleep(0.3)

def readfile():
  global data

  with open('main.mir') as json_file:
    data = json.load(json_file)
    while(True):
      for k, a in sorted(data['stream'].items()):
        execaction(a)

actions = {
  'LO' : lookfor,
  'CL' : click
}

readfile()
