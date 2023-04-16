import itertools


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

    def findStaleBlocks(self, numberOfConfirmationBlocks): # TODO przetestowac
        lastBlockId = self.blockList[-1].blockId
        confirmedBlockId = lastBlockId - numberOfConfirmationBlocks
        staleBlockIds = []
        for block in self.blockList:
            if block.previousBlockId == confirmedBlockId:
                return staleBlockIds

        staleBlockIds.append(confirmedBlockId)
        while True:
            for block in self.blockList:
                if block.blockId == confirmedBlockId:
                    confirmedBlockId = block.previousBlockId
                    break
            for block in self.blockList:
                if block.previousBlockId == confirmedBlockId:
                    return staleBlockIds
            staleBlockIds.append(confirmedBlockId)
