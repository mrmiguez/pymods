import os
import re
from lxml import etree

nameSpace_default = {None: '{http://www.loc.gov/mods/v3}',
                     'oai_dc': '{http://www.openarchives.org/OAI/2.0/oai_dc/}',
                     'dc': '{http://purl.org/dc/elements/1.1/}',
                     'mods': '{http://www.loc.gov/mods/v3}',
                     'dcterms': '{http://purl.org/dc/terms}'}


class MODSReader:
    """
    Superclass constructor and file reader.
    """
    def __init__(self, input_file):
        """
        General constructor class.
        :param input_file: file or directory of files to be accessed.
        """
        self.input_file = input_file
        self.tree = etree.parse(self.input_file)
        self.root = self.tree.getroot()
        

class MODS(MODSReader):
    """
    Class for accessing elements in the MODS namespace.
    """
    def __init__(self, input_file):
        """
        MODS constructor class.
        :param input_file: file or directory of files to be accessed.
        """
        super(MODS, self).__init__(input_file)
        record_list = []
        for mods_record in self.root.iterfind('.//{0}mods'.format(nameSpace_default['mods'])):
            record_list.append(mods_record)
        self.record_list = record_list

    def abstract(record):
        """
        Access mods:abstract elements and return a list of dicts:
        :param: a single MODS record
        :return: [{abstract displayLabel: abstract text}]
        """
        all_abstracts = []
        if record.find('./{0}abstract'.format(nameSpace_default['mods'])) is not None:
            for abstract in record.iterfind('./{0}abstract'.format(nameSpace_default['mods'])):
                if len(abstract.attrib) >= 1:
                    if 'type' in abstract.attrib.keys():
                        typed_abstract = {abstract.attrib['type']: abstract.text}
                        all_abstracts.append(typed_abstract)
                    elif 'displayLabel' in abstract.attrib.keys():
                        labeled_abstract = {abstract.attrib['displayLabel']: abstract.text}
                        all_abstracts.append(labeled_abstract)
                    else:
                        all_abstracts.append(abstract.text)
                else:
                    all_abstracts.append(abstract.text)
            return all_abstracts
        else:
            return None

    def date_constructor(record):
        """
        Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate,
        and mods:dateOther underneath mods:originInfo. Other date-type
        elements are ignored.
        :param: A single MODS record.
        :return: A date containing string or None.
        """
        date_list = ['{0}dateIssued'.format(nameSpace_default['mods']),
                     '{0}dateCreated'.format(nameSpace_default['mods']),
                     '{0}copyrightDate'.format(nameSpace_default['mods']),
                     '{0}dateOther'.format(nameSpace_default['mods'])]
        ignore_list = ['{0}place'.format(nameSpace_default['mods']),
                       '{0}publisher'.format(nameSpace_default['mods']),
                       '{0}dateCaptured'.format(nameSpace_default['mods']),
                       '{0}dateValid'.format(nameSpace_default['mods']),
                       '{0}dateModified'.format(nameSpace_default['mods']),
                       '{0}edition'.format(nameSpace_default['mods']),
                       '{0}issuance'.format(nameSpace_default['mods']),
                       '{0}frequency'.format(nameSpace_default['mods'])]
        if record.find('./{0}originInfo'.format(nameSpace_default['mods'])) is not None:
            origin_info = record.find('./{0}originInfo'.format(nameSpace_default['mods']))
            date = None
            for child in origin_info.iterchildren():
                if child.tag in date_list:
                    # date range
                    if 'point' in child.attrib.keys():
                        if child.attrib['point'] == 'start':
                            if date is None:
                                date = child.text
                            else:
                                date = child.text + ' - ' + date
                        elif child.attrib['point'] == 'end':
                            if date is None:
                                date = child.text
                            else:
                                date = date + ' - ' + child.text
                    # single date
                    else:
                        date = child.text
                elif child.tag in ignore_list:
                    pass
            return date

    def digital_origin(record):
        """
        Accesses mods:digitalOrigin element
        :param record: a single MODS record
        :return: mods:digitalOrigin's text
        """
        if record.find('.//{0}digitalOrigin'.format(nameSpace_default['mods'])) is not None:
            return record.find('.//{0}digitalOrigin'.format(nameSpace_default['mods'])).text
        else:
            return None

    def extent(record):
        """
        Accesses mods:extent element
        :param record: a single MODS record
        :return: list of mods:extent texts
        """
        allExtents = []
        if record.find('.//{0}extent'.format(nameSpace_default['mods'])) is not None:
            for extent in record.iterfind('.//{0}extent'.format(nameSpace_default['mods'])):
                allExtents.append(extent.text)
        else:
            allExtents.append('None')
        return allExtents

    #def genre(record):

    def issuance(record):
        all_issuances = []
        if record.find('.//{0}issuance'.format(nameSpace_default['mods'])) is not None:
            for issuance in record.iterfind('.//{0}issuance'.format(nameSpace_default['mods'])):
                all_issuances.append(issuance.text)
        else:
            all_issuances.append('None')
        return all_issuances

    def language(record):
        all_languages = []
        if record.find('.//{0}language'.format(nameSpace_default['mods'])) is not None:
            for language in record.iterfind('.//{0}language'.format(nameSpace_default['mods'])):
                languages = {}
                for term in language.iterchildren():
                    languages[term.attrib['type']] = term.text
                all_languages.append(languages)
            return all_languages
        else:
            return None

    def _nameGen_(names, fullName):
        keys = []
        for key in names.keys():
            keys.append(key)
        if all(x in keys for x in ['family', 'given',
                                   'termsOfAddress', 'date']):
            fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
        elif all(x in keys for x in ['family', 'given', 'date']):
            fullName = fullName + names['family'] + ', ' + names['given'] + ' ' + names['date']
        elif all(x in keys for x in ['family', 'given', 'termsOfAddress']):
            fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['family', 'termsOfAddress', 'date']):
            fullName = fullName + names['family'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
        elif all(x in keys for x in ['given', 'termsOfAddress', 'date']):
            fullName = fullName + names['given'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
        elif all(x in keys for x in ['family', 'given']):
            fullName = fullName + names['family'] + ', ' + names['given']
        elif all(x in keys for x in ['family', 'date']):
            fullName = fullName + names['family'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'termsOfAddress']):
            fullName = fullName + names['family'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['given', 'date']):
            fullName = fullName + names['given'] + ', ' + names['date']
        elif all(x in keys for x in ['given', 'termsOfAddress']):
            fullName = fullName + names['given'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['termsOfAddress', 'date']):
            fullName = fullName + ', ' + names['termsOfAddress'] + ' ' + names['date']
        elif 'date' in keys:
            fullName = fullName + ', ' + names['date']
        elif 'termsOfAddress' in keys:
            fullName = fullName + ', ' + names['termsOfAddress']
        return fullName

    def name_constructor(record):
        """
        Accesses mods:name/mods:namePart elements
        and reconstructs names into LOC order.
        :return: a list of strings.
        """
        all_names = []
        if len(record.findall('./{0}name'.format(nameSpace_default['mods']))) > 0:
            for name in record.iterfind('./{0}name'.format(nameSpace_default['mods'])):
                full_name = ""
                if len(name.findall('./{0}namePart'.format(nameSpace_default['mods']))) > 1:
                    # Multipart name
                    names = {}
                    for name_part in name.findall('./{0}namePart'.format(nameSpace_default['mods'])):
                        if 'type' not in name_part.attrib.keys():
                            full_name = name_part.text
                        elif 'type' in name_part.attrib.keys():
                            names[name_part.attrib['type']] = name_part.text
                    full_name = MODS._nameGen_(names, full_name)
                else:
                    # Single part name
                    full_name = full_name + name.find('./{0}namePart'.format(nameSpace_default['mods'])).text
                all_names.append(full_name)
            return all_names
        else:
            all_names.append('None')
            return all_names

mods = MODS('dev/fsu_cookbooksandherbals.xml')
for record in mods.record_list:
    print(MODS.date_constructor(record))