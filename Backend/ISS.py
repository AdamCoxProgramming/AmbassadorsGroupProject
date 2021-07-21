from enum import Enum
from .Accounts import UserAccounts
from .DataStore import AccessLayer
from .DataStore.AccessLayer import Location
from .Resources import Resources
from .Schedular import Schedular
from .InterfaceClasses import ShuttleState, ShuttleType

class Astronaut:
    """Represents an Astronaut user
    pre-condition: the email passed in the constructor must exist"""
    def __init__(self,userAccount):
        self.account = userAccount
        self.id = userAccount.id

    def getLocation(self):
        """Returns the users location
        pre-condition: None
        post-condition: Returns the users location"""
        return AccessLayer.getAstronautLocation(self.account.email)

    def setLocation(self,location):
        """sets the users location
        pre-condition: The location must be valid
        post-condition: Sets the users location"""
        AccessLayer.setAstronautLocation(location,self.account.email)

class Astronauts:
    """A factory for fetching astronauts"""
    @staticmethod
    def getAstronauts():
        """gets all the astronauts
        pre-condition:None
        post-condition:A list of astronauts is returned"""
        users = UserAccounts().getUserAccountsByType(AccessLayer.ASTRONAUT)
        astronauts = []
        for user in users:
            astronauts.append(Astronaut(user))
        return astronauts

    @staticmethod
    def getAstronautsAtLocation(location):
        """gets all the astronauts at a certain location
        pre-condition:the location must be valid
        post-condition:A list of astronauts at the specified location is returned in a list"""
        selected = []
        astronauts = Astronauts.getAstronauts()
        for astronaut in astronauts:
            astroLocation = astronaut.getLocation()
            locationString = str(location).split('.')[1]
            if locationString == astroLocation:
                selected.append(astronaut)
        return selected

    @staticmethod
    def getAstronautByEmail(email):
        """gets a specific astronaut by email
        pre-condition:None
        post-condition:If the Astronaut exists they are returned, other wise None is"""
        user = UserAccounts().getUserAccountByEmail(email)
        if user == None or user.accountType != str(AccessLayer.ASTRONAUT):
            return None
        return Astronaut(user)

    @staticmethod
    def getAstronautById(id):
        """gets a specific astronaut by id
        pre-condition:None
        post-condition:If the Astronaut exists they are returned, other wise None is"""
        user = UserAccounts().getUserAccountById(id)
        if user == None or user.accountType != str(AccessLayer.ASTRONAUT):
            return None
        return Astronaut(user)

class Shuttle:
    """Represents a shuttle in the system"""
    def __init__(self):
        self.flying = False
        self.percentage = 0
        self.destination = None
        self.location = Location.EARTH
        self.items = []
        self.passengers = []

    def addPassenger(self,astronaut):
        """Adds a passenger to the shuttle
        pre-condition:The passenger must be a valid astronaut account
        post-condition:The astronaut is 'stored' on the shuttle"""
        self.passengers.append(astronaut)

    def getPassengers(self):
        """Returns the astronauts on the shuttle
        pre-condition:None
        post-condition:A list of passengers on the shuttle is returned"""
        return self.passengers

    def clearPassengers(self):
        """The list of passengers on boared is cleared"""
        self.passengers = []

    def addOrderedItem(self,orderedItem):
        """Adds an item to the stock inventory
        pre-condition:None
        post-condition:A list of passengers on the shuttle is returned"""
        self.items.append(orderedItem)

    def launchToEarth(self):
        """Launches the shuttle to earth
        pre-condition:None
        post-condition:The shuttle begins its flight to earth"""
        self.flying = True
        self.destination = None
        self.percentage = 0
        self.location = Location.FLYING

    def launch(self,dockNo):
        """Launches the shuttle to the ISS
        pre-condition: Specify an un-occupied dock
        post-condition:The shuttle begins its flight to earth"""
        self.flying = True
        self.percentage = 0
        self.destination = dockNo
        self.location = Location.FLYING

    def fly(self):
        """Increments the shuttles current journey
        pre-condition: None
        post-condition: The shuttles journey progress increases"""
        self.percentage += 5

    def stopFlying(self):
        """End the current journey
        pre-condition: None
        post-condition: The shuttles will remain at its current location"""
        self.flying = False
        self.percentage = 0

class DockState(Enum):
    """Represents the potential states of a dock"""
    OCCUPIED = 0,
    ALLOCATED = 1,
    FREE = 2

class Dock:
    """Represents a dock"""
    def __init__(self):
        self.state = DockState.FREE

