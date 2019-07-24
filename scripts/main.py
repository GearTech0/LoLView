from PIL import Image, ImageGrab
from pytesseract import Output
import pytesseract
import win32gui, win32com.client

hwnd = win32gui.FindWindow(None, "League of Legends")

# Send alt keys
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')

win32gui.SetForegroundWindow(hwnd)
bbox = win32gui.GetWindowRect(hwnd)
img = ImageGrab.grab(bbox)
img = img.resize((6398, 3600), Image.ANTIALIAS)
img.save("image_300.jpg", "JPEG", dpi=(300, 300))

def output_to_array(output):
    ret = []
    word = ""
    for c in output:
        if c is '\n':
            if "joined the lobby" in word:
                ret.append(word)    
            word = ""
            continue
        else:
            word += c
    return ret

def get_players(list):
    players = []
    for word in list:
        ind = word.index("joined")
        player = word[:ind-1]
        if player not in players:
            players.append(player)
    return players

def read_screenshot():
    output_dict = pytesseract.image_to_string("image_300.jpg", config=r'-l eng --psm 11 --dpi 300')
    output_list = output_to_array(output_dict)
    players = get_players(output_list)
    print("Players are: ", players)

read_screenshot()