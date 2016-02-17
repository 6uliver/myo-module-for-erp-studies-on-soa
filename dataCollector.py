
class DataCollector():

    def __init__(self, sorszam, nem, kez):
        self.sorszam = sorszam
        self.nem = nem
        self.kez = kez
        self.output_file = None

    def openFile(self):
        filename = self.sorszam +'_HandMYO_aktiv_'+ self.nem + '_'+self.kez+'.txt'

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