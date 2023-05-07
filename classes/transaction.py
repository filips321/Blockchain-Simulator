import math
import random
from .node import Node


class Transaction:
    transactionId: int
    transactionSize: int
    transactionCreationTime: float
    transactionConfirmationTime: float
    startingNode: Node

    def __init__(self, transactionId, transactionCreationTime, averageTransactionSize, startingNode):
        self.transactionId = transactionId
        self.transactionCreationTime = transactionCreationTime
        self.transactionSize = self.exponentialDistribution(averageTransactionSize)
        self.startingNode = startingNode

    def exponentialDistribution(self, averageSize):
        size = -math.log(1 - random.uniform(0, 1)) / (1 / averageSize)
        return size
