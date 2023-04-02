from .blockchain import Blockchain
import random
from global_land_mask import globe


class Node:
    nodeId: int
    nodeType: str  # user / miner
    averagePowPosTime = 0
    xGeography = 0
    yGeography = 0

    neighbors: []
    availableTransactions: []
    blockchain: Blockchain

    def __init__(self, nodeId, nodeType, averagePowPosTime):
        self.nodeId = nodeId
        self.nodeType = nodeType
        self.averagePowPosTime = averagePowPosTime
        self.xGeography = self.generateLocation()[0]
        self.yGeography = self.generateLocation()[1]
        self.neighbors = []
        self.availableTransactions = []
        self.blockchain = Blockchain()

    def generateLocation(self):  # TODO - sprawdzic jak generuje, dodac proporcjonalna ilosc uzytkownik per kontynent (np. 0 na antarktydzie, duzo w USA)
        while True:
            xTemp = random.uniform(-90, 90)
            yTemp = random.uniform(-180, 180)
            if globe.is_land(xTemp, yTemp):
                return xTemp, yTemp

    def declareMiningTime(self):
        miningTime = self.averagePowPosTime * random.uniform(0.5, 1.5)  # TODO - generowac na podstawie np. rozkladu wykladniczego
        return miningTime

    def checkTransactionDuplicate(self, transaction):
        if transaction in self.availableTransactions:
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
