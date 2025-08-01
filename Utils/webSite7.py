import json

from requests import Session, Request

from Business.models.storage import Storage, STORAGE_TYPE
from Business.models.summary7 import SummaryItem, Operating
from Utils.tools import Tools


class WebSite7:
    def __init__(self):
        storage = Storage(storageType=STORAGE_TYPE.CONFIG)
        self.__token = storage.getStorage('tokenSete7')
        # self.__token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzaW5nIiwiYXVkIjoiIiwiaWF0IjoxNzU0MDM2NDk1LCJuYmYiOjE3NTQwMzY0OTUsImV4cCI6MTc1NDExNTY5NSwiZGF0YSI6eyJNYXN0ZXJJRCI6IjI2MDIiLCJNYXN0ZXJPcmRlciI6IjE4IiwiQWNjb3VudHMiOiJ0YW5rIiwiUGFzc3dvcmQiOiJlMTBhZGMzOTQ5YmE1OWFiYmU1NmUwNTdmMjBmODgzZSIsIkxhc3RMb2dpbklQIjoiMTI3LjAuMC4xIiwiTGFzdExvZ2luRGF0ZSI6IjIwMjUtMDctMzEgMDg6MjA6NDAuMDAwIiwiTG9naW5UaW1lcyI6IjkiLCJOaWNrTmFtZSI6Ilx1N2JhMVx1NzQwNlx1NTQ1OCIsIk51bGxpdHkiOiIwIiwiU2NvcmUiOiIwIiwiTWVkYWwiOiIwIiwiQ2hhbm5lbElEIjoiMCIsIkdvb2dsZVNlY3JldCI6Ik1BVVpZSVhWTDZRVktJSDMiLCJDaGFubmVsR3JvdXBJRCI6IjAiLCJEYXRhSURzIjoiIiwiSXNFeHBvcnQiOiIwIiwibWFzdGVyX29yZGVyIjp7Ik1hc3Rlck9yZGVySUQiOiIxOCIsIlJvbGVOYW1lIjoiXHU3NmQ4XHU1M2UzXHU4ZmQwXHU4NDI1ICAgICAgICAgICAgICAgICAgICAgICAgIiwiTWVudXNJRCI6IjEsMiwzLDQsNSw0NSw2LDc2LDksMTAsNjEsNzcsNDgsOTQsMTA4LDEwOSwxMTAsMTEyLDEyLDExNCwxMzEsMTMyLDEzMywxMzQsMTI0LDExMSw5NSwxMTMsODgsODksMTAyLDg1LDg2LDg3LDk3LDk5LDEwMCwxMDEsMTA0LDEwNSwxMzcsMTM4LDEzOSwxNDAsMjEsNTAsMjQsODIsMjksMzAsMzYsMTI5LDMxLDkwLDM1LDM3LDUzLDU0LDU1LDEyOCwxMzUsMTQ4LDk2LDMzLDEwNywxMzAsMTUsMTYsMzQsODMsMzgsMTksMTA2LDYzLDY0LDY1LDY2LDY3LDY4LDY5LDcwLDcxLDcyLDczLDc0LDc1LDU2LDU4LDU5LDc4LDc5LDgwLDgxLDExNSwxMTYsMTE3LDExOCwxMTksMTIwLDEyMSwxMjIsMTM2IiwiSXNEZWwiOiIwIn19fQ.OH3eTh1QuM0IK5DVuZX6PB777x_a30obfPWmHzGoqEQ'

    def getSummary(self, dateStr:str)-> list[SummaryItem] | None:
        if self.__token is None:
            return None

        dateID = Tools.dateToExcelSerial(dateStr)

        url = f'https://newplatform.mygamesete7.com/api/client/plat/query-send-score-by-day-stat?channelID=0&channelGroupID=0&dateID={dateID}'

        session = Session()
        request = Request('GET', url).prepare()
        request.headers['Access-Token'] = self.__token
        request.headers['X-Requested-With'] = 'XMLHttpRequest'
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        if request.headers.get('Content-Length'):
            del request.headers['Content-Length']

        try:
            response = session.send(request)
            result: list[SummaryItem] = []
            if response.status_code == 200:
                jsonObj = json.loads(response.text)
                if jsonObj.get('isSuccess'):
                    data:list=jsonObj.get('result').get('data')
                    if data:
                        for sub in data:
                            result.append(SummaryItem(**sub))
                else:
                    print(jsonObj.get('msg'))
            return result
        except Exception as e:
            print(e)

        return []

    def getOperating(self, dateStr:str)-> Operating | None:
        if self.__token is None:
            return None

        dateID = Tools.dateToExcelSerial(dateStr)

        url = f'https://newplatform.mygamesete7.com/api/client/plat/query-op-daily-stat?channelID=0&channelGroupID=0&startDateID={dateID}&endDateID={dateID}'

        session = Session()
        request = Request('GET', url).prepare()
        request.headers['Access-Token'] = self.__token
        request.headers['X-Requested-With'] = 'XMLHttpRequest'
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        if request.headers.get('Content-Length'):
            del request.headers['Content-Length']

        try:
            response = session.send(request)
            result: Operating = None
            if response.status_code == 200:
                jsonObj = json.loads(response.text)
                if jsonObj.get('isSuccess'):
                    data:list=jsonObj.get('result').get('data')
                    if data:
                        result = Operating.from_dict(data[0])
                else:
                    print(jsonObj.get('msg'))
            return result
        except Exception as e:
            print(e)

        return None

