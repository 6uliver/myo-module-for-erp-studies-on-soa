#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#HAND INDUKCIÓ 
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors

parallel.setPortAddress(0x378)#address for parallel port on many machines


#Azok az adatok, amiket a program indításkor bekér:
expstart1=gui.Dlg(title=u'A projekt adatai - INDUKCIÓ')
expstart1.addText('')
expstart1.addField(u'Kísérleti személy sorszáma','')
expstart1.addField(u'Neme', choices=[u"Válassz!",u"férfi", u"nő"]) 
expstart1.addField(u'Kéz', choices=[u"Válassz!",u"jobb", u"bal"]) 
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
else:
    sorszam=expstart1.data[0]
    nem=expstart1.data[1]
    kez=expstart1.data[2]
    session = expstart1.data[3]
    trialszam = int(expstart1.data[4])

#LOGFILE-OK
try:
    output_file = codecs.open(sorszam +'_HandMYO_indukcio_'+ nem +'.csv', 'r',encoding='utf-8')
except IOError: 
    #letezo=0
    print 'még nincs elmentve ilyen fájl, valószínűleg ez az első alkalom az indítások közül'
    #Ha a progi először indul, létrehozatjuk vele a 3 logfile-t 
    output_file = codecs.open(sorszam +'_HandMYO_indukcio_'+ nem +'.csv','a', encoding = 'utf-8')  #a személy válaszai
    output_file.write('sorszam' + ';' + 'nem' + ';' + 'kez' + ';' + 'trialszam'+';'+'session'+';'+'kez_hasonlo'+';'+'kez_sajat'+'\n')
else: 
    #letezo=1
    output_file = codecs.open(sorszam +'_HandMYO_indukcio_'+ nem + '.csv','a', encoding = 'utf-8')

myWin = visual.Window([1366,768],monitor="testMonitor", color = 'Black', allowGUI = True, units = 'cm',  waitBlanking=True, fullscr= True)

if nem == u"férfi":
    if kez == u"jobb":
        hand = visual.ImageStim(myWin, 'm_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'm_right_2.png', pos = (0,0))
        pinNumber = 2#choose a pin to write to (2-9). 
    elif kez == u"bal":
        hand = visual.ImageStim(myWin, 'm_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'm_left_2.png', pos = (0,0))
        pinNumber = 3#choose a pin to write to (2-9). 
elif nem == u"nő":
    if kez == u"jobb":
        hand = visual.ImageStim(myWin, 'f_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'f_right_2.png', pos = (0,0))
        pinNumber = 2#choose a pin to write to (2-9). 
    elif kez == u"bal":
        hand = visual.ImageStim(myWin, 'f_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'f_left_2.png', pos = (0,0))
        pinNumber = 3#choose a pin to write to (2-9). 

hand.size /= 5.75
hand_get.size /= 5.75

#VISUAL ITEMS
fixation=visual.TextStim(myWin, text='+', alignHoriz='center', alignVert='center', pos = (0.0, 0.0), color='Red', height = 3, units = 'cm')
stim = visual.Circle (myWin, radius = 1, units='cm', fillColor='Tomato', pos=[0,0])
stim = visual.Rect(myWin, width = 3, height = 3, units = 'cm', lineColor = 'Tomato', fillColor = 'Tomato', lineWidth = 1.5, pos = [0,0])
stim2 = visual.Rect(myWin, width = 3, height = 3, units = 'cm', lineColor = 'Khaki', fillColor = 'Khaki', lineWidth = 1.5, pos = [0,0])

gyak_text = visual.TextStim(myWin, text = u'', alignHoriz='center', alignVert='center', pos = (0.0, 0.0), color='white', height = 1, units = 'cm', wrapWidth = 27, font='courier new')
insrtukcio = visual.TextStim(myWin, text = u'', alignHoriz='center', alignVert='center', pos = (0.0, 0.2), color='white', height = 0.5, units = 'cm', wrapWidth = 27, font='courier new')

rateSAJAT_text = visual.TextStim(myWin, text = u'Mennyiére érzed magadnénak a képernyőn látható kezet? Értékeld az alábbi csúszka segítségével!', alignHoriz='center', alignVert='center',  pos = (-1, -6),wrapWidth = 25, color='white', height = 0.5, units = 'cm', font='courier new')
rateSAJAT_scale = visual.RatingScale(myWin, labels = [u"\nEgyáltalán nem érzem magamének", u"\nKözepesen érzem magaménak", u"\nTeljesen magaménak érzem"], textColor='LightGrey', marker='triangle', markerStart = 0, markerColor='dimgray', acceptPreText=u'értekeld!', acceptText=u'OK',textSize=0.7, scale=None, stretch = 2.40, low=-100, high=100, precision=1, showValue=False, lineColor='grey',
pos = (0, -0.7))
rateHAS_text = visual.TextStim(myWin, text = u'Mennyiére érzed hasonlónak a képernyőn látható kezet a saját kezedhez képest?\nÉrtékeld az alábbi csúszka segítségével!', alignHoriz='center', alignVert='center',  pos = (-1, -6),wrapWidth = 25, color='white', height = 0.5, units = 'cm', font='courier new')
rateHAS_scale = visual.RatingScale(myWin, labels = [u"\nEgyáltalán nem érzem hasonlónak", u"\nKözepesen érzem hasonlónak", u"\nTeljesen hasonlónak érzem"], textColor='LightGrey', marker='triangle', markerStart = 0, markerColor='dimgray', acceptPreText=u'értekeld!', acceptText=u'OK',textSize=0.7, scale=None, stretch = 2.40, low=-100, high=100, precision=1, showValue=False, lineColor='grey',
pos = (0, -0.7))


RT = core.Clock()
st_ido = core.Clock()

positions = [(-10, 7), (0, 7),(10,7),(10,0),(10,-7),(0,-7),(-10,-7), (-10,0)]
random.shuffle(positions)
positions_ALL = []

a = 0
for i in range(trialszam):
    positions_ALL.append(positions[a])
    a+=1
    if a%8 == 0:
        a = 0
random.shuffle(positions_ALL)


st_int = int(round(300/16.6, 0))

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

# TODO controller.induction
# sima indukció
for i in range (trialszam):
    b =0
    while b == 0:
        stim.pos = positions_ALL[i]
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

#CSÚSZKA
hand.pos = (0, 2)
while rateHAS_scale.noResponse:
    hand.draw()
    rateHAS_text.draw()
    rateHAS_scale.draw()
    myWin.flip()
rating_HASONLO = rateHAS_scale.getRating()
while rateSAJAT_scale.noResponse:
    hand.draw()
    rateSAJAT_text.draw()
    rateSAJAT_scale.draw()
    myWin.flip()
rating_SAJAT = rateSAJAT_scale.getRating()
print 'rating_HASONLO: ', rating_HASONLO, ',rating_SAJAT: ', rating_SAJAT
output_file.write(sorszam+';' + nem + ';' + kez + ';' + str(trialszam) + ';' + session + ';' + str(rating_HASONLO) + ';' + str(rating_SAJAT) + '\n')

event.clearEvents(eventType='keyboard')
v=[]
while True:
    insrtukcio.setPos([0.0, 0.0])
    insrtukcio.setText( u'Vége a feladatnak!')
    insrtukcio.draw()
    myWin.flip()
    v = event.getKeys(keyList=['space', 'return', 'escape'])
    if v:
        if v[-1] == 'space':
            break
        elif v[-1] == 'return':
            break
        elif v[-1] == 'escape':
            core.quit()