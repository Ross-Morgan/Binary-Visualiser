# Future imports
from __future__ import annotations

# Module imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, QSize, pyqtSlot
from pyautogui import size as screen_size
from resolutions import resolution, _size
import sys

# File imports
from assets import APPNAME, Assets, StyleSheets

from b64 import to_base64

from exit import exit_confirmation
from settings import SettingsWindow

WINDOW_TITLE = APPNAME
WINDOW_ICON_PATH = Assets.window_icon

FULLSCREEN = False
LOCKED_FULLSCREEN = False

FIXED_SIZE = True
MIN_SIZE = None, None
MAX_SIZE = None, None
WIDTH, HEIGHT = resolution.VGA
SWITCH_SIZE = 201, 280

MsgBoxButtons = QtWidgets.QMessageBox.StandardButton

class MainWindow(QtWidgets.QMainWindow):
    """Main Window class for the application"""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Initialise settings window object
        self.settings_window = SettingsWindow()

        self.switch_font = QtGui.QFont()
        self.switch_font.setPointSize(100)

        self.output_font = QtGui.QFont()
        self.output_font.setPointSize(25)

        self.setCentralWidget(QtWidgets.QWidget(self))

        self.setup_ui()
        self.set_window_size()
        self.setup_shortcuts()

    def set_window_size(self):
        if (not FULLSCREEN and
                WIDTH  is not None and
                HEIGHT is not None):

            window_width:  int = HEIGHT
            window_height: int = WIDTH

        elif FULLSCREEN:
            _window_size: _size = screen_size()

            window_width:  int = _window_size[0]
            window_height: int = _window_size[1]


        # Set window size bounds
        if FIXED_SIZE:
            self.setFixedSize(QSize(window_width, window_height))
        else:
            if all(MIN_SIZE):
                self.setMinimumSize(QSize(*MIN_SIZE))
            if all(MAX_SIZE):
                self.setMaximumSize(QSize(*MAX_SIZE))

            self.setGeometry(0,0, window_width, window_height)


        # Set inital window size
        self.setGeometry(QRect(0, 0, window_width, window_height))

        # Set window to fullscreen
        if FULLSCREEN:
            self.showMaximized()
            self.showFullScreen()

    def set_background(self):
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.background.setScaledContents(True)
        self.background.setPixmap(QtGui.QPixmap(Assets.background))

    def setup_shortcuts(self):
        self.fullscreen_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("f11"), self)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)

        self.exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("ctrl+w"), self)
        self.exit_shortcut.activated.connect(lambda: self.close())

        self.settings_button.clicked.connect(self.show_settings_window)
        self.exit_button.clicked.connect(self.exit_confirmation)

    @staticmethod
    def switch_position(n: int) -> int:
        return 100 + (n * (201 + 16))

    def setup_ui(self):
        """Setup the UI"""
        self.set_background()

        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.setGeometry(WIDTH - 84, HEIGHT - 42, 32, 32)
        self.settings_button.setStyleSheet(StyleSheets.settings_button)

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setGeometry(WIDTH - 42, HEIGHT - 42, 32, 32)
        self.exit_button.setStyleSheet(StyleSheets.exit_button)

        self.switch_positions = [
            [self.switch_position(n), 100] for n in range(8)
        ]

        # For the sake of syntax highlighting :)
        self.switches: list[QtWidgets.QPushButton] = [QtWidgets.QPushButton() for _ in range(8)]

        for i in range(8):
            self.switches[i] = QtWidgets.QPushButton(self)
            self.switches[i].setGeometry(*self.switch_positions[i], *SWITCH_SIZE)
            self.switches[i].setFont(self.switch_font)
            self.switches[i].setText("0")

        self.switches[0].clicked.connect(lambda: self.on_switch(0))
        self.switches[1].clicked.connect(lambda: self.on_switch(1))
        self.switches[2].clicked.connect(lambda: self.on_switch(2))
        self.switches[3].clicked.connect(lambda: self.on_switch(3))
        self.switches[4].clicked.connect(lambda: self.on_switch(4))
        self.switches[5].clicked.connect(lambda: self.on_switch(5))
        self.switches[6].clicked.connect(lambda: self.on_switch(6))
        self.switches[7].clicked.connect(lambda: self.on_switch(7))

        output_posx = self.switch_positions[7][0]

        self.dec_box = QtWidgets.QLineEdit(self)
        self.dec_box.setGeometry(output_posx, 430, 201, 50)
        self.dec_box.setFont(self.output_font)
        self.dec_box.setText("Decimal: 0")
        self.dec_box.setReadOnly(True)

        self.hex_box = QtWidgets.QLineEdit(self)
        self.hex_box.setGeometry(output_posx, 500, 201, 50)
        self.hex_box.setFont(self.output_font)
        self.hex_box.setText("Hex: 0")
        self.hex_box.setReadOnly(True)

        self.oct_box = QtWidgets.QLineEdit(self)
        self.oct_box.setGeometry(output_posx, 570, 201, 50)
        self.oct_box.setFont(self.output_font)
        self.oct_box.setText("Oct: 0")
        self.oct_box.setReadOnly(True)

        self.b64_box = QtWidgets.QLineEdit(self)
        self.b64_box.setGeometry(output_posx, 640, 201, 50)
        self.b64_box.setFont(self.output_font)
        self.b64_box.setText("Base 64: 0")
        self.b64_box.setReadOnly(True)

    def get_switches(self) -> str:
        return "".join([n.text() for n in self.switches])

    def on_switch(self, i: int):
        print("Clicked", i)
        if self.switches[i].text() == "0":
            text = "1"
        else:
            text = "0"

        self.switches[i].setText(text)

        self.update_counters()

    def update_counters(self):
        bin_i = int(self.get_switches(), base=2)

        self.update_dec(bin_i)
        self.update_hex(bin_i)
        self.update_oct(bin_i)
        self.update_b64(bin_i)

    def update_dec(self, bin_i):
        self.dec_box.setText(f"Decimal: {str(bin_i)}")

    def update_hex(self, bin_i):
        self.hex_box.setText(f"Hex: {hex(bin_i)[2:].upper()}")

    def update_oct(self, bin_i):
        self.oct_box.setText(f"Oct: {oct(bin_i)[2:]}")

    def update_b64(self, bin_i):
        self.b64_box.setText(f"Base64: {str(to_base64(bin_i))}")

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Called when window is resized"""
        old_size = event.oldSize() # type: QtGui.QSize
        new_size = event.size() # type: QtGui.QSize

        self.background.setGeometry(0, 0, self.width(), self.height())
        self.exit_button.setGeometry(self.width() - 42, self.height() - 42, 32, 32)
        self.settings_button.setGeometry(self.width() - 84, self.height() - 42, 32, 32)

    @pyqtSlot()
    def exit_confirmation(self):
        button = exit_confirmation()

        if button == MsgBoxButtons.Cancel:
            return
        if button == MsgBoxButtons.Ok:
            self.close()

    @pyqtSlot()
    def toggle_fullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        elif not LOCKED_FULLSCREEN:
            self.showNormal()
            self.resize(WIDTH, HEIGHT)

    @pyqtSlot()
    def show_settings_window(self):
        if not self.settings_window.isVisible():
            self.settings_window.show()
        else:
            self.settings_window.hide()


def main():
    app = QtWidgets.QApplication(sys.argv)

    ui = MainWindow()
    ui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
