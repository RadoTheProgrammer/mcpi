import time
enabled = True

class Timer:

    def __init__(self,name="Timer"):
        self.tt=0
        self.name=name
        self.reset()
    def reset(self):
        self.stt=self.tt=time.time()
    def print(self,txt):
        tt=time.time()
        if enabled:
            print(f"{self.name} {tt-self.stt:07.3f} {tt-self.tt:07.3f} {txt}")
        self.tt=tt
    
t=Timer()