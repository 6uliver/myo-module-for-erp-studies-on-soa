#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#TIME ASSESS
#HAND MOTOR 
#VIZUÁLIS
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors

parallel.setPortAddress(0x378)#address for parallel port on many machines


#Azok az adatok, amiket a program indításkor bekér:
expstart1=gui.Dlg(title=u'A projekt adatai - MOTOR')
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

#LOGFILE-OK
try:
    output_file = codecs.open(sorszam +'_HandMYO_motor_'+ nem + '_'+kez+'.txt', 'r',encoding='utf-8')
except IOError: 
    #letezo=0
    print 'még nincs elmentve ilyen fájl, valószínűleg ez az első alkalom az indítások közül'
    #Ha a progi először indul, létrehozatjuk vele a 3 logfile-t 
    output_file = codecs.open(sorszam +'_HandMYO_motor_'+ nem + '_'+kez+'.txt','a', encoding = 'utf-8')  #a személy válaszai

else: 
    #letezo=1
    expstart4 = gui.Dlg (title = u'ERROR')
    expstart4.addText(u'Létező beállítások ennél a személynél!\nAz adott sorszámú személynél korábban már elindult ez a blokk. Ha a blokkot újra kell kezdeni ennél a személynél, töröld ki a személy adott blokkjához tartozó .txt fájlt a scriptet tartalmazó mappából.')
    expstart4.show()
    if expstart4.OK:
        core.quit()

myWin = visual.Window([1366,768],monitor="testMonitor", color = 'Black', allowGUI = True, units = 'cm',  waitBlanking=True, fullscr= True)

