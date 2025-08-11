import sys
import time

from task import TimerTask, PlatformAdapter


def main():
    """主函数"""
    # 初始化定时任务
    timer = TimerTask(interval=300)  # 每10秒执行一次

    # 设置信号处理器
    PlatformAdapter.setupSignalHandlers(
        lambda sig, frame: timer.shutdown() or sys.exit(0)
    )

    # 启动定时任务
    timer.start()

    # 主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        timer.shutdown()


def parseArgs():
    """解析命令行参数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            PlatformAdapter.runAsService(main)
        elif sys.argv[1] == "stop":
            print("停止命令需要根据平台使用相应服务管理工具")
            sys.exit(0)
        elif sys.argv[1] in ("-h", "--help"):
            print("用法: python timer_task.py [start|stop]")
            print("  start - 作为服务/守护进程启动")
            print("  stop  - 停止服务")
            sys.exit(0)
        else:
            print("未知参数，使用 --help 查看帮助")
            sys.exit(1)
    else:
        main()


if __name__ == "__main__":
    parseArgs()