import statistics


class Calculator:
    nodes: []
    staleBlocks: []
    confirmedBlocks: []
    numberOfConfirmationBlocks: int

    def __init__(self, nodes, staleBlocks, numberOfConfirmationBlocks, confirmedBlocks):
        self.nodes = nodes
        self.staleBlocks = staleBlocks
        self.confirmedBlocks = confirmedBlocks
        self.numberOfConfirmationBlocks = numberOfConfirmationBlocks

    def calculate(self):
        numberOfConfirmedBlocks = len(self.confirmedBlocks)
        numberOfConfirmedTransactions = self.calculateTransactionsParameters()[0]
        completenessOfTransactions = self.calculateTransactionsParameters()[1]
        duplicateTransactions = self.calculateTransactionsParameters()[2]
        averageTransactionConfirmationDelay = self.calculateTransactionsParameters()[3]

        numberOfStaleBlocks = len(self.staleBlocks)

        self.printCalculations(numberOfConfirmedBlocks, numberOfConfirmedTransactions, numberOfStaleBlocks, averageTransactionConfirmationDelay, completenessOfTransactions, duplicateTransactions)

    def calculateTransactionsParameters(self):
        confirmedTransactions = []
        for block in self.confirmedBlocks:
            confirmedTransactions.extend(block.transactions)

        averageTransactionConfirmationDelay = statistics.fmean([x.transactionConfirmationTime - x.transactionCreationTime for x in confirmedTransactions])

        numberOfConfirmedTransactions = len(confirmedTransactions)
        completenessOfTransactions = True, None
        for i in range(numberOfConfirmedTransactions):
            for transaction in confirmedTransactions:
                if i == transaction.transactionId:
                    break
            else:
                completenessOfTransactions = False, i
            if completenessOfTransactions[0] is False:
                break

        seen = set()
        duplicates = [x for x in confirmedTransactions if x in seen or seen.add(x)]
        if len(duplicates) > 0:
            duplicatedTransactions = True, [duplicate.transactionId for duplicate in duplicates]
        else:
            duplicatedTransactions = False, [duplicate.transactionId for duplicate in duplicates]

        return numberOfConfirmedTransactions, completenessOfTransactions, duplicatedTransactions, averageTransactionConfirmationDelay

    def printCalculations(self, numberOfConfirmedBlocks, numberOfConfirmedTransactions, numberOfStaleBlocks, averageTransactionConfirmationDelay, completenessOfTransactions, duplicateTransactions):
        print('')
        print('--------------- CALCULATOR - RESULTS ---------------')
        print('Number of confirmed blocks - ' + str(numberOfConfirmedBlocks) + ': ' + str([x.blockId for x in self.confirmedBlocks]))
        print('Number of confirmed transactions - ' + str(numberOfConfirmedTransactions))
        print('Completeness of confirmed transactions (all indexes included) - ' + str(completenessOfTransactions[0]) + ': ' + str(completenessOfTransactions[1]))
        print('Duplicated transactions - ' + str(duplicateTransactions[0]) + ': ' + str(duplicateTransactions[1]))
        print('Number of stale blocks - ' + str(numberOfStaleBlocks) + ': ' + str([x.blockId for x in self.staleBlocks]))
        print('Average transaction confirmation delay - ' + str(averageTransactionConfirmationDelay))
