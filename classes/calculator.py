class Calculator:
    nodes: []
    staleBlocks: []

    def __init__(self, nodes, staleBlocks):
        self.nodes = nodes
        self.staleBlocks = staleBlocks

    def calculate(self):

        self.printCalculations()

    def printCalculations(self):
        print('')
        print('--------------- CALCULATOR - RESULTS ---------------')
