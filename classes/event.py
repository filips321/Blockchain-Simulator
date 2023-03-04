class Event:
    eventType: str # newBlock / newTransaction / propagateTransaction / propagateBlock
    eventTime: float

    def __init__(self, eventType, eventTime):
        self.eventType = eventType
        self.eventTime = eventTime