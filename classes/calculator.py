import statistics


class Calculator:
    nodes: []
    staleBlocks: []
    confirmedBlocks: []
    confirmedTransactions: []
    numberOfConfirmationBlocks: int

    def __init__(self, nodes, staleBlocks, confirmedBlocks, confirmedTransactions):
        self.nodes = nodes
        self.staleBlocks = staleBlocks
        self.confirmedBlocks = confirmedBlocks
        self.confirmedTransactions = confirmedTransactions

    def calculate(self):
        numberOfConfirmedBlocks = len(self.confirmedBlocks)
        numberOfConfirmedTransactions = len(self.confirmedTransactions)
        completenessOfTransactions = self.calculateTransactionsParameters()[0]
        duplicateTransactions = self.calculateTransactionsParameters()[1]
        averageTransactionConfirmationDelay = self.calculateTransactionsParameters()[2]

        numberOfStaleBlocks = len(self.staleBlocks)

        self.printCalculations(numberOfConfirmedBlocks, numberOfConfirmedTransactions, numberOfStaleBlocks, averageTransactionConfirmationDelay, completenessOfTransactions, duplicateTransactions)

    def calculateTransactionsParameters(self):
        averageTransactionConfirmationDelay = statistics.fmean([x.transactionConfirmationTime - x.transactionCreationTime for x in self.confirmedTransactions])

        completenessOfTransactions = True, None # TODO sprawdzic ta metryke czy dobrze liczy
        for i in range(len(self.confirmedTransactions)):
            for transaction in self.confirmedTransactions:
                if i == transaction.transactionId:
                    break
            else:
                for transaction in self.nodes[0].availableTransactions:
                    if i == transaction.transactionId:
                        break
                else:
                    for transaction in self.nodes[0].usedTransactions:
                        if i == transaction.transactionId:
                            break
                    else:
                        completenessOfTransactions = False, i
            if completenessOfTransactions[0] is False:
                break

        seen = set()
        duplicates = [x for x in self.confirmedTransactions if x in seen or seen.add(x)]
        if len(duplicates) > 0:
            duplicatedTransactions = True, [duplicate.transactionId for duplicate in duplicates]
        else:
            duplicatedTransactions = False, [duplicate.transactionId for duplicate in duplicates]

        return completenessOfTransactions, duplicatedTransactions, averageTransactionConfirmationDelay

    def printCalculations(self, numberOfConfirmedBlocks, numberOfConfirmedTransactions, numberOfStaleBlocks, averageTransactionConfirmationDelay, completenessOfTransactions, duplicateTransactions):
        print('')
        print('--------------- CALCULATOR - SUPPORTING CHECKS ---------------')
        print('Completeness of confirmed transactions (all indexes included) - ' + str(completenessOfTransactions[0]) + ': ' + str(completenessOfTransactions[1]))
        print('Duplicated transactions - ' + str(duplicateTransactions[0]) + ': ' + str(duplicateTransactions[1]))
        print('')
        print('--------------- CALCULATOR - RESULTS ---------------')
        print('Number of confirmed blocks - ' + str(numberOfConfirmedBlocks) + ': ' + str([x.blockId for x in self.confirmedBlocks]))
        print('Number of confirmed transactions - ' + str(numberOfConfirmedTransactions))
        print('Number of stale blocks - ' + str(numberOfStaleBlocks) + ': ' + str([x.blockId for x in self.staleBlocks]))
        print('Average transaction confirmation delay - ' + str(averageTransactionConfirmationDelay))
