from .node import Node

class Block:
    blockMaxSize: int
    blockCreationTime: float
    startingNode: Node

    transactions: []

    def __init__(self, blockCreationTime, blockMaxSize, startingNode):
        self.blockMaxSize = blockMaxSize
        self.blockCreationTime = blockCreationTime
        self.startingNode = startingNode
        self.transactions = []

    def fillWithTransactions(self, availableTransactions):
        while sum(transaction.transactionSize for transaction in self.transactions) < self.blockMaxSize:
            if len(availableTransactions) > 0:
                self.transactions.append(availableTransactions[0])
                availableTransactions.pop(0)
            else:
                break
