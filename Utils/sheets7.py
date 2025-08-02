from Business.models.summary7 import SummaryItem
from Utils.tools import Tools
from paths import getProjectPath
from Utils.googleSheets import GoogleSheets
class Sheets7:
    def __init__(self):
        projectPath = getProjectPath()
        CREDENTIALS_FILE = f'{projectPath}Static/autobotchats-4c5cfe7df47e.json'
        SPREADSHEET_ID = '13QPgO93klnr4KTckiZuozY6wBahUkbLnRBoUdKiR72c'
        self.__gs = GoogleSheets(CREDENTIALS_FILE, SPREADSHEET_ID)


    @staticmethod
    def __fillList(rowIndex:int,cellList:list,summary:list[SummaryItem],dateStr:str,totalPay:float):
        totalGiftAmount:float = 0

        # 初始化
        indexFrom = Tools.excelColumnToNumber('AS')-1
        indexTo = Tools.excelColumnToNumber('BL')-1
        for i in range(indexFrom,indexTo+1):
            cellList[i] = 0

        for sub in summary:
            if sub.scoreSum > 0:
                score = sub.scoreSum / 100
            else:
                score = 0

            if sub.message == '彩金排行榜':
                cellList[Tools.excelColumnToNumber('AS')-1] = score
                totalGiftAmount += score
            elif sub.message == '成长等级提升赠送':
                cellList[Tools.excelColumnToNumber('AT')-1] = score
                totalGiftAmount += score
            elif sub.message == '成长月礼包赠送' or sub.message == '成长周礼包赠送':
                cellList[Tools.excelColumnToNumber('AU')-1] = score
                totalGiftAmount += score
            elif sub.message == '充值返利奖励':
                cellList[Tools.excelColumnToNumber('AV')-1] = score
                totalGiftAmount += score
            elif sub.message == '分享宝箱奖励':
                cellList[Tools.excelColumnToNumber('AW')-1] = score
                totalGiftAmount += score
            elif sub.message == '分享拉新下家充值上家返利':
                cellList[Tools.excelColumnToNumber('AX')-1] = score
                totalGiftAmount += score
            elif sub.message == '分享转盘抽奖奖励':
                cellList[Tools.excelColumnToNumber('AY')-1] = score
                totalGiftAmount += score
            elif sub.message == '刮刮乐':
                cellList[Tools.excelColumnToNumber('AZ')-1] = score
                totalGiftAmount += score
            elif sub.message == '领取充能':
                cellList[Tools.excelColumnToNumber('BA')-1] = score
                totalGiftAmount += score
            elif sub.message == '每日救援金赠送':
                cellList[Tools.excelColumnToNumber('BB')-1] = score
                totalGiftAmount += score
            elif sub.message == '破产补助二次赠送':
                cellList[Tools.excelColumnToNumber('BC')-1] = score
                totalGiftAmount += score
            elif sub.message == '破产补助首次赠送':
                cellList[Tools.excelColumnToNumber('BD')-1] = score
                totalGiftAmount += score
            elif sub.message == '签到赠送':
                cellList[Tools.excelColumnToNumber('BE')-1] = score
                totalGiftAmount += score
            elif sub.message == '神秘彩金赠送':
                cellList[Tools.excelColumnToNumber('BF')-1] = score
                totalGiftAmount += score
            elif sub.message == '幸运转盘抽奖赠送':
                cellList[Tools.excelColumnToNumber('BG')-1] = score
                totalGiftAmount += score
            elif sub.message == '注册帐号赠送':
                cellList[Tools.excelColumnToNumber('BH')-1] = score
                totalGiftAmount += score
            elif sub.message == '充值额外赠送':
                cellList[Tools.excelColumnToNumber('BI')-1] = score
                totalGiftAmount += score
            elif sub.message == '分享转盘提现奖励':
                cellList[Tools.excelColumnToNumber('BJ')-1] = score
                totalGiftAmount += score
            elif sub.message == '连续签到赠送':
                cellList[Tools.excelColumnToNumber('BK')-1] = score
                totalGiftAmount += score
            elif sub.message == '每周救援金':
                cellList[Tools.excelColumnToNumber('BL')-1] = score
                totalGiftAmount += score

        # 日期
        cellList[Tools.excelColumnToNumber('A')-1] = dateStr
        # 赠送总额
        cellList[Tools.excelColumnToNumber('B') - 1] = totalGiftAmount
        # 充值总额
        if totalPay > 0:
            totalPay = totalPay / 100
        cellList[Tools.excelColumnToNumber('C') - 1] = totalPay

        # 统计
        cellList[Tools.excelColumnToNumber('D') - 1] = f'=IFERROR(B{rowIndex}/C{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('E') - 1] = f'=IFERROR(AS{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('F') - 1] = f'=IFERROR(AS{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('G') - 1] = f'=IFERROR(AT{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('H') - 1] = f'=IFERROR(AT{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('I') - 1] = f'=IFERROR(AU{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('J') - 1] = f'=IFERROR(AU{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('K') - 1] = f'=IFERROR(AV{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('L') - 1] = f'=IFERROR(AV{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('M') - 1] = f'=IFERROR(AW{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('N') - 1] = f'=IFERROR(AW{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('O') - 1] = f'=IFERROR(AX{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('P') - 1] = f'=IFERROR(AX{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('Q') - 1] = f'=IFERROR(AY{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('R') - 1] = f'=IFERROR(AY{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('S') - 1] = f'=IFERROR(AZ{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('T') - 1] = f'=IFERROR(AZ{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('U') - 1] = f'=IFERROR(BA{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('V') - 1] = f'=IFERROR(BA{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('W') - 1] = f'=IFERROR(BB{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('X') - 1] = f'=IFERROR(BB{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('Y') - 1] = f'=IFERROR(BC{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('Z') - 1] = f'=IFERROR(BC{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AA') - 1] = f'=IFERROR(BD{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AB') - 1] = f'=IFERROR(BD{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AC') - 1] = f'=IFERROR(BE{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AD') - 1] = f'=IFERROR(BE{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AE') - 1] = f'=IFERROR(BF{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AF') - 1] = f'=IFERROR(BF{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AG') - 1] = f'=IFERROR(BG{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AH') - 1] = f'=IFERROR(BG{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AI') - 1] = f'=IFERROR(BH{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AJ') - 1] = f'=IFERROR(BH{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AK') - 1] = f'=IFERROR(BI{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AL') - 1] = f'=IFERROR(BI{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AM') - 1] = f'=IFERROR(BJ{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AN') - 1] = f'=IFERROR(BJ{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AO') - 1] = f'=IFERROR(BK{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AP') - 1] = f'=IFERROR(BK{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AQ') - 1] = f'=IFERROR(BL{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AR') - 1] = f'=IFERROR(BL{rowIndex}/B{rowIndex},0)'


    def append(self,summary:list[SummaryItem],dateStr:str,totalPay:float, checkDate:bool= True)->bool:
        # 判断当前日期数据是否存在
        if checkDate:
            existDate = self.__gs.date_exists_in_column('SheetSete7', 'A', dateStr, weekday_aware=True)
            if existDate:
                return True

        rowCount = self.__gs.get_data_row_count('SheetSete7')

        length = Tools.excelColumnToNumber('BL')
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        Sheets7.__fillList(rowCount+1,cellList,summary,dateStr,totalPay)
        isSuccess = self.__gs.append_rows('SheetSete7', [cellList])
        if isSuccess:
            print("sheetSete7,追加成功")
            return True
        else:
            print("sheetSete7,追加失败")
            return False

    def update(self, summary:list[SummaryItem],dateStr:str,totalPay:float,indexRow):

        length = Tools.excelColumnToNumber('BL')
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        Sheets7.__fillList(indexRow, cellList,summary,dateStr,totalPay)
        isSuccess = self.__gs.update_row('SheetSete7',indexRow,[cellList])
        if isSuccess:
            print("sheet737,修改成功")
            return True
        else:
            print("sheet737,修改失败")
            return False

    def getDateColumn(self)->list:
        result = self.__gs.get_column_data('SheetSete7', 'A', skip_header=True)
        if result is None or len(result) <= 0:
            return []
        return result[1:]
