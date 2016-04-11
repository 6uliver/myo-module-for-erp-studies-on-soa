#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#HAND PASSIVE 
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors
from view import View
from eegsignal import Signal
from dataCollector import DataCollector
from controller import Controller

signal = Signal(0x378)
signal.disable()

personData = View.collectPersonData(u'PASSZÍV')

dataCollector = DataCollector('passziv', personData['sorszam'],  personData['nem'],  personData['kez'])

if not dataCollector.openFile():
    View.showErrorAndQuit(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')

male = (personData['nem'] == u"férfi")
right = (personData['kez'] == u"jobb")

if right:
    pinNumber = 2#choose a pin to write to (2-9).
else:
    pinNumber = 3#choose a pin to write to (2-9).

size = [1366, 768]
view = View(size)
controller = Controller(view)

view.quit = controller.quit

view.setHands(male, right)

controller.measureThresholds(False, True)

framerate_ms = view.measureFrameRate()
print framerate_ms

RT = core.Clock()
st_ido = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)

st_int = int(round(300/framerate_ms, 0))

view.continueScreen(u'Üdvözlő képernyő')

trialszam = 120
ISI = [1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300, 2350, 2400, 2450]
print len(ISI)

# ISI - inter-stimulus interval
allISI =[]

for i in range (int(trialszam/len(ISI))):
    for k in ISI:
        allISI.append(k)

print allISI
print len(allISI)

lista = [0, 1, 2, 3, 4, 5, 6]
ujszam = -1
for i in  range (len(allISI)):
    allISI[i] = allISI[i]/framerate_ms
    allISI[i] = int(round(allISI[i],0))

print allISI
random.shuffle(allISI)

# valamikor trigger és rögtön kéz, néha indukció
event.clearEvents(eventType='keyboard')
for i in range (trialszam):
    controller.checkQuit()

    # stimulus onset asynchronity
    for soa in range (allISI[i]):
        controller.checkQuit()
        view.drawFixation()
    signal.triggerPeak(pinNumber)

    controller.checkQuit()

    for st2 in range (st_int):
        controller.checkQuit()
        view.drawHand()

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