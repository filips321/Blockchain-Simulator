class Transaction:
    transactionSize: int
    transactionCreationTime: float

    def __init__(self, transactionCreationTime):
        self.transactionCreationTime = transactionCreationTime