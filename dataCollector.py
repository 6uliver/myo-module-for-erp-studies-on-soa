#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs

class DataCollector():

    def __init__(self, type, sorszam, nem, kez, session=None):
        self.type = type
        self.sorszam = sorszam
        self.nem = nem
        self.kez = kez
        self.session = session
        self.output_file = None

    def openFile(self):
        if self.session is None:
            filename = self.sorszam +'_HandMYO_' + self.type + '_'+ self.nem + '_'+self.kez+'.txt'
        else:
            filename = self.sorszam +'_HandMYO_' + self.type + '_' + self.session + '_' + self.nem + '_'+self.kez+'.txt'

        try:
            self.output_file = codecs.open(filename, 'r',encoding='utf-8')
        except IOError:
            # If the program started first time we create the file
            self.output_file = codecs.open(filename,'a', encoding = 'utf-8')
        else:
            return False

        return True

    def write(self, sorszam, nem, kez, trialszam, session, rating_HASONLO, rating_SAJAT):
        self.output_file.write(sorszam+';' + nem + ';' + kez + ';' + str(trialszam) + ';' + session + ';' + str(rating_HASONLO) + ';' + str(rating_SAJAT) + '\n')