#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#HAND INDUKCIÓ 
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors
from view import View
from dataCollector import DataCollector
from controller import Controller

personData = View.collectPersonData(u'INDUKCIÓ', True)

male = (personData['nem'] == u"férfi")
right = (personData['kez'] == u"jobb")
trialszam = personData['trialszam']
session = personData['session']

if right:
    pinNumber = 2#choose a pin to write to (2-9).
else:
    pinNumber = 3#choose a pin to write to (2-9).

#LOGFILE-OK
dataCollector = DataCollector('indukcio', personData['sorszam'],  personData['nem'],  personData['kez'])

if not dataCollector.openFile():
    View.showErrorAndQuit(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')

size = [1366, 768]

view = View(size, True)
controller = Controller(view)

view.quit = controller.quit

view.setHands(male, right)

controller.measureThresholds(False, True)

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)
positions_ALL = []

a = 0
for i in range(trialszam):
    positions_ALL.append(positions[a])
    a += 1
    if a % 8 == 0:
        a = 0
random.shuffle(positions_ALL)

view.continueScreen(u'Üdvözlő képernyő')

controller.induction(positions_ALL, trialszam)

#CSÚSZKA
rating_HASONLO, rating_SAJAT = view.getRating()
print 'rating_HASONLO: ', rating_HASONLO, ',rating_SAJAT: ', rating_SAJAT
dataCollector.write(personData['sorszam'], personData['nem'], personData['kez'], trialszam, session, rating_HASONLO, rating_SAJAT)

view.continueScreen(u'Vége')

controller.quit()