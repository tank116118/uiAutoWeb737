from Business.models.sheetStructItem import SheetStructItem
from Business.models.summary7 import SummaryItem
from paths import getProjectPath
from Utils.googleSheets import GoogleSheets
class Sheets7:
    __sheetStructList: list[SheetStructItem] = None

    def __init__(self):
        projectPath = getProjectPath()
        CREDENTIALS_FILE = f'{projectPath}Static/autobotchats-4c5cfe7df47e.json'
        SPREADSHEET_ID = '13QPgO93klnr4KTckiZuozY6wBahUkbLnRBoUdKiR72c'
        SPREADSHEET_ID_TEMPLATE = '1snBjPsrS12rXO3Kkcye6uzezRO81ILeyqzXNtXldl5w'
        self.__sheetName = 'SheetSete7'
        self.__gs = GoogleSheets(CREDENTIALS_FILE, SPREADSHEET_ID)
        self.__gs_temp = GoogleSheets(CREDENTIALS_FILE, SPREADSHEET_ID_TEMPLATE)
        if Sheets7.__sheetStructList is None:
            Sheets7.__sheetStructList = self.getSheetStruct()

    @staticmethod
    def __fillList(rowIndex:int, cellList:list, summary:list[SummaryItem], dateStr:str, total_recharge:float):

        def DivideBy100(valueParam: int | float) -> float:
            if valueParam is None:
                return 0
            if valueParam == 0:
                return 0
            return valueParam / 100

        valuesDict:dict[str,str|int|float] = {
            "dateStr":dateStr
        }

        giftAmount: float = 0
        for sub in summary:
            valuesDict[sub.message] = sub.scoreSum
            giftAmount += sub.scoreSum

        valuesDict['giftAmount'] = giftAmount
        valuesDict['total_recharge'] = total_recharge

        # 填充数据
        lenStruct = len(Sheets7.__sheetStructList)
        for i in range(lenStruct):
            struct = Sheets7.__sheetStructList[i]
            if struct.variableName:
                value: int | float | str = valuesDict.get(struct.variableName)
                if 'dateStr' != struct.variableName:
                    cellList[i] = DivideBy100(value)
                else:
                    cellList[i] = value
            elif struct.function:
                cellList[i] = struct.function.replace('4', str(rowIndex))

    def append(self,summary:list[SummaryItem],dateStr:str,total_recharge:float, checkDate:bool= True)->bool:
        # 判断当前日期数据是否存在
        if checkDate:
            existDate = self.__gs.date_exists_in_column(self.__sheetName, 'A', dateStr, weekday_aware=True)
            if existDate:
                return True

        rowCount = self.__gs.get_data_row_count(self.__sheetName)

        length = len(Sheets7.__sheetStructList)
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        Sheets7.__fillList(rowCount+1,cellList,summary,dateStr,total_recharge)
        isSuccess = self.__gs.append_rows(self.__sheetName, [cellList])
        if isSuccess:
            print(f"{self.__sheetName},追加成功")
            return True
        else:
            print(f"{self.__sheetName},追加失败")
            return False

    def update(self, summary:list[SummaryItem],dateStr:str,total_recharge:float,indexRow):

        length = len(Sheets7.__sheetStructList)
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        Sheets7.__fillList(indexRow, cellList,summary,dateStr,total_recharge)
        isSuccess = self.__gs.update_row(self.__sheetName,indexRow,[cellList])
        if isSuccess:
            print("sheet737,修改成功")
            return True
        else:
            print("sheet737,修改失败")
            return False

    def getDateColumn(self)->list:
        result = self.__gs.get_column_data(self.__sheetName, 'A', skip_header=True)
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
        result2 = self.__gs_temp.read_range(f'{self.__sheetName}!A5:{lastCellName}6')

        sheetStructList:list[SheetStructItem] = []
        for i in range(columnCount):
            variableName = result2[0][i]
            function = str(result1[0][i])
            value = result2[1][i]

            if function.find('=IFERROR') < 0:
                function = ''

            sheetStructItem = SheetStructItem(variableName=variableName,function=function,value=value,conversionFunction='')
            sheetStructList.append(sheetStructItem)

        return sheetStructList

    def updateSheetStructByNewVar(self,variableName:str)->bool:
        columnCount = self.__gs_temp.get_column_count(self.__sheetName)
        # 获取公式列表索引
        lenStruct = len(Sheets7.__sheetStructList)
        isStart = False
        indexFun = 0
        for i in range(lenStruct):
            sub = Sheets7.__sheetStructList[i]
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
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}1:{nameFunAdd1}1',values = [[variableName]]):
                return False
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}2:{nameFunAdd2}2', values=[['占比充值','占比赠送']]):
                return False


            nameLastAdd = GoogleSheets.column_index_to_letter(columnCountOld + 3)
            # 统计栏公式
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameFunAdd1}3:{nameFunAdd2}3',
                                  values=[[f'=IFERROR({nameLastAdd}3/C3,0)', f'=IFERROR({nameLastAdd}3/B3,0)']]):
                return False

            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}1:{nameLastAdd}1',
                           values=[[variableName]]):
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

            # 填充转换可变参数
            if not gs.write_range(range_name=f'{self.__sheetName}!{nameLastAdd}6:{nameLastAdd}6',
                           values=[['variable']]):
                return False

            return True

        if not insertSub(self.__gs_temp,indexFun,columnCount,isTemplate=True):
            return False
        if not insertSub(self.__gs, indexFun, columnCount):
            return False

        return True

    def checkNewVarForSheetStruct(self,summary:  list[SummaryItem])->bool:
        newVarList: list[str] = []

        for subSum in summary:
            bHave = False
            for sub in Sheets7.__sheetStructList:
                if sub.variableName == subSum.message:
                    bHave = True
                    break
            if not bHave:
                newVarList.append(subSum.message)

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
            Sheets7.__sheetStructList = self.getSheetStruct()

        return True
