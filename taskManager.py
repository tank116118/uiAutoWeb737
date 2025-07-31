import json

from PyQt5.QtCore import QObject
from instanceManager import InstanceManager


class TaskManager(QObject):
    instance = None

    def __init__(self):
        super().__init__()
        self.__dlgProgressBar: DlgProgressBar|None = None
        self.__taskList: list[Task]|None = None
        self.__taskSave: TaskSave|None = None
        self.__isGettingData: bool = False
        self.setAutoSave(interval=30)

    def release(self):
        if self.__taskList:
            lenTask = len(self.__taskList)
            for i in range(lenTask - 1, -1, -1):
                task = self.__taskList[i]
                task.stop()
                del self.__taskList[i]
        if self.__taskSave:
            self.__taskSave.stop()

    def setAutoSave(self, interval: int):
        if self.__taskSave:
            return

        self.__taskSave = TaskSave(interval=interval)
        self.__taskSave.signal_msg.connect(self.onReceiveMessage)
        self.__taskSave.start()

    def closeTask(self, task: TASK_ACCOUNT_TABLE):
        if self.__taskList is None:
            return

        lenTask = len(self.__taskList)
        for i in range(lenTask - 1, -1, -1):
            taskApp: Task = self.__taskList[i]
            if taskApp.task == task:
                taskApp.stop()
                del self.__taskList[i]

    def closeTaskByUid(self, uid: str):
        if uid is None:
            return
        if self.__taskList is None:
            return

        lenTask = len(self.__taskList)
        for i in range(lenTask - 1, -1, -1):
            taskApp: Task = self.__taskList[i]
            if taskApp.uid == uid:
                taskApp.stop()
                del self.__taskList[i]
                break

    # noinspection PyUnusedLocal
    def onReceiveMessage(self, method: str, operator: str, params: str):
        """
        任务消息回调
        :param method:
        :param operator:
        :param params:
        :return:
        """
        workSpace = InstanceManager.getWorkSpace()
        if workSpace is None:
            return

        accountTable = workSpace.accountTable

        if method == 'taskStop':
            taskUid = params
            self.closeTaskByUid(taskUid)
        elif method == 'toastMsg':
            jsonParam = json.loads(params)
            msg = jsonParam.get('msg')
            timeout = jsonParam.get('timeout')
            Toast.message(msg=msg, timeout=timeout)
        elif method == 'statusMsg':
            jsonParam = json.loads(params)
            msg = jsonParam.get('msg')
            timeout = jsonParam.get('timeout')
            Statusbar.message(msg, timeout)

    def progressBar(self, info: str|None, value: int):
        if self.__dlgProgressBar is None:
            self.__dlgProgressBar = DlgProgressBar()
            self.__dlgProgressBar.show()

        self.__dlgProgressBar.setInfo(info)
        self.__dlgProgressBar.setValue(value)

    def closeProgressBar(self):
        if self.__dlgProgressBar:
            self.__dlgProgressBar.close()
            self.__dlgProgressBar = None
