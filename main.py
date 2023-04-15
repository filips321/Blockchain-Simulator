from classes import simulation

# starting parameters
simulationTime = 100
numberOfNodes = 5
numberOfNeighbors = 3  # [2, inf> / musi byc mniejsze od liczby wezlow
propagationLatency = 0.000005  # per km / opoznienie wynosi okolo 5us/km
localVerificationLatency = 0.001  # opoznienie wynikajace z weryfikacji poprawnosci transakcji/bloku TODO sprawdzic ile powinna wynosic ta wartosc okolo
blockMaxSize = 5  # domyslnie dla BTC jest 1MB, transakcje sa zapisywane w bloku do momentu wygenerwoania nowego
transactionSize = 1  # srednio jedna transakcja to okolo 300-400B
averageTransactionsBreak = 10  # dla BTC srednio transakcje co 0.3s czyli okolo 3 transakcje na sekunde
averagePowPosTime = 10

if __name__ == '__main__':
    print('')
    print('---------------SIMULATION LOGS---------------')
    simulation = simulation.Simulation(simulationTime, numberOfNodes, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, transactionSize, blockMaxSize)
    simulation.startSimulation()


    # testing - supporting functions
    def printNeighbors(node):
        string = ''
        for i in node.neighbors:
            string += str(i.nodeId) + ' '
        return string


    # testing - printing
    print('')
    print('---------------TESTING---------------')

    for i in simulation.nodes:
        print('[ID ' + str(i.nodeId) + '] Node - x: ' + str(i.xGeography) + ', y: ' + str(
            i.yGeography) + ', neighbors: ' + printNeighbors(i))
