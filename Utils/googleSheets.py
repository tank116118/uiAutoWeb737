import re

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, date, timedelta
from typing import Union, List, Optional
from googleapiclient.errors import HttpError


class GoogleSheets:
    def __init__(self, credentials_file: str, spreadsheet_id: str = None):
        """
        初始化 Google Sheets API 客户端

        :param credentials_file: 服务账户的 JSON 凭证文件路径
        :param spreadsheet_id: 可选，默认操作的电子表格 ID
        """
        # autobotchats-4c5cfe7df47e.json
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.service = self._authenticate()

    def _authenticate(self):
        """认证并创建服务"""
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(self.credentials_file, scopes=scopes)
        return build('sheets', 'v4', credentials=creds)

    def set_spreadsheet(self, spreadsheet_id: str):
        """设置默认操作的电子表格 ID"""
        self.spreadsheet_id = spreadsheet_id

    @staticmethod
    def date_to_serial(date_obj):
        """将Python日期转换为Google Sheets序列化日期"""
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
        epoch = datetime(1899, 12, 30)
        delta = date_obj - epoch
        return float(delta.days) + (float(delta.seconds) / 86400)

    def get_sheet_names(self, spreadsheet_id: str = None) -> List[str]:
        """
        获取电子表格中所有工作表的名称

        :param spreadsheet_id: 电子表格 ID，如果未提供则使用默认值
        :return: 工作表名称列表
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            return [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]
        except HttpError as error:
            print(f"发生错误: {error}")
            return []

    def read_range(
            self,
            range_name: str,
            spreadsheet_id: str = None,
            major_dimension: str = "ROWS"
    ) -> List[List[str]]:
        """
        读取指定范围的数据

        :param range_name: 范围名称，例如 'Sheet1!A1:C10'
        :param spreadsheet_id: 电子表格 ID，如果未提供则使用默认值
        :param major_dimension: 主要维度，"ROWS" 或 "COLUMNS"
        :return: 二维数据列表
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                majorDimension=major_dimension
            ).execute()
            return result.get('values', [])
        except HttpError as error:
            print(f"发生错误: {error}")
            return []

    def write_range(
            self,
            range_name: str,
            values: List[List[Union[str, int, float]]],
            spreadsheet_id: str = None,
            value_input_option: str = "USER_ENTERED"
    ) -> bool:
        """
        写入数据到指定范围

        :param range_name: 范围名称
        :param values: 要写入的二维数据
        :param spreadsheet_id: 电子表格 ID
        :param value_input_option: "RAW" 或 "USER_ENTERED"
        :return: 是否成功
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            body = {'values': values}
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            return True
        except HttpError as error:
            print(f"发生错误: {error}")
            return False

    def append_rows(
            self,
            range_name: str,
            values: List[List[Union[str, int, float]]],
            spreadsheet_id: str = None,
            value_input_option: str = "USER_ENTERED"
    ) -> bool:
        """
        追加行到表格末尾

        :param range_name: 范围名称，例如 'Sheet1'
        :param values: 要追加的二维数据
        :param spreadsheet_id: 电子表格 ID
        :param value_input_option: "RAW" 或 "USER_ENTERED"
        :return: 是否成功
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            body = {'values': values}
            self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()
            return True
        except HttpError as error:
            print(f"发生错误: {error}")
            return False

    def create_sheet(
            self,
            title: str,
            spreadsheet_id: str = None,
            rows: int = 1000,
            columns: int = 26
    ) -> bool:
        """
        创建新工作表

        :param title: 工作表标题
        :param spreadsheet_id: 电子表格 ID
        :param rows: 初始行数
        :param columns: 初始列数
        :return: 是否成功
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            body = {
                "requests": [{
                    "addSheet": {
                        "properties": {
                            "title": title,
                            "gridProperties": {
                                "rowCount": rows,
                                "columnCount": columns
                            }
                        }
                    }
                }]
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()
            return True
        except HttpError as error:
            print(f"发生错误: {error}")
            return False

    def clear_range(
            self,
            range_name: str,
            spreadsheet_id: str = None
    ) -> bool:
        """
        清除指定范围的内容

        :param range_name: 范围名称
        :param spreadsheet_id: 电子表格 ID
        :return: 是否成功
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                body={}
            ).execute()
            return True
        except HttpError as error:
            print(f"发生错误: {error}")
            return False

    def get_cell_formula(
            self,
            range_name: str,
            spreadsheet_id: str = None
    ) -> Optional[str]:
        """
        获取单元格的公式

        :param range_name: 范围名称，如 'Sheet1!A1'
        :param spreadsheet_id: 电子表格 ID
        :return: 公式字符串，或 None
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                ranges=[range_name],
                includeGridData=True
            ).execute()

            sheet_data = result['sheets'][0]['data'][0]
            if 'rowData' in sheet_data and sheet_data['rowData']:
                cell_data = sheet_data['rowData'][0]['values'][0]
                if 'userEnteredValue' in cell_data and 'formulaValue' in cell_data['userEnteredValue']:
                    return cell_data['userEnteredValue']['formulaValue']
            return None
        except HttpError as error:
            print(f"发生错误: {error}")
            return None

    def date_exists_in_column(
            self,
            sheet_name: str,
            column: str,
            target_date: Union[str, date, datetime],
            spreadsheet_id: str = None,
            date_formats: List[str] = None,
            match_time: bool = False,
            weekday_aware: bool = True  # 新增参数，是否识别带星期的格式
    ) -> bool:
        """
        增强版日期检查，支持带星期的日期格式

        参数:
            weekday_aware: 是否尝试解析带星期的日期格式
            其他参数同原函数
        """
        # 设置默认日期格式（包含带星期的格式）
        if date_formats is None:
            date_formats = [
                "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y",  # 基础格式
                "%Y年%m月%d日", "%Y/%m/%d",  # 中文日期格式
                "%Y-%m-%d %A", "%A, %Y-%m-%d",  # 英文星期格式
                "%Y年%m月%d日%a", "%Y年%m月%d日%A"  # 中文星期格式
            ]

        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 标准化目标日期
        target_dt = self._normalize_date(target_date, date_formats)
        if target_dt is None:
            raise ValueError("无法解析目标日期格式")

        # 构造范围字符串
        range_name = f"{sheet_name}!{column}:{column}"

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                majorDimension="COLUMNS"
            ).execute()

            values = result.get('values', [[]])
            column_data = values[0] if values else []

            for cell_value in column_data:
                if not cell_value or not str(cell_value).strip():
                    continue

                cell_str = str(cell_value).strip()
                cell_dt = None

                # 尝试解析带星期的格式
                if weekday_aware:
                    cell_dt = self._parse_date_with_weekday(cell_str, target_dt)

                # 如果带星期解析失败，尝试常规解析
                if cell_dt is None:
                    cell_dt = self._parse_cell_date(cell_str, date_formats)

                if cell_dt is None:
                    continue

                # 比较日期
                if match_time and isinstance(target_dt, datetime) and isinstance(cell_dt, datetime):
                    if cell_dt == target_dt:
                        return True
                elif not match_time and cell_dt.date() == target_dt.date():
                    return True

            return False

        except HttpError as error:
            print(f"查询日期时发生错误: {error}")
            return False

    def _parse_date_with_weekday(
            self,
            cell_str: str,
            target_dt: Union[date, datetime]
    ) -> Optional[Union[date, datetime]]:
        """
        专门解析带星期的日期格式
        返回解析出的日期对象，或None(如果不是带星期的格式)
        """
        # 移除星期部分后尝试解析
        cleaned_str = re.sub(r'[星期周]\S+$', '', cell_str)  # 中文星期
        cleaned_str = re.sub(r'\b[A-Za-z]+\b$', '', cleaned_str)  # 英文星期
        cleaned_str = cleaned_str.strip()

        if cleaned_str != cell_str:  # 如果确实去除了星期部分
            try:
                # 尝试常见日期格式
                for fmt in ["%Y年%m月%d日", "%Y-%m-%d", "%m/%d/%Y"]:
                    try:
                        parsed_dt = datetime.strptime(cleaned_str, fmt)
                        # 验证星期是否正确
                        if self._weekday_matches(cell_str, parsed_dt):
                            return parsed_dt
                    except ValueError:
                        continue
            except:
                pass
        return None

    def _weekday_matches(
            self,
            original_str: str,
            parsed_dt: datetime
    ) -> bool:
        """验证日期字符串中的星期部分是否与实际日期匹配"""
        # 检查中文星期 (星期三/周三)
        cn_weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        weekday_num = parsed_dt.weekday()  # 0=周一,6=周日
        for pattern in [
            f'星期[{cn_weekdays[weekday_num]}]',
            f'周[{cn_weekdays[weekday_num]}]'
        ]:
            if re.search(pattern, original_str):
                return True

        # 检查英文星期
        en_weekday = parsed_dt.strftime("%A")
        en_abbr = parsed_dt.strftime("%a")
        return en_weekday in original_str or en_abbr in original_str

    def _normalize_date(
            self,
            date_value: Union[str, date, datetime],
            date_formats: List[str]
    ) -> Optional[Union[date, datetime]]:
        """将输入日期标准化为date或datetime对象"""
        if isinstance(date_value, date):
            return date_value
        elif isinstance(date_value, datetime):
            return date_value

        # 尝试用每种格式解析字符串
        for fmt in date_formats:
            try:
                return datetime.strptime(date_value, fmt)
            except ValueError:
                continue
        return None

    def _parse_cell_date(
            self,
            cell_value: str,
            date_formats: List[str]
    ) -> Optional[Union[date, datetime]]:
        """解析单元格中的日期值"""
        # 先尝试直接解析为datetime(处理Google Sheets的序列化日期)
        try:
            # Google Sheets有时会将日期存储为序列数字
            serial_number = float(cell_value)
            return datetime(1899, 12, 30) + timedelta(days=serial_number)
        except (ValueError, OverflowError):
            pass

        # 尝试用提供的格式解析
        for fmt in date_formats:
            try:
                return datetime.strptime(cell_value, fmt)
            except ValueError:
                continue

        return None

    def get_data_row_count(
            self,
            sheet_name: str,
            spreadsheet_id: str = None,
            column: str = "A"  # 默认检查A列
    ) -> int:
        """
        获取指定工作表中包含数据的行数

        :param sheet_name: 工作表名称(不带'!'符号)
        :param spreadsheet_id: 电子表格ID，如果未提供则使用默认值
        :param column: 用于检查的列(默认为A列)
        :return: 包含数据的行数(从1开始计数)，出错返回0
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 构造范围字符串(如 'Sheet1!A:A')
        range_name = f"{sheet_name}!{column}:{column}"

        try:
            # 获取该列所有数据
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                majorDimension="COLUMNS"
            ).execute()

            values = result.get('values', [])

            if not values:
                return 0

            # 获取第一列(因为我们只查询了一列)
            column_data = values[0]

            # 计算非空单元格数量
            # 注意: Google Sheets API会跳过末尾的空行
            return len(column_data)

        except HttpError as error:
            print(f"获取行数时发生错误: {error}")
            return 0