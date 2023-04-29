from classes import simulation

# starting parameters
simulationTime = 100
numberOfNodes = 5
numberOfNeighbors = 3  # [2, inf> / musi byc mniejsze od liczby wezlow
propagationLatency = 0.000005  # per km / opoznienie wynosi okolo 5us/km
localVerificationLatency = 0.001  # opoznienie wynikajace z weryfikacji poprawnosci transakcji/bloku TODO sprawdzic ile powinna wynosic ta wartosc okolo
blockMaxSize = 5  # domyslnie dla BTC jest 1MB, transakcje sa zapisywane w bloku do momentu wygenerwoania nowego
transactionSize = 1  # srednio jedna transakcja to okolo 300-400B
averageTransactionsBreak = 0.1  # dla BTC srednio transakcje co 0.3s czyli okolo 3 transakcje na sekunde
averagePowPosTime = 10
numberOfConfirmationBlocks = 6  # po tylu kolejnych blokach, blok i transakcje w nim zawarte sa potwierdzone

if __name__ == '__main__':
    print('')
    print('---------------SIMULATION LOGS---------------')
    simulation = simulation.Simulation(simulationTime, numberOfNodes, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, transactionSize, blockMaxSize, numberOfConfirmationBlocks)
    simulation.startSimulation()


    # testing - supporting functions
    def printNeighbors(node):
        string = ''
        for i in node.neighbors:
            string += str(i.nodeId) + ' '
        return string


    # testing - printing
    print('')
    print('---------------TESTING - NODES ---------------')

    for i in simulation.nodes:
        print('[ID ' + str(i.nodeId) + '] Node - x: ' + str(i.xGeography) + ', y: ' + str(i.yGeography) + ', neighbors: ' + printNeighbors(i))

    print('')
    print('---------------TESTING - BLOCKCHAINS ---------------')

    for i in simulation.nodes:
        blockchainIds = [(x.blockId, str(x.previousBlockId)) for x in i.blockchain.blockList]
        print('[Node ID - ' + str(i.nodeId) + '] Blockchain: ' + str(blockchainIds))

    print('')
    print('---------------TESTING - TRANSACTIONS ---------------')

    for i in range(len(simulation.nodes[0].blockchain.blockList)):
        for j in simulation.nodes:
            for p in j.blockchain.blockList:
                if p.blockId == i:
                    print('[Block ID - ' + str(i) + '] Node: ' + str(j.nodeId) + ' Transactions: ' + str([x.transactionId for x in p.transactions]))
