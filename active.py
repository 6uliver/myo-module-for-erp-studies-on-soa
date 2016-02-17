#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#HAND ACTIVE
#======================================================================

from __future__ import division
from psychopy import core, event
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors
from view import View
from eegsignal import Signal

signal = Signal(0x378)
view = View()

personData = View.collectPersonData()

male = (personData['nem'] == u"férfi")
right = (personData['kez'] == u"jobb")

if right:
    pinNumber = 2#choose a pin to write to (2-9).
else:
    pinNumber = 3#choose a pin to write to (2-9).

view.setHands(male, right)

filename = personData['sorszam'] +'_HandMYO_aktiv_'+ personData['nem'] + '_'+personData['kez']+'.txt'

#LOGFILE-OK
try:
    output_file = codecs.open(filename, 'r',encoding='utf-8')
except IOError:
    #letezo=0
    print 'még nincs elmentve ilyen fájl, valószínűleg ez az első alkalom az indítások közül'
    #Ha a progi először indul, létrehozatjuk vele a 3 logfile-t
    output_file = codecs.open(filename,'a', encoding = 'utf-8')  #a személy válaszai
else:
    #letezo=1
    View.showErrorAndQuit(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')

framerate_ms = view.measureFrameRate()
print framerate_ms

measurementClock = core.Clock()
test_clock = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)

stimulus_interval = int(round(300 / framerate_ms, 0))

view.continueScreen(u'Üdvözlő képernyő')

##GYAKORLÁS - Myo
ACC = 0
jovalasz = 0
gyakblokk =0
gyak_trialszam = 15
signal.reset()
while True:
    event.clearEvents(eventType='keyboard')
    measurementClock.reset()

    while True:  #equal 1 in case of answer
        view.drawFixation()

        v=[]
        while True:
            v = event.getKeys(keyList=['space', 'escape'])
            if v != []:
                waitTime = measurementClock.getTime()
                break
            view.drawFixation()

        if v:
            print str(waitTime)
            feedback = str(round(waitTime, 2)) + ' mp'
            if v[-1] == 'space':
                signal.triggerPeak(pinNumber)
                test_clock.reset()
                for st in range (stimulus_interval):
                    view.drawHand()
                st_time = test_clock.getTime()
                print st_time
                if waitTime > 1.75:
                    jovalasz +=1
                    for st2 in range (60):
                        view.drawCenterText(feedback)
                else:
                    for st2 in range (60):
                        view.drawCenterText(feedback)
            elif v[-1] == 'escape':
                print 'Session terminated by user.'
                core.quit()

            break

    gyakblokk +=1
    osszesValasz = gyak_trialszam*gyakblokk
    print 'jovalasz: ',jovalasz
    print osszesValasz
    jovalasz = float(jovalasz)
    ACC = float(jovalasz/(osszesValasz)*100)
    if ACC>=80: #15
        break

view.continueScreen(u'Vége a gyakorlásnak', u'Ha készen áll, nyomja meg a SPACE gombot')

#fixációs kereszt amíg meg nem nyom egy gombot
#ingerbemutatás x ideig
trialszam = 100
lista = [0, 1, 2, 3, 4, 5, 6]
ujszam = -1
for i in range (trialszam):
    view.drawFixation()
    core.wait(1.5)
    event.clearEvents(eventType='keyboard')

    while True:  #equal 1 in case of answer
        view.drawFixation()
        v=[]
        v = event.getKeys(keyList=['space', 'escape'])
        if v:
            if v[-1] == 'escape':
                print 'Session terminated by user.'
                core.quit()
            elif v[-1] == 'space':
                signal.triggerPeak(pinNumber)
                for st2 in range (stimulus_interval):
                    view.drawHand()
            break

    if (i+1) == 15 or (i+1) == 36 or (i+1) == 57 or (i+1) == 78:
        szam = random.choice(lista)
        print 'szam: ', szam
        ujszam = (i+1)+szam
    print 'ujszam: ',ujszam
    if (i+1) == ujszam:
        random.shuffle(positions)
        for i in range (8):
            while True:
                view.drawHandAndStimulus(False, positions[i])

                v = event.waitKeys()
                if v:
                    canGet = False
                    if v[-1] == 'up':
                        view.moveHand((0, 1))
                    elif v[-1] == 'down':
                        view.moveHand((0, -1))
                    elif v[-1] == 'right':
                        view.moveHand((1, 0))
                    elif v[-1] == 'left':
                        view.moveHand((-1, 0))
                    elif v[-1] == 'escape':
                        core.quit()
                    elif view.isHandCanGetStimulus() and v[-1] == 'space':
                        view.setHandGetPosition()
                        canGet = True

                    view.drawHandAndStimulus(canGet)
                    if canGet:
                        core.wait(0.8)
                        view.resetHandPosition()
                        break

        view.continueScreen(u'Most pihenhet egy kicsit.', u'Ha készen áll a folytatásra, nyomja meg a SPACE billentyűt.')

view.continueScreen(u'Vége')
