from psychopy import core, event

class Controller():

    def __init__(self, view):
        self.view = view

    # TODO Myo
    def induction(self, positions, count=8):
        for j in range (count):
            while True:
                self.view.drawHandAndStimulus(False, positions[j])

                v = event.waitKeys()
                if v:
                    canGet = False
                    if v[-1] == 'up':
                        self.view.moveHand((0, 1))
                    elif v[-1] == 'down':
                        self.view.moveHand((0, -1))
                    elif v[-1] == 'right':
                        self.view.moveHand((1, 0))
                    elif v[-1] == 'left':
                        self.view.moveHand((-1, 0))
                    elif v[-1] == 'escape':
                        core.quit()
                    elif self.view.isHandCanGetStimulus() and v[-1] == 'space':
                        self.view.setHandGetPosition()
                        canGet = True

                    self.view.drawHandAndStimulus(canGet)
                    if canGet:
                        core.wait(0.8)
                        self.view.resetHandPosition()
                        break

        self.view.continueScreen(u'Most pihenhet egy kicsit.', u'Ha készen áll a folytatásra, nyomja meg a SPACE billentyűt.')