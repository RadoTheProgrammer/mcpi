import time
enabled = False

class Timer:

    def __init__(self,name="Timer"):
        self.tt=0
        self.name=name
        self.reset()
        self.enabled = False
    def reset(self):
        self.stt=self.tt=time.time()
    def print(self,txt):
        tt=time.time()
        if enabled or self.enabled:
            print(f"{self.name} {tt-self.stt:07.3f} {tt-self.tt:07.3f} {txt}")
        self.tt=tt
    
t=Timer()