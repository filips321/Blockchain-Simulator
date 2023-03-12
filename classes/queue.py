class Queue:
    events: []

    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    def deleteEvent(self, event):
        self.events.remove(event)
