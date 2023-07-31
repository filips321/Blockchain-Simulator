class Blockchain:
    blockList: []

    def __init__(self):
        self.blockList = []

    def calculateBlockchainLength(self, block):
        currentLength = 0
        lookingForBlockId = block.blockId
        for block in reversed(self.blockList):
            if block.blockId == lookingForBlockId:
                currentLength += 1
                if block.previousBlock is None:
                    return currentLength
                lookingForBlockId = block.previousBlock.blockId
        return currentLength
