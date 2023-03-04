class Queue:
    events = []

    def addEvent(self, event):
        self.events.append(event)

    def deleteEvent(self, event):
        self.events.remove(event)

