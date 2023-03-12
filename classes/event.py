from .node import Node
from .transaction import Transaction
from .block import Block


class Event:
    eventType: str  # newBlock / newTransaction / propagateTransaction / propagateBlock
    eventTime: float
    node: Node
    currentTime: float
    transaction: Transaction
    block: Block

    def __init__(self, currentTime, eventType, eventTime, node):
        self.currentTime = currentTime
        self.eventType = eventType
        self.eventTime = eventTime
        self.node = node

        self.printEventInfo()

    def printEventInfo(self):
        match self.eventType:
            case 'newBlock':
                print('[' + str(round(self.currentTime, 2)) + ']' + ' NEW EVENT SCHEDULED - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 2)) + ', starting node: ' + str(self.node.nodeId))
            case 'newTransaction':
                print('[' + str(round(self.currentTime, 2)) + ']' + ' NEW EVENT SCHEDULED - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 2)) + ', starting node: ' + str(self.node.nodeId))
            case 'propagateTransaction':
                print('[' + str(round(self.currentTime, 2)) + ']' + ' NEW EVENT SCHEDULED - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 2)) + ', starting node: ' + str(self.node.nodeId))
            case 'propagateBlock':
                print('[' + str(round(self.currentTime, 2)) + ']' + ' NEW EVENT SCHEDULED - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 2)) + ', starting node: ' + str(self.node.nodeId))
            case _:
                print('UNEXPECTED EVENT')