class Blockchain:
    blockList: []

    def __init__(self):
        self.blockList = []

    def calculateBlockchainLength(self, blockId):
        currentLength = 0
        lookingForBlockId = blockId
        for block in reversed(self.blockList):
            if block.blockId == lookingForBlockId:
                currentLength += 1
                lookingForBlockId = block.previousBlockId
        return currentLength
