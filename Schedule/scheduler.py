import json
import re
import time
import uuid

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler

from Schedule.scheduleDesign import ScheduleDesign
from Business.models.schedules import Schedules
from Business.dao.schedulesServices import SchedulesServices
from Utils.objTools import ObjTools
from instanceManager import InstanceManager


class Task(QThread):
    signal_msg = pyqtSignal(str, str, str)

    def __init__(self, params: str|None, task: str ,parent=None):
        super(Task, self).__init__(parent=parent)
        self.__stopFlag = False
        self.__params = params
        self.__task = task
        # 设置名称
        self.setObjectName(f'customThread_{str(uuid.uuid4()).replace("-", "")[0:6]}')
        InstanceManager.activeThreads.append(self)

    def __del__(self):
        InstanceManager.activeThreads.remove(self)

    def stop(self):
        self.__stopFlag = True

    def statusMsg(self, msg: str, timeout: int = None):
        if timeout is None:
            timeout = 0
        self.sendSignalMsg('statusMsg', None, json.dumps({
            "msg": msg, "timeout": timeout
        }))

    def sendSignalMsg(self, method: str, operator: str|None, params: str):
        if method is None:
            return
        method = method.strip()
        if len(method) <= 0:
            return

        self.signal_msg.emit(method, operator, params)# type: ignore


    def getDatasFromServices(self):
        schedulesServices = SchedulesServices()

        listSchedules = schedulesServices.get(Schedules(enable=True), retryTimes=2)
        if listSchedules is None:
            listSchedules = []

        for scheduleSub in listSchedules:
            if scheduleSub.scheduleParams is None:
                continue
            scheduleParams :Schedules = ObjTools.dictToObj(json.loads(scheduleSub.scheduleParams), Schedules)
            scheduleSub.scheduleParams = None
            scheduleSub.startTime = scheduleParams.startTime
            scheduleSub.endTime = scheduleParams.endTime
            scheduleSub.interval = scheduleParams.interval
            scheduleSub.timeUnit = scheduleParams.timeUnit

            if scheduleSub.triggerName == 'cron':
                def toSchedulerParams(param,deleteWord):
                    temp = param
                    if re.match('每', temp):
                        temp = '*'
                    else:
                        temp = temp.replace(';', ',')
                        temp = temp.replace(' ', '')
                        temp = temp.replace(deleteWord, '')
                        temp = temp.replace('一', '0')
                        temp = temp.replace('二', '1')
                        temp = temp.replace('三', '2')
                        temp = temp.replace('四', '3')
                        temp = temp.replace('五', '4')
                        temp = temp.replace('六', '5')
                        temp = temp.replace('日', '6')
                    return temp

                scheduleSub.year = toSchedulerParams(scheduleParams.year,'年')
                scheduleSub.month = toSchedulerParams(scheduleParams.month, '月')
                scheduleSub.day = toSchedulerParams(scheduleParams.day, '日')
                scheduleSub.week = toSchedulerParams(scheduleParams.week, '周')
                scheduleSub.dayOfWeek = toSchedulerParams(scheduleParams.dayOfWeek, '星期')
                scheduleSub.hour = toSchedulerParams(scheduleParams.hour, '时')
                scheduleSub.minute = toSchedulerParams(scheduleParams.minute, '分')
                scheduleSub.second = toSchedulerParams(scheduleParams.second, '秒')
            elif scheduleSub.triggerName == 'interval':
                scheduleSub.week = None
                scheduleSub.day = None
                scheduleSub.hour = None
                scheduleSub.minute = None
                scheduleSub.second = None
                if scheduleParams.timeUnit == '周':
                    scheduleSub.week = scheduleSub.interval
                elif scheduleParams.timeUnit == '天':
                    scheduleSub.day = scheduleSub.interval
                elif scheduleParams.timeUnit == '小时':
                    scheduleSub.hour = scheduleSub.interval
                elif scheduleParams.timeUnit == '分钟':
                    scheduleSub.minute = scheduleSub.interval
                elif scheduleParams.timeUnit == '秒钟':
                    scheduleSub.second = scheduleSub.interval

        params = json.dumps(ObjTools.objToDict(listSchedules))
        self.sendSignalMsg('getScheduleFromServices', None, params)

    def run(self):
        if self.__task == 'getScheduleFromServices':
            self.getDatasFromServices()

        time.sleep(2)

