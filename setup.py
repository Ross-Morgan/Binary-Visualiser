from cx_Freeze import setup, Executable
import sys

APPNAME = ""
VERSION = "0.1"
DESCRIPTION = """A set of 8 switches, with conversion from binary to: Deimal, Hex, Oct and Base64"""


build_exe_options = {
    "packages": [],
    "excludes": ["tkinter"]
}

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

setup(
    name=APPNAME,
    version=VERSION,
    description=DESCRIPTION,
    options = {"build_exe" : build_exe_options},
    executables = [Executable("main.py", base=base)]
)