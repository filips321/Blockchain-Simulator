import random

from .node import Node
from .queue import Queue
from .transaction import Transaction
from .event import Event


class Simulation:
    simulationTime: int
    numberOfNodes: int
    numberOfNeighbors: int
    averagePowPosTime: float
    averageTransactionBreak: float
    nodes = []
    queue: Queue

    def __init__(self, simulationTime, numberOfNodes, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime):
        self.simulationTime = simulationTime
        self.numberOfNodes = numberOfNodes
        self.numberOfNeighbors = numberOfNeighbors
        self.averageTransactionBreak = averageTransactionsBreak
        self.averagePowPosTime = averagePowPosTime

    def generateNodes(self):
        for i in range(self.numberOfNodes):
            generatedNode = Node(i, 'xd', self.averagePowPosTime, [])
            self.nodes.append(generatedNode)

    def defineNeighbors(self):
        tempNodes = self.nodes.copy()
        for node in self.nodes:
            self.deleteFromListById(tempNodes, node.nodeId)
            while len(node.neighbors) < self.numberOfNeighbors:
                if len(tempNodes) == 0:
                    break
                potentialNeighbor = random.choice(tempNodes)
                if len(node.neighbors) < self.numberOfNeighbors and len(potentialNeighbor.neighbors) < self.numberOfNeighbors and potentialNeighbor not in node.neighbors:
                    node.neighbors.append(potentialNeighbor)
                    self.nodes[potentialNeighbor.nodeId].neighbors.append(node)
                    tempNodes = self.deleteCompleteNeighborsNodes(tempNodes)
        self.defineMissingNeighbors()

    def defineMissingNeighbors(self):
        tempNodes = self.nodes.copy()
        for node in self.nodes:
            while len(node.neighbors) < self.numberOfNeighbors:
                neighbor = random.choice(tempNodes)
                if node != neighbor:
                    node.neighbors.append(neighbor)
                    self.nodes[neighbor.nodeId].neighbors.append(node)
                    tempNodes.remove(neighbor)

    def deleteFromListById(self, list, id):
        for i in list:
            if i.nodeId == id:
                list.remove(i)
        return list

    def deleteCompleteNeighborsNodes(self, nodeList):
        for i in nodeList:
            if len(i.neighbors) >= self.numberOfNeighbors:
                nodeList.remove(i)
        return nodeList

    def scheduleNewTransactionEvent(self, time):
        transactionEvent = Event('newTransaction',
                                 time + self.averageTransactionBreak)  # TODO - generowac przerwe miedzy rozkladami losowo (np. rozklad wykladniczy)
        return transactionEvent

    def findShortestMiningTime(self):
        miningTimes = []
        for i in self.nodes:
            miningTime = i.declareMiningTime()
            miningTimes.append(miningTime)
        shortestMiningTime = min(miningTimes)
        return shortestMiningTime

    def scheduleNewBlockEvent(self, time, shortestMiningTime):
        blockEvent = Event('newBlock',
                           time + shortestMiningTime)  # TODO - generowac przerwe miedzy rozkladami losowo (np. rozklad wykladniczy)
        return blockEvent

    def startSimulation(self):
        # ustawienie stanu poczatkowego symulacji
        currentTime = 0
        self.queue = Queue()

        # poczatek symulacji - generowanie wezlow, pierwsze zdarzenie nowej transakcji, pierwsze zdarzenie nowego bloku
        self.generateNodes()
        self.defineNeighbors() # TODO - moze sie zapetlac i nie bedzie polaczenia miedzy wszystkimi wezlami (szczegolnie widoczne dla 2 sasiadow)
        self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))
        self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime()))

        # glowna petla symulacji
        while currentTime < self.simulationTime:
            self.queue.events.sort(key=lambda x: x.eventTime)
            currentEvent = self.queue.events[0]
            currentTime = currentEvent.eventTime
            self.queue.events.pop(0)

            match currentEvent.eventType:
                case 'newTransaction':
                    self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))
                    # zaczac propagowac transakcje
                    print('hi trans')
                case 'newBlock':
                    self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime()))
                    # zapelnic blok transakcjami
                    # zaczac propagowac blok
                    print('hi block')
                case 'propagateTransaction':
                    # propagowac transakcje dalej
                    # zaaktualizowac liste dostepnych transakcji do wziecia dla gornikow
                    print('')
                case 'propagateBlock':
                    # propagowac blok dalej
                    # zaaktualizowac blockchain
                    print('')
                case _:
                    print('QUEUE IS EMPTY')
