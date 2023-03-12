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
        print('[' + str(round(currentTime, 2)) + '] ' + string + ' - type: ' + self.eventType + ', time: ' + str(round(self.eventTime, 2)) + ', starting node: ' + str(self.node.nodeId) + ', neighbors: ' + self.node.printNeighbors())
