from Backend.DataStore import AccessLayer
from Backend.DataStore.Connection import Connection

class Resources:
    @staticmethod
    def getItemStockQuantity(itemNumber):
        return AccessLayer.getItemStockQuantity(itemNumber)

    @staticmethod
    def consumeItemStock(itemNumber,quantity):
        AccessLayer.consumeItemStock(itemNumber,quantity)

    @staticmethod
    def getAllStockedItems():
        rows = AccessLayer.getAllStockedItems()
        states = []
        for row in rows:
            states.append(ResourceState(row[0],row[1],row[2],row[3]))
        return states

class ResourceState:
    def __init__(self,itemNumber ,itemDescription, quantityInStock, minimumQuantity):
        self.itemNumber = itemNumber
        self.itemDescription = itemDescription
        self.quantityInStock = quantityInStock
        self.minimumQuantity = minimumQuantity