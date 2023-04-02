import math
import random
import geopy.distance
from .node import Node
from .queue import Queue
from .event import Event
from .transaction import Transaction
from .block import Block


class Simulation:
    simulationTime: int
    numberOfNodes: int
    numberOfNeighbors: int
    averagePowPosTime: float
    averageTransactionBreak: float
    propagationLatency: int
    localVerificationLatency: int
    transactionSize: int
    blockMaxSize: int
    nodes: []
    queue: Queue

    def __init__(self, simulationTime, numberOfNodes, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, transactionSize, blockMaxSize):
        self.simulationTime = simulationTime
        self.numberOfNodes = numberOfNodes
        self.numberOfNeighbors = numberOfNeighbors
        self.averageTransactionBreak = averageTransactionsBreak
        self.averagePowPosTime = averagePowPosTime
        self.propagationLatency = propagationLatency
        self.localVerificationLatency = localVerificationLatency
        self.transactionSize = transactionSize
        self.blockMaxSize = blockMaxSize
        self.nodes = []

    def generateNodes(self):
        for i in range(self.numberOfNodes):
            generatedNode = Node(i, 'xd', self.averagePowPosTime)  # TODO - ustawic typy wezlow
            self.nodes.append(generatedNode)

    def defineNeighbors(self):
        self.primAlgorithm()
        self.defineMissingNeighbors()

    def primAlgorithm(self):
        tempNodes = self.nodes.copy()
        minNode = None
        currentNode = None
        nodesIncluded = [tempNodes[0]]
        self.deleteFromListById(tempNodes, tempNodes[0].nodeId)
        while True:
            distance = 99999
            if len(tempNodes) <= 0:
                break
            for node in nodesIncluded:
                for potentialNeighbor in tempNodes:
                    tempDistance = self.calculateDistance(node, potentialNeighbor)
                    if tempDistance < distance and len(node.neighbors) < self.numberOfNeighbors:
                        distance = tempDistance
                        minNode = potentialNeighbor
                        currentNode = node
            minNode.neighbors.append(currentNode)
            currentNode.neighbors.append(minNode)
            nodesIncluded.append(minNode)
            self.deleteFromListById(tempNodes, minNode.nodeId)

    def defineMissingNeighbors(self):
        tempNodes = self.nodes.copy()
        minNode = None
        tempNodes = [node for node in tempNodes if len(node.neighbors) < self.numberOfNeighbors]
        for node in self.nodes:
            while len(node.neighbors) < self.numberOfNeighbors:
                distance = 99999
                self.deleteFromListById(tempNodes, node.nodeId)
                if len(tempNodes) <= 0:
                    break
                for potentialNeighbor in tempNodes:
                    if potentialNeighbor in node.neighbors:
                        continue
                    tempDistance = self.calculateDistance(node, potentialNeighbor)
                    if tempDistance < distance:
                        distance = tempDistance
                        minNode = potentialNeighbor
                minNode.neighbors.append(node)
                node.neighbors.append(minNode)
                if len(minNode.neighbors) >= self.numberOfNeighbors:
                    self.deleteFromListById(tempNodes, minNode.nodeId)

    def calculateDistance(self, node1, node2):
        coords1 = (node1.xGeography, node1.yGeography)
        coords2 = (node2.xGeography, node2.yGeography)
        distance = geopy.distance.distance(coords1, coords2).km
        return distance

    def deleteFromListById(self, list, id):
        for i in list:
            if i.nodeId == id:
                list.remove(i)
        return list

    def findShortestMiningTime(self):
        miningTimes = []
        for node in self.nodes:
            miningTime = node.declareMiningTime()
            miningTimes.append((node, miningTime))
        shortestMiningTime = min(miningTimes, key=lambda x: x[1])
        return shortestMiningTime

    def updateAvailableTransactions(self, block, availableTransactions):
        for transaction in block.transactions:
            if transaction in availableTransactions:
                availableTransactions.remove(transaction)
        return availableTransactions

    def exponentialDistribution(self, averageTime):
        time = -math.log(1 - random.uniform(0, 1)) / (1 / averageTime)
        return time

    def scheduleNewTransactionEvent(self, time):
        transactionEvent = Event('newTransaction', time + self.exponentialDistribution(self.averageTransactionBreak), random.choice(self.nodes))
        transactionEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return transactionEvent

    def scheduleNewBlockEvent(self, time, shortestMiningTime):
        blockEvent = Event('newBlock', time + shortestMiningTime[1], shortestMiningTime[0])
        blockEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return blockEvent

    def schedulePropagateTransactionEvent(self, currentNode, time, transaction, neighbor):
        distance = self.calculateDistance(currentNode, neighbor)
        propagationLatency = distance * self.propagationLatency
        propagateTransactionEvent = Event('propagateTransaction', time + self.localVerificationLatency + propagationLatency, neighbor)
        propagateTransactionEvent.transaction = transaction
        propagateTransactionEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return propagateTransactionEvent

    def schedulePropagateBlockEvent(self, currentNode, time, block, neighbor):
        distance = self.calculateDistance(currentNode, neighbor)
        propagationLatency = distance * self.propagationLatency
        propagateBlockEvent = Event('propagateBlock', time + self.localVerificationLatency + propagationLatency, neighbor)
        propagateBlockEvent.block = block
        propagateBlockEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return propagateBlockEvent

    def startSimulation(self):
        # ustawienie stanu poczatkowego symulacji
        currentTime = 0
        self.queue = Queue()

        # poczatek symulacji - generowanie wezlow, pierwsze zdarzenie nowej transakcji, pierwsze zdarzenie nowego bloku
        self.generateNodes()
        self.defineNeighbors()

        self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))
        self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime()))

        # glowna petla symulacji
        while currentTime < self.simulationTime:
            self.queue.events.sort(key=lambda x: x.eventTime)
            currentEvent = self.queue.events[0]
            currentTime = currentEvent.eventTime
            if currentTime > self.simulationTime:
                break
            self.queue.events.pop(0)
            currentEvent.printEventInfo('CURRENT EVENT', currentTime)

            match currentEvent.eventType:
                case 'newTransaction':
                    transaction = Transaction(currentTime, self.transactionSize, currentEvent.node)
                    self.nodes[currentEvent.node.nodeId].availableTransactions.append(transaction)  # dodac transakcje do availableTransactions danego wezla

                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateTransactionEvent(currentEvent.node, currentTime, transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada

                    self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))  # nastepna transakcja
                case 'newBlock':
                    block = Block(currentTime, self.blockMaxSize, currentEvent.node)
                    block.fillWithTransactions(currentEvent.node.availableTransactions)  # zapelnia blok transakcjami
                    self.nodes[currentEvent.node.nodeId].blockchain.blockList.append(block)  # dodac block do blockchainu danego wezla
                    self.nodes[currentEvent.node.nodeId].availableTransactions = self.updateAvailableTransactions(block, currentEvent.node.availableTransactions)  # aktualizuje dostepne transakje danego wezla

                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateBlockEvent(currentEvent.node, currentTime, block, neighbor))

                    self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime()))  # TODO - wezly powinny deklarowac kiedy stworza nowy blok dopiero w momencie gdy dostana spropagowane info o nowym bloku od nowego wezla
                case 'propagateTransaction':
                    if not self.nodes[currentEvent.node.nodeId].checkTransactionDuplicate(currentEvent.transaction):  # jezeli tej transakcji nie ma w wezle jeszcze to dodaj do dostepnych transakcji i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].availableTransactions.append(currentEvent.transaction)
                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateTransactionEvent(currentEvent.node, currentTime, currentEvent.transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case 'propagateBlock':
                    if not self.nodes[currentEvent.node.nodeId].checkBlockDuplicate(currentEvent.block):  # jezeli tego bloku nie ma w blockchainie wezla jeszcze to dodaj i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].blockchain.blockList.append(currentEvent.block)
                        self.nodes[currentEvent.node.nodeId].availableTransactions = self.updateAvailableTransactions(currentEvent.block, currentEvent.node.availableTransactions)  # aktualizuje dostepne transakje danego wezla

                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateBlockEvent(currentEvent.node, currentTime, currentEvent.block, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case _:
                    print('QUEUE IS EMPTY')
