from lxml import etree

from pymods.constants import NAMESPACES
from pymods.Record import Record


class MODSReader:

    def __init__(self, file_location):
        self.iterator = etree.parse(file_location).iter(
            '{0}mods'.format(NAMESPACES['mods']))

    def __next__(self):
        return Record(etree.tostring(next(self.iterator)))

    def __iter__(self):
        return self
