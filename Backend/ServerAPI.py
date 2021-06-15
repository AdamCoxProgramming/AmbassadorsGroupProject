import requests
from Backend.Accounts import addUserAccount, getUserAccountByEmail, isCorrectPassword
from Backend.DataStore.AccessLayer import AccountTypes
from Backend.ISS import launchAShuttleFromEarth, getStatesOfShuttles, getIssOxogenLevel
from ApiMode import ApiSetting
from SendEmail import SendEmailFromProjectAccount

class IssState:
    def __init__(self,oxogenLevel):
        self.oxogenLevel = oxogenLevel



def getIssState():
    if ApiSetting.serverMode:
        return requests.get("http://127.0.0.1:5000/system/").text
    else:
        return IssState(getIssOxogenLevel())


def getShuttlesStates():
    if ApiSetting.serverMode:
        raise Exception("need to implement adapter")
        return requests.get("http://127.0.0.1:5000/system/")
    else:
        return getStatesOfShuttles()

def launchAShuttle():
    if ApiSetting.serverMode:
        return requests.post("http://127.0.0.1:5000/system/")
    else:
        return launchAShuttleFromEarth()

def doesAstronautWithEmailExist(email):
    if ApiSetting.serverMode:
        raise Exception()#return requests.post("http://127.0.0.1:5000/system/")
    else:
        if email == 'admin':
            return True
        else:
            user = getUserAccountByEmail(email)
            if user != None and user.accountType == str(AccountTypes.ASTRONAUT):
                return True
        return False

def doesGroundControlUserWithEmailExist(login):
    if ApiSetting.serverMode:
        raise Exception()#return requests.post("http://127.0.0.1:5000/system/")
    else:
        if login == 'admin':
            return True
        else:
            user = getUserAccountByEmail(login)
            if user != None and user.accountType == str(AccountTypes.GROUND_CONTROL):
                return True
        return False

def doesUsersPasswordMatch(username, password):
    if ApiSetting.serverMode:
        raise Exception()#return requests.post("http://127.0.0.1:5000/system/")
    else:
        if username == 'admin':
            if password == 'password':
                return True
        else:
            return isCorrectPassword(username,password)
        return False

def registerGroundControlEmail(address):
    if ApiSetting.serverMode:
        raise Exception()#return requests.post("http://127.0.0.1:5000/system/")
    else:
        addUserAccount(address,AccountTypes.GROUND_CONTROL)

def registerAstronautsEmail(address):
    if ApiSetting.serverMode:
        raise Exception()#return requests.post("http://127.0.0.1:5000/system/")
    else:
        addUserAccount(address,AccountTypes.ASTRONAUT)