class GasCanister:
    """Represents a gas canister"""
    def getAmount(self):
        return Resources.getItemStockQuantity(OxygenResourceNumber)

    def addAmount(self,amount):
        Resources.consumeItemStock(OxygenResourceNumber,-amount)

    def removeAmount(self,amount):
        Resources.consumeItemStock(OxygenResourceNumber,amount)

class AirSimulation:
    def __init__(self):
        self.o2InAir = 7000
        self.updateSim()
        Schedular.addToSchedule(self.updateSim, 1)

    def measureO2(self):
        return self.o2InAir

    def updateSim(self):
        self.o2InAir -= 20

    def addO2(self,amount):
        self.o2InAir += amount

OxygenResourceNumber = 4

class SpaceStation:
    def __init__(self):
        self.docks = [Dock(), Dock(), Dock(), Dock(), Dock(), Dock()]
        self.oxogenCanister = GasCanister()
        self.carbonDioxideCanister = GasCanister
        self.air = AirSimulation()
        self.astronauts = []

    def updateStation(self):
        self.update()

    def update(self):
        o2InAir = self.air.measureO2()
        #print(str(self.oxogenCanister.amount))
        if o2InAir < 7000:
            self.releaseO2()
        self.orderNecassaryResources()

    def orderNecassaryResources(self):
        allResources = Resources.getAllStockedItems()
        for resource in allResources:
            if not IssOrders.hasResourceBeenOrdered(resource.itemNumber):
                if resource.quantityInStock < resource.minimumQuantity:
                    IssOrders.addOrder(Order(resource.itemNumber,  resource.minimumQuantity))

    def shuttleArived(self,shuttle):
        shuttle.location = Location.SPACE_STATION
        self.loadInventory(shuttle)
        shuttle.items = []

        for astronaut in shuttle.passengers:
            astronaut.setLocation(Location.SPACE_STATION)
            self.astronauts.append(astronaut)
        shuttle.passengers = []

    def loadInventory(self,shuttle):
        for orderedItem in shuttle.items:
            orderedItem.state = OrderState.ARRIVED
            Resources.consumeItemStock(orderedItem.itemNumber,-orderedItem.quantity)

    def releaseO2(self):
        if self.oxogenCanister.getAmount() < 0:
            print("Run out of oxygen")
        amountToConsume = 20
        self.oxogenCanister.removeAmount(amountToConsume)
        self.air.addO2(amountToConsume)

    def orderO2CanisterGas(self):
        IssOrders.addOrder(Order(OxygenResourceNumber,1000))

class OrderState(Enum):
    WAITING = 0,
    SHIPPED = 1,
    ARRIVED = 2

class Order:
    def __init__(self,itemNumber,quantity):
        self.itemNumber = itemNumber
        self.quantity = quantity
        self.state = OrderState.WAITING

    def setShipped(self):
        self.state = OrderState.SHIPPED

    def setArrived(self):
        self.state = OrderState.ARRIVED

class IssOrders:
    orders = []

    @staticmethod
    def getOrders():
        return IssOrders.orders

    @staticmethod
    def addOrder(order):
        IssOrders.orders.append(order)

    @staticmethod
    def getNextOrder():
        if len(IssOrders.orders) != 0:
            return IssOrders.orders[0]
    @staticmethod
    def removeNextOrder():
        if len(IssOrders.orders) != 0:
            IssOrders.orders = IssOrders.orders[1:]

    @staticmethod
    def getPendingOrders():
        pendingOrders = []
        for order in IssOrders.orders:
            if order.state == OrderState.WAITING:
                pendingOrders.append(order)
        return pendingOrders

    @staticmethod
    def hasResourceBeenOrdered(itemNumber):
        for order in IssOrders.getOrders():
            if order.itemNumber == itemNumber and order.state != OrderState.ARRIVED:
                return True
        return False

shuttles = [Shuttle(),Shuttle(),Shuttle()]
unMannedShuttles = [Shuttle(),Shuttle()]
spaceStation = SpaceStation()

def update():
    moveFlyingShuttles()
    shipPendingOrders()
    returnUnmannedShuttles()
    spaceStation.update()

def returnUnmannedShuttles():
    for shuttle in unMannedShuttles:
        if shuttle.location == Location.SPACE_STATION:
            spaceStation.docks[shuttle.destination].state = DockState.FREE
            shuttle.launchToEarth()