if nem == u"férfi":
    if kez == u"jobb":
        hand = visual.ImageStim(myWin, 'm_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'm_right_2.png', pos = (0,0))
        pinNumber = 6#choose a pin to write to (2-9). 
    elif kez == u"bal":
        hand = visual.ImageStim(myWin, 'm_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'm_left_2.png', pos = (0,0))
        pinNumber = 7#choose a pin to write to (2-9). 
elif nem == u"nő":
    if kez == u"jobb":
        hand = visual.ImageStim(myWin, 'f_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'f_right_2.png', pos = (0,0))
        pinNumber = 6#choose a pin to write to (2-9). 
    elif kez == u"bal":
        hand = visual.ImageStim(myWin, 'f_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'f_left_2.png', pos = (0,0))
        pinNumber = 7#choose a pin to write to (2-9). 

hand.size /= 5.75
hand_get.size /= 5.75


#VISUAL ITEMS
fixation=visual.TextStim(myWin, text='+', alignHoriz='center', alignVert='center', pos = (0.0, 0.0), color='Red', height = 3, units = 'cm')
stim = visual.Circle (myWin, radius = 1, units='cm', fillColor='Tomato', pos=[0,0])
stim = visual.Rect(myWin, width = 3, height = 3, units = 'cm', lineColor = 'Tomato', fillColor = 'Tomato', lineWidth = 1.5, pos = [0,0])
stim2 = visual.Rect(myWin, width = 3, height = 3, units = 'cm', lineColor = 'Khaki', fillColor = 'Khaki', lineWidth = 1.5, pos = [0,0])

gyak_text = visual.TextStim(myWin, text = u'', alignHoriz='center', alignVert='center', pos = (0.0, 0.0), color='white', height = 1, units = 'cm', wrapWidth = 27, font='courier new')
insrtukcio = visual.TextStim(myWin, text = u'', alignHoriz='center', alignVert='center', pos = (0.0, 0.2), color='white', height = 0.5, units = 'cm', wrapWidth = 27, font='courier new')

RT = core.Clock()
st_ido = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)

#st_int = int(round(300/framerate_ms, 0))

v =[]
while True:
    insrtukcio.setPos([0.0, 6])
    insrtukcio.setText( u'Üdvözlő képernyő')
    insrtukcio.draw()
    insrtukcio.setPos([0.0, 3])
    insrtukcio.setText(u'')
    insrtukcio.draw()
    insrtukcio.setPos([0.0, -3])
    insrtukcio.setText( u'')
    insrtukcio.draw()
    myWin.flip()
    v = event.getKeys(keyList=['space', 'escape'])
    if v:
        if v[-1] == 'space':
            break
        elif v[-1] == 'escape':
            core.quit()

# GYAKORLÁS
# ugyanaz, mint az aktív gyakorlás, csak sosincs kéz
ACC = 0
jovalasz = 0
z = 0
gyakblokk =0
gyak_trialszam = 15
while z ==0:
    for i in range (gyak_trialszam):
        event.clearEvents(eventType='keyboard')
        RT.reset()
        a = 0
        while a == 0:  #equal 1 in case of answer
            fixation.draw()
            myWin.flip()
            v=[]
            while True:
                v = event.getKeys(keyList=['space', 'escape'])
                if v != []:
                    RI = RT.getTime()
                    break
                fixation.draw()
                myWin.flip()
            if v:
                print str(RI)
                feedback = str(round(RI, 2)) + ' mp'
                gyak_text.setText(feedback)
                if v[-1] == 'space':
#                    for k in range(20):
#                        parallel.setPin(pinNumber,1) #TRIGGER be!
#                    for k in range(20):
#                        parallel.setData(0) #TRIGGER ki!
# !!! nincs drawHand
                    if RI > 1.75:
                        jovalasz +=1
                        for st2 in range (60):
                            gyak_text.draw()
                            myWin.flip()
                    else:
                        for st2 in range (60):
                            gyak_text.draw()
                            myWin.flip()
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
        z=1

tovabb=['']
while not tovabb[0] == 'space':
    insrtukcio.setPos([0.0, 6])
    insrtukcio.setText( u'Vége a gyakorlásnak')
    insrtukcio.draw()
    insrtukcio.setPos([0.0, 3])
    insrtukcio.setText(u'Ha készen áll, nyomja meg a SPACE gombot')
    insrtukcio.draw()
    insrtukcio.setPos([0.0, -3])
    insrtukcio.setText( u'')
    insrtukcio.draw()
    myWin.flip()
    tovabb = event.waitKeys()



# ugyanaz, mint az aktívnál, csak nincs kéz
#fixációs kereszt amíg meg nem nyom egy gombot
#ingerbemutatás x ideig
trialszam = 100
lista = [0, 1, 2, 3, 4, 5, 6]
ujszam = -1
for i in range (trialszam):
    fixation.draw()
    myWin.flip()
    core.wait(1.5)
    event.clearEvents(eventType='keyboard')
    a = 0
    while a == 0:  #equal 1 in case of answer
        fixation.draw()
        myWin.flip()
        v=[]
        v = event.getKeys(keyList=['space', 'escape'])
        if v:
            if v[-1] == 'space':
                print 'trigger'
#                for k in range(20):
#                    parallel.setPin(pinNumber,1) #TRIGGER be!
#                for k in range(20):
#                    parallel.setData(0) #TRIGGER ki!
            elif v[-1] == 'escape':
                print 'Session terminated by user.'
                core.quit()
            a = 1
    if (i+1) == 15 or (i+1) == 36 or (i+1) == 57 or (i+1) == 78:
        szam = random.choice(lista)
        print 'szam: ', szam
        ujszam = (i+1)+szam
    print 'ujszam: ',ujszam
    if (i+1) == ujszam:
        random.shuffle(positions)
        # indukcio, ugyanaz
        for i in range (8):
            b =0
            while b == 0:
                stim.pos = positions[i]
                stim.draw()
                hand.draw()
                
                myWin.flip()
                v = event.waitKeys()
                if hand.overlaps(stim) or hand.contains(stim.pos):
                    
                    if v:
                        if v[-1] == 'up':
                            hand.pos += (0, 1)
                        elif v[-1] == 'down':
                            hand.pos += (0, -1)
                        elif v[-1] == 'right':
                            hand.pos += (1, 0)
                        elif v[-1] == 'left':
                            hand.pos += (-1, 0)
                        elif v[-1] == 'escape':
                            core.quit()
                        elif v[-1] == 'space':
                            hand_get.pos = hand.pos
                            stim.draw()
                            hand_get.draw()
                            
                            myWin.flip()
                            core.wait(0.8)
                            hand.pos = (0,0)
                            b = 1
                else:
                    
                    if v:
                        if v[-1] == 'up':
                            hand.pos += (0, 1)
                        elif v[-1] == 'down':
                            hand.pos += (0, -1)
                        elif v[-1] == 'right':
                            hand.pos += (1, 0)
                        elif v[-1] == 'left':
                            hand.pos += (-1, 0)
                        elif v[-1] == 'escape':
                            core.quit()
                    stim.draw()
                    hand.draw()
                    myWin.flip()

        
        event.clearEvents(eventType='keyboard')
        v=[]
        while True:
            insrtukcio.setPos([0.0, 6])
            insrtukcio.setText( u'Most pihenhet egy kicsit.')
            insrtukcio.draw()
            insrtukcio.setPos([0.0, -3])
            insrtukcio.setText( u'Ha készen áll a folytatásra, nyomja meg a SPACE billentyűt.')
            insrtukcio.draw()
            myWin.flip()
            v = event.getKeys(keyList=['space', 'escape'])
            if v:
                if v[-1] == 'space':
                    break
                elif v[-1] == 'escape':
                    core.quit()
event.clearEvents(eventType='keyboard')
v=[]
while True:
    insrtukcio.setPos([0.0, 6])
    insrtukcio.setText( u'Vége')
    insrtukcio.draw()
    insrtukcio.setPos([0.0, 3])
    insrtukcio.setText(u'')
    insrtukcio.draw()
    insrtukcio.setPos([0.0, -3])
    insrtukcio.setText( u'')
    insrtukcio.draw()
    myWin.flip()
    v = event.getKeys(keyList=['space', 'escape'])
    if v:
        if v[-1] == 'space':
            break
        elif v[-1] == 'escape':
            core.quit()