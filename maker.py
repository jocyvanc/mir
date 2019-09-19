from pynput import keyboard
import pyautogui, os, json

data = {'stream': {}, 'triggerable': {}}
current = set()
pos1, pos2 = None, None
sscount = 0
streamid = 1
triggerableid = 1

SSCOMBO = [
  {keyboard.Key.shift, keyboard.KeyCode(char='S')}
]

POS1COMBO = [
  {keyboard.Key.shift, keyboard.KeyCode(char='Z')}
]

POS2COMBO = [
  {keyboard.Key.shift, keyboard.KeyCode(char='X')}
]

LOCATECOMBO = [
  {keyboard.Key.shift, keyboard.KeyCode(char='L')}
]

CLICKCOMBO = [
  {keyboard.Key.shift, keyboard.KeyCode(char='C')}
]

ENDCOMBO = [
  {keyboard.Key.shift, keyboard.KeyCode(char='Q')}
]

COMBINATIONS = SSCOMBO + POS1COMBO + POS2COMBO + ENDCOMBO + LOCATECOMBO + CLICKCOMBO

def on_press(key):
  global pos1, pos2

  if any([key in COMBO for COMBO in COMBINATIONS]):
    current.add(key)
    if any(all(k in current for k in COMBO) for COMBO in SSCOMBO):
      screenshot()
    if any(all(k in current for k in COMBO) for COMBO in POS1COMBO):
      pos1 = pyautogui.position()
    if any(all(k in current for k in COMBO) for COMBO in POS2COMBO):
      pos2 = pyautogui.position()
    if any(all(k in current for k in COMBO) for COMBO in ENDCOMBO):
      end()
    if any(all(k in current for k in COMBO) for COMBO in LOCATECOMBO):
      locate()
    if any(all(k in current for k in COMBO) for COMBO in CLICKCOMBO):
      click()

  clear()

def on_release(key):
  if any([key in COMBO for COMBO in COMBINATIONS]):
    current.remove(key)

def screenshot():
  global sscount
  sscount = sscount + 1

  ss = pyautogui.screenshot(region=(pos1.x, pos1.y, pos2.x - pos1.x, pos2.y - pos1.y))
  ss.save("ss%d.png" % sscount)

def locate():
  clear()
  print(data['triggerable'])

  action = {
    'type': 'LO',
    'img': ("ss%d.png" % sscount),
    'area': {'x': pos1.x, 'y': pos1.y, 'w': pos2.x - pos1.x, 'h': pos2.y - pos1.y},
    'trigger': input('id >> ')
  }

  addtodata(action)

def click():
  action = {
    'type': 'CL',
    'point': {'x': pos1.x, 'y': pos1.y}
  }

  addtodata(action)

def addtodata(action):
  global data, triggerableid, streamid

  clear()
  if(input('[t/s] >> ') == 't'):
    data['triggerable'][triggerableid] = action
    triggerableid = triggerableid + 1
  else:
    data['stream'][streamid] = action
    streamid = streamid + 1

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def end():
  with open('main.mir', 'w') as outfile:
    json.dump(data, outfile)
    exit()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
  listener.join()
