from datetime import datetime

from Business.models.summary737 import Summary
from Utils.tools import Tools
from paths import getProjectPath
from Utils.googleSheets import GoogleSheets
class Sheets737:
    def __init__(self):
        projectPath = getProjectPath()
        CREDENTIALS_FILE = f'{projectPath}Static/autobotchats-4c5cfe7df47e.json'
        SPREADSHEET_ID = '13QPgO93klnr4KTckiZuozY6wBahUkbLnRBoUdKiR72c'
        self.__gs = GoogleSheets(CREDENTIALS_FILE, SPREADSHEET_ID)

    @staticmethod
    def __fillList(rowIndex: int, cellList: list, summary: Summary, dateStr: str):
        totalGiftAmount: float = 0

        # 初始化
        indexFrom = Tools.excelColumnToNumber('BO') - 1
        indexTo = Tools.excelColumnToNumber('DL') - 1
        for i in range(indexFrom, indexTo + 1):
            cellList[i] = 0

        def DivideBy100(value:int|float)->float:
            if value is None:
                return 0
            if value == 0:
                return 0
            return value / 100

        #计算赠送金额
        giftAmount = 0
        for k in dir(summary.gift_coins_detail):
            # 排除私有成员
            if k.startswith('__'):
                continue
            attr = getattr(summary.gift_coins_detail, k)
            # 排除方法
            if callable(attr):
                continue
            giftAmount += attr
        giftAmount += summary.commission

        cellList[Tools.excelColumnToNumber('BO') - 1] = summary.visit_ip
        cellList[Tools.excelColumnToNumber('BP') - 1] = summary.login_user
        cellList[Tools.excelColumnToNumber('BQ') - 1] = summary.new_user
        cellList[Tools.excelColumnToNumber('BR') - 1] = summary.bet_user
        cellList[Tools.excelColumnToNumber('BS') - 1] = summary.first_recharge_user
        cellList[Tools.excelColumnToNumber('BT') - 1] = summary.recharge_user
        cellList[Tools.excelColumnToNumber('BU') - 1] = DivideBy100(summary.first_recharge_coins)
        cellList[Tools.excelColumnToNumber('BV') - 1] = DivideBy100(summary.total_bet)
        cellList[Tools.excelColumnToNumber('BW') - 1] = DivideBy100(summary.system_score)
        cellList[Tools.excelColumnToNumber('BX') - 1] = DivideBy100(summary.issue_coins)
        cellList[Tools.excelColumnToNumber('BY') - 1] = DivideBy100(summary.total_recharge)
        cellList[Tools.excelColumnToNumber('BZ') - 1] = DivideBy100(summary.total_withdraw)
        cellList[Tools.excelColumnToNumber('CA') - 1] = DivideBy100(summary.total_recharge - summary.total_withdraw)
        cellList[Tools.excelColumnToNumber('CB') - 1] = DivideBy100(summary.withdraw_commission)
        cellList[Tools.excelColumnToNumber('CC') - 1] = DivideBy100(summary.total_coins)
        cellList[Tools.excelColumnToNumber('CD') - 1] = DivideBy100(giftAmount) # 错误
        cellList[Tools.excelColumnToNumber('CE') - 1] = DivideBy100(summary.commission)
        cellList[Tools.excelColumnToNumber('CF') - 1] = DivideBy100(summary.gift_coins_detail.cashback_newuser)
        cellList[Tools.excelColumnToNumber('CG') - 1] = DivideBy100(summary.gift_coins_detail.cashback_activeuser)
        cellList[Tools.excelColumnToNumber('CH') - 1] = DivideBy100(summary.gift_coins_detail.cashback_recharge)
        cellList[Tools.excelColumnToNumber('CI') - 1] = DivideBy100(summary.gift_coins_detail.recharge_gift)
        cellList[Tools.excelColumnToNumber('CJ') - 1] = DivideBy100(summary.gift_coins_detail.user_rank)
        cellList[Tools.excelColumnToNumber('CK') - 1] = DivideBy100(summary.gift_coins_detail.fucard_reward)
        cellList[Tools.excelColumnToNumber('CL') - 1] = DivideBy100(summary.gift_coins_detail.fucard_exchange)
        cellList[Tools.excelColumnToNumber('CM') - 1] = DivideBy100(summary.act_consume_detail.pf_purchase)
        cellList[Tools.excelColumnToNumber('CN') - 1] = DivideBy100(summary.gift_coins_detail.pf_reward)
        cellList[Tools.excelColumnToNumber('CO') - 1] = DivideBy100(summary.gift_coins_detail.member_day)
        cellList[Tools.excelColumnToNumber('CP') - 1] = DivideBy100(summary.gift_coins_detail.fish_reward)
        cellList[Tools.excelColumnToNumber('CQ') - 1] = DivideBy100(summary.gift_coins_detail.game_benefit)
        cellList[Tools.excelColumnToNumber('CR') - 1] = DivideBy100(summary.gift_coins_detail.week_benefit)
        cellList[Tools.excelColumnToNumber('CS') - 1] = DivideBy100(summary.gift_coins_detail.red_envelope_rain)
        cellList[Tools.excelColumnToNumber('CT') - 1] = DivideBy100(summary.gift_coins_detail.vip_reward)
        cellList[Tools.excelColumnToNumber('CU') - 1] = DivideBy100(summary.gift_coins_detail.pwa_reward)
        cellList[Tools.excelColumnToNumber('CV') - 1] = DivideBy100(summary.gift_coins_detail.first_recharge)
        cellList[Tools.excelColumnToNumber('CW') - 1] = DivideBy100(summary.gift_coins_detail.pdd_reward)
        cellList[Tools.excelColumnToNumber('CX') - 1] = DivideBy100(summary.gift_coins_detail.total_recharge_reward)
        cellList[Tools.excelColumnToNumber('CY') - 1] = DivideBy100(summary.gift_coins_detail.redeem_code)
        cellList[Tools.excelColumnToNumber('CZ') - 1] = DivideBy100(summary.gift_coins_detail.jackpot)
        cellList[Tools.excelColumnToNumber('DA') - 1] = DivideBy100(summary.gift_coins_detail.mystery)
        cellList[Tools.excelColumnToNumber('DB') - 1] = DivideBy100(summary.gift_coins_detail.box_reward)
        cellList[Tools.excelColumnToNumber('DC') - 1] = DivideBy100(summary.gift_coins_detail.blind_box_reward)
        cellList[Tools.excelColumnToNumber('DD') - 1] = DivideBy100(summary.gift_coins_detail.pwa_convert_reward)
        cellList[Tools.excelColumnToNumber('DE') - 1] = DivideBy100(summary.gift_coins_detail.wash_chip)
        cellList[Tools.excelColumnToNumber('DF') - 1] = DivideBy100(summary.gift_coins_detail.global_wash_chip)
        cellList[Tools.excelColumnToNumber('DG') - 1] = DivideBy100(summary.gift_coins_detail.recharge_bargain_sales)
        cellList[Tools.excelColumnToNumber('DH') - 1] = DivideBy100(summary.gift_coins_detail.super_bet_day_reward)
        cellList[Tools.excelColumnToNumber('DI') - 1] = DivideBy100(summary.gift_coins_detail.sevenday_cashback_reward)
        cellList[Tools.excelColumnToNumber('DJ') - 1] = DivideBy100(summary.gift_coins_detail.active_bonus_reward)
        cellList[Tools.excelColumnToNumber('DK') - 1] = DivideBy100(summary.gift_coins_detail.mystery_task_reward)
        cellList[Tools.excelColumnToNumber('DL') - 1] = DivideBy100(summary.gift_coins_detail.lucky_wheel_reward)

        # 日期
        cellList[Tools.excelColumnToNumber('A') - 1] = dateStr
        # 赠送总额
        cellList[Tools.excelColumnToNumber('B') - 1] = DivideBy100(summary.gift_coins)
        cellList[Tools.excelColumnToNumber('C') - 1] = DivideBy100(summary.total_recharge)

        # 统计
        cellList[Tools.excelColumnToNumber('D') - 1] = f'=IFERROR(B{rowIndex}/C{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('E') - 1] = f'=IFERROR(CE{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('F') - 1] = f'=IFERROR(CE{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('G') - 1] = f'=IFERROR(CF{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('H') - 1] = f'=IFERROR(CF{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('I') - 1] = f'=IFERROR(CG{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('J') - 1] = f'=IFERROR(CG{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('K') - 1] = f'=IFERROR(CH{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('L') - 1] = f'=IFERROR(CH{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('M') - 1] = f'=IFERROR(CI{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('N') - 1] = f'=IFERROR(CI{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('O') - 1] = f'=IFERROR(CJ{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('P') - 1] = f'=IFERROR(CJ{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('Q') - 1] = f'=IFERROR(CK{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('R') - 1] = f'=IFERROR(CK{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('S') - 1] = f'=IFERROR(CL{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('T') - 1] = f'=IFERROR(CL{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('U') - 1] = f'=IFERROR(CM{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('V') - 1] = f'=IFERROR(CM{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('W') - 1] = f'=IFERROR(CN{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('X') - 1] = f'=IFERROR(CN{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('Y') - 1] = f'=IFERROR(CO{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('Z') - 1] = f'=IFERROR(CO{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AA') - 1] = f'=IFERROR(CP{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AB') - 1] = f'=IFERROR(CP{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AC') - 1] = f'=IFERROR(CQ{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AD') - 1] = f'=IFERROR(CQ{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AE') - 1] = f'=IFERROR(CR{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AF') - 1] = f'=IFERROR(CR{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AG') - 1] = f'=IFERROR(CS{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AH') - 1] = f'=IFERROR(CS{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AI') - 1] = f'=IFERROR(CT{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AJ') - 1] = f'=IFERROR(CT{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AK') - 1] = f'=IFERROR(CU{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AL') - 1] = f'=IFERROR(CU{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AM') - 1] = f'=IFERROR(CV{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AN') - 1] = f'=IFERROR(CV{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AO') - 1] = f'=IFERROR(CW{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AP') - 1] = f'=IFERROR(CW{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AQ') - 1] = f'=IFERROR(CX{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AR') - 1] = f'=IFERROR(CX{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AS') - 1] = f'=IFERROR(CY{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AT') - 1] = f'=IFERROR(CY{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AU') - 1] = f'=IFERROR(CZ{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AV') - 1] = f'=IFERROR(CZ{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AW') - 1] = f'=IFERROR(DA{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AX') - 1] = f'=IFERROR(DA{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('AY') - 1] = f'=IFERROR(DB{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('AZ') - 1] = f'=IFERROR(DB{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BA') - 1] = f'=IFERROR(DC{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BB') - 1] = f'=IFERROR(DC{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BC') - 1] = f'=IFERROR(DG{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BD') - 1] = f'=IFERROR(DG{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('BE') - 1] = f'=IFERROR(DH{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BF') - 1] = f'=IFERROR(DH{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BG') - 1] = f'=IFERROR(DI{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BH') - 1] = f'=IFERROR(DI{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BI') - 1] = f'=IFERROR(DJ{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BJ') - 1] = f'=IFERROR(DJ{rowIndex}/B{rowIndex},0)'

        cellList[Tools.excelColumnToNumber('BK') - 1] = f'=IFERROR(DK{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BL') - 1] = f'=IFERROR(DK{rowIndex}/B{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BM') - 1] = f'=IFERROR(DL{rowIndex}/C{rowIndex},0)'
        cellList[Tools.excelColumnToNumber('BN') - 1] = f'=IFERROR(DL{rowIndex}/B{rowIndex},0)'

    def append(self, summary:  Summary, checkDate: bool = True):
        date = datetime.fromtimestamp(summary.daytime)
        dateStr: str = date.strftime("%Y-%m-%d")

        # 判断当前日期数据是否存在
        if checkDate:
            existDate = self.__gs.date_exists_in_column('Sheet737', 'A', dateStr, weekday_aware=True)
            if existDate:
                return True

        rowCount = self.__gs.get_data_row_count('Sheet737')

        length = Tools.excelColumnToNumber('DL')
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        Sheets737.__fillList(rowCount + 1, cellList, summary, dateStr)
        isSuccess = self.__gs.append_rows('Sheet737', [cellList])
        if isSuccess:
            print("sheet737,追加成功")
            return True
        else:
            print("sheet737,追加失败")
            return False

    def update(self, summary:  Summary, indexRow):
        date = datetime.fromtimestamp(summary.daytime)
        dateStr: str = date.strftime("%Y-%m-%d")

        length = Tools.excelColumnToNumber('DL')
        default_value = None  # 可以替换为你想要的初始值
        cellList = [default_value for _ in range(length)]

        Sheets737.__fillList(indexRow, cellList, summary, dateStr)
        isSuccess = self.__gs.update_row('Sheet737',indexRow,[cellList],start_column=1)
        if isSuccess:
            print("sheet737,修改成功")
            return True
        else:
            print("sheet737,修改失败")
            return False

    def getDateColumn(self)->list:
        result = self.__gs.get_column_data('Sheet737','A',skip_header=True)
        if result is None or len(result) <= 0:
            return []
        return result[1:]