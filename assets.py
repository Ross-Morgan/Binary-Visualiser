from __future__ import annotations

from urllib.request import urlretrieve as download
from urllib.error import HTTPError
import socket
import os

APPNAME = "Binary Visualisation"

_DEFAULT_BKG_FNAME = "1920x1080-battleship-grey-solid-color-background.jpg"
_ASSET_DIR = f"{os.path.dirname(__file__)}/Assets".replace("\\", "/")
_HOMEIP = "127.0.0.1"
_BUTTON_SCRIPT_FILE = "button.qss"


def _asset(assetpath: str, pardir:str = "", relative = False):
    asset_dir = _ASSET_DIR if not relative else "Assets"
    return f"{asset_dir}/{pardir}{'/' if pardir else ''}{assetpath}"

'''
def check_internet_connection():
    if socket.gethostbyname(socket.gethostname()) == _HOMEIP:
        return False
    else:
        return True

def construct_image_filename(colour: str, w: int, h: int):
    return "{}x{}-{}-solid-color-background.jpg".format \
            (w, h, "-".join(colour.strip().split()))

def download_background(colour: str, w: int, h: int) - > Optional[bool]:

    filename = construct_image_filename(colour, w, h)

    if os.path.exists(os.path.abspath(filename)):
        return None

    url = f"https://www.solidbackgrounds.com/images/{w}x{h}/{filename}"

    try:
        download(url, os.path.abspath(_asset(filename, pardir = "Backgrounds")))
    except HTTPError:
        return None
'''


def script(script_path):
    return open(_asset(script_path, pardir = "Scripts", relative = True)).read()



class Colours:
    #? Actually properly implement this?
    dark_grey = 100, 100, 100


class Assets:
    window_icon = _asset("binary.png", pardir="Icons")
    info_icon = _asset("information.png", pardir="Icons")
    danger_icon = _asset("danger.png", pardir="Icons")
    attribution_icon = _asset("pencil.png", pardir="Icons")
    settings_icon = _asset("settings.png", pardir="Icons", relative=True)
    exit_icon = _asset("power.png", pardir="Icons", relative=True)

    background = _asset(_DEFAULT_BKG_FNAME, pardir = "Backgrounds")
    settings_background = _asset("settings_background.jpg")

    attibution_text = open(_asset("attribution.txt"), "r").read()


class StyleSheets:
    """Class containing stylesheets for Elements"""
    settings_button = script(_BUTTON_SCRIPT_FILE).format(Assets.settings_icon)
    exit_button = script(_BUTTON_SCRIPT_FILE).format(Assets.exit_icon)

    binary_switch = script("binary.qss")
