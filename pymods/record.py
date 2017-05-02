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

    @property
    def oai_urn(self):
        if '{http://repox.ist.utl.pt}' in self.tag:
            try:
                oai_id = self.attrib['id']
                return oai_id
            except AttributeError:
                pass
        elif '{http://www.openarchives.org/OAI/2.0/oai_dc/}' in self.tag:
            try:
                return self.find('{0}header/{0}identifier'.format(NAMESPACES['oai_dc']))
            except AttributeError:
                pass
