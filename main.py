from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDesktopWidget, QDialog

from Business.models.storage import Storage, STORAGE_TYPE
from UI.uiMain import Ui_Dialog
import warnings

from dlgSetting import DlgSetting
from task import Task

warnings.filterwarnings('ignore', category=DeprecationWarning)

class Main(QDialog):
    signal_msg = pyqtSignal(str, str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uiMain: Ui_Dialog = Ui_Dialog()
        self.uiMain.setupUi(self)

        self.__task: Task | None = None

        # 获取桌面对象
        desktop = QDesktopWidget()
        # 获取主屏幕的大小
        screen_rect = desktop.screenGeometry()
        self.screenWidth = screen_rect.width()
        self.screenHeight = screen_rect.height()

        self.uiMain.btnRun.clicked.connect(self.onRun)
        self.uiMain.btnSetting.clicked.connect(self.onSetting)

    def onRun(self):
        if self.uiMain.btnRun.text() == '运行':
            if self.__task is None:
                self.__task = Task()
                self.__task.signal_msg.connect(self.onReceiveMessage)
                self.__task.start()
                self.uiMain.btnRun.setText('停止运行')
        else:
            if self.__task:
                self.__task.stop()
                self.__task = None
                self.uiMain.btnRun.setText('运行')

    def onSetting(self):
        dlgSetting = DlgSetting()
        if not dlgSetting.exec():
            return

        token737 = dlgSetting.getToken737()
        tokenSete7 = dlgSetting.getTokenSete7()

        storage = Storage(storageType=STORAGE_TYPE.CONFIG)
        storage.setStorage('token737',token737)
        storage.setStorage('tokenSete7', tokenSete7)

    def closeEvent(self, a0: QtGui.QCloseEvent|None) -> None:
        """
        关闭窗口事件
        """
        pass

    # noinspection PyUnusedLocal
    def onReceiveMessage(self, method: str, operator: str, params: str):
        """
        任务消息回调
        :param method:
        :param operator:
        :param params:
        :return:
        """
        pass