def shipPendingOrders():
        pendingOrders = IssOrders.getPendingOrders()
        if len(pendingOrders) != 0:
            shuttle = getNextAvailiableUnmannedShuttle()
            if shuttle != None:
                dockNo = getNextAvailbleDockNo()
                if dockNo != None:
                    for order in pendingOrders:
                        shuttle.addOrderedItem(order)
                        order.state = OrderState.SHIPPED
                    shuttle.launch(dockNo)
                    spaceStation.docks[dockNo].state = DockState.ALLOCATED

def getNextAvailbleDockNo():
    dockNo = 0
    for dock in spaceStation.docks:
        if dock.state == DockState.FREE:
            return dockNo
        dockNo += 1
    return None

def getNextAvailiableUnmannedShuttle():
    for shuttle in unMannedShuttles:
        if shuttle.location == Location.EARTH:
            return shuttle

def getNextAvailiableShuttle():
    for shuttle in shuttles:
        if shuttle.location == Location.EARTH:
            return shuttle

def moveFlyingShuttles():
    shuttleNo = 1
    allShuttles = shuttles + unMannedShuttles
    for shuttle in allShuttles:
        if shuttle.flying:
            shuttle.fly()
            if shuttle.percentage >= 100:
                shuttle.stopFlying()
                if shuttle.destination is not None:
                    dockNo = shuttle.destination
                    spaceStation.docks[dockNo].state = DockState.OCCUPIED
                    spaceStation.shuttleArived(shuttle)
                else:
                    shuttleArrivedAtEarth(shuttle)
        shuttleNo += 1

def shuttleArrivedAtEarth(shuttle):
    shuttle.location = Location.EARTH
    shuttle.items = []
    for astronaut in shuttle.passengers:
        astronaut.setLocation(Location.EARTH)
    shuttle.clearPassengers()

def getIssOxogenLevel():
    return spaceStation.oxogenCanister.getAmount()

def getIssAstronautsOnBoard():
    return Astronauts.getAstronautsAtLocation(Location.SPACE_STATION)

def getStatesOfShuttles():
    return addTypeOfShuttle(shuttles,ShuttleType.MANNED) + addTypeOfShuttle(unMannedShuttles,ShuttleType.UN_MANNED)

def addTypeOfShuttle(shuttles,type):
    shuttleStates = []
    shuttleNo = 1
    for shuttle in shuttles:
        destination = ''
        toEarth = shuttle.destination == None
        if shuttle.flying == False:
            destination += 'Not flying'
        elif toEarth:
            destination += 'Earth'
        else:
            destination += 'ISS dock number ' + str(shuttle.destination)
        nextState = ShuttleState(shuttleNo,shuttle.flying,destination,shuttle.percentage,shuttle.location,type)
        shuttleStates.append(nextState)
        shuttleNo += 1

    return shuttleStates


def doesShuttleCarryOxogen(shuttle):
    for item in shuttle.items:
        if item.itemNumber == OxygenResourceNumber and item.state != OrderState.ARRIVED:
            return True
    return False

Schedular.addToSchedule(update, 1)

def getAstronauts():
    return Astronauts.getAstronauts()

def launchShuttleToAppropriateDestination(shuttleNo,astronautIds):
    if shuttles[shuttleNo].location == Location.EARTH:
        launchShuttleFromEarth(shuttleNo,astronautIds)
    else:
        launchShuttleFromIss(shuttleNo, astronautIds)

def launchShuttleFromEarth(shuttleNo,astronautIds):
    shuttle = shuttles[shuttleNo]
    prepareShuttleForFlight(shuttle,astronautIds)

    dockNo = getNextAvailbleDockNo()
    shuttle.launch(dockNo)
    spaceStation.docks[dockNo].state = DockState.ALLOCATED

def launchShuttleFromIss(shuttleNo, astronautIds):
    shuttle = shuttles[shuttleNo]
    prepareShuttleForFlight(shuttle,astronautIds)

    spaceStation.docks[shuttle.destination].state = DockState.FREE
    shuttle.launchToEarth()

def prepareShuttleForFlight(shuttle,astronautIds):
    astronauts = []
    for astronautId in astronautIds:
        astronaut = Astronauts.getAstronautById(astronautId)
        if astronaut != None:
            astronauts.append(astronaut)

    for astronaut in astronauts:
        shuttle.addPassenger(astronaut)
        astronaut.setLocation(Location.FLYING)

def isShuttleOnEarth(shuttleNumber):
    try:
        return shuttles[shuttleNumber].location == Location.EARTH
    except:
        return False