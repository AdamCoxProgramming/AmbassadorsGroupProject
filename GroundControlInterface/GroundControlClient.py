import sys
from getpass import getpass

from Backend import ServerAPI
from Backend.DataStore.CreateTables import createTables, dropAllTables
from Backend.ISS import Astronauts, Location
from Backend.InterfaceClasses import ShuttleType
from Backend.Schedular import Schedular
from CommandLineControler import Controller, NextState
from GroundControlInterface.Workouts import options

class LoginState:
    def run(self):
        ServerAPI.apiSecretKey = None #clear the server api key so the next user cannot inherit it from the previous
        print("--Welcome To Ground Control--")
        print("Type 'back' at anytime to return to the previous state")
        email = None

        loggedIn = False
        while loggedIn != True:
            while email == None:
                username = input("What is your ground control login: ")
                if username == "back":
                    return None
                userFound = ServerAPI.doesGroundControlUserWithEmailExist(username)
                if userFound != True:
                    print("A ground control user with that login does not exist")
                else:
                    email = username

            correctPassword = False
            while correctPassword != True:
                password = getpass("What is your password: ")
                if password == "back":
                    return None
                correctPassword = ServerAPI.doesUsersPasswordMatch(email,password)
                if correctPassword != True:
                    print("Incorrect password")
            loggedIn = True

        return NextState(HomeState(email),False)

def getHiddenInput(prompt):
    print(prompt)
    return sys.stdin.readline().rstrip()

class IssState:
    def run(self):
        print("--ISS Overview--")
        oxogenLevel = ServerAPI.getIssState().oxogenLevel
        print("ISS Oxygen Remaining: " + str(oxogenLevel))
        print("Astronauts on board:")
        asronautsOverview = ServerAPI.getAstronautsOverview()
        for astronautState in asronautsOverview:
            if astronautState.location == Location.SPACE_STATION.name:
                print("    " + astronautState.email + ", location: " + astronautState.location)

        while True:
            cmd = input("type 'back'")
            if cmd == "back":
                return None

class ShuttlesState:
    def run(self):
        print("--Shuttles--")

        shuttleStates = ServerAPI.getShuttlesStates()
        for shuttleState in shuttleStates:
            stateString = ''
            if shuttleState.type == ShuttleType.MANNED:
                stateString = "Shuttle No:" + str(shuttleState.shuttleId) + ", "
            stateString += "type:" + shuttleState.type.name + ", location:" + shuttleState.location.name
            stateString += ", destination:" + shuttleState.destination + ", flightPercent:" + str(
                shuttleState.flightPercent)
            print(stateString)

        passed = False
        cmd = None
        while not passed:
            cmd = input("type 'back' or 'launch': ")
            if cmd == 'back':
                return None
            if cmd == 'launch':
                passed = True
            else:
                print("invalid input")

        if cmd == 'launch':
            return NextState(LaunchShuttleState(),False)

class LaunchShuttleState:
    def run(self):
        print("--Launch Shuttle--")

        passed = False
        shuttleNumber = None
        while passed != True:
            shuttleInput = input("type the shuttle number to launch: ")
            if shuttleInput == "back":
                return None
            else:
                try:
                    shuttleNumber = int(shuttleInput) -1
                    passed = True
                except:
                    return None

        shuttleLocation = None
        states = ServerAPI.getShuttlesStates()
        for shuttle in states:
            if shuttle.type == ShuttleType.MANNED:
                if shuttle.shuttleId == shuttleNumber +1:
                    shuttleLocation = shuttle.location

        if shuttleLocation == None:
            print("Invalid shuttle name, launch aborted")
            return None

        print("The shuttle will be launched from " + shuttleLocation.name.lower())

        asronautsOverview = ServerAPI.getAstronautsOverview()
        states = []
        for asronautState in asronautsOverview:
            if asronautState.location == shuttleLocation.name:
                states.append(asronautState)

        astroIds = []
        if len(states) > 0:
            print("Which astronauts should be onboard?")

            index =0
            for astronautState in states:
                print(str(index) + " : " + astronautState.email + ", location: " + astronautState.location)
                index += 1

            done= False

            while done == False:
                print("please type the numbers of the astronauts to add:")
                print("(each number should be separated by a space)")
                res = input("numbers : ")
                if res =="back":
                    return None
                try:
                    if res == ' ':
                        done = True
                    else:
                        astroNumbers = res.split(' ')
                        for number in list(map(int, astroNumbers)):
                            if number >= index:
                                raise Exception()
                            astroIds.append(states[number].id)
                        done = True
                except:
                    print("invalid input")
                    done = False

        ServerAPI.launchShuttle(shuttleNumber,astroIds)
        print("Shuttle launched")

