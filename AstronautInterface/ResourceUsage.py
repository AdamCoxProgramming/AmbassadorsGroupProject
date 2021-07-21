from Backend import ServerAPI
from CommandLineControler import NextState

class ResourcesState:
    def run(self):
        print("--Food State--")
        while True:
            choice = input("type 'show' or 'consume': ")
            if (choice == 'back'):
                return None
            elif (choice == 'show'):
                return NextState(DisplayItemsState(),False)
            elif (choice == 'consume'):
                #try:
                itemNumber = int(input("Enter item number to be consumed: "))
                userInputedQuantity = int(input("Enter Qty to be consumed: "))
                quantityInStock = ServerAPI.getResourceQuantity(itemNumber)
                if userInputedQuantity > 0 and userInputedQuantity <= quantityInStock:
                    ServerAPI.consumeResource(itemNumber,userInputedQuantity)
                else:
                    print("Invalid quantity entered, start again")
                #except:
                #    print("Invalid input, start again")
            else:
                print("Incorrect choice")

class DisplayItemsState():
    def run(self):
        print ("--Foods List--")
        items = ServerAPI.getAvailibleItems()
        for item in items:
            print("Item number:" + str(item.itemNumber) + ", description:" + item.itemDescription +", quantity remaining:" + str(item.quantityInStock))

        while True:
            res = input("Type 'back' when you are ready: ")
            if res == 'back':
                return None