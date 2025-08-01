
import base64
import re

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad,pad
from datetime import datetime, timedelta
import pytz

class Tools:
    def __init__(self):
        pass

    @staticmethod
    def decryptAES(e, keyStr):
        """
            使用原始密钥字符串（UTF-8）解密 AES-CBC

            参数:
                e (str): Base64 编码的密文
                key_str (str): 原始密钥（如 "xYgRhi0MMcS*iL^q"）
            返回:
                str: 解密后的明文
            """
        try:
            # 1. 将原始密钥转为字节（UTF-8 编码）
            key = keyStr.encode("utf-8")

            # 2. 解码 Base64 密文
            ciphertext = base64.b64decode(e)

            # 3. 使用密钥作为 IV（与 JavaScript 逻辑一致）
            iv = key[:16]  # AES-CBC 需要 16 字节 IV

            # 4. 解密
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

            # 5. 返回 UTF-8 明文
            return decrypted.decode("utf-8")
        except Exception as e:
            raise ValueError("解密失败，请检查密钥或密文") from e

    @staticmethod
    def encryptAES(plaintext: str, keyStr: str) -> str:
        """
        AES-CBC 加密（与 JavaScript 的 CryptoJS 行为一致）

        :param plaintext: 待加密的明文
        :param keyStr: Base64 编码的密钥（与 JavaScript 的 `window.base64Mode()` 返回值一致）
        :return: Base64 编码的密文
        """
        try:
            # 1. 将原始密钥和明文转为字节（UTF-8 编码）
            key_bytes = keyStr.encode('utf-8')  # 密钥直接按 UTF-8 编码
            plaintext_bytes = plaintext.encode('utf-8')
            iv = key_bytes  # IV = 密钥（与 JavaScript 代码一致）

            # 2. 检查密钥长度（AES-128/192/256 需要 16/24/32 字节）
            if len(key_bytes) not in [16, 24, 32]:
                raise ValueError("密钥长度必须是 16、24 或 32 字节（AES-128/192/256）")

            # 3. 使用 AES-CBC + PKCS7 填充加密
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(pad(plaintext_bytes, AES.block_size))

            # 4. 返回 Base64 编码的密文
            return base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            raise ValueError("解密失败，请检查密钥或密文") from e

    @staticmethod
    def dateToExcelSerial(dateStr):
        """
        将日期字符串（格式：YYYY-MM-DD）转换为 Excel 1900 日期系统的序列值。
        注意：Excel 错误地将 1900 年视为闰年，因此 1900-02-29 是有效日期。
        """
        # Excel 的基准日期是 1899-12-31（序列值 0），但 1900-01-01 是序列值 1
        excel_epoch = datetime(1899, 12, 31)
        target_date = datetime.strptime(dateStr, "%Y-%m-%d")

        delta = target_date - excel_epoch
        serial = delta.days

        # Excel 错误地认为 1900 是闰年，所以从 1900-03-01 开始需要减去 1 天
        if target_date >= datetime(1900, 3, 1):
            serial -= 1

        return serial

    @staticmethod
    def excelSerialToDate(serial):
        """
        将 Excel 1900 日期系统的序列值转换为日期字符串（格式：YYYY-MM-DD）。
        """
        # Excel 的基准日期是 1899-12-31（序列值 0），但 1900-01-01 是序列值 1
        excel_epoch = datetime(1899, 12, 31)

        # 处理 Excel 的 1900 年闰日错误
        if serial >= 60:
            serial += 1  # 补偿 Excel 的 1900-02-29 错误

        target_date = excel_epoch + timedelta(days=serial)
        return target_date.strftime("%Y-%m-%d")

    @staticmethod
    def convertTimeToTimezone(target_timezone, source_timezone=None, time_obj=None):
        """
        使用 zoneinfo 的时区转换函数 (Python 3.9+)
        """
        if time_obj is None:
            # 默认使用本地时区（如果未提供 source_timezone）
            if source_timezone is None:
                time_obj = datetime.now(pytz.UTC)  # 默认用 UTC，避免 naive datetime
            else:
                time_obj = datetime.now(pytz.timezone(source_timezone))

            # 如果 time_obj 仍然是 naive，尝试用 source_timezone 附加时区
        if time_obj.tzinfo is None:
            if source_timezone is None:
                raise ValueError("time_obj 是 naive datetime，且未提供 source_timezone")
            time_obj = pytz.timezone(source_timezone).localize(time_obj)

            # 转换为目标时区
        target_tz = pytz.timezone(target_timezone)
        converted_time = time_obj.astimezone(target_tz)

        return converted_time

    @staticmethod
    def excelColumnToNumber(column):
        num = 0
        for c in column:
            num = num * 26 + (ord(c.upper()) - ord('A') + 1)
        return num

    @staticmethod
    def date_range(start_date, end_date):
        """
        生成两个日期之间的每一天

        参数:
            start_date (str/datetime): 开始日期，格式为 'YYYY-MM-DD' 或 datetime 对象
            end_date (str/datetime): 结束日期，格式为 'YYYY-MM-DD' 或 datetime 对象

        返回:
            generator: 生成从开始日期到结束日期的每一天的 datetime 对象
        """
        # 如果输入是字符串，转换为 datetime 对象
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # 确保开始日期不大于结束日期
        if start_date > end_date:
            raise ValueError("开始日期不能晚于结束日期")

        # 计算日期范围
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += timedelta(days=1)

    @staticmethod
    def normalize_date(date_str):
        # 定义多种可能的日期格式
        date_formats = [
            "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y",  # 基础格式
            "%Y年%m月%d日", "%Y/%m/%d",  # 中文日期格式
            "%Y-%m-%d %A", "%A, %Y-%m-%d",  # 英文星期格式
            "%Y年%m月%d日%a", "%Y年%m月%d日%A"  # 中文星期格式
        ]

        # 尝试用各种格式解析日期
        for fmt in date_formats:
            try:
                # 处理包含星期几的情况(中英文)
                cleaned_date_str = re.sub(r'[星期周]+[一二三四五六七日天]|[,，]', '', date_str)
                cleaned_date_str = re.sub(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', '',
                                          cleaned_date_str, flags=re.IGNORECASE)
                cleaned_date_str = re.sub(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)', '', cleaned_date_str, flags=re.IGNORECASE)

                # 尝试解析
                dt = datetime.strptime(cleaned_date_str.strip(), fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # 如果所有格式都尝试失败，返回原始字符串或抛出异常
        return date_str  # 或者 raise ValueError(f"无法解析日期: {date_str}")

    @staticmethod
    def date_diff(date_str1, date_str2, date_format="%Y-%m-%d"):
        """
        计算两个日期字符串之间的天数差

        参数:
            date_str1: 第一个日期字符串
            date_str2: 第二个日期字符串
            date_format: 日期格式(默认为"%Y-%m-%d")

        返回:
            两个日期之间的天数差(date1 - date2)
        """
        # 将字符串转换为日期对象
        date1 = datetime.strptime(date_str1, date_format)
        date2 = datetime.strptime(date_str2, date_format)

        # 计算差值
        delta = date1 - date2

        return delta.days

