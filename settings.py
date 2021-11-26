# Module imports
from PyQt5 import QtCore, QtGui, QtWidgets
import os

# File imports
from resolutions import resolution
from assets import APPNAME, Assets, StyleSheets

WINDOW_TITLE = f"{APPNAME} - Settings"
WINDOW_ICON_PATH = os.path.abspath(Assets.settings_icon)
# Portrait VGA
HEIGHT, WIDTH = resolution.VGA


class SettingsWindow(QtWidgets.QWidget):
    """Settings window for the application"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.applied = False

        self.setup_ui()
        self.set_window_size()
        self.setup_shortcuts()

    def set_window_size(self):
        self.setFixedSize(WIDTH, HEIGHT)

    def set_background(self):
        self.background = QtWidgets.QLabel(self)
        self.background.setPixmap(QtGui.QPixmap(Assets.settings_background))

    def setup_ui(self):
        self.set_background()
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon(Assets.settings_icon))

        self.attribution_button = QtWidgets.QPushButton(self)
        self.attribution_button.setGeometry(15, 600, 75, 25)
        self.attribution_button.clicked.connect(self.show_attribution)
        self.attribution_button.setText("Credits")

        self.reset_button = QtWidgets.QPushButton(self)
        self.reset_button.setGeometry(210, 600, 75, 25)
        self.reset_button.clicked.connect(self.reset_settings)
        self.reset_button.setText("Reset")

        self.apply_button = QtWidgets.QPushButton(self)
        self.apply_button.setGeometry(300, 600, 75, 25)
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setText("Apply")

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setGeometry(390, 600, 75, 25)
        self.exit_button.clicked.connect(lambda: self.close())
        self.exit_button.setText("Exit")

    def show_attribution(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Asset Attribution")
        msg_box.setWindowIcon(QtGui.QIcon(Assets.attibution_icon))
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Close)

        msg_box.setText(Assets.attibution_text)

        msg_box.exec()

    def reset_settings(self):
        pass

    def apply_settings(self):
        self.applied = True

    def setup_shortcuts(self):
        self.exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("ctrl+w"), self)
        self.exit_shortcut.activated.connect(lambda: self.close())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = SettingsWindow()
    ui.show()

    sys.exit(app.exec_())