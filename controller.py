#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, event
import math
from myo import *
from Queue import Queue

def avg(list):
    return sum(list) / len(list)

class Controller():

    def __init__(self, view):
        self.view = view
        self.count = 0
        self.restThreshold = 1000
        self.activeThreshold = 1000
        self.rest = True
        self.positionQueue = Queue()
        self.intensityQueue = Queue()
        self.emgHistory = []
        self.mouse = MyoMouse([2,1.5])
        self.mouse.onPosition(self.onPosition)
        self.myoHub = Myo()
        self.myoHub.onConnected(self.onConnected)
        
    def quit(self):
        self.myoHub.close()
        core.quit()

    def onConnected(self, myo):
        self.myo = myo
        self.myo.setStreamEMG(True)
        self.myo.setLockingPolicy(LockingPolicy.NONE)
        self.myo.onOrientation(self.mouse.onOrientation)
        self.myo.onPose(self.printPose)
        self.myo.onEMG(self.printEMG)

    def isGesture(self):
        intensity = self.intensityQueue.get(True)
        self.view.drawIntensity(int(intensity))
        if intensity > self.restThreshold:
            if self.rest:
                self.rest = False
                return True
        elif intensity < self.restThreshold/2:
            self.rest = True
        return False

    def drawIntensity(self):
        intensity = self.intensityQueue.get(True)
        self.view.drawIntensity(int(intensity))

    def countdown(self):
        for i in range(3, 0, -1):
            self.view.drawCountdownText(i)
            core.wait(1)

    def onPosition(self, position):
        if self.positionQueue.empty():
            self.positionQueue.put(position)

    def printPose(self, pose):
        pass
        #print pose

    def rms(self, list):
        squares = [x**2 for x in list]
        squareMeans = sum(squares) / len(squares)
        return math.sqrt(squareMeans)

    def getCount(self):
        return self.count

    def printEMG(self, emg):
        self.count += 1
        #print emg
        self.emgHistory.append(emg)
        while len(self.emgHistory) > 20:
            self.emgHistory.pop(0)

        emgDatas = map(list, zip(*self.emgHistory))

        rmsList = []
        for emgData in emgDatas:
            rmsList.append(self.rms(emgData))

        avg = sum(rmsList) / len(rmsList)
        #print avg
        #print max(rmsList)
        intensity = avg
        #intensity = self.rms(rmsList)
        #intensity = max(rmsList)
        if self.intensityQueue.empty():
            self.intensityQueue.put(intensity)
            
    def measureThresholds(self, rest=True, active=True):
        if rest:
            self.view.continueScreen(u'Kalibrálás', u'Nyugalmi helyzetben')
            self.restThreshold = self.measure(True)
        if active:
            self.view.continueScreen(u'Kalibrálás', u'Felemelt helyzetben')
            self.activeThreshold = self.measure(False)
            
    def measure(self, rest, count=3):
        below = []
        above = []
        for j in range (count*2):
            get = (j % 2) == 1
            if get:
                if rest:
                    self.view.drawFixation()
                else:
                    self.view.drawHandGet()
            else:
                self.view.drawHand()
            while True:
                intensity = self.intensityQueue.get(True)
           
                k = event.getKeys(keyList=['escape', 'space'])
                if k:
                    if k[-1] == 'escape':
                        self.quit()
                    elif k[-1] == 'space':
                        if get:
                            above.append(intensity)
                        else:
                            below.append(intensity)
                        break
        print below, above
        print avg(below), avg(above)
        print (avg(below) + avg(above))/2
        return (avg(below) + avg(above))/2

    def checkQuit(self):
        v = event.getKeys(keyList=['escape'])
        if v != [] and v[-1] == 'escape':
            print 'Session terminated by user.'
            self.quit()

    def induction(self, positions, count=8, restText=True):
        self.countdown()
        for j in range (count):
            while True:
                intensity = self.intensityQueue.get(True)

                catch = intensity > self.activeThreshold

                #print intensity

                position = self.positionQueue.get(True)
                position[0] *= self.view.getSize()[0]/35
                position[1] *= self.view.getSize()[1]/30

                self.view.setHandPosition(position)

                self.view.drawIntensity(int(intensity))
                self.view.drawHandAndStimulus(catch, positions[j % len(positions)])

                if self.view.isHandCanGetStimulus() and catch:
                    core.wait(0.8)
                    # self.mouse.reset()
                    while not self.positionQueue.empty():
                        self.positionQueue.get(True)
                    break
                    
                self.checkQuit()
        self.view.resetHandPosition()

        if restText:
            self.view.continueScreen(u'Most pihenhet egy kicsit.', u'Ha készen áll a folytatásra, nyomja meg a SPACE billentyűt.')