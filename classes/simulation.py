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

    def generateNodes(self, nodes, numberOfNodes, averagePowPosTime):
        for i in range(numberOfNodes):
            generatedNode = Node(i, 'xd', averagePowPosTime, []) # TODO - ustawic typy wezlow
            nodes.append(generatedNode)
        return nodes

    def defineNeighbors(self, nodes, numberOfNeighbors):
        tempNodes = nodes.copy()
        for node in nodes:
            self.deleteFromListById(tempNodes, node.nodeId)
            while len(node.neighbors) < numberOfNeighbors:
                if len(tempNodes) == 0:
                    break
                potentialNeighbor = random.choice(tempNodes)
                if len(node.neighbors) < numberOfNeighbors and len(potentialNeighbor.neighbors) < numberOfNeighbors and potentialNeighbor not in node.neighbors:
                    node.neighbors.append(potentialNeighbor)
                    nodes[potentialNeighbor.nodeId].neighbors.append(node)
                    tempNodes = self.deleteCompleteNeighborsNodes(tempNodes, numberOfNeighbors)
        nodes = self.defineMissingNeighbors(nodes, numberOfNeighbors)
        return nodes

    def defineMissingNeighbors(self, nodes, numberOfNeighbors):
        tempNodes = nodes.copy()
        for node in nodes:
            while len(node.neighbors) < numberOfNeighbors:
                neighbor = random.choice(tempNodes)
                if node != neighbor:
                    node.neighbors.append(neighbor)
                    nodes[neighbor.nodeId].neighbors.append(node)
                    tempNodes.remove(neighbor)
        return nodes

    def deleteFromListById(self, list, id):
        for i in list:
            if i.nodeId == id:
                list.remove(i)
        return list

    def deleteCompleteNeighborsNodes(self, tempNodes, numberOfNeighbors):
        for i in tempNodes:
            if len(i.neighbors) >= numberOfNeighbors:
                tempNodes.remove(i)
        return tempNodes

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
        self.nodes = self.generateNodes(self.nodes, self.numberOfNodes, self.averagePowPosTime)
        self.nodes = self.defineNeighbors(self.nodes, self.numberOfNeighbors) # TODO - moze sie zapetlac i nie bedzie polaczenia miedzy wszystkimi wezlami (szczegolnie widoczne dla 2 sasiadow)

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
