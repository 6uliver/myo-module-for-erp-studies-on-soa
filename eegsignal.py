from psychopy import parallel

class Signal():

    def __init__(self, port):
        parallel.setPortAddress(port) #address for parallel port on many machines

    def triggerPeak(self, pinNumber):
        for k in range(20):
            parallel.setPin(pinNumber, 1) #TRIGGER be!
        for k in range(20):
            parallel.setData(0) #TRIGGER ki!

    def reset(self):
        for k in range(20):
            parallel.setData(0) #TRIGGER!
