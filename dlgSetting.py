
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from models import Storage, STORAGE_TYPE
from UI.uiSetting import Ui_Dialog
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

class DlgSetting(QDialog):
    signal_msg = pyqtSignal(str, str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiMain: Ui_Dialog = Ui_Dialog()
        self.uiMain.setupUi(self)

        storage = Storage(storageType=STORAGE_TYPE.CONFIG)
        token737 = storage.getStorage('token737')
        tokenSete7 = storage.getStorage('tokenSete7')
        if token737:
            self.uiMain.plainTextEdit737.setPlainText(token737)
        if tokenSete7:
            self.uiMain.plainTextEditSete7.setPlainText(tokenSete7)

    def getToken737(self)->str:
        return self.uiMain.plainTextEdit737.toPlainText()

    def getTokenSete7(self)->str:
        return self.uiMain.plainTextEditSete7.toPlainText()
