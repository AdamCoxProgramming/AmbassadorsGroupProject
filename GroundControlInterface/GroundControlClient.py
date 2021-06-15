from Backend import ServerAPI
from Backend.DataStore.CreateTables import createTables, dropAllTables
from Backend.Schedular import Schedular
from CommandLineControler import Controller, NextState

class LoginState:
    def run(self):
        print("--Welcome To Ground Control--")
        print("Type 'back' at anytime to return to the previous state")

        userName = None
        loggedIn = False
        while loggedIn != True:
            while userName == None:
                username = input("What is your ground control login: ")
                if username == "back":
                    return None
                userFound = ServerAPI.doesGroundControlUserWithEmailExist(username)
                if userFound != True:
                    print("A ground control user with that login does not exist")
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

class IssState:
    def run(self):
        print("--ISS Overview--")
        oxogenLevel = ServerAPI.getIssState().oxogenLevel
        print("ISS Oxygen Remaining: " + str(oxogenLevel))

        while True:
            cmd = input("type 'back'")
            if cmd == "back":
                return None

class ShuttlesState:
    def run(self):
        print("--Shuttles--")
        passed = False
        cmd = None
        while not passed:
            cmd = input("type 'view', 'launch': ")
            if cmd == 'back':
                return None
            if cmd == 'view' or cmd == 'launch':
                passed = True
            else:
                print("invalid input")

        if cmd == 'view':
            return NextState(ShuttlesOverviewState(),False)
        else:
            ServerAPI.launchAShuttle()
            return NextState(LaunchShuttleState(),False)

class LaunchShuttleState:
    def run(self):
        print("--Launch Shuttle--")

        while True:
            cmd = input("type 'back'")
            if cmd == "back":
                return None

class ShuttlesOverviewState:
    def run(self):
        shuttleStates = ServerAPI.getStatesOfShuttles()
        for shuttleStates in shuttleStates:
            stateString = "Shuttle No:" + str(shuttleStates.shuttleId) + ", isFlying:" + str(shuttleStates.isFlying)
            stateString += ", destination:" + shuttleStates.destination + ", flightPercent:" + str(
                shuttleStates.flightPercent)
            print(stateString)
        while True:
            cmd = input("type 'back'")
            if cmd == "back":
                return None

class HomeState:
    def __init__(self,username):
        self.username = username

    def run(self):
        print("--Ground Control Home--")
        while True:
            cmd = ''
            passed = False
            while not passed:
                cmd = input("type 'shuttles', 'iss' or 'add account': ")
                if cmd == 'back':
                    return None
                if cmd == 'shuttles' or cmd == 'iss' or cmd == 'add account':
                    passed = True
                else:
                    print("invalid input")
            if cmd == 'shuttles':
                return NextState(ShuttlesState(),False)
            if cmd == 'add account':
                return NextState(CreateAccountState(),False)
            elif cmd == 'iss':
                return NextState(IssState(),False)

class CreateAccountState:
    def run(self):
        print("--Add Account--")

        typeSelected = None
        typeChosen = None
        while typeSelected != True:
            typeChosen = input("What account type, either 'astro', 'ground': ")
            if typeChosen == "back":
                return None
            if typeChosen == 'astro' or typeChosen == 'ground':
                typeSelected = True

        accountCreated = False
        while accountCreated != True:
            address = input("Enter your email address: ")
            if address == "back":
                return None
            else:
                if typeChosen == 'ground':
                    if not ServerAPI.doesGroundControlUserWithEmailExist(address):
                        try:
                            ServerAPI.registerGroundControlEmail(address)
                        except:
                            print("The account could not be created")
                        return None
                    else:
                        print("A user with that email already exists")
                elif typeChosen == 'astro':
                    if not ServerAPI.doesAstronautWithEmailExist(address):
                        try:
                            ServerAPI.registerAstronautsEmail(address)
                        except:
                            print("The account could not be created")
                        return None
                    else:
                        print("A user with that email already exists")
        return None

#dropAllTables()
#createTables()

controller = Controller()
controller.start(NextState(LoginState(),False))
Schedular.endAllSchedules()