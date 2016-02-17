from psychopy import parallel

class Signal():

    def __init__(self, port):
        parallel.setPortAddress(port) #address for parallel port on many machines
        self.disabled = False

    def disable(self):
        self.disabled = True

    def triggerPeak(self, pinNumber):
        if self.disabled:
            return

        for k in range(20):
            parallel.setPin(pinNumber, 1) #TRIGGER be!
        for k in range(20):
            parallel.setData(0) #TRIGGER ki!

    def reset(self):
        if self.disabled:
            return

        for k in range(20):
            parallel.setData(0) #TRIGGER!
