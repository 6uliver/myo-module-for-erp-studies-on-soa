#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs

class DataCollector():

    def __init__(self, type, sorszam, nem, kez):
        self.type = type
        self.sorszam = sorszam
        self.nem = nem
        self.kez = kez
        self.output_file = None

    def openFile(self):
        filename = self.sorszam +'_HandMYO_' + self.type + '_'+ self.nem + '_'+self.kez+'.txt'

        #LOGFILE-OK
        try:
            self.output_file = codecs.open(filename, 'r',encoding='utf-8')
        except IOError:
            #letezo=0
            print 'még nincs elmentve ilyen fájl, valószínűleg ez az első alkalom az indítások közül'
            #Ha a progi először indul, létrehozatjuk vele a 3 logfile-t
            self.output_file = codecs.open(filename,'a', encoding = 'utf-8')  #a személy válaszai
        else:
            #letezo=1
            return False

        return True

    def write(self, sorszam, nem, kez, trialszam, session, rating_HASONLO, rating_SAJAT):
        self.output_file.write(sorszam+';' + nem + ';' + kez + ';' + str(trialszam) + ';' + session + ';' + str(rating_HASONLO) + ';' + str(rating_SAJAT) + '\n')