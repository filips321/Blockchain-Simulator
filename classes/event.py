from .node import Node
from .transaction import Transaction
from .block import Block


class Event:
    eventType: str  # newBlock / newTransaction / propagateTransaction / propagateBlock
    eventTime: float
    node: Node
    transaction: Transaction
    block: Block

    def __init__(self, eventType, eventTime, node):
        self.eventType = eventType
        self.eventTime = eventTime
        self.node = node

    def printEventInfo(self, string, currentTime):
        if self.eventType == 'newBlock':
            print('[' + str(round(currentTime, 3)) + '] ' + string + ' - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 3)) + ', starting node: ' + str(self.node.nodeId) + ', neighbors: ' + self.node.printNeighbors())
        if self.eventType == 'propagateBlock':
            print('[' + str(round(currentTime, 3)) + '] ' + string + ' - type: ' + self.eventType + ', blockID: ' + str(self.block.blockId) + ', time: ' + str(round(self.eventTime, 3)) + ', starting node: ' + str(self.node.nodeId) + ', neighbors: ' + self.node.printNeighbors())
        if self.eventType == 'newTransaction':
            print('[' + str(round(currentTime, 3)) + '] ' + string + ' - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 3)) + ', starting node: ' + str(self.node.nodeId) + ', neighbors: ' + self.node.printNeighbors())
        if self.eventType == 'propagateTransaction':
            print('[' + str(round(currentTime, 3)) + '] ' + string + ' - type: ' + self.eventType + ', transactionID: ' + str(self.transaction.transactionId) + ', time: ' + str(round(self.eventTime, 3)) + ', starting node: ' + str(self.node.nodeId) + ', neighbors: ' + self.node.printNeighbors())
