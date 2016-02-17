#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Szalóki Szilvia
#HAND PASSIVE 
#======================================================================

from __future__ import division
from psychopy import visual, core, event, gui, misc, sound
import time, random, cPickle, codecs, os, copy, math, collections
from psychopy import parallel, monitors

parallel.setPortAddress(0x378)#address for parallel port on many machines


#Azok az adatok, amiket a program indításkor bekér:
expstart1=gui.Dlg(title=u'A projekt adatai - PASSZÍV')
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
    output_file = codecs.open(sorszam +'_HandMYO_passziv_'+ nem + '_'+kez+'.txt', 'r',encoding='utf-8')
except IOError: 
    #letezo=0
    print 'még nincs elmentve ilyen fájl, valószínűleg ez az első alkalom az indítások közül'
    #Ha a progi először indul, létrehozatjuk vele a 3 logfile-t 
    output_file = codecs.open(sorszam +'_HandMYO_passziv_'+ nem + '_'+kez+'.txt','a', encoding = 'utf-8')  #a személy válaszai

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
        pinNumber = 4#choose a pin to write to (2-9). 
    elif kez == u"bal":
        hand = visual.ImageStim(myWin, 'm_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'm_left_2.png', pos = (0,0))
        pinNumber = 5#choose a pin to write to (2-9). 
elif nem == u"nő":
    if kez == u"jobb":
        hand = visual.ImageStim(myWin, 'f_right_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'f_right_2.png', pos = (0,0))
        pinNumber = 4#choose a pin to write to (2-9). 
    elif kez == u"bal":
        hand = visual.ImageStim(myWin, 'f_left_1.png', pos = (0,0))
        hand_get = visual.ImageStim(myWin, 'f_left_2.png', pos = (0,0))
        pinNumber = 5#choose a pin to write to (2-9). 

hand.size /= 5.75
hand_get.size /= 5.75

#MEASURE FRAMERATE
frametest =visual.TextStim(myWin, text=u'Indítás...', alignHoriz='center', alignVert='center', pos = (0.0, 0.0), color='silver', opacity=0.6, height = 0.8, units = 'cm')

fr = core.Clock()
frame = core.Clock()
frame.reset()
FRAMES = []
for i in range(100):
    fr.reset()
    frametest.draw()
    myWin.flip()
    frrate = fr.getTime()
    print frrate
    FRAMES.append(frrate)
#tenframes = frame.getTime()
#framerate_ms = tenframes*100
#print framerate_ms

for i in range (len(FRAMES)):
    k = float(FRAMES[i])
    k = round(FRAMES[i], 4)
    print k
    FRAMES[i] = k

print FRAMES

counts = collections.Counter(FRAMES)
new_list = sorted(FRAMES, key=counts.get, reverse=True) #egyes frame-ek gyakoriság szerint sorbarendezve

print new_list

framerate_ms = new_list[0]*1000
print framerate_ms

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

st_int = int(round(300/framerate_ms, 0))

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
    


trialszam = 100
ISI = [1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150, 2200, 2250, 2300, 2350, 2400, 2450]
print len(ISI)

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

event.clearEvents(eventType='keyboard')
v=[]
for i in range (trialszam):
    v = event.getKeys(keyList=['space', 'escape'])
    if v:
        if v[-1] == 'escape':
            core.quit()
    for soa in range (allISI[i]):
        fixation.draw()
        myWin.flip()
#    for k in range(20):
#        parallel.setPin(pinNumber,1) #TRIGGER be!
#    for k in range(20):
#        parallel.setData(0) #TRIGGER ki!
    for st2 in range (st_int):
        hand.draw()
        myWin.flip()
    if (i+1) == 15 or (i+1) == 36 or (i+1) == 57 or (i+1) == 78:
        szam = random.choice(lista)
        print 'szam: ', szam
        ujszam = (i+1)+szam
    print 'ujszam: ',ujszam
    if (i+1) == ujszam:
        random.shuffle(positions)
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
    