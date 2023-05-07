import cProfile
import sys
from classes import simulation


# starting parameters
simulationTime = 100 # [s]
numberOfNodes = 500
minersProportion = 0.1 # proporcja liczby gornikow do full nodes (miners/fullNodes), zakres 0-1 (np. 0.2 znaczy ze 20% to gornicy)
numberOfNeighbors = 3  # [2, inf> / musi byc mniejsze od liczby wezlow
propagationLatency = 0.000005  # per km / opoznienie wynosi okolo 5us/km
localVerificationLatency = 0.00001  # opoznienie wynikajace z weryfikacji poprawnosci transakcji/bloku TODO sprawdzic ile powinna wynosic ta wartosc okolo
blockMaxSize = 1000  # [kB] domyslnie dla BTC jest 1MB (1000kB), transakcje sa zapisywane w bloku do momentu wygenerwoania nowego
averageTransactionSize = 0.35  # [kB] srednio jedna transakcja to okolo 300-400B (0.3-0.4kB)
averageTransactionsBreak = 0.4  # [s] dla BTC srednio transakcje co 0.3s czyli okolo 3 transakcje na sekunde
averagePowPosTime = 100
numberOfConfirmationBlocks = 6  # po tylu kolejnych blokach, blok i transakcje w nim zawarte sa potwierdzone

if __name__ == '__main__':
    # save console output to file
    # with open('output.txt', 'w') as f:
    #     sys.stdout = f

    # simulation start + logs printing
    print('--------------- SIMULATION LOGS ---------------')
    simulation = simulation.Simulation(simulationTime, numberOfNodes, minersProportion, numberOfNeighbors, averageTransactionsBreak, averagePowPosTime, propagationLatency, localVerificationLatency, averageTransactionSize, blockMaxSize, numberOfConfirmationBlocks)
    simulation.startSimulation()

    # simulation properties printing
    simulation.printSimulationProperties()

    # simulation input printing
    simulation.printSimulationInput()

    # metrics calculation and printing
    simulation.calculateSimulationMetrics()

    # stop saving console output to file
    # sys.stdout = sys.__stdout__
