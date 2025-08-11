import threading
import signal
import sys
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

from Utils.sheets7 import Sheets7
from Utils.sheets737 import Sheets737
from Utils.tools import Tools
from Utils.webSite7 import WebSite7
from Utils.webSite737 import WebSite737

class PlatformAdapter:
    """处理平台差异的适配器类"""
    @staticmethod
    def getLogDir():
        """获取日志目录"""
        if os.name == 'posix':  # Linux/Unix
            return Path('/var/log/timer_task')
        else:  # Windows
            return Path(os.environ.get('ProgramData', 'C:/')) / 'TimerTask' / 'logs'

    @staticmethod
    def setupSignalHandlers(handler):
        """设置平台特定的信号处理器"""
        if os.name == 'posix':  # Linux/Unix
            signal.signal(signal.SIGINT, handler)  # Ctrl+C
            signal.signal(signal.SIGTERM, handler)  # kill命令
        else:  # Windows
            signal.signal(signal.SIGINT, handler)  # Ctrl+C
            try:
                import win32api
                def consoleCtrlHandler(ctrl_type):
                    if ctrl_type in (win32api.CTRL_C_EVENT, win32api.CTRL_BREAK_EVENT):
                        handler(signal.SIGINT, None)
                        return True
                    return False

                win32api.SetConsoleCtrlHandler(consoleCtrlHandler, True)
            except ImportError:
                pass

    @staticmethod
    def runAsService(main_func):
        """作为服务/守护进程运行"""
        if os.name == 'posix':  # Linux/Unix
            try:
                import daemon
                with daemon.DaemonContext():
                    main_func()
            except ImportError:
                main_func()
        else:  # Windows
            try:
                import servicemanager
                import win32serviceutil
                import win32service

                class TimerTaskService(win32serviceutil.ServiceFramework):
                    _svc_name_ = "PythonTimerTask"
                    _svc_display_name_ = "Python Timer Task Service"

                    def SvcDoRun(self):
                        main_func()

                    def SvcStop(self):
                        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                        TimerTask.instance.shutdown()

                if __name__ == '__main__':
                    win32serviceutil.HandleCommandLine(TimerTaskService)
            except ImportError:
                main_func()

