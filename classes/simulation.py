import random
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

    def deleteCompleteNeighborsNodes(self, tempNodes):
        for i in tempNodes:
            if len(i.neighbors) >= self.numberOfNeighbors:
                tempNodes.remove(i)
        return tempNodes

    def findShortestMiningTime(self):
        miningTimes = []
        for i in self.nodes:
            miningTime = i.declareMiningTime()
            miningTimes.append((i, miningTime))
        shortestMiningTime = min(miningTimes, key=lambda x: x[1])
        return shortestMiningTime

    def updateAvailableTransactions(self, block, availableTransactions):
        for transaction in block.transactions:
            if transaction in availableTransactions:
                availableTransactions.remove(transaction)
        return availableTransactions

    def scheduleNewTransactionEvent(self, time):
        transactionEvent = Event('newTransaction', time + self.averageTransactionBreak * random.uniform(0.5, 1.5), random.choice(self.nodes))  # TODO - generowac przerwe miedzy rozkladami losowo (np. rozklad wykladniczy)
        transactionEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return transactionEvent

    def scheduleNewBlockEvent(self, time, shortestMiningTime):
        blockEvent = Event('newBlock', time + shortestMiningTime[1], shortestMiningTime[0])  # TODO - generowac przerwe miedzy rozkladami losowo (np. rozklad wykladniczy)
        blockEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return blockEvent

    def schedulePropagateTransactionEvent(self, time, transaction, neighbor):
        propagateTransactionEvent = Event('propagateTransaction', time + self.localVerificationLatency + self.propagationLatency, neighbor)  # TODO - uzaleznic propagationLatency od odleglosci miedzy sasiadami
        propagateTransactionEvent.transaction = transaction
        propagateTransactionEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return propagateTransactionEvent

    def schedulePropagateBlockEvent(self, time, block, neighbor):  # TODO
        propagateBlockEvent = Event('propagateBlock', time + self.localVerificationLatency + self.propagationLatency, neighbor)  # TODO - uzaleznic propagationLatency od odleglosci miedzy sasiadami
        propagateBlockEvent.block = block
        propagateBlockEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return propagateBlockEvent

    def startSimulation(self):
        # ustawienie stanu poczatkowego symulacji
        currentTime = 0
        self.queue = Queue()

        # poczatek symulacji - generowanie wezlow, pierwsze zdarzenie nowej transakcji, pierwsze zdarzenie nowego bloku
        self.generateNodes()
        self.defineNeighbors()  # TODO - moze sie zapetlac i nie bedzie polaczenia miedzy wszystkimi wezlami (szczegolnie widoczne dla 2 sasiadow)

        self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))
        self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime()))

        # glowna petla symulacji
        while currentTime < self.simulationTime:
            self.queue.events.sort(key=lambda x: x.eventTime)
            currentEvent = self.queue.events[0]
            currentTime = currentEvent.eventTime
            self.queue.events.pop(0)
            currentEvent.printEventInfo('CURRENT EVENT', currentTime)

            match currentEvent.eventType:
                case 'newTransaction':
                    transaction = Transaction(currentTime, self.transactionSize, currentEvent.node)
                    self.nodes[currentEvent.node.nodeId].availableTransactions.append(transaction)  # dodac transakcje do availableTransactions danego wezla

                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateTransactionEvent(currentTime, transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada

                    self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))  # nastepna transakcja
                case 'newBlock':
                    block = Block(currentTime, self.blockMaxSize, currentEvent.node)
                    block.fillWithTransactions(currentEvent.node.availableTransactions)  # zapelnia blok transakcjami
                    self.nodes[currentEvent.node.nodeId].blockchain.blockList.append(block)  # dodac block do blockchainu danego wezla
                    self.nodes[currentEvent.node.nodeId].availableTransactions = self.updateAvailableTransactions(block, currentEvent.node.availableTransactions)  # aktualizuje dostepne transakje danego wezla

                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateBlockEvent(currentTime, block, neighbor))

                    self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime()))  # TODO - wezly powinny deklarowac kiedy stworza nowy blok dopiero w momencie gdy dostana spropagowane info o nowym bloku od nowego wezla
                case 'propagateTransaction':
                    if not self.nodes[currentEvent.node.nodeId].checkTransactionDuplicate(currentEvent.transaction):  # jezeli tej transakcji nie ma w wezle jeszcze to dodaj do dostepnych transakcji i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].availableTransactions.append(currentEvent.transaction)
                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateTransactionEvent(currentTime, currentEvent.transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case 'propagateBlock':
                    if not self.nodes[currentEvent.node.nodeId].checkBlockDuplicate(currentEvent.block):  # jezeli tego bloku nie ma w blockchainie wezla jeszcze to dodaj i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].blockchain.blockList.append(currentEvent.block)
                        self.nodes[currentEvent.node.nodeId].availableTransactions = self.updateAvailableTransactions(currentEvent.block, currentEvent.node.availableTransactions)  # aktualizuje dostepne transakje danego wezla

                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateBlockEvent(currentTime, currentEvent.block, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case _:
                    print('QUEUE IS EMPTY')
