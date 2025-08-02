import json
import time
import uuid
from datetime import datetime, timedelta

from PyQt5.QtCore import QThread, pyqtSignal

from Utils.sheets7 import Sheets7
from Utils.sheets737 import Sheets737
from Utils.tools import Tools
from Utils.webSite7 import WebSite7
from Utils.webSite737 import WebSite737


class Task(QThread):
    signal_msg = pyqtSignal(str, str, str)

    def __init__(self, showMsg:bool = True, parent=None):
        super(Task, self).__init__(parent)
        self.uid = str(uuid.uuid4()).replace('-', '')
        self.__stopFlag = False
        self.__showMsg = showMsg
        # 设置名称
        self.setObjectName(f'customThread_{str(uuid.uuid4()).replace("-", "")[0:6]}')

        self.__dateColumn7 = []
        self.__dateColumn737 = []
        self.__timeBefore7 = datetime.now()
        self.__timeBefore737 = datetime.now()

    def __del__(self):
        pass

    def stop(self):
        self.__stopFlag = True

    def runTask(self):
        self.task737()
        # self.taskSete7()

    def taskSete7(self):
        timeNow = datetime.now()
        time_diff = timeNow - self.__timeBefore7
        time_diff_hour = time_diff.total_seconds() / 3600

        webSite7 = WebSite7()
        dateLast = Tools.normalize_date(self.__dateColumn7[-1])
        if time_diff_hour < 1:
            listItem = webSite7.getSummary(dateLast)
            if listItem:
                print('sete7 会话有效')
            else:
                print('sete7 会话失效..')
            return

        self.__timeBefore7 = datetime.now()

        today = datetime.now().date()
        dateTo = str(today + timedelta(days=1))
        sheets7 = Sheets7()
        for single_date in Tools.date_range(dateLast, dateTo):
            dateStr = single_date.strftime('%Y-%m-%d')
            summaryList: list = webSite7.getSummary(dateStr)
            operating = webSite7.getOperating(dateStr)

            if len(summaryList) <= 0 or operating is None:
                break

            if dateStr == dateLast:
                indexRow = len(self.__dateColumn7)
                if not sheets7.update(summaryList,dateStr, operating.payCash,  indexRow + 3):
                    break
            if summaryList:
                if not sheets7.append(summaryList, dateStr, operating.payCash, True):
                    break

        self.__dateColumn7 = sheets7.getDateColumn()


    def task737(self):
        timeNow = datetime.now()
        time_diff = timeNow - self.__timeBefore737
        time_diff_hour = time_diff.total_seconds() / 3600

        webSite737 = WebSite737()
        dateLast = Tools.normalize_date(self.__dateColumn737[-1])
        if time_diff_hour < 1:
            listItem = webSite737.getSummary(page=1)
            if listItem:
                print('737 会话有效')
            else:
                print('737 会话失效..')
            return

        self.__timeBefore737 = datetime.now()

        today = datetime.now().date()
        dateTo = str(today + timedelta(days=1))

        sheets737 = Sheets737()
        dateDiff = Tools.date_diff(dateTo,dateLast)
        summaryList = webSite737.getSummary(page=1, limit=dateDiff + 1)
        lenList = len(summaryList)
        for i in range(lenList - 1, -1, -1):
            summary = summaryList[i]
            if i == lenList - 1:
                indexRow = len(self.__dateColumn737)
                if not sheets737.update(summary,indexRow+3):
                    break
            else:
                if not sheets737.append(summary,True):
                    break

        self.__dateColumn737 = sheets737.getDateColumn()


    def __initialTask(self):
        sheets737 = Sheets737()
        dateColumn = sheets737.getDateColumn()
        lenDate = len(dateColumn)
        if lenDate <= 0:
            webSite737 = WebSite737()
            summaryList = webSite737.getSummary(page=1,limit=2000)
            lenList = len(summaryList)
            if lenList > 0:
                for i in range(lenList-1,-1,-1):
                    summary = summaryList[i]
                    sheets737.append(summary,False)

            self.__dateColumn737 = sheets737.getDateColumn()
        else:
            self.__dateColumn737 = dateColumn

        # ===============
        sheets7 = Sheets7()
        dateColumn2 = sheets7.getDateColumn()
        lenDate = len(dateColumn2)
        if lenDate <= 0:
            webSite7 = WebSite7()
            # 获取当前日期
            dateTo = str(Tools.convertTimeToTimezone('America/Sao_Paulo'))
            for single_date in Tools.date_range('2025-06-02', dateTo):
                dateStr = single_date.strftime('%Y-%m-%d')
                summaryList:list = webSite7.getSummary(dateStr)
                operating = webSite7.getOperating(dateStr)
                if summaryList:
                    sheets7.append(summaryList[0],dateStr,operating.payCash,False)
            self.__dateColumn7 = sheets7.getDateColumn()
        else:
            self.__dateColumn7 = dateColumn2


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
        self.__initialTask()
        while True:
            if self.__stopFlag:
                break
            self.runTask()
            time.sleep(60)

        self.sendSignalMsg('taskStop', None, self.uid)
