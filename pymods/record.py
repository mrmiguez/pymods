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
            #for elem in self.iter('{http://repox.ist.utl.pt}*'):
            #    print(elem)
            self.oai_id = self.find('{0}record/{0}header/{0}identifier'.format(NAMESPACES['repox'])).text
        elif '{http://www.openarchives.org/OAI/2.0/oai_dc/}' in self.tag:
            self.oai_id = self.attrib['id']
