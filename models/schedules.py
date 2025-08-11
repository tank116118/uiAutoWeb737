

class Schedules:
    def __init__(self,
                 id: int = None,
                 type: int = None,
                 name: str = None,
                 task: str = None,
                 taskParams: str = None,
                 accountParams: str = None,
                 triggerName: str = None,
                 startTime: str = None,
                 endTime: str = None,
                 interval: int = None,
                 timeUnit: str = None,
                 year: str = None,
                 month: str = None,
                 day: str = None,
                 week: str = None,
                 dayOfWeek: str = None,
                 hour: str = None,
                 minute: str = None,
                 second: str = None,
                 enable: bool = None,
                 scheduleParams: str = None,
                 isSelected: bool = None):
        self.id: int = id
        self.type: int = type
        self.name: str = name
        self.task: str = task
        self.taskParams: str = taskParams
        self.accountParams: str = accountParams
        self.triggerName: str = triggerName
        self.startTime: str = startTime
        self.endTime: str = endTime
        self.interval: int = interval
        self.timeUnit: str = timeUnit
        self.year: str = year
        self.month: str = month
        self.day: str = day
        self.week: str = week
        self.dayOfWeek: str = dayOfWeek
        self.hour: str = hour
        self.minute: str = minute
        self.second: str = second
        self.enable: bool = enable
        self.scheduleParams: str = scheduleParams
        self.isSelected: bool = isSelected