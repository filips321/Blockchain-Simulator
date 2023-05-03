import statistics


class Calculator:
    nodes: []
    staleBlocks: []
    confirmedTransactions: []
    confirmedBlocks: []
    numberOfConfirmationBlocks: int

    def __init__(self, nodes, staleBlocks, numberOfConfirmationBlocks, confirmedTransactions, confirmedBlocks):
        self.nodes = nodes
        self.staleBlocks = staleBlocks
        self.confirmedTransactions = confirmedTransactions
        self.confirmedBlocks = confirmedBlocks
        self.numberOfConfirmationBlocks = numberOfConfirmationBlocks

    def calculate(self):
        numberOfConfirmedBlocks = len(self.confirmedBlocks)
        numberOfConfirmedTransactions = len(self.confirmedTransactions)
        numberOfStaleBlocks = len(self.staleBlocks)
        averageTransactionConfirmationDelay = statistics.fmean([x.transactionConfirmationTime - x.transactionCreationTime for x in self.confirmedTransactions])

        self.printCalculations(numberOfConfirmedBlocks, numberOfConfirmedTransactions, numberOfStaleBlocks, averageTransactionConfirmationDelay)

    def printCalculations(self, numberOfConfirmedBlocks, numberOfConfirmedTransactions, numberOfStaleBlocks, averageTransactionConfirmationDelay):
        print('')
        print('--------------- CALCULATOR - RESULTS ---------------')
        print('Number of confirmed blocks - ' + str(numberOfConfirmedBlocks) + ': ' + str([x.blockId for x in self.confirmedBlocks]))
        print('Number of confirmed transactions - ' + str(numberOfConfirmedTransactions) + ': ' + str([x.transactionId for x in self.confirmedTransactions]))
        print('Number of stale blocks - ' + str(numberOfStaleBlocks) + ': ' + str([x.blockId for x in self.staleBlocks]))
        print('Average transaction confirmation delay - ' + str(averageTransactionConfirmationDelay))
