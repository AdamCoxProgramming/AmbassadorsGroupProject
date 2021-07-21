from datetime import datetime, timedelta
from pathlib import Path
from file_read_backwards import FileReadBackwards
import subprocess
import sys
import pkg_resources
from subprocess import PIPE, Popen

from Backend.RelativeRootPath import getRelativeRootPath
from Backend.Schedular import Schedular

def getNumberOfCallInLastXMins(minuetsAgo):
    count = 0
    timeXMinsAgo = datetime.now() -timedelta(minutes = minuetsAgo)
    logFilePath = "api_logs.txt"
    if not Path(logFilePath).is_file():
        return 0
    else:
        with FileReadBackwards(logFilePath, encoding="utf-8") as frb:
            for log in frb:
                timeOfLog = _getLogsTime(log)
                if timeOfLog != None:
                    if timeOfLog < timeXMinsAgo:
                        return count
                    else:
                        count += 1
        return count #fallback incase there are no calls in the past 15 mins

def _getLogsTime(log):
    try:
        dateStringPortion = log.split('[')[1].split(']')[0]
        return datetime.strptime(dateStringPortion,"%d/%b/%Y %H:%M:%S")
    except:
        return None

def install_safety():
    required = {'safety'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'safety'])

def outputToLog(string):
    file = open(getRelativeRootPath() + 'Backend\\' + 'safetylog.txt', 'a')
    file.write(string)
    file.close()

def safety_check():
    try:
        import safety
    except:
        install_safety()
    command = "safety check"
    process = Popen(command, stdout=PIPE, stderr=None, shell=True, universal_newlines=True)
    output = process.communicate()[0]
    packackesOutput = output.split('| package                    | installed | affected                 | ID       |')[1]
    dateTime = datetime.now()
    outputToLog(str(dateTime) + '\n' + packackesOutput + '\n')

Schedular.addToSchedule(safety_check, 60)