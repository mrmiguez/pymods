from lxml import etree

from pymods import Record
from pymods.constants import NAMESPACES
from pymods.exceptions import NameSpaceInvalid


class Reader:
    """
    A base class for all iterating readers in the pymods package.
    """
#    def __iter__(self):
#        return self


class MODSReader(Reader):

    def __init__(self, mods_target):
        """

        :param mods_target:
        """
        super(MODSReader, self).__init__()
        if mods_target is not None:
            self.mods_target = mods_target
            self.tree = etree.parse(self.mods_target)
            self.root = self.tree.getroot()
        self.record_list = []
        for record in self.root.iterfind('{0}mods'.format(NAMESPACES['mods'])):
            self.record = Record(record)
            self.record_list.append(self.record)

    def close(self):
        """

        :return:
        """
        if self.mods_target is not None:
            self.mods_target.close()
            self.mods_target = None

    def __iter__(self):
        return iter(self.record_list)

'''
    def __next__(self):
        """

        :return:
        """
        if self.getnext() is not None:
            record = self.getnext()
            return record
        else:
            raise StopIteration
'''


class OAIReader(Reader):
    def __init__(self, mods_target):
        """

        :param mods_target:
        """
        super(OAIReader, self).__init__()
        if mods_target is not None:
            self.mods_target = mods_target
            self.tree = etree.parse(self.mods_target)
            self.root = self.tree.getroot()

    def close(self):
        """

        :return:
        """
        if self.mods_target is not None:
            self.mods_target.close()
            self.mods_target = None

    def __next__(self):
        """

        :return:
        """