class HomeState:
    def __init__(self,username):
        self.username = username

    def run(self):
        print("--Ground Control Home--")
        deafultPermsions = ['iss', 'shuttles','astros','workouts']

        if self.username == 'admin':
            print("ADMINISTRATOR PERMISSIONS ENABLED")
            extraPermsions = ['add account', 'monitor']
            deafultPermsions = deafultPermsions + extraPermsions

        while True:
            cmd = ''
            passed = False
            while not passed:
                cmd = input("type '" + "' or '".join(deafultPermsions) + "':")
                if cmd == 'back':
                    return None
                if cmd in deafultPermsions:
                    passed = True
                else:
                    print("invalid input")
            if cmd == 'shuttles':
                return NextState(ShuttlesState(),False)
            elif cmd == 'add account':
                return NextState(CreateAccountState(),False)
            elif cmd == 'astros':
                return NextState(AstronautsOverviewState(),False)
            elif cmd == 'iss':
                return NextState(IssState(),False)
            elif cmd == 'workouts':
                return NextState(WorkState(), False)
            elif cmd == 'monitor':
                return NextState(MonitoringState(), False)

class MonitoringState:
    def run(self):
        print("--Monitoring--")
        numberOfCallsInLast15Mins = ServerAPI.getNumberOfApiCallsInLast15Mins()
        print("number of api calls in the last 15 minuets: " + str(numberOfCallsInLast15Mins))
        if numberOfCallsInLast15Mins > 60:
            print("WARNING: This is exceptionally high, a DDOS attack may be occurring")
        while True:
            cmd = input("type 'back'")
            if cmd == "back":
                return None

class AstronautsOverviewState:
    def run(self):
        print("--Astronauts Overview--")
        asronautsOverview = ServerAPI.getAstronautsOverview()
        for astronautState in asronautsOverview:
            print(astronautState.email + ", location: " + astronautState.location)
        while True:
            cmd = input("type 'back'")
            if cmd == "back":
                return None

class PhoneNumber:
    def __init__(self,number,countryCode):
        self.number = number
        self.countryCode = countryCode

class CreateAccountState:
    def run(self):
        print("--Add Account--")

        typeSelected = None
        typeChosen = None
        while typeSelected != True:
            choosen = input("What account type, either 'astro', 'ground': ")
            if choosen == "back":
                return None
            if choosen == 'astro' or choosen == 'ground':
                typeSelected = True
                typeChosen = choosen

        accountCreated = False
        while accountCreated != True:
            address = input("Enter your email address: ")
            if address == "back":
                return None
            else:
                try:
                    if typeChosen == 'astro':
                        ServerAPI.registerAstronautsEmail(address)
                        accountCreated = True
                    else:
                        ServerAPI.registerGroundControlEmail(address)
                        accountCreated = True
                except:
                    print("could not create account")
                    return None
                """
                phoneNumber = self.getPhoneNumber()
                if phoneNumber == None:
                    print("Could not register phone number, aborted")
                    return None

                if typeChosen == 'ground':
                    if not ServerAPI.doesGroundControlUserWithEmailExist(address):
                        try:
                            #ServerAPI.registerUserMfaAccount(address, str(phoneNumber.number),str(phoneNumber.countryCode))
                            ServerAPI.registerGroundControlEmail(address)
                        except:
                            print("The account could not be created")
                        return None
                    else:
                        print("A user with that email already exists")
                elif typeChosen == 'astro':
                    if not ServerAPI.doesAstronautWithEmailExist(address):
                        try:
                            #ServerAPI.registerUserMfaAccount(address, str(phoneNumber.number),str(phoneNumber.countryCode))
                            ServerAPI.registerAstronautsEmail(address)
                        except:
                            print("The account could not be created")
                        return None
                    else:
                        print("A user with that email already exists")
                    """
        return None

    def getPhoneNumber(self):
        try:
            number = input("Enter your phone number: ")
            if number == "back":
                return None

            countryCode = input("Enter your country code: ")
            if countryCode == "back":
                return None
            return PhoneNumber(int(number[1:]), int(countryCode))
        except:
            return None

class WorkState():

    def run(self):

        print("--Physical Workout Menu--")
        while True:
            cmd = ''
            passed = False
            while not passed:
                cmd = input("1. Assign workout to Astronauts")
                if cmd == 'back':
                    return None
                if cmd == "1" or cmd == "2" or cmd == "3":
                    passed = True
                else: print("Invalid choice")
            if cmd == "1":
                userchoice = int(input("What workout will you like to assign to the astronauts: \n1. 2X Weeks \n2. 4X Weeks\n3. Everyday\n"))
                while userchoice > len(options) or userchoice < 1:
                    print("invalid choice. Try again!")
                currentWorkout = options[userchoice - 1]
                print('You have selected -->', currentWorkout)

#dropAllTables()
#createTables()

Schedular.start()
controller = Controller()
controller.start(NextState(LoginState(),False))
Schedular.endAllSchedules()