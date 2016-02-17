#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import collections


class View():
    def __init__(self, win=None):
        if win != None:
            self.win = win
        else:
            self.win = visual.Window([1366, 768], monitor="testMonitor", color='Black', allowGUI=True, units='cm',
                                     waitBlanking=True, fullscr=True)
        self.frametest = visual.TextStim(self.win, text=u'Indítás...', alignHoriz='center', alignVert='center',
                                         pos=(0.0, 0.0), color='silver', opacity=0.6, height=0.8, units='cm')
        self.fixation = visual.TextStim(self.win, text='+', alignHoriz='center', alignVert='center', pos=(0.0, 0.0),
                                        color='Red', height=3, units='cm')
        self.stimulus = visual.Rect(self.win, width=3, height=3, units='cm', lineColor='Tomato', fillColor='Tomato',
                                    lineWidth=1.5, pos=[0, 0])
        self.instrukcio = visual.TextStim(self.win, text=u'', alignHoriz='center', alignVert='center', pos=(0.0, 0.2),
                                          color='white', height=0.5, units='cm', wrapWidth=27, font='courier new')
        self.centerText = visual.TextStim(self.win, text=u'', alignHoriz='center', alignVert='center', pos=(0.0, 0.0),
                                          color='white', height=1, units='cm', wrapWidth=27, font='courier new')

    def addHands(self, hand, hand_get):
        self.hand = hand
        self.hand_get = hand_get

    def setHands(self, male, right):

        if male:
            prefix = "m"
        else:
            prefix = "f"

        if right:
            hand = 'right'
        else:
            hand = 'left'

        self.hand = visual.ImageStim(self.win, 'images/' + prefix + '_' + hand + '_1.png', pos=(0, 0))
        self.hand_get = visual.ImageStim(self.win, 'images/' + prefix + '_' + hand + '_2.png', pos=(0, 0))

        self.hand.size /= 5.75
        self.hand_get.size /= 5.75

    def drawHand(self):
        self.hand.draw()
        self.win.flip()

    def moveHand(self, offset):
        self.hand.pos += offset

    def setInstructions(self, top, middle=u'', bottom=u''):
        self.instrukcio.setPos([0.0, 6])
        self.instrukcio.setText(top)
        self.instrukcio.draw()
        self.instrukcio.setPos([0.0, 3])
        self.instrukcio.setText(middle)
        self.instrukcio.draw()
        self.instrukcio.setPos([0.0, -3])
        self.instrukcio.setText(bottom)
        self.instrukcio.draw()
        self.win.flip()

    def measureFrameRate(self):
        # MEASURE FRAMERATE
        frametest = visual.TextStim(self.win, text=u'Indítás...', alignHoriz='center', alignVert='center',
                                    pos=(0.0, 0.0), color='silver', opacity=0.6, height=0.8, units='cm')

        fr = core.Clock()
        FRAMES = []
        for i in range(100):
            fr.reset()
            frametest.draw()
            self.win.flip()
            frrate = fr.getTime()
            print frrate
            FRAMES.append(frrate)

        for i in range(len(FRAMES)):
            k = float(FRAMES[i])
            k = round(FRAMES[i], 4)
            print k
            FRAMES[i] = k

        print FRAMES

        counts = collections.Counter(FRAMES)
        new_list = sorted(FRAMES, key=counts.get, reverse=True)  # egyes frame-ek gyakoriság szerint sorbarendezve

        print new_list

        framerate_ms = new_list[0] * 1000
        return framerate_ms

    def drawFixation(self):
        self.fixation.draw()
        self.win.flip()

    def drawHandAndStimulus(self, get, position=None):
        if position:
            self.stimulus.pos = position
        self.stimulus.draw()
        if get:
            self.hand_get.draw()
        else:
            self.hand.draw()
        self.win.flip()

    def isHandCanGetStimulus(self):
        return self.hand.overlaps(self.stimulus) or self.hand.contains(self.stimulus.pos)

    def setHandGetPosition(self):
        self.hand_get.pos = self.hand.position

    def resetHandPosition(self):
        self.hand.pos = (0,0)

    def continueScreen(self, top, middle=u''):
        self.setInstructions(top, middle)
        event.waitKeys(keyList=['space', 'escape'])
        key = event.getKeys(keyList=['space', 'escape'])
        if key and (key[-1] == 'escape'):
            core.quit()

    def drawCenterText(self, text):
        self.centerText.setText(text)
        self.centerText.draw()
        self.win.flip()
