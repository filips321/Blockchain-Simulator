import math
from .blockchain import Blockchain
import random
from global_land_mask import globe


class Node:
    nodeId: int
    nodeType: str  # miner / node
    averagePowPosTime = 0
    xGeography = 0
    yGeography = 0
    hashWorkingBlock: None
    neighbors: []
    availableTransactions: []
    usedTransactions: []
    blockchain: Blockchain

    def __init__(self, nodeId, nodeType, averagePowPosTime):
        self.nodeId = nodeId
        self.nodeType = nodeType
        self.averagePowPosTime = averagePowPosTime
        self.xGeography = self.generateLocation()[0]
        self.yGeography = self.generateLocation()[1]
        self.neighbors = []
        self.availableTransactions = []
        self.usedTransactions = []
        self.blockchain = Blockchain()
        self.hashWorkingBlock = None

    def generateLocation(self):  # TODO - sprawdzic jak generuje, dodac proporcjonalna ilosc uzytkownik per kontynent (np. 0 na antarktydzie, duzo w USA)
        while True:
            xTemp = random.uniform(-90, 90)
            yTemp = random.uniform(-180, 180)
            if globe.is_land(xTemp, yTemp):
                return xTemp, yTemp

    def declareMiningTime(self):
        miningTime = self.exponentialDistribution(self.averagePowPosTime)
        return miningTime

    def exponentialDistribution(self, averageTime):
        time = -math.log(1 - random.uniform(0, 1)) / (1 / averageTime)
        return time

    def checkTransactionDuplicate(self, transaction):
        if transaction in self.availableTransactions or transaction in self.usedTransactions:
            return True
        else:
            return False

    def checkBlockDuplicate(self, block):
        if block in self.blockchain.blockList:
            return True
        else:
            return False

    def printNeighbors(self):
        string = ''
        for neighbor in self.neighbors:
            string += str(neighbor.nodeId) + ' '
        return string

    def updateUsedTransactions(self, block):
        self.usedTransactions.extend(block.transactions)
