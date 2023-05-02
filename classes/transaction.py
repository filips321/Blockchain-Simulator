from .node import Node


class Transaction:
    transactionId: int
    transactionSize: int
    transactionCreationTime: float
    transactionConfirmationTime: float
    startingNode: Node

    def __init__(self, transactionId, transactionCreationTime, transactionSize, startingNode):
        self.transactionId = transactionId
        self.transactionCreationTime = transactionCreationTime
        self.transactionSize = transactionSize
        self.startingNode = startingNode
