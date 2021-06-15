from Backend.Schedular import Schedular
from CommandLineControler import Controller, NextState
import Backend.ServerAPI as ServerAPI


class LoginState:
    def run(self):
        print("--Welcome Astronaut--")
        print("Type 'back' at anytime to return to the previous state")

        userName = None
        loggedIn = False
        while loggedIn != True:
            while userName == None:
                username = input("What is your astronaut login: ")
                if username == "back":
                    return None
                userFound = ServerAPI.doesAstronautWithEmailExist(username)
                if userFound != True:
                    print("An astronaut with that login does not exist")
                else:
                    userName = username

            correctPassword = False
            while correctPassword != True:
                password = input("What is your password: ")
                if password == "back":
                    return None
                correctPassword = ServerAPI.doesUsersPasswordMatch(userName,password)
                if correctPassword != True:
                    print("Incorrect password")
                else:
                    loggedIn = True

        return NextState(HomeState(userName),False)

class HomeState:
    def __init__(self,username):
        self.username = username

    def run(self):
        print("--Astronaut Home--")
        while True:
            cmd = ''
            passed = False
            while not passed:
                cmd = input("type 'back': ")
                if cmd == 'back':
                    return None

#dropAllTables()
#createTables()

controller = Controller()
controller.start(NextState(LoginState(),False))
Schedular.endAllSchedules()