import json
import time
import uuid

from PyQt5.QtCore import QThread, pyqtSignal


class Task(QThread):
    signal_msg = pyqtSignal(str, str, str)

    def __init__(self, showMsg:bool = True, parent=None):
        super(Task, self).__init__(parent)
        self.uid = str(uuid.uuid4()).replace('-', '')
        self.__stopFlag = False
        self.__showMsg = showMsg
        # 设置名称
        self.setObjectName(f'customThread_{str(uuid.uuid4()).replace("-", "")[0:6]}')

    def __del__(self):
        pass

    def stop(self):
        self.__stopFlag = True

    def runTask(self):
        print('run')

    def statusMsg(self, msg: str, timeout: int = None):
        if timeout is None:
            timeout = 0
        self.sendSignalMsg('statusMsg', None, json.dumps({
            "msg": msg, "timeout": timeout
        }))

    def sendSignalMsg(self, method: str, operator: str|None, params: str|None):
        if method is None:
            return
        method = method.strip()
        if len(method) <= 0:
            return

        self.signal_msg.emit(method, operator, params)# type: ignore

    def run(self):
        while True:
            if self.__stopFlag:
                break
            self.runTask()
            time.sleep(10)

        self.sendSignalMsg('taskStop', None, self.uid)
