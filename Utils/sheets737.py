import time
from datetime import datetime

from Business.models.sheetStructItem import SheetStructItem
from Business.models.summary737 import Summary
from Utils.tools import Tools
from paths import getProjectPath
from Utils.googleSheets import GoogleSheets
class Sheets737:
    __sheetStructList:list[SheetStructItem] = None

    def __init__(self):
        projectPath = getProjectPath()
        CREDENTIALS_FILE = f'{projectPath}Static/autobotchats-4c5cfe7df47e.json'
        SPREADSHEET_ID = '13QPgO93klnr4KTckiZuozY6wBahUkbLnRBoUdKiR72c'
        SPREADSHEET_ID_TEMPLATE = '1snBjPsrS12rXO3Kkcye6uzezRO81ILeyqzXNtXldl5w'
        self.__sheetName = 'Sheet737'
        self.__gs = GoogleSheets(CREDENTIALS_FILE, SPREADSHEET_ID)
        self.__gs_temp = GoogleSheets(CREDENTIALS_FILE, SPREADSHEET_ID_TEMPLATE)
        if Sheets737.__sheetStructList is None:
            Sheets737.__sheetStructList = self.getSheetStruct()

    def __fillList(self,rowIndex: int, cellList: list, summary: Summary, dateStr: str):
        # 初始化
        def DivideBy100(valueParam: int | float) -> float:
            if valueParam is None:
                return 0
            if valueParam == 0:
                return 0
            return valueParam / 100

        valuesDict = {
            "dateStr":dateStr
        }

        # 计算赠送金额
        giftAmount = 0
        for k in dir(summary.gift_coins_detail):
            # 排除私有成员
            if k.startswith('__'):
                continue
            attr = getattr(summary.gift_coins_detail, k)
            # 排除方法
            if callable(attr):
                continue

            valuesDict[k] = attr
            giftAmount += attr

        giftAmount += summary.commission
        diffRechargeAndWithdraw = summary.total_recharge - summary.total_withdraw
        valuesDict['giftAmount'] = giftAmount
        valuesDict['diffRechargeAndWithdraw'] = diffRechargeAndWithdraw

        for k in dir(summary.act_consume_detail):
            # 排除私有成员
            if k.startswith('__'):
                continue
            attr = getattr(summary.act_consume_detail, k)
            # 排除方法
            if callable(attr):
                continue

            valuesDict[k] = attr

        for k in dir(summary):
            # 排除私有成员
            if k.startswith('__'):
                continue
            if k == 'gift_coins_detail' or k == 'act_consume_detail':
                continue

            attr = getattr(summary, k)
            # 排除方法
            if callable(attr):
                continue

            valuesDict[k] = attr

        # 填充数据
        lenStruct = len(Sheets737.__sheetStructList)
        for i in range(lenStruct):
            struct = Sheets737.__sheetStructList[i]
            if struct.variableName:
                value:int|float|str = valuesDict.get(struct.variableName)
                if struct.conversionFunction == 'DivideBy100':
                    cellList[i] = DivideBy100(value)
                else:
                    cellList[i] = value
            elif struct.function:
                cellList[i] = struct.function.replace('4',str(rowIndex))


    def append(self, summary:  Summary, checkDate: bool = True):
        date = datetime.fromtimestamp(summary.daytime)
        dateStr: str = date.strftime("%Y-%m-%d")

        # 判断当前日期数据是否存在
        if checkDate:
            existDate = self.__gs.date_exists_in_column(self.__sheetName, 'A', dateStr, weekday_aware=True)
            if existDate:
                return True

        rowCount = self.__gs.get_data_row_count(self.__sheetName)

        length = len(Sheets737.__sheetStructList)
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        self.__fillList(rowCount + 1, cellList, summary, dateStr)
        isSuccess = self.__gs.append_rows(self.__sheetName, [cellList])
        if isSuccess:
            print(f"{self.__sheetName},追加成功")
            return True
        else:
            print(f"{self.__sheetName},追加失败")
            return False

    def update(self, summary:  Summary, indexRow):
        date = datetime.fromtimestamp(summary.daytime)
        dateStr: str = date.strftime("%Y-%m-%d")

        length = len(Sheets737.__sheetStructList)
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        self.__fillList(indexRow, cellList, summary, dateStr)
        isSuccess = self.__gs.update_row(self.__sheetName,indexRow,[cellList],start_column=1)
        if isSuccess:
            print(f"{self.__sheetName},修改成功")
            return True
        else:
            print(f"{self.__sheetName},修改失败")
            return False

    def getDateColumn(self)->list:
        result = self.__gs.get_column_data(self.__sheetName,'A',skip_header=True)
        if result is None or len(result) <= 0:
            return []
        return result[1:]

    def getSheetStruct(self)->list[SheetStructItem]:
        """
        获取sheet表结构
        """
        columnCount = self.__gs_temp.get_column_count(self.__sheetName)
        lastCellName = self.__gs_temp.column_index_to_letter(columnCount)
        result1 = self.__gs_temp.read_range(f'{self.__sheetName}!A4:{lastCellName}4',value_render_option="FORMULA")
        result2 = self.__gs_temp.read_range(f'{self.__sheetName}!A5:{lastCellName}7')

        sheetStructList:list[SheetStructItem] = []
        for i in range(columnCount):
            variableName = result2[0][i]
            function = str(result1[0][i])
            conversionFunction = result2[1][i]
            value = result2[2][i]

            if function.find('=IFERROR') < 0:
                function = ''

            sheetStructItem = SheetStructItem(variableName=variableName,function=function,value=value,conversionFunction=conversionFunction)
            sheetStructList.append(sheetStructItem)

        return sheetStructList

    def updateSheetStructByNewVar(self,variableName:str)->bool:
        columnCount = self.__gs_temp.get_column_count(self.__sheetName)
        # 获取公式列表索引
        lenStruct = len(Sheets737.__sheetStructList)
        isStart = False
        indexFun = 0
        for i in range(lenStruct):
            sub = Sheets737.__sheetStructList[i]
            if sub.function != '':
                isStart = True
            else:
                if isStart:
                    indexFun = i
                    break

        def insertSub(gs:GoogleSheets,indexFunLast,columnCountOld,isTemplate:bool=False)->bool:
            nameFunLast = GoogleSheets.column_index_to_letter(indexFunLast)
            # 在第n列后插入，并继承左侧格式
            if not gs.insert_column(
                sheet_name=self.__sheetName,
                column=nameFunLast,
                inherit_from_before=True
            ):
                return False

            if not gs.insert_column(
                sheet_name=self.__sheetName,
                column=nameFunLast,
                inherit_from_before=True
            ):
                return False

            nameLastNew = GoogleSheets.column_index_to_letter(columnCountOld + 2)
            if not gs.insert_column(
                sheet_name=self.__sheetName,
                column=nameLastNew,
                inherit_from_before=True
            ):
                return False

            # 合并标题栏
            nameFunAdd1 = GoogleSheets.column_index_to_letter(indexFunLast+1)
            nameFunAdd2 = GoogleSheets.column_index_to_letter(indexFunLast+2)
            gs.merge_cells(self.__sheetName,f'{nameFunAdd1}1:{nameFunAdd2}1')

            # 填充标题内容
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}1:{nameFunAdd1}1',values = [[f'新字段:{variableName}']]):
                return False
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}2:{nameFunAdd2}2', values=[['占比充值','占比赠送']]):
                return False


            nameLastAdd = GoogleSheets.column_index_to_letter(columnCountOld + 3)
            # 统计栏公式
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}3:{nameFunAdd2}3',
                                  values=[[f'=IFERROR({nameLastAdd}3/C3,0)', f'=IFERROR({nameLastAdd}3/B3,0)']]):
                return False

            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}1:{nameLastAdd}1',
                           values=[[f'新字段:{variableName}']]):
                return False
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}3:{nameLastAdd}3',
                           values=[[f'=SUM({nameLastAdd}4:{nameLastAdd}3000)']]):
                return False


            if not isTemplate:
                return True

            # 填充公式和值
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}4:{nameFunAdd2}4',
                           values=[[f'=IFERROR({nameLastAdd}4/C4,0)', f'=IFERROR({nameLastAdd}4/B4,0)']]):
                return False

            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}4:{nameLastAdd}4',
                           values=[[100]]):
                return False

            # 填充对象名称
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}5:{nameLastAdd}5',
                           values=[[variableName]]):
                return False

            # 填充转换函数
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}6:{nameLastAdd}6',
                           values=[['DivideBy100']]):
                return False

            # 填充转换可变参数
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}7:{nameLastAdd}7',
                           values=[['variable']]):
                return False

            return True

        if not insertSub(self.__gs_temp,indexFun,columnCount,isTemplate=True):
            return False
        if not insertSub(self.__gs, indexFun, columnCount):
            return False

        return True

    def checkNewVarForSheetStruct(self,summary:  Summary)->bool:
        newVarList:list[str] = []
        for k in dir(summary.gift_coins_detail):
            # 排除私有成员
            if k.startswith('__'):
                continue
            attr = getattr(summary.gift_coins_detail, k)
            # 排除方法
            if callable(attr):
                continue

            bHave = False
            for sub in Sheets737.__sheetStructList:
                if sub.variableName == k:
                    bHave = True
                    break
            if not bHave:
                newVarList.append(k)

        lenNew = len(newVarList)
        if lenNew <= 0:
            return False

        print(f'添加sheet新字段：{lenNew}')
        for i in range(lenNew):
            newVar = newVarList[i]
            print(f'{i+1} 执行中...')
            self.updateSheetStructByNewVar(newVar)
            print(f'{i + 1} 新增成功')
            #
            # 获取新的结构
            Sheets737.__sheetStructList = self.getSheetStruct()

        return True

