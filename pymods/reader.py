from lxml import etree
from pymods import MODSRecord, OAIRecord
from pymods.constants import NAMESPACES


class Reader(etree.XMLParser):

    def __init__(self, file_location, iter_elem, parser=None):
        """
        Basic XML parser & iterator
        :param file_location: XML encoded file
        :param iter_elem: element to use as record iterator
        :param parser: a custom etree.XMLParser (required for custom etree.ElementBase subclasses)
        """
        super(Reader, self).__init__()

        if parser is not None:
            self.iterator = etree.parse(file_location, parser=parser).iter(iter_elem)
        else:
            self.iterator = etree.parse(file_location).iter(iter_elem)

    def __next__(self):
        return next(self.iterator)

    def __iter__(self):
        return self

    # def __index__(self):
    #     return self
    #
    # def __int__(self):
    #     return self


class MODSReader(Reader):

    def __init__(self, file_location):
        """
        Parser/iterator for the MODSRecord class. Iterates on mods:mods elements.
        :param file_location:
        """
        mods_parser_registration = etree.ElementDefaultClassLookup(element=MODSRecord)
        mods_parser = etree.XMLParser()
        mods_parser.set_element_class_lookup(mods_parser_registration)
        super(MODSReader, self).__init__(file_location, '{0}mods'.format(NAMESPACES['mods']), parser=mods_parser)


class OAIReader(Reader):

    def __init__(self, file_location):
        """
        Parser/iterator for the OAIRecord class. Iterates over record elements in any namespace (repox or oai-pmh).
        :param file_location:
        """
        oai_parser_registration = etree.ElementDefaultClassLookup(element=OAIRecord)
        oai_parser = etree.XMLParser()
        oai_parser.set_element_class_lookup(oai_parser_registration)
        super(OAIReader, self).__init__(file_location, '{*}record', parser=oai_parser)
