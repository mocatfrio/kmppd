class Progress:
    def __init__(self, queue_size, range_progress=2):
        self.counter = 0
        self.queue_size = queue_size
        self.progress = [i for i in range(range_progress, 101, range_progress)]
        self.now_progress = 0
    
    def counting(self):
        self.__print()
        self.counter += 1

    def __print(self):
        now_progress = round((self.now_progress/100) * self.queue_size)
        if self.counter == now_progress:
            print("================================")
            print("Progress", str(self.now_progress) + "%")
            self.now_progress = self.progress.pop(0)
