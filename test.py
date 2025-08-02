# noinspection PyMethodMayBeStatic
# noinspection PyUnusedLocal
# type: ignore
import csv
import random


# html="""
# """

# pattern = r'https?://www\.facebook\.com/groups/(\d+)(?:/|\?|$)'
#
# match = re.findall(pattern, html)
# if match:
#     # extra = match.group(0)
#     # print(extra)
#     print(match)

# accountsServices = AccountsServices()
# accountsServices.resetMsgIndex(ids=[123,456],msgType='group')

# gemini = Gemini()
#
# while True:
#     chatInput = input("请输入内容：")
#     if chatInput == 'exit':
#         print('退出')
#         break
#     print('你说：',chatInput)
#     answer = gemini.chat(chatInput=chatInput)
#     print("🤖回复：", answer)

# deepSeek = DeepSeek(instruction='请模拟真人聊天，不要太多说明和反问，尽量自然，不要reasoning_content内容，直接回复就好',
#                     chatModel=DEEPSEEK_CHAT_MODEL.PRO)
#
# while True:
#     chatInput = input("请输入内容：")
#     if chatInput == 'exit':
#         print('退出')
#         break
#     print('你说：',chatInput)
#     answer,isOK = deepSeek.chat(chatInput=chatInput)
#     if isOK:
#         print("🤖回复：", answer)


# 'HaiXeHiSaDai'
# accountsServices = AccountsServices()
# listAccount:list[Account] = accountsServices.get(Account(userName='TiuReMeKou'))
# if listAccount is None or len(listAccount) <= 0:
#     print('没有找到账号')

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from Business.models.summary7 import SummaryItem, Operating
from Utils.tools import Tools
from Utils.webSite737 import WebSite737
from Utils.webSite7 import WebSite7
from Utils.sheets7 import Sheets7
import datetime
import time
from Utils.googleSheets import GoogleSheets
from Utils.sheets737 import Sheets737
from paths import getProjectPath
from datetime import datetime, timedelta


# encrypted_data = "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"
# a = Tools.decryptAES(encrypted_data,'xYgRhi0MMcS*iL^q')
# print(a)
# a = Tools.dateToExcelSerial('2025-07-27')
# print(a)
# b = Tools.convertTimeToTimezone('America/Sao_Paulo')
# print(str(b.date()))

# webSite7 = WebSite7()
# c = webSite7.getOperating('2025-06-07')
# print(c)




# def date_range(start_date, end_date):
#     """
#     生成两个日期之间的每一天
#
#     参数:
#         start_date (str/datetime): 开始日期，格式为 'YYYY-MM-DD' 或 datetime 对象
#         end_date (str/datetime): 结束日期，格式为 'YYYY-MM-DD' 或 datetime 对象
#
#     返回:
#         generator: 生成从开始日期到结束日期的每一天的 datetime 对象
#     """
#     # 如果输入是字符串，转换为 datetime 对象
#     if isinstance(start_date, str):
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#     if isinstance(end_date, str):
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
#
#     # 确保开始日期不大于结束日期
#     if start_date > end_date:
#         raise ValueError("开始日期不能晚于结束日期")
#
#     # 计算日期范围
#     current_date = start_date
#     while current_date <= end_date:
#         yield current_date
#         current_date += timedelta(days=1)


# if __name__ == "__main__":
#     # 示例1：使用字符串日期
#     sheets7 = Sheets7()
#     webSite7 = WebSite7()
#     for single_date in Tools.date_range('2025-06-02', '2025-08-02'):
#         dateStr = single_date.strftime('%Y-%m-%d')
#         print(dateStr)
#         summaryList = webSite7.getSummary(dateStr)
#         operating = webSite7.getOperating(dateStr)
#         if summaryList:
#             sheets7.append(summaryList, dateStr,operating.payCash,False)
#         print('done')

# if __name__ == "__main__":
#     sheets737 = Sheets737()
#     webSite737 = WebSite737()
#
#     summaryList = webSite737.getSummary(page=1,limit=1000)
#     lenList = len(summaryList)
#     indexRow = 4
#     for i in range(lenList-1,-1,-1):
#         summary = summaryList[i]
#         # sheets737.append(summary)
#         if not sheets737.update(summary,indexRow):
#             print('修改失败')
#             break
#
#         indexRow += 1
#         time.sleep(1)
#         print('done')

from datetime import date, timedelta

today = datetime.strptime('2025-01-01', "%Y-%m-%d").date()
print("今天:", today)

next_day = str(today + timedelta(days=1))
print("明天:", next_day)





