import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class ActConsumeDetail:
    pf_purchase: int = 0 # 公积金购买
    pass_mission_purchase: int = 0 # 通行证购买

@dataclass
class GiftCoinsDetail:
    recharge_gift: int = 0 # 充值赠送
    recharge_package: int = 0
    user_rank: int = 0  # 用户等级奖励
    fucard_reward: int = 0  # 转盘抽卡
    fucard_exchange: int = 0 # 转盘兑换
    cashback_recharge: int = 0  # 充值返现
    cashback_newuser: int = 0  # 新用户返现
    cashback_activeuser: int = 0  # 活跃用户返现
    game_benefit: int = 0  #救济金
    red_envelope_rain: int = 0  #红包雨
    vip_reward: int = 0  #VIP 奖励
    pwa_reward: int = 0  #PWA 奖励
    first_recharge: int = 0   #首冲奖励
    pdd_reward: int = 0  #拼多多
    total_recharge_reward: int = 0  # 累充奖励
    week_benefit: int = 0  #周补偿金
    redeem_code: int = 0  #兑换码
    jackpot: int = 0  # 刮刮乐
    mystery: int = 0  # 神秘彩金
    box_reward: int = 0  #宝箱彩金
    blind_box_reward: int = 0  #盲盒彩金
    pf_reward: int = 0  # 公积金发放
    member_day: int = 0  #超级会员日
    wash_chip: int = 0  # 厂商洗码
    global_wash_chip: int = 0  # 全站洗码
    fish_reward: int = 0  #新人专享
    pwa_convert_reward: int = 0 # h5转化PWA
    recharge_bargain_sales: int = 0  # 充值大酬宾
    super_bet_day_reward: int = 0  # 超级打码日
    sevenday_cashback_reward: int = 0  #7日返金
    active_bonus_reward: int = 0  #活跃彩金
    mystery_task_reward: int = 0  #神秘任务
    lucky_wheel_reward: int = 0  #幸运转盘
    happy_hour_reward: int = 0  #欢乐时光
    day_first_recharge_reward: int = 0  # 日首存
    pass_mission_reward: int = 0  # 通行证奖励
    audit_box_reward: int = 0 #活跃宝箱

@dataclass
class Summary:
    act_consume_detail: ActConsumeDetail
    gift_coins_detail: GiftCoinsDetail
    act_consume: int = 0
    bet_user: int = 0  #投注用户
    commission: int = 0  # 发放佣金
    daytime: int = 0
    dealer_num: int = 0
    first_recharge_coins: int = 0  #首充金额
    first_recharge_fission_user: int = 0
    first_recharge_user: int = 0  # 首充用户
    game_benefit: int = 0
    gift_coins: int = 0
    issue_coins: int = 0   #现金充值
    login_user: int = 0  #登录用户
    new_user: int = 0  #新增用户
    recharge_user: int = 0  #充值用户
    remain_commission: int = 0
    system_deduction: int = 0
    system_score: int = 0  #平台盈利
    total_bet: int = 0  #投注金额
    total_bet_count: int = 0
    total_coins: int = 0  #流通金额
    total_recharge: int = 0  #订单充值
    total_user: int = 0
    total_withdraw: int = 0  #订单提现
    visit_ip: int = 0  # 访问ip
    withdraw_commission: int = 0  #提现手续费

    @classmethod
    def from_dict(cls, data: Dict):
        temp = data.get('act_consume_detail')
        if isinstance(temp,dict):
            act_consume_detail = ActConsumeDetail(**temp)
        elif isinstance(temp,str):
            tempDict = json.loads(temp)
            act_consume_detail = ActConsumeDetail(**tempDict)

        temp = data.get('gift_coins_detail')
        if isinstance(temp, dict):
            gift_coins_detail = GiftCoinsDetail(**temp)
        elif isinstance(temp, str):
            tempDict = json.loads(temp)
            gift_coins_detail = GiftCoinsDetail(**tempDict)

        return cls(
            act_consume=data['act_consume'],
            act_consume_detail=act_consume_detail,
            bet_user=data['bet_user'],
            commission=data['commission'],
            daytime=data['daytime'],
            dealer_num=data['dealer_num'],
            first_recharge_coins=data['first_recharge_coins'],
            first_recharge_fission_user=data['first_recharge_fission_user'],
            first_recharge_user=data['first_recharge_user'],
            game_benefit=data['game_benefit'],
            gift_coins=data['gift_coins'],
            gift_coins_detail=gift_coins_detail,
            issue_coins=data['issue_coins'],
            login_user=data['login_user'],
            new_user=data['new_user'],
            recharge_user=data['recharge_user'],
            remain_commission=data['remain_commission'],
            system_deduction=data['system_deduction'],
            system_score=data['system_score'],
            total_bet=data['total_bet'],
            total_bet_count=data['total_bet_count'],
            total_coins=data['total_coins'],
            total_recharge=data['total_recharge'],
            total_user=data['total_user'],
            total_withdraw=data['total_withdraw'],
            visit_ip=data['visit_ip'],
            withdraw_commission=data['withdraw_commission']
        )