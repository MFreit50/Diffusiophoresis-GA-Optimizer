class DataBroadcaster:
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    
    def broadcast(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)