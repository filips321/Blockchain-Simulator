from .node import Node


class Transaction:
    transactionSize: int
    transactionCreationTime: float
    startingNode: Node

    def __init__(self, transactionCreationTime, transactionSize, startingNode):
        self.transactionCreationTime = transactionCreationTime
        self.transactionSize = transactionSize
        self.startingNode = startingNode
