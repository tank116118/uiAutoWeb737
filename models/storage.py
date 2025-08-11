import json
import os
from enum import Enum

from paths import getProjectPath


class STORAGE_TYPE(Enum):
    STORAGE = "/Static/storage.sto"
    CONFIG = "/Static/app.conf"


class Storage:
    def __init__(self, storageType: STORAGE_TYPE = STORAGE_TYPE.STORAGE):
        self.path = storageType.value
        self.jsonObj = self.__readFile()

    def __readFile(self) -> dict|None:
        try:
            cur_path = getProjectPath() + self.path
            cur_path = cur_path.replace("\\", '/')
            cur_path = cur_path.replace("//", '/')
            if not os.path.exists(cur_path):
                return None

            with open(cur_path, encoding='utf-8') as f:
                lines = f.readlines()

            strStorage = ''
            if lines and len(lines) > 0:
                for lineSub in lines:
                    strStorage += lineSub

            strConf = strStorage.strip()
            strConf = strConf.replace('\n', '')
            strConf = strConf.replace('\'', '"')
            if len(strConf) > 0:
                jsonObj = json.loads(strConf)
            else:
                jsonObj = {}

            return jsonObj
        except Exception as e:
            print(e)
            return None

    def __saveFile(self, content: str)->bool:
        try:
            if content is None:
                return False
            # 写入
            cur_path = getProjectPath()
            with open(cur_path + self.path, encoding='utf-8', mode='w+') as f:
                f.write(content)

            return True
        except Exception as e:
            print(e)
            return False

    def setStorage(self, key: str, value):
        if key is None or len(key) <= 0 or value is None:
            return
        if self.jsonObj is None:
            self.jsonObj = {}

        self.jsonObj[key] = value
        strSave = json.dumps(self.jsonObj)
        self.__saveFile(strSave)

    def getStorage(self, key: str) -> any:
        if self.jsonObj is None or key is None or len(key) <= 0:
            return None
        return self.jsonObj.get(key)
