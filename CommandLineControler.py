
class Controller:
    """This class is the main controller for the command line interface.
    New interface states can be added to the prevStates stack(list) and the previous state can be re-started."""

    def __init__(self):
        self.prevStates = []

    def start(self,nextState):
        """This function starts the command line program from the state specified
        A state must implement a run function.
        The run function should return the next state and whether or not it is temporary or alternatively a None object.
        Returning a None object will cause the previous state to be resumed.
        The program will end when None is returned and there are no states on the stack to return to.
        pre-condition:The first state should be passed as an argument.
        post-condition:The first state will be run"""
        currNextState = nextState
        reusedState = False
        while True:
            temp = currNextState.tempoary
            if currNextState.tempoary == False and reusedState == False:
                self.prevStates.append(currNextState)
            currNextState = currNextState.nextState.run()
            if currNextState == None:
                reusedState = True
                if temp == False:
                    self.prevStates.pop()
                if len(self.prevStates) == 0:
                    return
                currNextState = self.prevStates[-1]
            else:
                reusedState = False

class NextState:
    def __init__(self,nextState,tempory):
        self.nextState = nextState
        self.tempoary = tempory