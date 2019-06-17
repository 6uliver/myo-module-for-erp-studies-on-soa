#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================

from __future__ import division
from view import View
from controller import Controller
from config import Config

size = [1366, 768]

personData = View.collectPersonData(u'KALIBRÁLÁS', True, True)

male = (personData['nem'] == u"férfi")
right = (personData['kez'] == u"jobb")

view = View(size, Config.fullscreen)
controller = Controller(view)

view.quit = controller.quit

view.setHands(male, right)

controller.measureThresholds()
controller.saveThresholds()

view.continueScreen(u'Vége')

controller.quit()