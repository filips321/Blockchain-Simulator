from .node import Node


class Block:
    blockId: int
    blockCreationTime: float
    blockMaxSize: int
    startingNode: Node
    previousBlockId: int
    transactions: []

    def __init__(self, blockId, blockCreationTime, blockMaxSize, startingNode, previousBlockId):
        self.blockId = blockId
        self.blockMaxSize = blockMaxSize
        self.blockCreationTime = blockCreationTime
        self.startingNode = startingNode
        self.previousBlockId = previousBlockId
        self.transactions = []

    def fillWithTransactions(self, availableTransactions):
        while sum(transaction.transactionSize for transaction in self.transactions) < self.blockMaxSize:
            if len(availableTransactions) > 0:
                self.transactions.append(availableTransactions[0])
                availableTransactions.pop(0)
            else:
                break
