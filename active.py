#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#HAND ACTIVE
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors
from view import View

parallel.setPortAddress(0x378)#address for parallel port on many machines


#Azok az adatok, amiket a program indításkor bekér:
expstart1=gui.Dlg(title=u'A projekt adatai - AKTÍV')
expstart1.addText('')
expstart1.addField(u'Kísérleti személy sorszáma','')
expstart1.addField(u'Neme', choices=[u"Válassz!",u"férfi", u"nő"])
expstart1.addField(u'Kéz', choices=[u"Válassz!",u"jobb", u"bal"])
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
else:
    sorszam=expstart1.data[0]
    nem=expstart1.data[1]
    kez=expstart1.data[2]

if nem == u"férfi":
    male = True
else:
    male = False

if kez == u"jobb":
    right = True
else:
    right = False

#LOGFILE-OK
try:
    output_file = codecs.open(sorszam +'_HandMYO_aktiv_'+ nem + '_'+kez+'.txt', 'r',encoding='utf-8')
except IOError:
    #letezo=0
    print 'még nincs elmentve ilyen fájl, valószínűleg ez az első alkalom az indítások közül'
    #Ha a progi először indul, létrehozatjuk vele a 3 logfile-t
    output_file = codecs.open(sorszam +'_HandMYO_aktiv_'+ nem + '_'+kez+'.txt','a', encoding = 'utf-8')  #a személy válaszai

else:
    #letezo=1
    expstart4 = gui.Dlg (title = u'ERROR')
    expstart4.addText(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')
    expstart4.show()
    if expstart4.OK:
        core.quit()

myWin = visual.Window([1366,768],monitor="testMonitor", color = 'Black', allowGUI = True, units = 'cm',  waitBlanking=True, fullscr= True)

view = View(myWin)

if male:
    if right:
        hand = visual.ImageStim(myWin, 'images/m_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'images/m_right_2.png', pos = (0,0))
        pinNumber = 2#choose a pin to write to (2-9).
    else:
        hand = visual.ImageStim(myWin, 'images/m_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'images/m_left_2.png', pos = (0,0))
        pinNumber = 3#choose a pin to write to (2-9).
else:
    if right:
        hand = visual.ImageStim(myWin, 'images/f_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'images/f_right_2.png', pos = (0,0))
        pinNumber = 2#choose a pin to write to (2-9).
    else:
        hand = visual.ImageStim(myWin, 'images/f_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'images/f_left_2.png', pos = (0,0))
        pinNumber = 3#choose a pin to write to (2-9).

hand.size /= 5.75
hand_get.size /= 5.75

view.addHands(hand, hand_get)

framerate_ms = view.measureFrameRate()
print framerate_ms

RT = core.Clock()
stimulus_ido = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)

stimulus_interval = int(round(300 / framerate_ms, 0))

view.continueScreen(u'Üdvözlő képernyő')

##GYAKORLÁS - Myo
ACC = 0
jovalasz = 0
gyakblokk =0
gyak_trialszam = 15
##for k in range(20):
##    parallel.setData(0) #TRIGGER!
while True:
    event.clearEvents(eventType='keyboard')
    RT.reset()
    a = 0
    while a == 0:  #equal 1 in case of answer
        view.drawFixation()
        v=[]
        while True:
            v = event.getKeys(keyList=['space', 'escape'])
            if v != []:
                RI = RT.getTime()
                break
            view.drawFixation()
        if v:
            print str(RI)
            feedback = str(round(RI, 2)) + ' mp'
            if v[-1] == 'space':
##                for k in range(20):
##                    parallel.setPin(pinNumber,1)
##                for k in range(20):
##                    parallel.setData(0) #TRIGGER!
                stimulus_ido.reset()
                for st in range (stimulus_interval):
                    view.drawHand()
                st_time = stimulus_ido.getTime()
                print st_time
                if RI > 1.75:
                    jovalasz +=1
                    for st2 in range (60):
                        view.drawCenterText(feedback)
                else:
                    for st2 in range (60):
                        view.drawCenterText(feedback)
            elif v[-1] == 'escape':
                print 'Session terminated by user.'
                core.quit()

            a = 1
    print 'jovalasz: ',jovalasz
    gyakblokk +=1
    print gyak_trialszam*gyakblokk
    jovalasz = float(jovalasz)
    ACC = float(jovalasz/(gyak_trialszam*gyakblokk)*100)
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
            if v[-1] == 'space':
#                for k in range(20):
#                    parallel.setPin(pinNumber,1) #TRIGGER be!
#                for k in range(20):
#                    parallel.setData(0) #TRIGGER ki!
                for st2 in range (stimulus_interval):
                    view.drawHand()
            elif v[-1] == 'escape':
                print 'Session terminated by user.'
                core.quit()
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
