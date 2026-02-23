class QueueManager:
    def __init__(self):
        self.queue = []

    def add(self, number):
        filename = f"{int(number):05d}.mp4"
        self.queue.append(filename)

    def next(self):
        if self.queue:
            return self.queue.pop(0)
        return None