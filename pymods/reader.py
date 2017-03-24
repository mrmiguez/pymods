from lxml import etree

from pymods import Record
from pymods.constants import NAMESPACES
from pymods.exceptions import NameSpaceInvalid


class Reader(etree.XMLParser):
    """
    A base class for all iterating readers in the pymods package.
    """
    def __init__(self, mods_target):
        """

        """
        if mods_target is not None:
            self.mods_target = mods_target
            self.tree = etree.parse(self.mods_target)
            self.root = self.tree.getroot()
        self.record_list = []

    def close(self):
        """

        :return:
        """
        if self.mods_target is not None:
            self.mods_target.close()
            self.mods_target = None

    def __iter__(self):
        return iter(self.record_list)

    def __len__(self):
        return len(self.record_list)


class MODSReader(Reader):

    def __init__(self, mods_target):
        """

        :param mods_target:
        """
        super(MODSReader, self).__init__(mods_target)

        self.mods_parser_registration = etree.ElementDefaultClassLookup(element=Record)
        self.mods_parser = etree.XMLParser()
        self.mods_parser.set_element_class_lookup(self.mods_parser_registration)

        self.record_list = []
        for record in self.root.iter('{0}mods'.format(NAMESPACES['mods'])):
            record_tree = etree.ElementTree(record, parser=self.mods_parser)
            record_root = record_tree.getroot()
            #record_root = Record(record_tree.getroot())
            self.record = Record(record_root)
            self.record_list.append(self.record)


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
