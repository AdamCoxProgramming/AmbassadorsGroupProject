from enum import Enum
from .Schedular import Schedular
from .InterfaceClasses import ShuttleState

class Location(Enum):
    EARTH =0,
    FLYING =1,
    SPACE_STATION =2

class Shuttle:
    def __init__(self):
        self.flying = False
        self.percentage = 0
        self.destination = None
        self.location = Location.EARTH
        self.items = []
        self.passengers = []

    def addOrderedItem(self,orderedItem):
        self.items.append(orderedItem)

    def addPassenger(self,astronaut):
        self.passengers.append(astronaut)

    def launchToEarth(self):
        self.flying = True
        self.destination = None
        self.percentage = 0
        self.location = Location.FLYING

    def launch(self,dockNo):
        self.flying = True
        self.percentage = 0
        self.destination = dockNo
        self.location = Location.FLYING

    def fly(self):
        self.percentage += 5

    def stopFlying(self):
        self.flying = False
        self.percentage = 0

class DockState(Enum):
    OCCUPIED = 0,
    ALLOCATED = 1,
    FREE = 2

class Dock:
    def __init__(self):
        self.state = DockState.FREE

class GasCanister:
    def __init__(self):
        self.amount = 0

    def addAmount(self,amount):
        self.amount += amount

    def removeAmount(self,amount):
        self.amount -= amount

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

class SpaceStation:
    def __init__(self):
        self.docks = [Dock(), Dock(), Dock(), Dock(), Dock(), Dock()]
        self.oxogenCanister = GasCanister()
        self.oxogenCanister.addAmount(2000)
        self.carbonDioxideCanister = GasCanister
        self.air = AirSimulation()
        self.updateStation()
        Schedular.addToSchedule(self.updateStation, 1)

    def updateStation(self):
        self.update()

    def update(self):
        o2InAir = self.air.measureO2()
        #print(str(self.oxogenCanister.amount))
        if o2InAir < 7000:
            self.releaseO2()

        o2Left = self.oxogenCanister.amount
        if o2Left < 1000:
            if not self.hasOxogenBeenOrdered():
                self.orderO2CanisterGas()

    def shuttleArived(self,shuttle):
        shuttle.location = Location.SPACE_STATION
        self.loadInventory(shuttle)
        self.docks[shuttle.destination].state = DockState.FREE
        shuttle.launchToEarth()


    def loadInventory(self,shuttle):
        for orderedItem in shuttle.items:
            orderedItem.state = OrderState.ARRIVED
            if orderedItem.resourceType == ResourceType.OXYGEN:
                gasCanister = GasCanister()
                gasCanister.addAmount(2000)
                self.add02CanisterGas(gasCanister)
        shuttle.items = []

    def hasOxogenBeenOrdered(self):
        orders = IssOrders.getOrders()
        for order in orders:
            if order.resourceType == ResourceType.OXYGEN and order.state != OrderState.ARRIVED:
                return True
        return False

    def releaseO2(self):
        if self.oxogenCanister.amount < 0:
            raise Exception("Run out of oxygen")
        self.oxogenCanister.amount -= 80
        self.air.addO2(80)

    def add02CanisterGas(self,o2):
        self.oxogenCanister.addAmount(o2.amount)

    def orderO2CanisterGas(self):
        IssOrders.addOrder(Order(ResourceType.OXYGEN))

class ResourceType(Enum):
    OXYGEN = 0

class OrderState(Enum):
    WAITING = 0,
    SHIPPED = 1,
    ARRIVED = 2

class Order:
    def __init__(self,resourceType):
        self.resourceType = resourceType
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

class Astronaut:
    def __init__(self,id):
        self.id = id

    def getLocation(self):
        pass

shuttles = [Shuttle(),Shuttle(),Shuttle()]
spaceStation = SpaceStation()

def update():
    moveFlyingShuttles()
    shipPendingOrders()

def shipPendingOrders():
        pendingOrders = IssOrders.getPendingOrders()
        if len(pendingOrders) != 0:
            shuttle = getNextAvailiableShuttle()
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

def getNextAvailiableShuttle():
    for shuttle in shuttles:
        if shuttle.location == Location.EARTH:
            return shuttle

def moveFlyingShuttles():
    shuttleNo = 1
    for shuttle in shuttles:
        if shuttle.flying:
            shuttle.fly()
            if shuttle.percentage >= 100:
                shuttle.stopFlying()
                if shuttle.destination is not None:
                    dockNo = shuttle.destination
                    spaceStation.docks[dockNo].state = DockState.OCCUPIED
                    spaceStation.shuttleArived(shuttle)
                else:
                    shuttle.location = Location.EARTH

        shuttleNo += 1

def getIssOxogenLevel():
    return spaceStation.oxogenCanister.amount

def getStatesOfShuttles():
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

        nextState = ShuttleState(shuttleNo,shuttle.flying,destination,shuttle.percentage)
        shuttleStates.append(nextState)
        shuttleNo += 1

    return shuttleStates

def doesShuttleCarryOxogen(shuttle):
    for item in shuttle.items:
        if item.resourceType == ResourceType.OXYGEN and item.state != OrderState.ARRIVED:
            return True
    return False

Schedular.addToSchedule(update, 1)

def launchAShuttleFromEarth():
    shuttle = getNextAvailiableShuttle()
    if shuttle != None:
        dockNo = getNextAvailbleDockNo()
        if dockNo != None:
            shuttle.launch(dockNo)
            spaceStation.docks[dockNo].state = DockState.ALLOCATED