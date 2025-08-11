import json
import logging
import time

from requests import Session, Request

from models.storage import Storage, STORAGE_TYPE
from Utils.tools import Tools
from urllib.parse import quote
from models.summary737 import Summary

class WebSite737:
    def __init__(self):
        storage = Storage(storageType=STORAGE_TYPE.CONFIG)
        self.__token = storage.getStorage('token737')
        self.__keyAES = 'xYgRhi0MMcS*iL^q'

    def getSummary(self, page:int=1, limit:int=1)-> list[Summary]|None:
        if self.__token is None:
            return None

        # 获取时间戳
        timestamp = int(time.time() * 1000)
        params = f'page={page}&limit={limit}&aid=5118&s={self.__token}&a_type=4&dn=30050&abbyyqq={timestamp}'
        paramAES = Tools.encryptAES(params,self.__keyAES)
        # url编码
        encodedParam = quote(paramAES)

        url = f'https://capi31.nomaycms.com/cms/platform/dailySummary?param={encodedParam}'

        session = Session()
        request = Request('GET', url).prepare()
        request.headers['X-Token'] = self.__token
        request.headers['Origin'] = 'https://737game.topcms.org'
        request.headers['Referer'] = 'https://737game.topcms.org'
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        if request.headers.get('Content-Length'):
            del request.headers['Content-Length']

        try:

            response = session.send(request)
            result:list[Summary] = []
            if response.status_code == 200:
                jsonObj = json.loads(response.text)
                if jsonObj.get('result') == '0':
                    data = jsonObj.get('data')
                    dataRealStr = Tools.decryptAES(data,self.__keyAES)
                    dataReal:dict = json.loads(dataRealStr)
                    dailySummarys:list = dataReal.get('dailySummarys')
                    if dailySummarys:
                        for sub in dailySummarys:
                            summary = Summary.from_dict(sub)
                            result.append(summary)
                else:
                    logging.error(jsonObj.get('msg'))
            return result
        except Exception as e:
            logging.error(e)

        return []

