import re

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, date, timedelta
from typing import Union, List, Optional, Dict
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
            major_dimension: str = "ROWS",
            include_formulas: bool = False,
            value_render_option: str = "FORMATTED_VALUE",
            unformatted: bool = False
    ) -> Union[List[List[str]], Dict[str, Union[List[List[str]], List[List[str]]]]]:
        """
                读取指定范围的数据，支持获取公式

                参数:
                    range_name: 范围名称(如 'Sheet1!A1:C10')
                    spreadsheet_id: 电子表格ID(可选)
                    major_dimension:
                        "ROWS" - 按行组织数据(默认)
                        "COLUMNS" - 按列组织数据
                    include_formulas: 是否同时返回公式(默认False)
                    value_render_option:
                        "FORMATTED_VALUE" - 返回格式化字符串(默认)
                        "UNFORMATTED_VALUE" - 返回原始值
                        "FORMULA" - 返回公式
                    unformatted: 是否返回未格式化的数字/日期(覆盖value_render_option)

                返回:
                    如果 include_formulas=False: 二维数据列表
                    如果 include_formulas=True: 字典 {
                        "values": 二维值列表,
                        "formulas": 二维公式列表(空字符串表示无公式)
                    }
                """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 处理未格式化请求
        if unformatted:
            value_render_option = "UNFORMATTED_VALUE"

        try:
            # 基本数据请求
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                majorDimension=major_dimension,
                valueRenderOption=value_render_option
            ).execute()

            values = result.get('values', [])

            # 如果不需公式，直接返回
            if not include_formulas:
                return values

            # 如果需要公式，发起第二个请求获取公式
            formula_result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                majorDimension=major_dimension,
                valueRenderOption="FORMULA"
            ).execute()

            formulas = formula_result.get('values', [])

            # 确保两个结果维度相同
            if len(values) != len(formulas):
                print("警告: 值和公式结果维度不匹配")
                formulas = [[""] * len(row) for row in values]
            else:
                for i in range(len(values)):
                    if len(values[i]) != len(formulas[i]):
                        formulas[i] = formulas[i] + [""] * (len(values[i]) - len(formulas[i]))

            return {
                "values": values,
                "formulas": formulas
            }

        except HttpError as error:
            print(f"读取范围时发生错误: {error}")
            return [] if not include_formulas else {"values": [], "formulas": []}

    def read_range_with_metadata(
            self,
            range_name: str,
            spreadsheet_id: str = None
    ) -> List[List[Dict[str, Union[str, dict]]]]:
        """
                读取范围数据及完整元数据(包括值、公式、格式等)

                返回:
                    二维字典列表，每个单元格包含:
                    {
                        "value": 显示值,
                        "formula": 公式(若无则为None),
                        "format": 格式字典,
                        "note": 单元格注释
                    }
                """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id

        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                ranges=[range_name],
                includeGridData=True,
                fields="sheets(data(rowData(values(effectiveValue,formattedValue,userEnteredValue,userEnteredFormat,note)))"
            ).execute()

            sheet_data = result['sheets'][0]['data'][0]
            row_data = sheet_data.get('rowData', [])

            grid = []
            for row in row_data:
                row_cells = []
                for cell in row.get('values', []):
                    cell_info = {
                        "value": cell.get('formattedValue'),
                        "raw_value": cell.get('effectiveValue'),
                        "formula": cell.get('userEnteredValue', {}).get('formulaValue'),
                        "format": cell.get('userEnteredFormat', {}),
                        "note": cell.get('note')
                    }
                    row_cells.append(cell_info)
                grid.append(row_cells)

            return grid

        except HttpError as error:
            print(f"获取元数据时发生错误: {error}")
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

    def insert_column(
            self,
            sheet_name: str,
            column: Union[str, int],
            values: Optional[List[Union[str, int, float, bool]]] = None,
            spreadsheet_id: str = None,
            insert_position: str = "after",  # "before" 或 "after"
            inherit_from_before: bool = False,
            clear_content: bool = False
    ) -> bool:
        """
        在工作表中插入新列

        参数:
            sheet_name: 工作表名称
            column: 列字母(如"A")或列索引(1-based)，新列将插入到此列前/后
            values: 可选，要插入的数据列表
            spreadsheet_id: 可选，指定电子表格ID
            insert_position:
                "before" - 插入到指定列前
                "after" - 插入到指定列后(默认)
            inherit_from_before: 是否从左侧列继承格式(默认False)
            clear_content: 是否清空插入列的内容(默认False)

        返回:
            是否成功插入
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 获取工作表ID
        sheet_id = self._get_sheet_id(sheet_name, spreadsheet_id)
        if sheet_id is None:
            print(f"找不到工作表: {sheet_name}")
            return False

        # 转换列索引为数字
        if isinstance(column, str):
            column_index = self.letter_to_column_index(column)
        else:
            if column < 1:
                raise ValueError("列索引必须大于0")
            column_index = column

        # 调整插入位置
        if insert_position == "after":
            column_index += 1

        # 构造请求
        requests = [{
            "insertDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": column_index - 1,  # 0-based
                    "endIndex": column_index  # 插入一列
                },
                "inheritFromBefore": inherit_from_before
            }
        }]

        # 如果需要清空内容
        if clear_content:
            requests.append({
                "updateCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startColumnIndex": column_index - 1,
                        "endColumnIndex": column_index,
                        "dimension": "COLUMNS"
                    },
                    "fields": "userEnteredValue"
                }
            })

        try:
            # 执行插入列操作
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": requests}
            ).execute()

            # 如果有数据要写入
            if values:
                new_column_letter = self.column_index_to_letter(column_index)
                range_name = f"{sheet_name}!{new_column_letter}1:{new_column_letter}{len(values)}"

                self.service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="USER_ENTERED",
                    body={"values": [[v] for v in values]}  # 转换为二维数组
                ).execute()

            return True

        except HttpError as error:
            print(f"插入列时发生错误: {error}")
            return False

    def insert_columns(
            self,
            sheet_name: str,
            column: Union[str, int],
            num_columns: int = 1,
            spreadsheet_id: str = None,
            insert_position: str = "after",
            inherit_from_before: bool = False,
            clear_content: bool = False
    ) -> bool:
        """
        批量插入多列

        参数:
            num_columns: 要插入的列数
            其他参数同insert_column

        返回:
            是否成功插入
        """
        if num_columns < 1:
            raise ValueError("插入列数必须大于0")

        # 插入多列实际上是多次插入单列(因为插入位置会变化)
        success = True
        for i in range(num_columns):
            # 第一次插入在指定位置，后续插入在前一次插入的列后
            if i == 0:
                current_col = column
            else:
                if isinstance(column, str):
                    current_col = self.column_index_to_letter(
                        self.letter_to_column_index(column) + i
                    )
                else:
                    current_col = column + i

            if not self.insert_column(
                    sheet_name=sheet_name,
                    column=current_col,
                    spreadsheet_id=spreadsheet_id,
                    insert_position=insert_position,
                    inherit_from_before=inherit_from_before,
                    clear_content=clear_content
            ):
                success = False

        return success

    def _get_sheet_id(self, sheet_name: str, spreadsheet_id: str) -> Optional[int]:
        """获取工作表的ID"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                fields="sheets(properties(sheetId,title))"
            ).execute()

            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            return None
        except HttpError:
            return None

    def merge_cells(
            self,
            sheet_name: str,
            range_str: Optional[str] = None,
            start_row: Optional[int] = None,
            end_row: Optional[int] = None,
            start_col: Optional[Union[str, int]] = None,
            end_col: Optional[Union[str, int]] = None,
            spreadsheet_id: str = None,
            merge_type: str = "MERGE_ALL"  # "MERGE_ALL", "MERGE_COLUMNS", "MERGE_ROWS"
    ) -> bool:
        """
        合并指定范围的单元格

        参数:
            sheet_name: 工作表名称
            range_str: 范围字符串(如"A1:C3")，优先使用此参数
            start_row: 起始行号(1-based)
            end_row: 结束行号
            start_col: 起始列(字母或数字)
            end_col: 结束列
            spreadsheet_id: 可选，指定电子表格ID
            merge_type:
                "MERGE_ALL" - 合并所有单元格为一个(默认)
                "MERGE_COLUMNS" - 按列合并
                "MERGE_ROWS" - 按行合并

        返回:
            是否成功合并
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 获取工作表ID
        sheet_id = self._get_sheet_id(sheet_name, spreadsheet_id)
        if sheet_id is None:
            print(f"找不到工作表: {sheet_name}")
            return False

        # 处理范围参数
        if range_str:
            # 解析范围字符串
            range_parts = self._parse_range(range_str)
            start_row = range_parts["start_row"]
            end_row = range_parts["end_row"]
            start_col_idx = range_parts["start_col"]
            end_col_idx = range_parts["end_col"]
        else:
            # 验证手动指定的范围参数
            if None in (start_row, end_row, start_col, end_col):
                raise ValueError("必须提供range_str或完整的start/end行列参数")

            # 转换列格式
            if isinstance(start_col, str):
                start_col_idx = self.letter_to_column_index(start_col)
            else:
                start_col_idx = start_col

            if isinstance(end_col, str):
                end_col_idx = self.letter_to_column_index(end_col)
            else:
                end_col_idx = end_col

        # 构造合并请求
        merge_type_enum = {
            "MERGE_ALL": "MERGE_ALL",
            "MERGE_COLUMNS": "MERGE_COLUMNS",
            "MERGE_ROWS": "MERGE_ROWS"
        }.get(merge_type.upper(), "MERGE_ALL")

        request = {
            "mergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row - 1,  # 转换为0-based
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col_idx - 1,
                    "endColumnIndex": end_col_idx
                },
                "mergeType": merge_type_enum
            }
        }

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": [request]}
            ).execute()
            return True
        except HttpError as error:
            print(f"合并单元格时发生错误: {error}")
            return False

    def _parse_range(self, range_str: str) -> dict:
        """
        解析范围字符串(如"Sheet1!A1:C3"或"A1:C3")
        返回包含行列信息的字典
        """
        # 移除工作表名部分(如果有)
        if '!' in range_str:
            range_part = range_str.split('!')[1]
        else:
            range_part = range_str

        # 分割起始和结束位置
        if ':' in range_part:
            start_ref, end_ref = range_part.split(':')
        else:
            start_ref = end_ref = range_part

        # 解析起始位置
        start_col_str = ''.join(filter(str.isalpha, start_ref))
        start_row = int(''.join(filter(str.isdigit, start_ref)))
        start_col = self.letter_to_column_index(start_col_str)

        # 解析结束位置
        end_col_str = ''.join(filter(str.isalpha, end_ref))
        end_row = int(''.join(filter(str.isdigit, end_ref)))
        end_col = self.letter_to_column_index(end_col_str)

        return {
            "start_row": start_row,
            "end_row": end_row,
            "start_col": start_col,
            "end_col": end_col,
            "start_col_letter": start_col_str,
            "end_col_letter": end_col_str
        }

    def get_column_count(
            self,
            sheet_name: str,
            spreadsheet_id: str = None,
            include_empty: bool = False
    ) -> int:
        """
        获取指定工作表中的总列数

        参数:
            sheet_name: 工作表名称
            spreadsheet_id: 可选，指定电子表格ID
            include_empty: 是否包含空列(默认False，只计算有数据的列)

        返回:
            列数(整数)，出错返回0
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            # 获取工作表属性
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                ranges=[f"{sheet_name}"],
                includeGridData=include_empty,
                fields="sheets(properties(gridProperties(columnCount)))"
            ).execute()

            # 提取列数信息
            sheet_props = result.get('sheets', [{}])[0].get('properties', {})
            grid_props = sheet_props.get('gridProperties', {})
            return grid_props.get('columnCount', 0)

        except HttpError as error:
            print(f"获取列数时发生错误: {error}")
            return 0

    def get_used_column_count(
            self,
            sheet_name: str,
            spreadsheet_id: str = None
    ) -> int:
        """
        获取工作表中有数据的列数(基于内容)

        参数:
            sheet_name: 工作表名称
            spreadsheet_id: 可选，指定电子表格ID

        返回:
            有数据的列数(整数)
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        try:
            # 获取整个工作表的数据范围
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}",
                majorDimension="ROWS"
            ).execute()

            values = result.get('values', [])
            if not values:
                return 0

            # 返回第一行的列数(假设第一行代表完整列结构)
            return len(values[0])

        except HttpError as error:
            print(f"获取使用列数时发生错误: {error}")
            return 0

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

    def get_column_data(
            self,
            sheet_name: str,
            column: str,
            spreadsheet_id: str = None,
            skip_header: bool = False,
            skip_blanks: bool = True,
            value_render_option: str = "FORMATTED_VALUE",
            max_results: int = None
    ) -> Union[List[str], List[float], List[bool], List[List[Union[str, float, bool]]]]:
        """
        获取指定列的数据

        参数:
            sheet_name: 工作表名称
            column: 列字母(如"A")或列索引(如1)
            spreadsheet_id: 可选，指定电子表格ID
            skip_header: 是否跳过第一行(表头)
            skip_blanks: 是否跳过空单元格
            value_render_option:
                "FORMATTED_VALUE" - 返回显示值(默认)
                "UNFORMATTED_VALUE" - 返回原始值
                "FORMULA" - 返回公式
            max_results: 可选，限制返回结果数量

        返回:
            列数据列表，根据内容自动判断类型
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 转换列索引为字母(如果输入是数字)
        if isinstance(column, int):
            if column < 1:
                raise ValueError("列索引必须大于0")
            column = self.column_index_to_letter(column)

        range_name = f"{sheet_name}!{column}:{column}"

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                majorDimension="COLUMNS",  # 按列获取
                valueRenderOption=value_render_option
            ).execute()

            values = result.get('values', [[]])
            column_data = values[0] if values else []

            # 处理数据
            if skip_header and column_data:
                column_data = column_data[1:]

            if skip_blanks:
                column_data = [cell for cell in column_data if cell != '' and cell is not None]

            if max_results is not None and max_results > 0:
                column_data = column_data[:max_results]

            return column_data

        except HttpError as error:
            print(f"读取列数据时发生错误: {error}")
            return []

    def get_column_data_with_metadata(
            self,
            sheet_name: str,
            column: str,
            spreadsheet_id: str = None
    ) -> List[dict[str, Union[str, float, bool, dict]]]:
        """
        获取列数据及单元格元数据(包括格式、公式等)

        返回包含完整单元格信息的字典列表
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id

        # 转换列索引为字母
        if isinstance(column, int):
            column = self.column_index_to_letter(column)

        range_name = f"{sheet_name}!{column}:{column}"

        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                ranges=[range_name],
                includeGridData=True
            ).execute()

            sheet_data = result['sheets'][0]['data'][0]
            row_data = sheet_data.get('rowData', [])

            cells = []
            for row in row_data:
                if 'values' in row and row['values']:
                    cell_info = {
                        'value': row['values'][0].get('formattedValue'),
                        'raw_value': row['values'][0].get('effectiveValue'),
                        'formula': row['values'][0].get('userEnteredValue', {}).get('formulaValue'),
                        'format': row['values'][0].get('userEnteredFormat', {}),
                        'note': row['values'][0].get('note')
                    }
                    cells.append(cell_info)

            return cells

        except HttpError as error:
            print(f"获取列元数据时发生错误: {error}")
            return []

    def update_row(
            self,
            sheet_name: str,
            row_number: int,
            new_values: List[Union[str, int, float, bool]],
            spreadsheet_id: str = None,
            value_input_option: str = "USER_ENTERED",
            start_column: Union[str, int] = 1
    ) -> bool:
        """
        修改指定行的数据

        参数:
            sheet_name: 工作表名称
            row_number: 行号(1-based)
            new_values: 新值列表
            spreadsheet_id: 可选，指定电子表格ID
            value_input_option:
                "RAW" - 直接插入原始值
                "USER_ENTERED" - 像用户输入一样解释值(默认)
            start_column: 起始列(字母或数字，默认为1/A列)

        返回:
            是否成功更新
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            raise ValueError("未提供 spreadsheet_id")

        # 转换列索引为字母
        if isinstance(start_column, int):
            start_column = self.column_index_to_letter(start_column)

        # 构造范围(如 "Sheet1!A2:C2")
        range_name = f"{sheet_name}!{start_column}{row_number}:{self.column_index_to_letter(len(new_values[0]) + self.letter_to_column_index(start_column) - 1)}{row_number}"

        try:
            body = {
                "values": new_values  # 注意: 需要二维数组
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()

            print(f"更新了 {result.get('updatedCells')} 个单元格")
            return True

        except HttpError as error:
            print(f"更新行时发生错误: {error}")
            return False

    def update_row_by_filter(
            self,
            sheet_name: str,
            filter_column: Union[str, int],
            filter_value: Union[str, int, float, bool],
            new_values: List[Union[str, int, float, bool]],
            spreadsheet_id: str = None,
            value_input_option: str = "USER_ENTERED",
            start_column: Union[str, int] = 1,
            exact_match: bool = True
    ) -> bool:
        """
        根据条件查找并修改行数据

        参数:
            filter_column: 用于筛选的列(字母或数字)
            filter_value: 要匹配的值
            exact_match: 是否精确匹配(默认True)
            其他参数同update_row

        返回:
            是否成功更新
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id

        # 查找匹配的行
        row_num = self._find_row_by_value(
            sheet_name=sheet_name,
            column=filter_column,
            value=filter_value,
            spreadsheet_id=spreadsheet_id,
            exact_match=exact_match
        )

        if row_num is None:
            print("未找到匹配的行")
            return False

        return self.update_row(
            sheet_name=sheet_name,
            row_number=row_num,
            new_values=new_values,
            spreadsheet_id=spreadsheet_id,
            value_input_option=value_input_option,
            start_column=start_column
        )

    def _find_row_by_value(
            self,
            sheet_name: str,
            column: Union[str, int],
            value: Union[str, int, float, bool],
            spreadsheet_id: str = None,
            exact_match: bool = True
    ) -> Optional[int]:
        """查找包含指定值的行号"""
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id

        # 获取列数据
        column_data = self.get_column_data(
            sheet_name=sheet_name,
            column=column,
            spreadsheet_id=spreadsheet_id,
            skip_header=False,
            value_render_option="UNFORMATTED_VALUE"
        )

        # 查找匹配项
        for i, cell_value in enumerate(column_data, 1):
            if exact_match:
                if cell_value == value:
                    return i
            else:
                if str(value).lower() in str(cell_value).lower():
                    return i
        return None

    @staticmethod
    def column_index_to_letter(column_index: int) -> str:
        """将列索引(1-based)转换为字母"""
        if column_index < 1:
            raise ValueError("列索引必须大于0")

        letters = []
        while column_index > 0:
            column_index, remainder = divmod(column_index - 1, 26)
            letters.append(chr(65 + remainder))
        return ''.join(reversed(letters))

    @staticmethod
    def letter_to_column_index(column_letter: str) -> int:
        """将列字母转换为索引(1-based)"""
        column_letter = column_letter.upper()
        index = 0
        for char in column_letter:
            if not 'A' <= char <= 'Z':
                raise ValueError("无效的列字母")
            index = index * 26 + (ord(char) - ord('A') + 1)
        return index