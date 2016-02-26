#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, event
import math
from myo import *
from Queue import Queue

class Controller():

    def __init__(self, view):
        self.view = view
        self.count = 0
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
        return intensity > 15

    def drawIntensity(self):
        intensity = self.intensityQueue.get(True)
        self.view.drawIntensity(int(intensity))

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

    def induction(self, positions, count=8):
        for j in range (count):
            while True:
                intensity = self.intensityQueue.get(True)

                catch = intensity > 25

                #print intensity

                position = self.positionQueue.get(True)
                position[0] *= self.view.getSize()[0]/30
                position[1] *= self.view.getSize()[1]/20

                self.view.setHandPosition(position)

                self.view.drawIntensity(int(intensity))
                self.view.drawHandAndStimulus(catch, positions[j % len(positions)])

                if self.view.isHandCanGetStimulus() and catch:
                    core.wait(0.8)
                    self.mouse.reset()
                    while not self.positionQueue.empty():
                        self.positionQueue.get(True)
                    break
                    
                k = event.getKeys(keyList='escape')
                if k and k[-1] == 'escape':
                    self.quit()


        self.view.continueScreen(u'Most pihenhet egy kicsit.', u'Ha készen áll a folytatásra, nyomja meg a SPACE billentyűt.')