import threading
import ApiMode

class PerpetualTimer():
    def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = threading.Timer(self.t,self.handle_function)

    def handle_function(self):
       if not Schedular.paused:
            self.hFunction()
       self.thread = threading.Timer(self.t,self.handle_function)
       self.thread.start()

    def start(self):
      self.thread.start()

    def cancel(self):
      self.thread.cancel()

class Schedular:
    timers = []
    paused = True
    @staticmethod
    def addToSchedule(function,time):
        run = False
        if not ApiMode.ApiSetting.distrubuted:
            run = True
        elif ApiMode.ApiSetting.runningServerOnly:
            run = True
        if run:
            timer = PerpetualTimer(time, function)
            Schedular.timers.append(timer)
            timer.start()

    @staticmethod
    def start():
        Schedular.paused = False

    @staticmethod
    def endAllSchedules():
        for timer in Schedular.timers:
            timer.cancel()