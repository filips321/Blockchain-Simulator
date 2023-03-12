from .node import Node

class Block:
    blockMaxSize: int
    blockCreationTime: float
    startingNode: Node
    transactions = []

    def __init__(self, blockCreationTime, blockMaxSize, startingNode):
        self.blockMaxSize = blockMaxSize
        self.blockCreationTime = blockCreationTime
        self.startingNode = startingNode
