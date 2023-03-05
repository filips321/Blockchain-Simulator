from .node import Node


class Event:
    eventType: str  # newBlock / newTransaction / propagateTransaction / propagateBlock
    eventTime: float
    startingNode: Node
    currentTime: float

    def __init__(self, currentTime, eventType, eventTime, startingNode):
        self.currentTime = currentTime
        self.eventType = eventType
        self.eventTime = eventTime
        self.startingNode = startingNode

        self.printEventInfo()

    def printEventInfo(self):
        print('[' + str(
            round(self.currentTime, 2)) + ']' + ' NEW EVENT SCHEDULED - type: ' + self.eventType + ', time: ' + str(
            round(self.eventTime, 2)) + ', starting node: ' + str(self.startingNode.nodeId))
