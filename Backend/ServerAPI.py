import json
import pickle
import requests
from Backend.Accounts import addUserAccount, isCorrectPassword, UserAccounts
from Backend.DataStore.AccessLayer import ASTRONAUT, GROUND_CONTROL, ADMIN
from Backend.ISS import getStatesOfShuttles, getIssOxogenLevel, \
    getAstronauts, launchShuttleToAppropriateDestination
from ApiMode import ApiSetting
from Backend.Monitoring import getNumberOfCallInLastXMins
from Backend.MultiFactorAuthentication import verifyMfaAccount, registerMfaAccount
from Backend.RelativeRootPath import getRelativeRootPath
from Backend.Resources import Resources
import warnings

apiSecretKey = None

def get(extension,params= None):
    headers = {"apiKey": apiSecretKey}
    with warnings.catch_warnings(record=True) as w:
        return requests.get("https://127.0.0.1:5000" + extension , verify=getRelativeRootPath()+ '/Backend/Keys/cert.pem',params=params,headers=headers)

def put(extension,params= None):
    headers = {"apiKey": apiSecretKey}
    with warnings.catch_warnings(record=True) as w:
        return requests.put("https://127.0.0.1:5000" + extension , verify=getRelativeRootPath()+'/Backend/Keys/cert.pem',params=params,headers=headers)

def post(extension,params= None):
    headers = {"apiKey": apiSecretKey}
    with warnings.catch_warnings(record=True) as w:
        return requests.post("https://127.0.0.1:5000" + extension , verify=getRelativeRootPath()+'/Backend/Keys/cert.pem',params=params,headers=headers)

def unpickle(text):
    formated = text[1:-2].replace('\\n','\n')
    return pickle.loads(formated.encode())

class IssState:
    def __init__(self,oxogenLevel):
        self.oxogenLevel = oxogenLevel

class AstronautState:
    def __init__(self,email,location,id):
        self.email = email
        self.location = location
        self.id = id

def getResourceQuantity(itemNumber):
    if ApiSetting.distrubuted:
        result = get("/ResourceItem/"+str(itemNumber))
        if result.status_code == 501:
            raise Exception("could not create account")
        else:
            return int(result.text)
    else:
        return Resources.getItemStockQuantity(itemNumber)

def consumeResource(itemNumber,amountToConsume):
    if ApiSetting.distrubuted:
        return put("/ResourceItem/"+str(itemNumber),{"amountToConsume":str(amountToConsume)})
    else:
        return Resources.consumeItemStock(itemNumber,amountToConsume)

def getAvailibleItems():
    if ApiSetting.distrubuted:
        return unpickle(get("/ResourceItems/").text)
    else:
        return Resources.getAllStockedItems()

def getIssState():
    if ApiSetting.distrubuted:
        return unpickle(get("/Iss/").text)
    else:
        return IssState(getIssOxogenLevel())

def getShuttlesStates():
    if ApiSetting.distrubuted:
        return unpickle(get('/Shuttles/').text)
    else:
        return getStatesOfShuttles()

def getNumberOfApiCallsInLast15Mins():
    if ApiSetting.distrubuted:
        return unpickle(get("/Monitor/").text)
    else:
        return getNumberOfCallInLastXMins(15)

def launchShuttle(shuttleNo, astronautIds):
    if ApiSetting.distrubuted:
        post("/ShuttlesLocation/" + str(shuttleNo),{"astronautIds":json.dumps(astronautIds)})
    else:
        launchShuttleToAppropriateDestination(shuttleNo,astronautIds)

def getAstronautsOverview():
    def formatAsStates(astronauts):
        states = []
        for astronaut in astronauts:
            states.append(AstronautState(astronaut.account.email, astronaut.getLocation(), astronaut.id))
        return states

    if ApiSetting.distrubuted:
        return formatAsStates(unpickle(get("/Astronauts/").text))
    else:
        return formatAsStates(getAstronauts())

def doesAstronautWithEmailExist(email):
    return _doesUserOfTypeExist(email,ASTRONAUT)

def doesGroundControlUserWithEmailExist(email):
    return _doesUserOfTypeExist(email,GROUND_CONTROL) or _doesUserOfTypeExist(email,ADMIN)

def _doesUserOfTypeExist(email, type):
    user = None
    if ApiSetting.distrubuted:
        user = unpickle(get("/User/", {"email": email}).text)
    else:
        user = UserAccounts().getUserAccountByEmail(email)

    if user != None and user.accountType == str(type):
        return True
    return False

def doesUsersPasswordMatch(username, password):
    if ApiSetting.distrubuted:
        reqResult = get("/Password/", {"email": username,"password":password})
        object = unpickle(reqResult.text)
        correctPassword = object['passwordMatch']
        if correctPassword:
            global apiSecretKey
            apiSecretKey = object['apiKey']

        return correctPassword
    else:
        return isCorrectPassword(username,password)

def registerUserMfaAccount(email, phone, countryCode):
    if ApiSetting.distrubuted:
        post("/MFA/", {"email": email,"phone":phone,"countryCode":countryCode})
    else:
        registerMfaAccount(email, phone, countryCode)

def doesUsersMfaCodeMatch(email, mfaCode):
    if ApiSetting.distrubuted:
        return unpickle(get("/MFA/", {"email": email,"mfaCode":mfaCode}))
    else:
        return verifyMfaAccount(email,mfaCode)

def registerGroundControlEmail(address):
    if ApiSetting.distrubuted:
        code = post("/User/", {"email": address,"type":GROUND_CONTROL}).status_code
        if code == 501:
            raise Exception("could not create account")
    else:
        addUserAccount(address,GROUND_CONTROL)

def registerAstronautsEmail(address):
    if ApiSetting.distrubuted:
        code = post("/User/", {"email": address,"type":ASTRONAUT}).status_code
        if code == 501:
            raise Exception("could not create account")
    else:
        addUserAccount(address,ASTRONAUT)