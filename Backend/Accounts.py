from random import randrange
from SendEmail import SendEmailFromProjectAccount
from .DataStore import AccessLayer
from .DataStore.AccessLayer import AccountTypes

class UserAccount:
    def __init__(self,email):
        self.email = email
        self.accountType = None

    def setPassword(self,newPasword):
        AccessLayer.setUserPassword(self.email,newPasword)
    def getPassword(self):
        return AccessLayer.getUserByEmail(self.email)[4]

class UserAccounts:
    def addUserAccount(self, email,type):
        if self.getUserAccountByEmail(email) != None:
            raise ValueError()
        AccessLayer.addUser(email, 'DEFAULT_PASSWORD', type)

    def getUserAccountByEmail(self, email):
        rows = AccessLayer.getUserByEmail(email)
        if rows == None:
            return None
        return self._createUserAccountObject(rows, email)

    def _createUserAccountObject(self, rows, email):
        account = UserAccount(email)
        account.accountType = rows[2]
        return account

def getAstronautByEmail(email):
    return UserAccounts().getUserAccountByEmail(email)

def getUserAccountByEmail(email):
    return UserAccounts().getUserAccountByEmail(email)


def addUserAccount(emailAddress,type):
    UserAccounts().addUserAccount(emailAddress,type)
    astronaut = UserAccounts().getUserAccountByEmail(emailAddress)
    randomPassword = generateRandomPassword()
    astronaut.setPassword(randomPassword)
    SendEmailFromProjectAccount(emailAddress, 'Your password is ' + randomPassword)

def generateRandomPassword():
    return str(randrange(1000,9999))

def isCorrectPassword(email,passwordIn):
    user = getUserAccountByEmail(email)
    password = user.getPassword()
    return password == passwordIn
