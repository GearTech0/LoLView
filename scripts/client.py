from PIL import Image, ImageGrab, JpegImagePlugin
from pytesseract import Output
import pytesseract
import win32gui
import win32com.client


def get_client_screenshot(dest=None):
    """
    Screenshot the LoL client and scale image to be 300dpi

    Parameters
    ----------
    dest : path
        Save destination (optional)

    Returns
    -------
    PIL.Image.Image
        Processed image of LoL client
    """
    hwnd = win32gui.FindWindow(None, "League of Legends")

    # Send alt keys
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)

    tess_dpi = 300
    img = ImageGrab.grab(bbox)
    img = scale_and_resample(img, tess_dpi)    # Scale to tess specs

    if dest is not None:
        img.save(dest, "JPEG", dpi=(tess_dpi, tess_dpi))    # Saves debug

    return img


def scale_and_resample(img, dest_dpi):
    """
    Scales target image and resamples to new DPI

    Parameters
    ----------
    img : PIL.Image.Image or path
        Target image to scale and resample

    Returns
    -------
    PIL.Image.Image
        New scaled and resampled image
    """
    print(type(img))
    if not isinstance(img, Image.Image):
        img = Image.open(img)

    width, height = img.size
    try:
        dpi = img.info['dpi']
        print("Found DPI: ", dpi)
    except KeyError as e:
        dpi = (75, 75)
        print("Defaulted DPI to ", dpi)

    width = int(width * (dest_dpi / dpi[0]))
    height = int(height * (dest_dpi / dpi[1]))

    return img.resize((width, height), Image.ANTIALIAS)


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


def get_players_from_image(client_image):
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
