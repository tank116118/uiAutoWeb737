import json

from requests import Session, Request

from Business.models.storage import Storage, STORAGE_TYPE
from Business.models.summary7 import SummaryItem, Operating
from Utils.tools import Tools


class WebSite7:
    def __init__(self):
        storage = Storage(storageType=STORAGE_TYPE.CONFIG)
        self.__token = storage.getStorage('tokenSete7')

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

