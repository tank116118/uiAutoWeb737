import re

from PyQt5.QtCore import QObject, QMetaObject, QMetaMethod, QByteArray
from PyQt5.QtWidgets import QComboBox


class ObjTools:
    @staticmethod
    def objToDict(obj):
        if isinstance(obj, dict):
            return obj

        def toDict(objSub):
            if objSub is None:
                return None

            ret = {}
            for k in dir(objSub):
                # 排除私有成员
                if k.startswith('__'):
                    continue
                attr = getattr(objSub, k)
                # 排除方法
                if callable(attr):
                    continue

                if attr is not None:
                    if ObjTools.isObjectType(attr):
                        attr = ObjTools.objToDict(attr)
                    elif isinstance(attr, list) and len(attr) > 0:
                        temp = []
                        for sub in attr:
                            if sub is not None and ObjTools.isObjectType(sub):
                                sub = ObjTools.objToDict(sub)
                                temp.append(sub)
                            else:
                                temp.append(sub)
                        attr = temp

                ret[k] = attr
            return ret

        if isinstance(obj, list):
            result = []
            for objReal in obj:
                result.append(toDict(objReal))
            return result
        else:
            return toDict(obj)

    @staticmethod
    def dictToObj(dictObj, objClass, childObjClass: dict|None = None):
        if dictObj is None or objClass is None:
            return None

        def toObj(dictObjToObj, ObjClassSub, childObjClassSub: any = None):
            obj = ObjClassSub()
            for k in dir(obj):
                if k in dictObjToObj:
                    value = dictObjToObj.get(k)
                    if childObjClassSub and k in childObjClassSub:
                        ChildClass = childObjClassSub.get(k)
                        childValue = ObjTools.dictToObj(value, ChildClass)
                        setattr(obj, k, childValue)
                    else:
                        setattr(obj, k, value)

            return obj

        if isinstance(dictObj, list):
            objTemp = []
            for dictObjSub in dictObj:
                objTemp.append(toObj(dictObjSub, objClass, childObjClass))
            return objTemp
        else:
            return toObj(dictObj, objClass, childObjClass)

    @staticmethod
    def isObjectType(obj) -> bool:
        if obj is None:
            return False

        if (isinstance(obj, str)
                or isinstance(obj, float)
                or isinstance(obj, int)
                or isinstance(obj, bool)
                or isinstance(obj, list)
                or isinstance(obj, dict)
                or isinstance(obj, tuple)
                or isinstance(obj, set)):
            return False

        return True

    @staticmethod
    def isSignalConnected(obj: QObject, name: str):
        """判断信号是否连接
        :param obj: 对象
        :param name: 信号名，如 clicked()
        """
        metaObj: QMetaObject = obj.metaObject()
        methodCount = metaObj.methodCount()
        method: QMetaMethod|None = None
        for i in range(methodCount):
            methodSub: QMetaMethod = metaObj.method(i)
            methodNameSub: QByteArray = methodSub.name()
            if len(re.findall(name, str(methodNameSub))) == 1:
                method = methodSub
                break

        if method is None:
            return False
        isSignalConnected = obj.isSignalConnected(method)
        return isSignalConnected

    @staticmethod
    def clearComboBox(comboBox: QComboBox):
        if comboBox is None:
            return
        count = comboBox.count()
        for i in range(count - 1, -1, -1):
            comboBox.removeItem(i)
