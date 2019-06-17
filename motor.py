#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#TIME ASSESS
#HAND MOTOR
#VISUAL
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
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

personData = View.collectPersonData(u'MOTOR')

male = (personData['nem'] == u"férfi")
right = (personData['kez'] == u"jobb")

# pin number 2 for right hand and port number 3 for left hand
if right:
    pinNumber = 2
else:
    pinNumber = 3

dataCollector = DataCollector('motor', personData['sorszam'],  personData['nem'],  personData['kez'])

if not dataCollector.openFile():
    View.showErrorAndQuit(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')

size = [1366, 768]

view = View(size, Config.fullscreen)
controller = Controller(view)

view.quit = controller.quit

view.setHands(male, right)

controller.loadThresholds()

RT = core.Clock()
st_ido = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)

view.continueScreen(u'Üdvözlő képernyő')

# practicing
# same as active but we don't show the hand
ACC = 0
jovalasz = 0
gyakblokk =0
gyak_trialszam = 15
while True:
    for i in range (gyak_trialszam):
        event.clearEvents(eventType='keyboard')
        RT.reset()

        view.drawFixation()

        while True:
            controller.checkQuit()
            controller.drawIntensity()
            view.drawFixation()
            if controller.isGesture():
                RI = RT.getTime()
                break

        controller.checkQuit()

        print str(RI)
        feedback = str(round(RI, 2)) + ' mp'

        signal.triggerPeak(pinNumber)
        if RI > 1.75:
            jovalasz +=1
            for st2 in range (60):
                view.drawCenterText(feedback)
        else:
            for st2 in range (60):
                view.drawCenterText(feedback)

    print 'jovalasz: ',jovalasz
    gyakblokk +=1
    print gyak_trialszam*gyakblokk
    jovalasz = float(jovalasz)
    ACC = float(jovalasz/(gyak_trialszam*gyakblokk)*100)
    if ACC>=80:
        break

view.continueScreen(u'Vége a gyakorlásnak', u'Ha készen áll, nyomja meg a SPACE gombot')

# same as active but we don't show the hand
# fixation cross while the participant does not make a gesture
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