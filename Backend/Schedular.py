import threading

class PerpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = threading.Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = threading.Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

class Schedular:
    timers = []
    @staticmethod
    def addToSchedule(function,time):
        timer = PerpetualTimer(time, function)
        Schedular.timers.append(timer)
        timer.start()

    @staticmethod
    def endAllSchedules():
        for timer in Schedular.timers:
            timer.cancel()