class Scheduler(QObject):
    instance = None
    def __init__(self):
        super().__init__()
        self.__scheduler = BackgroundScheduler()
        self.__scheduleList: list[Schedules] = []

    def getScheduleFromServices(self):
        task = Task(params=None, task='getScheduleFromServices',
                    parent=self)
        task.signal_msg.connect(self.onReceiveMessage)# type: ignore

        task.start()

    # noinspection PyUnusedLocal
    def onReceiveMessage(self, method: str, operator: str, params: str):
        if method == 'getScheduleFromServices':
            jsonParams = json.loads(params)
            self.__scheduleList = ObjTools.dictToObj(jsonParams, Schedules)
            self.restart()

    def release(self):
        self.shutdown()
        self.removeAllJob()
        self.__scheduler = None

    def restart(self):
        self.shutdown()
        self.removeAllJob()

        self.__scheduler = None
        if self.__scheduleList is None or len(self.__scheduleList) <= 0:
            return
        self.__scheduler = BackgroundScheduler()
        for schedule in self.__scheduleList:
            self.addJob(schedule)
        self.start()

    def getSchedule(self, scheduleId)->Schedules|None:
        for schedule in self.__scheduleList:
            if str(schedule.id) == scheduleId:
                return schedule
        return None

    def start(self):
        if self.__scheduler:
            self.__scheduler.start()

    def shutdown(self):
        if self.__scheduler and self.__scheduler.running:
            self.__scheduler.shutdown()
    
    def addJob(self,schedules: Schedules):
        if self.__scheduler is None or schedules is None:
            return

        scheduleFunctions = InstanceManager.getScheduleFunctions()
        if scheduleFunctions is None:
            return

        design: ScheduleDesign = ScheduleDesign()
        functionName = None
        taskName = None
        for designSub in design.scheduleList:
            if designSub.get('name') == schedules.task:
                functionName = designSub.get('function')
                taskName = designSub.get('taskName')
                break
        if functionName is None:
            return

        functionInstance = getattr(scheduleFunctions,'scheduleRun')
        if functionInstance is None:
            return

        if schedules.triggerName == 'cron':
            self.__scheduler.add_job(id=str(schedules.id),
                                     name=f'{schedules.name}-{schedules.task}',
                                     args=[str(schedules.id),functionName,taskName],
                                     trigger=schedules.triggerName,
                                     start_date=schedules.startTime,
                                     end_date=schedules.endTime,
                                     year=schedules.year,
                                     month=schedules.month,
                                     day=schedules.day,
                                     week=schedules.week,
                                     day_of_week=schedules.dayOfWeek,
                                     hour=schedules.hour,
                                     minute=schedules.minute,
                                     second=schedules.second,
                                     func=functionInstance)
        elif schedules.triggerName == 'interval':
            self.__scheduler.add_job(id=str(schedules.id),
                                     name=f'{schedules.name}-{schedules.task}',
                                     args=[str(schedules.id),functionName,taskName],
                                     trigger=schedules.triggerName,
                                     start_date=schedules.startTime,
                                     end_date=schedules.endTime,
                                     weeks=schedules.week,
                                     days=schedules.day,
                                     hours=schedules.hour,
                                     minutes=schedules.minute,
                                     seconds=schedules.second,
                                     func=functionInstance)
        elif schedules.triggerName == 'date':
            self.__scheduler.add_job(id=str(schedules.id),
                                     name=f'{schedules.name}-{schedules.task}',
                                     args=[str(schedules.id),functionName,taskName],
                                     trigger=schedules.triggerName,
                                     start_date=schedules.startTime,
                                     func=functionInstance)

    def removeAllJob(self):
        if self.__scheduler is None:
            return

        listJob: list[Job] = self.__scheduler.get_jobs()
        if listJob is None or len(listJob) <= 0:
            return

        for jobSub in listJob:
            self.__scheduler.pause_job(jobSub.id)
            self.__scheduler.remove_job(jobSub.id)

    def removeJob(self,jobId: str):
        if self.__scheduler is None:
            return
        self.__scheduler.remove_job(jobId)

    def pauseJob(self,jobId: str):
        if self.__scheduler is None:
            return
        self.__scheduler.pause_job(jobId)

    def resumeJob(self,jobId: str):
        if self.__scheduler is None:
            return
        self.__scheduler.resume_job(jobId)

    def manualRunJob(self,jobId: str,params: list|None):
        if self.__scheduler is None:
            return

        listJob: list[Job] = self.__scheduler.get_jobs()
        if listJob is None or len(listJob) <= 0:
            return

        jobSelect: Job|None = None
        for jobSub in listJob:
            if jobSub.id == jobId:
                jobSelect = jobSub
                break
        if jobSelect is None:
            return

        if params is None:
            jobSelect.func()
        else:
            jobSelect.func(*params)
