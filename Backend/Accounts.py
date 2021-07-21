from random import randrange
from Backend.SendEmail import SendEmailFromProjectAccount
from .DataStore import AccessLayer

class UserAccount:
    """This class represents a users account"""
    def __init__(self,email,id):
        self.email = email
        self.accountType = None
        self.name = 'default name'
        self.id = id

    def setPassword(self,newPasword):
        """Sets the users password
        pre-condition:The user must have been stored using the UserAccounts class before this can function can be called
        post-condition:The users password is updated"""
        AccessLayer.setUserPassword(self.email,newPasword)
    def getPassword(self):
        return AccessLayer.getUserByEmail(self.email)[4]

class UserAccounts:
    """This is a factory class for adding and returning UserAccounts"""
    def addUserAccount(self, email,type,password):
        if self.getUserAccountByEmail(email) != None:
            raise ValueError()
        AccessLayer.addUser(email, password, type)

    def getUserAccountsByType(self,type):
        """gets all the account of a certain type
        pre-condition:The type to filter by must be entered as a parameter
        post-condition:A list of users is returned all with the matching type"""
        rows = AccessLayer.getUsers()
        if rows == None:
            return []
        accounts = []
        for row in rows:
            accountType = row[2]
            if accountType == type:
                accounts.append(self._createUserAccountObject(row))
        return accounts

    def getUserAccountByEmail(self, email):
        """gets a specific user by email address
        pre-condition:The user must exist
        post-condition:If the user exists a UserAccount is returned, other wise None is"""
        rows = AccessLayer.getUserByEmail(email)
        if rows == None:
            return None
        return self._createUserAccountObject(rows)

    def getUserAccountById(self, id):
        """gets a specific user by id
        pre-condition:The user must exist
        post-condition:If the user exists a UserAccount is returned, other wise None is"""
        rows = AccessLayer.getUserById(id)
        if rows == None:
            return None
        return self._createUserAccountObject(rows)

    def _createUserAccountObject(self, rows):
        """Converts from the data access rows into a UserAccountObject
        pre-condition:The user rows from the data access layer must be in the correct order
        post-condition:Returns a UserAccount object"""
        account = UserAccount(rows[1],rows[0])
        account.accountType = rows[2]
        return account

def addUserAccount(emailAddress,type):
    """Adds a new UserAccount to the system
    pre-condition:The email and type must be specified
    post-condition:Adds the user account to the system and emails the user with their password"""
    randomPassword = generateRandomPassword()
    UserAccounts().addUserAccount(emailAddress,type,randomPassword)
    SendEmailFromProjectAccount(emailAddress, 'Your password is ' + randomPassword)

def generateRandomPassword():
    """Generates a random password as a string with a numeric value between 1000 and 9999"""
    return str(randrange(1000,9999))

def isCorrectPassword(email,passwordIn):
    """Compares a users read password to input
    pre-condition:A user with the email must exist
    post-condition:Returns a boolean indicating if the password was correct"""
    user = UserAccounts().getUserAccountByEmail(email)
    password = user.getPassword()
    return password == passwordIn