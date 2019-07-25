from PIL import Image, ImageGrab
from pytesseract import Output
import pytesseract
import win32gui
import win32com.client

"""
    1900 = 1 inch/96 pixels = 19.7917in
    600 = 1 inch/96 pixels = 6.25in
"""


def get_client_screenshot():
    """
    Screenshot the LoL client and scale image to be 300dpi

    Returns
    -------
    Image
        Processed image of LoL client
    """
    hwnd = win32gui.FindWindow(None, "League of Legends")

    # Send alt keys
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)

    # Calculate new size based on DPI change to 300
    width, height = img.size
    dpi = 96
    if img.info['dpi']:
        dpi = img.info['dpi']

    width = width * (300 / dpi)
    height = height * (300 / dpi)

    img = img.resize((width, height), Image.ANTIALIAS)
    img.save("image_300.jpg", "JPEG", dpi=(300, 300))
    return img


def parse_tesseract_output(output):
    """
    Parse the output of the tesseract and

    Parameters
    ----------
    output : string
        The output string given by the tesseract

    Returns
    -------
    list
        List of relevant information
    """
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
    """
    Parse players from a list of relevant information

    Parameters
    ----------
    list : list
        List of relevant information

    Returns
    -------
    list
        List of all players in the lobby
    """
    players = []
    for word in list:
        ind = word.index("joined")
        player = word[:ind-1]
        if player not in players:
            players.append(player)
    return players


def get_players_from_image(client_image="image_300.jpg"):
    """
    Use pytesseract to extract player names from LoL client image

    Parameters
    ----------
    client_image : string or Image
        The image to extract player names from

    Returns
    -------
    list
        Players processed from tesseract output
    """
    output = pytesseract.image_to_string(
        client_image, config=r'-l eng --psm 11 --dpi 300')
    output = parse_tesseract_output(output)
    players = get_players(output)

    return players
