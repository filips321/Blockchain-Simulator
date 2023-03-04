from classes import simulation

# starting parameters
simulationTime = 100
numberOfNodes = 10
numberOfNeighbors = 3
propagationLatency = 10
localVerificationLatency = 10 # opoznienie wynikajace z weryfikacji poprawnosci transakcji/bloku
blockMaxSize = 10 # domyslnie dla BTC jest 1MB, transakcje sa zapisywane w bloku do momentu wygenerwoania nowego
transactionSize = 10 # srednio jedna transakcja to okolo 300-400B
averageTransactionsBreak = 10 # dla BTC srednio transakcje co 0.3s czyli okolo 3 transakcje na sekunde
averagePowPosTime = 10

if __name__ == '__main__':

    simulation = simulation.Simulation(simulationTime, numberOfNodes, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime)
    simulation.startSimulation()

# testing - supporting functions
    def printNeighbors(node):
        string = ''
        for i in node.neighbors:
            string += str(i.nodeId) + ' '
        return string

# testing - printing
    for i in simulation.nodes:
        print('[ID ' + str(i.nodeId) + '] Node - x: ' + str(i.xGeography) + ', y: ' + str(i.yGeography) + ', neighbors: ' + printNeighbors(i))

    for i in simulation.queue.events:
        print(i.eventType, i.eventTime)