class TimerTask:
    """跨平台定时任务类"""
    instance = None

    def __init__(self, interval=60):
        TimerTask.instance = self
        self.interval = interval
        self.timer = None
        self.isRunning = False
        self.lock = threading.Lock()
        self._setupLogging()

        self.__dateColumn7 = []
        self.__dateColumn737 = []
        self.__timeBefore7 = datetime.now()
        self.__timeBefore737 = datetime.now()

    def _setupLogging(self):
        """配置跨平台日志"""
        log_dir = PlatformAdapter.getLogDir()
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'timer_task.log'),
                logging.StreamHandler()
            ]
        )

    def runTask(self):
        """执行定时任务"""
        with self.lock:
            if not self.isRunning:
                return

            try:
                logging.info(f"执行定时任务... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                # 在这里添加你的任务逻辑
                self._task737()
                self._taskSete7()

            except Exception as e:
                logging.error(f"任务执行出错: {str(e)}")

            # 设置下次执行
            self.timer = threading.Timer(self.interval, self.runTask)
            self.timer.start()

    def _taskSete7(self, waitDiff=True):
        timeNow = datetime.now()
        time_diff = timeNow - self.__timeBefore7
        time_diff_hour = time_diff.total_seconds() / 3600

        webSite7 = WebSite7()
        sheets7 = Sheets7()
        dateLast = Tools.normalize_date(self.__dateColumn7[-1])

        if waitDiff:
            if time_diff_hour < 1:
                listItem = webSite7.getSummary(dateLast)
                if listItem:
                    logging.info('sete7 会话有效')
                else:
                    logging.error('sete7 会话失效..')
                    return
                # 判断是否有新字段
                if sheets7.checkNewVarForSheetStruct(listItem):
                    # 获取当前日期
                    dateTo = str(Tools.convertTimeToTimezone('America/Sao_Paulo').date())
                    lenDateColumn = len(self.__dateColumn7)
                    for single_date in Tools.date_range('2025-06-02', dateTo):
                        if not self.isRunning:
                            break
                        dateStr = single_date.strftime('%Y-%m-%d')
                        summaryList: list = webSite7.getSummary(dateStr)
                        operating = webSite7.getOperating(dateStr)
                        if len(summaryList) <= 0 or operating is None:
                            break

                        indexRow = 0
                        for j in range(lenDateColumn):
                            if dateStr == self.__dateColumn7[j]:
                                indexRow = j + 1
                                break

                        if indexRow > 0:
                            if not sheets7.update(summaryList, dateStr, operating.payCash, indexRow + 3):
                                break
                        else:
                            if not sheets7.append(summaryList, dateStr, operating.payCash, True):
                                break
                return

        self.__timeBefore7 = datetime.now()

        today = datetime.now().date()
        dateTo = str(today + timedelta(days=1))
        lenDateColumn = len(self.__dateColumn7)
        for single_date in Tools.date_range(dateLast, dateTo):
            if not self.isRunning:
                break
            dateStr = single_date.strftime('%Y-%m-%d')
            summaryList: list = webSite7.getSummary(dateStr)
            operating = webSite7.getOperating(dateStr)

            if len(summaryList) <= 0 or operating is None:
                break

            indexRow = 0
            for j in range(lenDateColumn):
                if dateStr == self.__dateColumn7[j]:
                    indexRow = j + 1
                    break

            if indexRow > 0:
                if not sheets7.update(summaryList,dateStr, operating.payCash,  indexRow + 3):
                    break
            else:
                if not sheets7.append(summaryList, dateStr, operating.payCash, True):
                    break

        self.__dateColumn7 = sheets7.getDateColumn()

    def _task737(self, waitDiff=True):
        timeNow = datetime.now()
        time_diff = timeNow - self.__timeBefore737
        time_diff_hour = time_diff.total_seconds() / 3600

        webSite737 = WebSite737()
        sheets737 = Sheets737()
        dateLast = Tools.normalize_date(self.__dateColumn737[-1])

        if waitDiff:
            if time_diff_hour < 1:
                listItem = webSite737.getSummary(page=1)
                if listItem:
                    logging.info('737 会话有效')
                else:
                    logging.error('737 会话失效..')
                    return
                # 判断是否有新字段
                if sheets737.checkNewVarForSheetStruct(listItem[0]):
                    # 更新所有数据
                    self.__dateColumn737 = sheets737.getDateColumn()

                    summaryList = webSite737.getSummary(page=1, limit=3000)
                    lenList = len(summaryList)
                    lenDateColumn = len(self.__dateColumn737)
                    for i in range(lenList - 1, -1, -1):
                        if not self.isRunning:
                            break
                        summary = summaryList[i]

                        date = datetime.fromtimestamp(summary.daytime)
                        dateStr: str = Tools.normalize_date(date.strftime("%Y-%m-%d"))
                        indexRow = 0
                        for j in range(lenDateColumn):
                            if dateStr == self.__dateColumn737[j]:
                                indexRow = j + 1
                                break

                        if indexRow > 0:
                            if not sheets737.update(summary, indexRow + 3):
                                break
                        else:
                            if not sheets737.append(summary, True):
                                break
                    self.__dateColumn737 = sheets737.getDateColumn()
                return

        self.__timeBefore737 = datetime.now()

        today = datetime.now().date()
        dateTo = str(today + timedelta(days=1))
        dateDiff = Tools.date_diff(dateTo,dateLast)
        summaryList = webSite737.getSummary(page=1, limit=dateDiff + 3)
        lenList = len(summaryList)
        lenDateColumn = len(self.__dateColumn737)
        for i in range(lenList - 1, -1, -1):
            if not self.isRunning:
                break
            summary = summaryList[i]

            date = datetime.fromtimestamp(summary.daytime)
            dateStr: str = Tools.normalize_date(date.strftime("%Y-%m-%d"))
            indexRow = 0
            for j in range(lenDateColumn):
                if dateStr == self.__dateColumn737[j]:
                    indexRow = j + 1
                    break

            if indexRow > 0:
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
                    if not self.isRunning:
                        break
                    summary = summaryList[i]
                    sheets737.append(summary,False)

            self.__dateColumn737 = sheets737.getDateColumn()
        else:
            self.__dateColumn737 = dateColumn
            self._task737(waitDiff=False)

        # ===============
        sheets7 = Sheets7()
        dateColumn2 = sheets7.getDateColumn()
        lenDate = len(dateColumn2)
        if lenDate <= 0:
            webSite7 = WebSite7()
            # 获取当前日期
            dateTo = str(Tools.convertTimeToTimezone('America/Sao_Paulo').date())
            for single_date in Tools.date_range('2025-06-02', dateTo):
                if not self.isRunning:
                    break
                dateStr = single_date.strftime('%Y-%m-%d')
                summaryList:list = webSite7.getSummary(dateStr)
                operating = webSite7.getOperating(dateStr)
                if summaryList:
                    sheets7.append(summaryList,dateStr,operating.payCash,False)
            self.__dateColumn7 = sheets7.getDateColumn()
        else:
            self.__dateColumn7 = dateColumn2
            self._taskSete7(waitDiff=False)

    def start(self):
        """启动定时任务"""
        with self.lock:
            if self.isRunning:
                logging.warning("定时任务已经在运行中")
                return

            self.__initialTask()  # 初始化任务

            self.isRunning = True
            self.timer = threading.Timer(0, self.runTask)  # 立即执行第一次
            self.timer.start()
            logging.info("定时任务已启动")

    def stop(self):
        """停止定时任务"""
        with self.lock:
            if not self.isRunning:
                logging.warning("定时任务未在运行")
                return

            self.isRunning = False
            if self.timer:
                self.timer.cancel()
            logging.info("定时任务已停止")

    def shutdown(self):
        """关闭任务"""
        self.stop()