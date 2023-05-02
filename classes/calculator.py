class Calculator:
    nodes: []
    staleBlocks: []
    numberOfConfirmationBlocks: int

    def __init__(self, nodes, staleBlocks, numberOfConfirmationBlocks):
        self.nodes = nodes
        self.staleBlocks = staleBlocks
        self.numberOfConfirmationBlocks = numberOfConfirmationBlocks

    def calculate(self):
        finalBlockList = self.nodes[0].blockchain.blockList[:-self.numberOfConfirmationBlocks or None] # TODO znalezc wszystkie z czasem potwierdzenia
        numberOfConfirmedBlocks = len(finalBlockList)
        numberOfStaleBlocks = len(self.staleBlocks)
        self.printCalculations(numberOfConfirmedBlocks, numberOfStaleBlocks)

    def printCalculations(self, numberOfConfirmedBlocks, numberOfStaleBlocks):
        print('')
        print('--------------- CALCULATOR - RESULTS ---------------')
        print('Number of confirmed blocks - ' + str(numberOfConfirmedBlocks))
        print('Number of stale blocks - ' + str(numberOfStaleBlocks))
