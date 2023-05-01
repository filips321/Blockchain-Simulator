import sys
from classes import simulation

# starting parameters
simulationTime = 100
numberOfNodes = 100
minersProportion = 0.1 # proporcja liczby gornikow do full nodes (miners/fullNodes), zakres 0-1 (np. 0.2 znaczy ze 20% to gornicy)
numberOfNeighbors = 3  # [2, inf> / musi byc mniejsze od liczby wezlow
propagationLatency = 0.00005  # per km / opoznienie wynosi okolo 5us/km
localVerificationLatency = 0.001  # opoznienie wynikajace z weryfikacji poprawnosci transakcji/bloku TODO sprawdzic ile powinna wynosic ta wartosc okolo
blockMaxSize = 5  # domyslnie dla BTC jest 1MB, transakcje sa zapisywane w bloku do momentu wygenerwoania nowego
transactionSize = 1  # srednio jedna transakcja to okolo 300-400B
averageTransactionsBreak = 0.1  # dla BTC srednio transakcje co 0.3s czyli okolo 3 transakcje na sekunde
averagePowPosTime = 10
numberOfConfirmationBlocks = 6  # po tylu kolejnych blokach, blok i transakcje w nim zawarte sa potwierdzone

if __name__ == '__main__':

    # save console output to file
    # with open('output.txt', 'w') as f:
    #     sys.stdout = f

    # simulation start + logs printing
    print('--------------- SIMULATION LOGS ---------------')
    simulation = simulation.Simulation(simulationTime, numberOfNodes, minersProportion, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, transactionSize, blockMaxSize, numberOfConfirmationBlocks)
    simulation.startSimulation()

    # simulation properties printing
    simulation.printSimulationProperties()

    # metrics calculation
    simulation.calculateSimulationMetrics()

    # stop saving console output to file
    # sys.stdout = sys.__stdout__
