from psychopy import parallel

class Signal():

    def __init__(self, port):
        parallel.setPortAddress(port) # set address for parallel port
        self.disabled = False

    def disable(self):
        self.disabled = True

    def triggerPeak(self, pinNumber):
        if self.disabled:
            return

        for k in range(20):
            parallel.setPin(pinNumber, 1) # trigger on
        for k in range(20):
            parallel.setData(0) # trigger off

    def reset(self):
        if self.disabled:
            return

        for k in range(20):
            parallel.setData(0) # trigger off
