import time
class FPS:
    def __init__(self):
        self.count = 0
        self.start_time = 0
    
    def increment(self):
        self.count += 1
    
    def start(self):
        self.start_time = time.time()
        return self

    def fps(self):
        elapsed_time = time.time() - self.start_time
        return int(self.count / elapsed_time)
    


# Multiprocessing -> Cannot find working solution for generator functions
# Multithreading -> Doesn't perform well 