#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui
import collections


class View():
    def __init__(self, size, fullscreen=False):
        self.size = size
        self.win = visual.Window(size, monitor="testMonitor", color='Black', allowGUI=True, units='cm',
                                     waitBlanking=True, fullscr=fullscreen)
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
        self.intensityText = visual.TextStim(self.win, text=u'', alignHoriz='center', alignVert='center', pos=(-10.0, -10.0),
                                          color='white', height=1, units='cm', wrapWidth=27, font='courier new')

        self.rateSAJAT_text = visual.TextStim(self.win, text = u'Mennyire érzed magadénak a képernyőn látható kezet? Értékeld az alábbi csúszka segítségével!', alignHoriz='center', alignVert='center',  pos = (-1, -6),wrapWidth = 25, color='white', height = 0.5, units = 'cm', font='courier new')
        self.rateSAJAT_scale = visual.RatingScale(self.win, labels = [u"\nEgyáltalán nem érzem magamének", u"\nKözepesen érzem magaménak", u"\nTeljesen magaménak érzem"], textColor='LightGrey', marker='triangle', markerStart = 0, markerColor='dimgray', acceptPreText=u'értekeld!', acceptText=u'OK',textSize=0.7, scale=None, stretch = 2.40, low=-100, high=100, precision=1, showValue=False, lineColor='grey', pos = (0, -0.7))
        self.rateHAS_text = visual.TextStim(self.win, text = u'Mennyire érzed hasonlónak a képernyőn látható kezet a saját kezedhez képest?\nÉrtékeld az alábbi csúszka segítségével!', alignHoriz='center', alignVert='center',  pos = (-1, -6),wrapWidth = 25, color='white', height = 0.5, units = 'cm', font='courier new')
        self.rateHAS_scale = visual.RatingScale(self.win, labels = [u"\nEgyáltalán nem érzem hasonlónak", u"\nKözepesen érzem hasonlónak", u"\nTeljesen hasonlónak érzem"], textColor='LightGrey', marker='triangle', markerStart = 0, markerColor='dimgray', acceptPreText=u'értekeld!', acceptText=u'OK',textSize=0.7, scale=None, stretch = 2.40, low=-100, high=100, precision=1, showValue=False, lineColor='grey', pos = (0, -0.7))

    def getSize(self):
        return self.size

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

    def getRating(self):
        self.setHandPosition((0, 2))
        while self.rateHAS_scale.noResponse:
            self.hand.draw()
            self.rateHAS_text.draw()
            self.rateHAS_scale.draw()
            self.win.flip()
        rating_HASONLO = self.rateHAS_scale.getRating()
        while self.rateSAJAT_scale.noResponse:
            self.hand.draw()
            self.rateSAJAT_text.draw()
            self.rateSAJAT_scale.draw()
            self.win.flip()
        rating_SAJAT = self.rateSAJAT_scale.getRating()

        return rating_HASONLO, rating_SAJAT

    def drawHandGet(self):
        self.hand_get.draw()
        self.win.flip()

    def drawHand(self):
        self.hand.draw()
        self.win.flip()

    def drawIntensity(self, intensity):
        self.intensityText.setText(intensity)
        self.intensityText.draw()

    def setHandPosition(self, position):
        self.hand.pos = position
        self.setHandGetPosition()

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
            #print frrate
            FRAMES.append(frrate)

        for i in range(len(FRAMES)):
            k = float(FRAMES[i])
            k = round(FRAMES[i], 4)
            #print k
            FRAMES[i] = k

        #print FRAMES

        counts = collections.Counter(FRAMES)
        new_list = sorted(FRAMES, key=counts.get, reverse=True)  # egyes frame-ek gyakoriság szerint sorbarendezve

        #print new_list

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
        return self.stimulus.contains(self.hand.pos)#self.hand.overlaps(self.stimulus) or self.hand.contains(self.stimulus.pos)

    def setHandGetPosition(self):
        self.hand_get.pos = self.hand.pos

    def resetHandPosition(self):
        self.hand.pos = (0,0)

    def continueScreen(self, top, middle=u''):
        self.setInstructions(top, middle)
        key = event.waitKeys(keyList=['space', 'escape'])
        if key and (key[-1] == 'escape'):
            self.quit()

    def drawCenterText(self, text):
        self.centerText.setText(text)
        self.centerText.draw()
        self.win.flip()

    @staticmethod
    def collectPersonData(type, trial=False):
        #Azok az adatok, amiket a program indításkor bekér:
        expstart1=gui.Dlg(title=u'A projekt adatai - ' + type)
        expstart1.addText('')
        expstart1.addField(u'Kísérleti személy sorszáma','')
        expstart1.addField(u'Neme', choices=[u"Válassz!",u"férfi", u"nő"])
        expstart1.addField(u'Kéz', choices=[u"Válassz!",u"jobb", u"bal"])
        if trial:
            expstart1.addText('')
            expstart1.addField(u'Session','')
            expstart1.addField(u'Trialszám','')
        expstart1.show()
        if not expstart1.OK:
            core.quit()
        if expstart1.data[1] == u"Válassz!":
            expstart2 = gui.Dlg (title = u'ERROR')
            expstart2.addText(u'A résztvevő neme ismeretlen!')
            expstart2.show()
            if expstart2.OK:
                core.quit()
        elif expstart1.data[2] == u"Válassz!":
            expstart3 = gui.Dlg (title = u'ERROR')
            expstart3.addText(u'Válassz kezet!')
            expstart3.show()
            if expstart3.OK:
                core.quit()

        data =  {
            'sorszam': expstart1.data[0],
            'nem': expstart1.data[1],
            'kez': expstart1.data[2]
        }

        if trial:
            data['session'] = expstart1.data[3]
            data['trialszam'] = int(expstart1.data[4])

        return data

    @staticmethod
    def showErrorAndQuit(text):
        expstart4 = gui.Dlg (title = u'ERROR')
        expstart4.addText(text)
        expstart4.show()
        core.quit()