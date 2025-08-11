
from dataclasses import dataclass

@dataclass
class SummaryItem:
    message: str
    userCount: int
    scoreSum: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            message=data.get('message'),
            userCount=data.get('userCount'),
            scoreSum=data.get('scoreSum')
        )


@dataclass
class Operating:
    dateID: int
    agentID: int
    regCount: int
    downCount: int
    logonCount: int
    rechargeCount: int
    rechargeScore: int
    exchangeCount: int
    exchangeScore: int
    betScore: int
    winScore: int
    payCount: int
    payScore: int
    withdrawCount: int
    withdrawScore: int
    tCRechargeCount: int
    tCRechargeScore: int
    tCExchangeCount: int
    tCExchangeScore: int
    tCPayCount: int
    tCPayScore: int
    tCWithdrawCount: int
    tCWithdrawScore: int
    tCBetScore: int
    tCWinScore: int
    payOrderCash: int
    payCash: int # 充值金额
    withdrawOrderCash: int
    withdrawCash: int
    payUserCount: int
    withdrawUserCount: int
    present: int
    payAndBetUserCount: int
    firstPayUser: int
    betUser: int
    fitstPayReBet2Day: int
    fitstPayReBet3Day: int
    fitstPayReBet7Day: int
    bindCount: int
    betScoreExp: int
    winScoreExp: int
    firstPayTotalCash: int
    pwaCount: int
    oneNewPayUser: int
    oneNewPayCash: int
    oneFirstPayUser: int
    oneFirstPayCash: int
    newPayUser: int
    newPayCash: int
    firstPayCash: int
    oneFirstPayTotalCash: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            dateID=data.get('dateID', 0),
            agentID=data.get('agentID', 0),
            regCount=data.get('regCount', 0),
            downCount=data.get('downCount', 0),
            logonCount=data.get('logonCount', 0),
            rechargeCount=data.get('rechargeCount', 0),
            rechargeScore=data.get('rechargeScore', 0),
            exchangeCount=data.get('exchangeCount', 0),
            exchangeScore=data.get('exchangeScore', 0),
            betScore=data.get('betScore', 0),
            winScore=data.get('winScore', 0),
            payCount=data.get('payCount', 0),
            payScore=data.get('payScore', 0),
            withdrawCount=data.get('withdrawCount', 0),
            withdrawScore=data.get('withdrawScore', 0),
            tCRechargeCount=data.get('tCRechargeCount', 0),
            tCRechargeScore=data.get('tCRechargeScore', 0),
            tCExchangeCount=data.get('tCExchangeCount', 0),
            tCExchangeScore=data.get('tCExchangeScore', 0),
            tCPayCount=data.get('tCPayCount', 0),
            tCPayScore=data.get('tCPayScore', 0),
            tCWithdrawCount=data.get('tCWithdrawCount', 0),
            tCWithdrawScore=data.get('tCWithdrawScore', 0),
            tCBetScore=data.get('tCBetScore', 0),
            tCWinScore=data.get('tCWinScore', 0),
            payOrderCash=data.get('payOrderCash', 0),
            payCash=data.get('payCash', 0),
            withdrawOrderCash=data.get('withdrawOrderCash', 0),
            withdrawCash=data.get('withdrawCash', 0),
            payUserCount=data.get('payUserCount', 0),
            withdrawUserCount=data.get('withdrawUserCount', 0),
            present=data.get('present', 0),
            payAndBetUserCount=data.get('payAndBetUserCount', 0),
            firstPayUser=data.get('firstPayUser', 0),
            betUser=data.get('betUser', 0),
            fitstPayReBet2Day=data.get('fitstPayReBet2Day', 0),
            fitstPayReBet3Day=data.get('fitstPayReBet3Day', 0),
            fitstPayReBet7Day=data.get('fitstPayReBet7Day', 0),
            bindCount=data.get('bindCount', 0),
            betScoreExp=data.get('betScoreExp', 0),
            winScoreExp=data.get('winScoreExp', 0),
            firstPayTotalCash=data.get('firstPayTotalCash', 0),
            pwaCount=data.get('pwaCount', 0),
            oneNewPayUser=data.get('oneNewPayUser', 0),
            oneNewPayCash=data.get('oneNewPayCash', 0),
            oneFirstPayUser=data.get('oneFirstPayUser', 0),
            oneFirstPayCash=data.get('oneFirstPayCash', 0),
            newPayUser=data.get('newPayUser', 0),
            newPayCash=data.get('newPayCash', 0),
            firstPayCash=data.get('firstPayCash', 0),
            oneFirstPayTotalCash=data.get('oneFirstPayTotalCash', 0)
        )