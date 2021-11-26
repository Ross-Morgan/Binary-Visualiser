from assets import Assets
from PyQt5 import QtGui, QtWidgets

def exit_confirmation() -> int:
    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowTitle("Exit Confirmation")
    msg_box.setWindowIcon(QtGui.QIcon(Assets.danger_icon))
    msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
    msg_box.setText("Are you sure you want to exit?")
    return msg_box.exec()

class x:
    def init_subclasses(cls, **kwargs):
        cls.__init_subclass__()