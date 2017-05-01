from lxml import etree
from pymods.constants import NAMESPACES


class Record(etree.ElementBase):

    def _init(self):
        super(Record, self)._init()


class MODSRecord(Record):

    def _init(self):
        super(MODSRecord, self)._init()


class OAIRecord(Record):

    def _init(self):
        super(OAIRecord, self)._init()
        if '{http://repox.ist.utl.pt}' in self.tag:
            #print('check') #debug
            #for elem in self.iter('{http://repox.ist.utl.pt}*'):
            #    print(elem)
            try:
                self.oai_id = self.find('{0}record'.format(NAMESPACES['repox'])).attrib['id']
            except AttributeError:
                pass
        elif '{http://www.openarchives.org/OAI/2.0/oai_dc/}' in self.tag:
            try:
                self.oai_id = self.find('{0}header/{0}identifier'.format(NAMESPACES['oai_dc']))
            except AttributeError:
                pass
