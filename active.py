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
from dataCollector import DataCollector
from controller import Controller
from config import Config

signal = Signal(Config.parallelPort)

if Config.parallelDisabled:
    signal.disable()

personData = View.collectPersonData(u'AKTÍV')

male = (personData['nem'] == u"férfi")
right = (personData['kez'] == u"jobb")

# pin number 2 for right hand and port number 3 for left hand
if right:
    pinNumber = 2
else:
    pinNumber = 3

dataCollector = DataCollector('aktiv', personData['sorszam'],  personData['nem'],  personData['kez'])

if not dataCollector.openFile():
    View.showErrorAndQuit(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')

size = [1366, 768]

view = View(size, Config.fullscreen)
controller = Controller(view)

view.quit = controller.quit

view.setHands(male, right)

controller.loadThresholds()

framerate_ms = view.measureFrameRate()
print framerate_ms

measurementClock = core.Clock()
test_clock = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)

stimulus_interval = int(round(300 / framerate_ms, 0))

view.continueScreen(u'Üdvözlő képernyő')

## Practicing - Myo
## the same as the next one, just the participant has a feedback.
## she can continue if she reach a level. there's no reinforcement of control
ACC = 0
jovalasz = 0
gyakblokk =0
gyak_trialszam = 15
signal.reset()
while True:
    for i in range (gyak_trialszam):
        event.clearEvents(eventType='keyboard')
        measurementClock.reset()

        view.drawFixation()

        v=[]
        while True:
            controller.checkQuit()
            controller.drawIntensity()
            view.drawFixation()
            if controller.isGesture():
                waitTime = measurementClock.getTime()
                break

        controller.checkQuit()

        print str(waitTime)
        feedback = str(round(waitTime, 2)) + ' mp'

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

    gyakblokk +=1
    osszesValasz = gyak_trialszam*gyakblokk
    print 'jovalasz: ',jovalasz
    print osszesValasz
    jovalasz = float(jovalasz)
    ACC = float(jovalasz/(osszesValasz)*100)
    if ACC>=80:
        break

view.continueScreen(u'Vége a gyakorlásnak', u'Ha készen áll, nyomja meg a SPACE gombot')

# after the gesture the hand drawn, reinforcement of control comes randomly
trialszam = Config.trialszam
lista = [0, 1, 2, 3, 4, 5, 6]
ujszam = -1
for i in range (trialszam):
    view.drawFixation()
    core.wait(1.5)

    while True:
        controller.checkQuit()
        controller.drawIntensity()
        view.drawFixation()
        if controller.isGesture():
            signal.triggerPeak(pinNumber)
            for st2 in range (stimulus_interval):
                view.drawHand()
            break

    controller.checkQuit()

    if (i+1) == 15 or (i+1) == 36 or (i+1) == 57 or (i+1) == 78 or (i+1) == 99:
        szam = random.choice(lista)
        print 'szam: ', szam
        ujszam = (i+1)+szam
    print 'ujszam: ',ujszam
    if (i+1) == ujszam:
        random.shuffle(positions)
        controller.induction(positions)

view.continueScreen(u'Vége')

controller.quit()