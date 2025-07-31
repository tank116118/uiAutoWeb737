from tkinter.tix import NoteBook

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from UI.uiTelegram import Ui_Form

class Common(QWidget):
    signal_msg = pyqtSignal(str, str, str)
    def __init__(self, accountTaskManager=None, robotTaskManager=None,groupTaskManager=None,statisticsTaskManager=None,parent=None):
        super(Common, self).__init__(parent)
        self.uiMain: Ui_Form = Ui_Form()
        self.uiMain.setupUi(self)

        self.accountTaskManager = None
        self.robotTaskManager = None
        self.groupTaskManager = None
        self.statisticsTaskManager = None

        # 账号任务管理
        if accountTaskManager:
            from Business.service.common.account.taskManager import TaskManager
            self.accountTaskManager:TaskManager= accountTaskManager

        # 机器人任务管理
        if robotTaskManager:
            from Business.service.common.robot.taskManager import TaskManager as RobotTaskManager
            self.robotTaskManager:RobotTaskManager = robotTaskManager

        # 账号任务管理
        if groupTaskManager:
            from Business.service.common.group.taskManager import TaskManager as GroupTaskManager
            self.groupTaskManager:GroupTaskManager = groupTaskManager

        # 统计任务管理
        if statisticsTaskManager:
            from Business.service.common.statistics.taskManager import TaskManager as StatisticsTaskManager
            self.statisticsTaskManager:StatisticsTaskManager = statisticsTaskManager

    def release(self):
        """
        释放资源
        """
        if self.accountTaskManager:
            self.accountTaskManager.release()
            self.accountTaskManager = None
        if self.groupTaskManager:
            self.groupTaskManager.release()
            self.groupTaskManager = None
        if self.robotTaskManager:
            self.robotTaskManager.release()
            self.robotTaskManager = None
        if self.statisticsTaskManager:
            self.statisticsTaskManager.release()
            self.statisticsTaskManager = None

    @staticmethod
    def getAccountBusiness():
        from Business.service.common.account.main import Main
        return Main

    @staticmethod
    def getRobotBusiness():
        from Business.service.common.robot.main import Main
        return Main

    @staticmethod
    def getGroupBusiness():
        from Business.service.common.group.main import Main
        return Main

    @staticmethod
    def getStatisticsBusiness():
        from Business.service.common.statistics.main import Main
        return Main
