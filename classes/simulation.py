import random
from .node import Node
from .queue import Queue
from .event import Event
from .transaction import Transaction


class Simulation:
    simulationTime: int
    numberOfNodes: int
    numberOfNeighbors: int
    averagePowPosTime: float
    averageTransactionBreak: float
    propagationLatency: int
    localVerificationLatency: int
    transactionSize: int
    nodes = []
    queue: Queue

    def __init__(self, simulationTime, numberOfNodes, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, transactionSize):
        self.simulationTime = simulationTime
        self.numberOfNodes = numberOfNodes
        self.numberOfNeighbors = numberOfNeighbors
        self.averageTransactionBreak = averageTransactionsBreak
        self.averagePowPosTime = averagePowPosTime
        self.propagationLatency = propagationLatency
        self.localVerificationLatency = localVerificationLatency
        self.transactionSize = transactionSize

    def generateNodes(self, nodes, numberOfNodes, averagePowPosTime):
        for i in range(numberOfNodes):
            generatedNode = Node(i, 'xd', averagePowPosTime, [])  # TODO - ustawic typy wezlow
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

    def findShortestMiningTime(self, nodes):
        miningTimes = []
        for i in nodes:
            miningTime = i.declareMiningTime()
            miningTimes.append((i, miningTime))
        shortestMiningTime = min(miningTimes, key=lambda x: x[1])
        return shortestMiningTime

    def scheduleNewTransactionEvent(self, time, nodes):
        transactionEvent = Event(time, 'newTransaction', time + self.averageTransactionBreak * random.uniform(0.5, 1.5), random.choice(nodes))  # TODO - generowac przerwe miedzy rozkladami losowo (np. rozklad wykladniczy)
        return transactionEvent

    def scheduleNewBlockEvent(self, time, shortestMiningTime):
        blockEvent = Event(time, 'newBlock', time + shortestMiningTime[1], shortestMiningTime[0])  # TODO - generowac przerwe miedzy rozkladami losowo (np. rozklad wykladniczy)
        return blockEvent

    def schedulePropagateTransactionEvent(self, time, transaction, node):
        propagateTransactionEvent = Event(time, 'propagateTransaction', time + self.localVerificationLatency + self.propagationLatency, node)  # TODO - uzaleznic propagationLatency od odleglosci miedzy sasiadami
        propagateTransactionEvent.transaction = transaction
        return propagateTransactionEvent

    def schedulePropagateBlockEvent(self):  # TODO
        print('')

    def startSimulation(self):
        # ustawienie stanu poczatkowego symulacji
        currentTime = 0
        self.queue = Queue()

        # poczatek symulacji - generowanie wezlow, pierwsze zdarzenie nowej transakcji, pierwsze zdarzenie nowego bloku
        self.nodes = self.generateNodes(self.nodes, self.numberOfNodes, self.averagePowPosTime)
        self.nodes = self.defineNeighbors(self.nodes, self.numberOfNeighbors)  # TODO - moze sie zapetlac i nie bedzie polaczenia miedzy wszystkimi wezlami (szczegolnie widoczne dla 2 sasiadow)

        self.queue.events.append(self.scheduleNewTransactionEvent(currentTime, self.nodes))
        self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime(self.nodes)))

        # glowna petla symulacji
        while currentTime < self.simulationTime:
            self.queue.events.sort(key=lambda x: x.eventTime)
            currentEvent = self.queue.events[0]
            currentTime = currentEvent.eventTime
            self.queue.events.pop(0)

            match currentEvent.eventType:
                case 'newTransaction':
                    transaction = Transaction(currentTime, self.transactionSize, currentEvent.node)
                    self.nodes[currentEvent.node.nodeId].availableTransactions.append(transaction)  # dodac transakcje do availableTransactions danego wezla
                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateTransactionEvent(currentTime, transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada

                    self.queue.events.append(self.scheduleNewTransactionEvent(currentTime, self.nodes))  # nastepna transakcja
                case 'newBlock':
                    self.queue.events.append(self.scheduleNewBlockEvent(currentTime, self.findShortestMiningTime(self.nodes)))  # TODO - wezly powinny deklarowac kiedy stworza nowy blok dopiero w momencie gdy dostana spropagowane info o nowym bloku od nowego wezla
                    # zapelnic blok transakcjami
                    # zaczac propagowac blok
                case 'propagateTransaction':
                    if not self.nodes[currentEvent.node.nodeId].checkTransactionDuplicate(currentEvent.transaction):  # jezeli tej transakcji nie ma w wezle jeszcze to dodaj do dostepnych transakcji i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].availableTransactions.append(currentEvent.transaction)
                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateTransactionEvent(currentTime, currentEvent.transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case 'propagateBlock':
                    # propagowac blok dalej
                    # zaaktualizowac blockchain
                    print('')
                case _:
                    print('QUEUE IS EMPTY')
