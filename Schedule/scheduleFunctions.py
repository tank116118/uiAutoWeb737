import json

from PyQt5.QtCore import QObject, pyqtSignal

from Business.models.account import Account
from Business.models.accountData import AccountData
from Business.models.enums import TASK_WEB
from Business.models.messages import Messages
from Business.dao.accountsServices import AccountsServices
from Business.dao.messagesServices import MessagesServices
from Utils.objTools import ObjTools
from instanceManager import InstanceManager


class ScheduleFunctions(QObject):
    instance = None
    signal_msg = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.signal_msg.connect(self.onReceiveMessage)# type: ignore

    def sendSignalMsg(self, method: str, accountParams: str|None=None, taskParams: str|None=None):
        if method is None:
            return
        method = method.strip()
        if len(method) <= 0:
            return

        self.signal_msg.emit(method, accountParams, taskParams)# type: ignore

    # noinspection PyMethodMayBeStatic
    def onReceiveMessage(self, method: str, accountParams: str|None=None, taskParams: str|None = None):
        listAccount: list[Account]|None = None
        if accountParams:
            listAccount = ObjTools.dictToObj(dictObj=json.loads(accountParams),
                                                            objClass=Account,
                                                            childObjClass={'accountDatasList':AccountData})
        workSpace = InstanceManager.getWorkSpace()
        accountBusiness = workSpace.getAccountBusiness()
        groupBusiness = workSpace.getGroupBusiness()

        if method == 'onImportGroups':
            '''导入群链接'''
            groupBusiness.importGroups(taskParams=taskParams)
        elif method == 'onIndustryClassification':
            groupBusiness.industryClassification(text=None, taskParams=taskParams)
        elif method == 'onDetermineDisable':
            '''封号检测'''
            accountBusiness.determineDisable(scheduleAccounts=listAccount)
        elif method == 'onDetermineRestricted':
            '''受限检测'''
            accountBusiness.determineRestricted(scheduleAccounts=listAccount)
        elif method == 'onEnterGroup':
            '''加入群'''
            accountBusiness.enterGroup(scheduleAccounts=listAccount, taskParams=taskParams)
        elif method == 'onAddSession':
            '''添加会话'''
            accountBusiness.addSession(scheduleAccounts=listAccount)
        elif method == 'onApplyForRobot':
            '''创建机器人'''
            accountBusiness.createRobot(scheduleAccounts=listAccount)
        elif method == 'onRefreshRobotToken':
            '''刷新机器人token'''
            accountBusiness.refreshRobotToken(scheduleAccounts=listAccount)
        elif method == 'onBotEnterGroup':
            '''机器人加入群'''
            accountBusiness.botEnterGroup(scheduleAccounts=listAccount)
        elif method == 'onCollectGroupMembers':
            '''采集群成员'''
            accountBusiness.collectGroupMembers(scheduleAccounts=listAccount, taskParams=taskParams)
        elif method == 'onCollectGroupInfo':
            '''遍历群信息'''
            accountBusiness.collectGroupInfo(scheduleAccounts=listAccount)
        elif method == 'onAddUserInGroup':
            '''拉用户进群'''
            accountBusiness.addUserInGroup(scheduleAccounts=listAccount)
        elif method == 'onSendNormalMsg':
            '''普通号私发'''
            accountBusiness.sendNormalMsg(scheduleAccounts=listAccount, taskParams=taskParams)
        elif method == 'onSendGroupMsg':
            '''普通号群发'''
            accountBusiness.sendGroupMsg(scheduleAccounts=listAccount, taskParams=taskParams)
        elif method == 'onSendGroupMsgByRobot':
            '''机器人群发'''
            accountBusiness.sendGroupMsgByRobot(scheduleAccounts=listAccount, taskParams=taskParams)
        elif method == 'onSendMsgToEachOther':
            '''互发消息'''
            accountBusiness.sendMsgToEachOther(scheduleAccounts=listAccount, taskParams=taskParams)

    # noinspection PyMethodMayBeStatic
    def __getAccounts(self,scheduleId: str)->list[Account]|None:
        schedulerInstance = InstanceManager.getScheduler()
        schedule = schedulerInstance.getSchedule(scheduleId)
        if schedule is None or schedule.accountParams is None:
            return  None

        jsonParam = json.loads(schedule.accountParams)
        accountParam: Account = ObjTools.dictToObj(jsonParam,Account)
        accountParam.withAccountDatas = True
        accountsServices = AccountsServices()
        listAccount: list[Account]|None = accountsServices.get(params=accountParam)
        return listAccount

    # noinspection PyMethodMayBeStatic
    def __getTaskParams(self,scheduleId: str)->str|None:
        schedulerInstance = InstanceManager.getScheduler()
        schedule = schedulerInstance.getSchedule(scheduleId)
        if schedule is None:
            return  None

        return schedule.taskParams

    # noinspection PyMethodMayBeStatic
    def __getTasks(self,task: TASK_WEB)->list[TASK_WEB]|None:
        webTaskManager = InstanceManager.getWorkSpace().webTaskManager
        if webTaskManager is None:
            return None

        return webTaskManager.getTasks(task=task)

    def scheduleRun(self, scheduleId: str, functionName: str, taskName: str):
        if functionName is None or taskName is None:
            return

        if taskName:
            task:TASK_WEB|None = None
            for taskSub in TASK_WEB:
                if taskSub.name == taskName:
                    task = taskSub
                    break

            if task is None:
                return

            # 启动任务前判断任务是否在执行
            listTask: list[TASK_WEB] = self.__getTasks(task=task)
            if listTask is None or len(listTask) > 0:
                return

        accountParams = None
        listAccount: [Account] = self.__getAccounts(scheduleId=scheduleId)
        if listAccount:
            accountParams = json.dumps(ObjTools.objToDict(listAccount))

        taskParams: str | None = self.__getTaskParams(scheduleId)
        self.sendSignalMsg(method=functionName,
                           accountParams=accountParams,
                           taskParams=taskParams)

    # noinspection PyMethodMayBeStatic
    def getPrettingMessages(self):
        messagesServices = MessagesServices()
        listMessages: list[Messages] = messagesServices.get(Messages())
        result = []
        if listMessages:
            for msgSub in listMessages:
                result.append({'title':msgSub.name,'value':msgSub.id})
        return result

    # noinspection PyMethodMayBeStatic
    def getAccountCountries(self):
        """
        获取账号国家分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getAccountBusiness()

        listResult = business.getTags().get('countries')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value':sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getAccountProvinces(self):
        """
        获取账号省份分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getAccountBusiness()

        listResult = business.getTags().get('provinces')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getAccountCities(self):
        """
        获取账号城市分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getAccountBusiness()

        listResult = business.getTags().get('cities')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getAccountRegions(self):
        """
        获取账号地区分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getAccountBusiness()

        listResult = business.getTags().get('regions')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getAccountIndustries(self):
        """
        获取账号行业分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getAccountBusiness()

        listResult = business.getTags().get('industries')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getAccountRemarks(self):
        """
        获取账号备注分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getAccountBusiness()

        listResult = business.getTags().get('remarks')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getGroupCountries(self):
        """
        获取群组国家分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getGroupBusiness()

        listResult = business.getTags().get('countries')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getGroupProvinces(self):
        """
        获取群组省份分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getGroupBusiness()

        listResult = business.getTags().get('provinces')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getGroupCities(self):
        """
        获取群组城市分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getGroupBusiness()

        listResult = business.getTags().get('cities')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getGroupRegions(self):
        """
        获取群组地区分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getGroupBusiness()

        listResult = business.getTags().get('regions')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getGroupIndustries(self):
        """
        获取群组行业分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getGroupBusiness()

        listResult = business.getTags().get('industries')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result

    # noinspection PyMethodMayBeStatic
    def getGroupRemarks(self):
        """
        获取群组备注分类
        :return:
        """
        business = InstanceManager.getWorkSpace().getGroupBusiness()

        listResult = business.getTags().get('remarks')
        result = []
        if listResult:
            for sub in listResult:
                if sub == '':
                    continue
                result.append({'title': sub, 'value': sub})
        return result