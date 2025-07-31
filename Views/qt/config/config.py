# -*- coding: utf-8 -*-
"""
@Project : uiAuto
@File    : config.py.py
@Author  : Admin
@Date    : 2025/3/27 14:36
@Desc    : 
"""
from PyQt5.QtGui import QColor

from paths import getProjectPath


class Config:
    colorHighlight: QColor = QColor(240, 240, 255)
    colorWarringBg: QColor = QColor(240, 240, 120)
    colorWarringText: QColor = QColor(50, 50, 200)
    colorNormalBg: QColor = QColor(255, 255, 255)
    colorNormalText: QColor = QColor(100, 100, 100)
    colorErrorBg: QColor = QColor(220, 100, 100)
    colorErrorText: QColor = QColor(255, 255, 255)
    colorBtnNormalBg: QColor = QColor(230,230,255)
    buttonStyleNormal: str = """
                QPushButton {
                    # background-color: #a0c4e0 !important;
                    border: none;
                    color: #2c3e50;
                    padding: 4px;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #89b4d8;
                }
                QPushButton:pressed {
                    background-color: #6a9bc3;
                    padding-top: 5px;
                    padding-bottom: 3px;
                }"""
    buttonStyleRunning: str = """
                    QPushButton {
                        background-color: rgb(255,50,50) !important;
                        border: none;
                        color: rgb(255,255,255);
                        padding: 4px;
                        border-radius: 4px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: rgb(255,60,60);;
                    }
                    QPushButton:pressed {
                        background-color: rgb(255,60,60);
                        padding-top: 5px;
                        padding-bottom: 3px;
                    }"""

    tabWidgetStyle = """
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #e0e0e0;
                color: #555;
                border: none;
                padding: 8px 16px 8px 24px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                height: 24px;
            }
                QTabBar::tab:first {
                margin-left: 5px;  /* 第一个标签左边距 */
            }
            QTabBar::tab:selected {
                background: #4fc3f7;  /* 选中标签浅蓝色背景 */
                color: #eee;      /* 选中标签文字颜色 */
                font-weight: bold;  /* 选中标签加粗 */
            }
            QTabBar::tab:hover {
                background: #b3e5fc;  /* 悬停时更浅的蓝色 */
            }
            QTabWidget::tab-bar {
                left: 5px;  /* 标签栏左边距 */
            }
    """

    tableSetStyle="""
            QTableWidget {
                border: none;
                background: white;
                gridline-color: transparent;
                font-size:16px;
            }
            QHeaderView::section {
                background-color: white;
                color: #555;
                border: none;
                border-bottom: 1px solid rgba(200,200,200,0.7);
                padding: 3px;
                font-size: 12px;
            }
            """

    scrollStyle = """
            /* 垂直滚动条 */
            QScrollBar:vertical {
                border: none;
                background: #f5f5f5;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
            /* 水平滚动条 */
            QScrollBar:horizontal {
                border: none;
                background: #f5f5f5;
                height: 10px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            """

    ""
    @staticmethod
    def getCommonStyle():
        root = getProjectPath()
        style = f"""
                QDateEdit{{
                    border: 1px solid #ccc;
                    border-right: none;
                    border-radius: 3px;
                    padding: 1px 18px 1px 3px;
                    min-width: 2em;
                    background: white;
                    font-size: 11px;
                }}
                QDateEdit:disabled {{
                    color: #888888;
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                }}
                /* 上下箭头按钮 */
                QDateEdit::up-button, QDateEdit::down-button {{
                    border: 1px solid #ccc;
                    subcontrol-origin: border;
                    width: 16px;
                    border-left: none;
                    background: white;
                    font-size: 11px;
                }}
                QDateEdit::up-button {{
                    border-bottom: none;
                    border-top-right-radius: 3px;
                }}
                QDateEdit::down-button {{
                    border-top: none;
                    border-bottom-right-radius: 3px;
                }}
                /* 上箭头图标 */
                QDateEdit::up-arrow {{
                    image: url({root + '/Static/images/upArrow.ico'});
                    width: 10px;
                    height: 10px;
                }}
                /* 下箭头图标 */
                QDateEdit::down-arrow {{
                    image: url({root + '/Static/images/downArrow.ico'});
                    width: 10px;
                    height: 10px;
                }}
                /* 按钮悬停状态 */
                QDateEdit::up-button:hover, QDateEdit::down-button:hover {{
                    background: #e0e0e0;
                }}
                /* 按钮按下状态 */
                QDateEdit::up-button:pressed, QDateEdit::down-button:pressed {{
                    background: #d0d0d0;
                }}
                QComboBox {{
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    padding: 1px 18px 1px 3px;
                    min-width: 2em;
                    background: white;
                    font-size: 11px;
                }}
                QComboBox:disabled {{
                    color: #888888;
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                }}
                QComboBox::drop-down {{
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 15px;
                    border-left-width: 0px;
                    border-left-color: #ccc;
                    border-left-style: solid;
                    border-top-right-radius: 3px;
                    border-bottom-right-radius: 3px;
                    background: rgba(255,255,255,0);
                }}
                QComboBox::down-arrow {{
                    image: url({root + '/Static/images/downArrow.ico'});
                    width: 12px;
                    height: 12px;
                }}
                QComboBox QScrollBar:vertical {{
                    border: none;
                    background: #F0F0F0;
                    width: 10px;
                    margin: 0px 0px 0px 0px;
                }}
                QComboBox QScrollBar::handle:vertical {{
                    background: #C0C0C0;
                    min-height: 20px;
                    border-radius: 5px;
                }}
                QComboBox QScrollBar::handle:vertical:hover {{
                    background: #A0A0A0;
                }}
                QComboBox QScrollBar::add-line:vertical, QComboBox QScrollBar::sub-line:vertical {{
                    height: 0px;
                    background: none;
                }}
                QComboBox QScrollBar::add-page:vertical, QComboBox QScrollBar::sub-page:vertical {{
                    background: none;
                }}
                QLineEdit {{
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    padding: 1px 18px 1px 3px;
                    min-width: 2em;
                    background: white;
                    font-size: 11px;
                }}
                QLineEdit:disabled {{
                    color: #888888;
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                }}
                QPushButton {{
                    background-color: #a0c4e0;
                    border: none;
                    color: #2c3e50;
                    padding: 4px;
                    border-radius: 4px;
                    font-size: 12px;
                }}
                QPushButton:disabled {{
                    color: #888888;
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                }}
                QPushButton:hover {{
                    background-color: #89b4d8;
                }}
                QPushButton:pressed {{
                    background-color: #6a9bc3;
                    padding-top: 5px;
                    padding-bottom: 3px;
                }}
                QCheckBox {{
                    font-size: 11px;
                }}
                QCheckBox::indicator {{
                    height: 12px;
                    width: 12px;
                }}
                QLabel {{
                    font-size: 11px;
                }}
                QPlainTextEdit {{
                    font-size: 11px;
                }}
                        """
        return style

