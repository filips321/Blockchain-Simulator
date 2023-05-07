import collections
import math
import random
import geopy.distance
from .calculator import Calculator
from .node import Node
from .queue import Queue
from .event import Event
from .transaction import Transaction
from .block import Block


class Simulation:
    simulationTime: int
    numberOfNodes: int
    minersProportion: float
    numberOfNeighbors: int
    averagePowPosTime: float
    averageTransactionBreak: float
    propagationLatency: int
    localVerificationLatency: int
    transactionSize: int
    blockMaxSize: int
    numberOfConfirmationBlocks: int
    nodes: []
    queue: Queue
    staleBlocks: []
    calculator: Calculator
    confirmedTransactions = []
    confirmedBlocks = []

    def __init__(self, simulationTime, numberOfNodes, minersProportion, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, transactionSize, blockMaxSize, numberOfConfirmationBlocks):
        self.simulationTime = simulationTime
        self.numberOfNodes = numberOfNodes
        self.minersProportion = minersProportion
        self.numberOfNeighbors = numberOfNeighbors
        self.averageTransactionBreak = averageTransactionsBreak
        self.averagePowPosTime = averagePowPosTime
        self.propagationLatency = propagationLatency
        self.localVerificationLatency = localVerificationLatency
        self.transactionSize = transactionSize
        self.blockMaxSize = blockMaxSize
        self.numberOfConfirmationBlocks = numberOfConfirmationBlocks
        self.nodes = []
        self.confirmedTransactions = []
        self.confirmedBlocks = []
        self.staleBlocks = []


    # CORE SIMULATION FUNCTION
    def startSimulation(self):
        # ustawienie stanu poczatkowego symulacji
        currentTime = 0
        currentNumberOfBlocks = 0
        currentNumberOfTransactions = 0
        self.queue = Queue()

        # poczatek symulacji - generowanie wezlow, pierwsze zdarzenie nowej transakcji, pierwsze zdarzenie nowego bloku
        self.generateNodes()
        self.defineNeighbors()

        self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))
        self.queue.events.extend(self.scheduleInitialBlockEvents(currentTime))

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
                    transaction = Transaction(currentNumberOfTransactions, currentTime, self.transactionSize, currentEvent.node)
                    currentNumberOfTransactions += 1
                    self.nodes[currentEvent.node.nodeId].availableTransactions.append(transaction)  # dodac transakcje do availableTransactions danego wezla

                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateTransactionEvent(currentEvent.node, currentTime, transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada

                    self.queue.events.append(self.scheduleNewTransactionEvent(currentTime))  # nastepna transakcja
                case 'newBlock':
                    block = Block(currentNumberOfBlocks, currentTime, self.blockMaxSize, currentEvent.node, currentEvent.node.hashWorkingBlock)
                    currentNumberOfBlocks += 1
                    block.fillWithTransactions(currentEvent.node.availableTransactions)  # zapelnia blok transakcjami i aktualizuje dostepne transakcje danego wezla
                    self.nodes[currentEvent.node.nodeId].updateUsedTransactions(block)
                    self.nodes[currentEvent.node.nodeId].blockchain.blockList.append(block) # dodac block do blockchainu danego wezla

                    for neighbor in currentEvent.node.neighbors:
                        self.queue.events.append(self.schedulePropagateBlockEvent(currentEvent.node, currentTime, block, neighbor))

                    self.queue.events.append(self.scheduleNewBlockEvent(currentTime, currentEvent.node))  # wezel deklaruje kiedy stworzy nowy blok
                    currentEvent.node.hashWorkingBlock = block # zmiana aktualnego haszu bloku nad ktorym aktualnie pracuje wezel po stworzeniu bloku

                    confirmedBlock = self.confirmBlock(currentEvent.node.nodeId, currentTime) # zatwierdzanie waznosci bloku stworzonego o 'numberOfConfirmationBlocks' blokow wczesniej (dla BTC 6)
                    if confirmedBlock is not None:
                        self.confirmTransactions(confirmedBlock, currentTime) # TODO uproszczenie ze czas zatwierdzenia transakcji dla wszystkich wezlow dzieje sie w tym samym momencie gdy stworzy sie potwierdzajacy blok w jednym wezle
                        self.updateStaleBlocks(confirmedBlock, currentEvent.node.nodeId)

                case 'propagateTransaction':
                    if not self.nodes[currentEvent.node.nodeId].checkTransactionDuplicate(currentEvent.transaction):  # jezeli tej transakcji nie ma w wezle jeszcze to dodaj do dostepnych transakcji i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].availableTransactions.append(currentEvent.transaction)
                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateTransactionEvent(currentEvent.node, currentTime, currentEvent.transaction, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case 'propagateBlock':
                    if not self.nodes[currentEvent.node.nodeId].checkBlockDuplicate(currentEvent.block):  # jezeli tego bloku nie ma w blockchainie wezla jeszcze to dodaj i propaguj dalej
                        self.nodes[currentEvent.node.nodeId].blockchain.blockList.append(currentEvent.block)
                        self.nodes[currentEvent.node.nodeId].availableTransactions = self.updateAvailableTransactions(currentEvent.block, currentEvent.node.availableTransactions)
                        self.nodes[currentEvent.node.nodeId].updateUsedTransactions(currentEvent.block)

                        if self.nodes[currentEvent.node.nodeId].nodeType == 'miner':
                            if currentEvent.node.hashWorkingBlock is None or currentEvent.node.blockchain.calculateBlockchainLength(currentEvent.block) > currentEvent.node.blockchain.calculateBlockchainLength(currentEvent.node.hashWorkingBlock):  # zmienic wydarzenie nowego bloku tylko w momencie nowo dodany blok do blockchainu tworzy nowy najdluzszy lancuch
                                self.queue.events.remove(self.findBlockEvent(self.nodes[currentEvent.node.nodeId]))  # znalezc w kolejce zdarzenie wykopania nowego bloku przez aktualnie badany wezel i je usunac
                                self.queue.events.append(self.scheduleNewBlockEvent(currentTime, currentEvent.node))  # dodac nowe zdarzenie wykopania bloku
                                currentEvent.node.hashWorkingBlock = currentEvent.block  # zmiana aktualnego haszu bloku nad ktorym aktualnie pracuje wezel po stworzeniu bloku

                        for neighbor in currentEvent.node.neighbors:
                            self.queue.events.append(self.schedulePropagateBlockEvent(currentEvent.node, currentTime, currentEvent.block, neighbor))  # zdarzenie propagacji do kazdego sasiada
                case _:
                    print('QUEUE IS EMPTY')


    # SIMULATION SUPPORTING FUNCTIONS
    def generateNodes(self):
        for i in range(self.numberOfNodes):
            randomNumber = random.uniform(0, 1)
            if randomNumber <= self.minersProportion:
                generatedNode = Node(i, 'miner', self.averagePowPosTime)
            else:
                generatedNode = Node(i, 'node', 0)
            self.nodes.append(generatedNode)
        if self.checkAvailableMiners() is False:
            self.nodes[0].nodeType = 'miner'
            self.nodes[0].averagePowPosTime = self.averagePowPosTime

    def checkAvailableMiners(self):
        flag = False
        for node in self.nodes:
            if node.nodeType == 'miner':
                flag = True
                return flag
        return flag

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

    def scheduleInitialBlockEvents(self, time):
        blockEvents = []
        for node in self.nodes:
            if node.nodeType == 'miner':
                blockEvent = Event('newBlock', time + node.declareMiningTime(), node)
                blockEvents.append(blockEvent)
                blockEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        #blockEvents.sort(key=lambda x: x.eventTime)
        return blockEvents

    def scheduleNewBlockEvent(self, time, node):
        blockEvent = Event('newBlock', time + node.declareMiningTime(), node)
        blockEvent.printEventInfo('NEW EVENT SCHEDULED', time)
        return blockEvent

    def findBlockEvent(self, node):
        for event in self.queue.events:
            if event.eventType == 'newBlock' and event.node == node:
                return event

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

    def confirmBlock(self, nodeId, time):
        iterationBlock = self.nodes[nodeId].blockchain.blockList[-1]
        flag = True
        for i in range(self.numberOfConfirmationBlocks):
            if iterationBlock.previousBlock is None:
                flag = False
                break
            iterationBlock = iterationBlock.previousBlock
        if flag and not bool(iterationBlock.blockConfirmationTime):
            iterationBlock.blockConfirmationTime = time
            self.confirmedBlocks.append(iterationBlock)
            return iterationBlock
        else:
            return None

    def confirmTransactions(self, confirmedBlock, time):
        for transaction in confirmedBlock.transactions:
            transaction.transactionConfirmationTime = time
            self.confirmedTransactions.append(transaction)
            for node in self.nodes:
                if transaction in node.availableTransactions:
                    node.availableTransactions.remove(transaction)


    def updateStaleBlocks(self, confirmedBlock, nodeId): # TODO cos jest zle i dw razy dodaje te same transakcje do blokow a niektorych wgl nie dodaje
        lookingForBlock = confirmedBlock.previousBlock
        potentialStaleBlocks = []
        while True:
            for block in reversed(self.nodes[nodeId].blockchain.blockList): # TODO potencjalnie mozna nie iterowac po calej liscie zeby przyspieszyc program
                if block != lookingForBlock and block != confirmedBlock and block.previousBlock == lookingForBlock:
                    if block not in self.staleBlocks:
                        potentialStaleBlocks.append(block)
                        self.staleBlocks.append(block)
                        transactionsToBeAdded = [x for x in block.transactions if x not in self.confirmedTransactions]
                        transactionsToBeAdded2 = []
                        for transaction in transactionsToBeAdded:
                            flag = True
                            for node in self.nodes:
                                if collections.Counter(node.usedTransactions)[transaction] > 1:
                                    flag = False
                                    break
                            if flag:
                                transactionsToBeAdded2.append(transaction)
                        for node in self.nodes:
                            node.availableTransactions.extend(transactionsToBeAdded2) # TODO uproszczenie ze nie ma propagacji tych transakcji tylko automatycznie sa dodawane do listy dla kazdego wezla
                            node.availableTransactions = list(dict.fromkeys(node.availableTransactions))

            if len(potentialStaleBlocks) > 0:
                lookingForBlock = potentialStaleBlocks[0]
                potentialStaleBlocks.pop(0)
            else:
                break


    # CALCULATE SIMULATION METRICS
    def calculateSimulationMetrics(self):
        self.calculator = Calculator(self.nodes, self.staleBlocks, self.confirmedBlocks, self.confirmedTransactions)
        self.calculator.calculate()


    # SIMULATION PROPERTIES PRINTING FUNCTIONS
    def printSimulationInput(self):
        print('')
        print('--------------- SIMULATION - INPUT ---------------')
        print('Simulation time [s] - ' + str(self.simulationTime))
        print('Number of nodes - ' + str(self.numberOfNodes))
        print('Miners to nodes proportion [0-1] - ' + str(self.minersProportion))
        print('Number of neighbors - ' + str(self.numberOfNeighbors))
        print('Propagation latency [s] - ' + str(self.propagationLatency))
        print('Local block/transaction verification latency [s] - ' + str(self.minersProportion))
        print('Max block size [kB] - ' + str(self.blockMaxSize))
        print('Transaction size [kB] - ' + str(self.transactionSize))
        print('Average break between new transactions [s] - ' + str(self.transactionSize))
        print('Average PoW/PoS time [s] - ' + str(self.averagePowPosTime))
        print('Number of confirmation blocks - ' + str(self.numberOfConfirmationBlocks))

    def printSimulationProperties(self):
        print('')
        print('--------------- TESTING - NODES ---------------')
        for i in self.nodes:
            print('[ID ' + str(i.nodeId) + '] Type: ' + i.nodeType + ', x: ' + str(i.xGeography) + ', y: ' + str(i.yGeography) + ', neighbors: ' + self.printNeighbors(i))
        print('')
        print('--------------- TESTING - BLOCKCHAINS ---------------')
        for i in self.nodes:
            blockchainIds = [(x.blockId, str(None if x.previousBlock is None else x.previousBlock.blockId)) for x in i.blockchain.blockList]
            print('[Node ID - ' + str(i.nodeId) + '] Blockchain: ' + str(blockchainIds))
        print('')
        print('--------------- TESTING - TRANSACTIONS ---------------')
        for i in range(len(self.nodes[0].blockchain.blockList)):
            for j in self.nodes:
                for p in j.blockchain.blockList:
                    if p.blockId == i:
                        print('[Block ID - ' + str(i) + '] Node: ' + str(j.nodeId) + ' Transactions: ' + str([x.transactionId for x in p.transactions]))
        print('')
        print('--------------- TESTING - STALE BLOCKS ---------------')
        staleBlocks = [(x.blockId, [y.transactionId for y in x.transactions]) for x in self.staleBlocks]
        if len(staleBlocks) > 0:
            for i in staleBlocks:
                print('[Stale Block ID - ' + str(i[0]) + '] Transactions: ' + str(i[1]))
        else:
            print('NO STALE BLOCKS')

    def printNeighbors(self, node):
        string = ''
        for i in node.neighbors:
            string += str(i.nodeId) + ' '
        return string
