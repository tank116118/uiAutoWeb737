import multiprocessing
import sys

from PyQt5.QtWidgets import QApplication
from main import Main

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    # 创建主视图
    main = Main()
    main.show()
    # 登录检测
    sys.exit(app.exec_())


