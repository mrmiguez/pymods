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
        :param record: a single MODS record.
        :return: [{abstract displayLabel: abstract text}] or None.
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
        :param record: A single MODS record.
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
        Accesses mods:digitalOrigin element.
        :param record: a single MODS record.
        :return: mods:digitalOrigin's text or None.
        """
        if record.find('.//{0}digitalOrigin'.format(nameSpace_default['mods'])) is not None:
            return record.find('.//{0}digitalOrigin'.format(nameSpace_default['mods'])).text
        else:
            return None

    def extent(record):
        """
        Accesses mods:extent element.
        :param record: a single MODS record.
        :return: list of mods:extent texts or None.
        """
        all_extents = []
        if record.find('.//{0}extent'.format(nameSpace_default['mods'])) is not None:
            for extent in record.iterfind('.//{0}extent'.format(nameSpace_default['mods'])):
                all_extents.append(extent.text)
        else:
            all_extents.append('None')
        return all_extents

    #def genre(record):

    def issuance(record):
        """
        Accesses mods:issuance element.
        :param record: a single MODS record.
        :return: list of mods:issuance texts or None.
        """
        all_issuances = []
        if record.find('.//{0}issuance'.format(nameSpace_default['mods'])) is not None:
            for issuance in record.iterfind('.//{0}issuance'.format(nameSpace_default['mods'])):
                all_issuances.append(issuance.text)
        else:
            all_issuances.append('None')
        return all_issuances

    def language(record):
        """
        Accesses mods:languageterm elements.
        :param record: a single MODS record.
        :return: list of of dicts [{term-type: term}] or None.
        """
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
        :param record: A single MODS record.
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

    def note(record):
        """
        Access mods:note elements and return a list of dicts:
        :param record: a single MODS record.
        :return: [{note-type: note-text}, untyped-note-text]
        """
        all_notes = []
        for note in record.iterfind('./{0}note'.format(nameSpace_default['mods'])):
            if len(note.attrib) >= 1:
                if 'type' in note.attrib.keys():
                    typed_note = {note.attrib['type']: note.text}
                    all_notes.append(typed_note)
                elif 'displayLabel' in note.attrib.keys():
                    labeled_note = {note.attrib['displayLabel']: note.text}
                    all_notes.append(labeled_note)
                else:
                    all_notes.append(note.text)
            else:
                all_notes.append(note.text)
        return all_notes

    def physical_description_note(record):
        """

        :return:
        """
        all_notes = []
        for physical_description in record.iterfind('./{0}physicalDescription'.format(nameSpace_default['mods'])):
            for note in physical_description.iterfind('./{0}note'.format(nameSpace_default['mods'])):
                all_notes.append(note.text)
        return all_notes

    def physical_location(record):
        """

        :return:
        """
        all_locations = []
        if record.find('.//{0}physicalLocation'.format(nameSpace_default['mods'])) is not None:
            for location in record.iterfind('.//{0}physicalLocation'.format(nameSpace_default['mods'])):
                all_locations.append(location.text)
        else:
            all_locations.append(None)
        return all_locations

    def publication_place(record):
        """

        :return:
        """
        all_places = []
        if record.find('.//{0}place'.format(nameSpace_default['mods'])) is not None:
            for place in record.iterfind('.//{0}place'.format(nameSpace_default['mods'])):
                places = {}
                for term in place.iterchildren():
                    places[term.attrib['type']] = term.text
                all_places.append(places)
        else:
            all_places.append('None')
        return all_places

    def publisher(record):
        """

        :return:
        """
        all_publishers = []
        if record.find('.//{0}publisher'.format(nameSpace_default['mods'])) is not None:
            for publisher in record.iterfind('.//{0}publisher'.format(nameSpace_default['mods'])):
                all_publishers.append(publisher.text)
        else:
            all_publishers.append('None')
        return all_publishers

    #def subject(record):

    def title_constructor(record):
        """

        :return:
        """
        all_titles = []
        for title in record.iterfind('.//{0}titleInfo'.format(nameSpace_default['mods'])):
            if title.find('./{0}nonSort'.format(nameSpace_default['mods'])) is not None and title.find(
                          './{0}title'.format(nameSpace_default['mods'])) is not None and title.find(
                          './{0}subTitle'.format(nameSpace_default['mods'])) is not None:
                title_full = title.find('./{0}nonSort'.format(nameSpace_default['mods'])).text + ' ' + title.find(
                                        './{0}title'.format(nameSpace_default['mods'])).text + ': ' + title.find(
                                        './{0}subTitle'.format(nameSpace_default['mods'])).text
            elif title.find('./{0}nonSort'.format(nameSpace_default['mods'])) is not None and title.find(
                            './{0}title'.format(nameSpace_default['mods'])) is not None:
                title_full = title.find('./{0}nonSort'.format(nameSpace_default['mods'])).text + ' ' + title.find(
                                        './{0}title'.format(nameSpace_default['mods'])).text
            else:
                title_full = title.find('./{0}title'.format(nameSpace_default['mods'])).text
            all_titles.append(title_full)
        return all_titles

    def type_of_resource(record):
        """

        :return:
        """
        if record.find('.//{0}typeOfResource'.format(nameSpace_default['mods'])) is not None:
            type_of_resource = record.find('.//{0}typeOfResource'.format(nameSpace_default['mods']))
            return type_of_resource.text
        else:
            return None


class FSUDL(MODSReader):
    """
    Helper functions specific to Florida State
    University's DigiNole: http://diginole.lib.fsu.edu
    """
    def __init__(self, input_file):
        """
        MODS constructor class.
        :param input_file: file or directory of files to be accessed.
        """
        super(FSUDL, self).__init__(input_file)
        record_list = []
        for mods_record in self.root.iterfind('.//{0}mods'.format(nameSpace_default['mods'])):
            record_list.append(mods_record)
        self.record_list = record_list

    def purl_search(record):
        """
        Accesses record's Persistent URL from mods:mods/mods:location/mods:url.
        :param record: A single MODS record.
        :return: item PURL as string.
        """
        purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
        for url in record.iterfind('./{0}location/{1}url'.format(nameSpace_default['mods'], nameSpace_default['mods'])):
            match = purl.search(url.text)
            if match:
                return match.group()

    def pid_search(record):
        """
        Get fedora PID from MODS record.
        :param record: A single MODS record.
        :return: item's fedora PID.
        """
        pid = re.compile('fsu:[0-9]*')
        for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['mods'])):
            match = pid.search(identifier.text)
            if match:
                return match.group()

    def local_identifier(record):
        """
        Get DigiNole IID from MODS record.
        :param record: A single MODS record
        :return: item's fedora PID
        """
        for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['mods'])):
            if 'type' in identifier.attrib is not None:
                if 'IID' == identifier.attrib['type']:
                    return identifier.text


class OAI(MODSReader):
    """
    oai_dc elements are output wrappers from OAI-PMH feeds. This
    class provides access to those elements.

    Some implementations of the OAI-PMH standard do not include the
    default namespace for oai_dc. A future release will include a test
    for inclusion of the default namespace,and add it to the file when
    not present.
    """
    def __init__(self, input_file):
        """
        Constructor class for oai_dc namespace elements.
        :param input_file: file or directory of files to be accessed.
        """
        super(OAI, self).__init__(input_file)
        record_list = []
        for oai_record in self.root.iterfind('.//{0}record'.format(nameSpace_default['oai_dc'])):
            record_list.append(oai_record)
        self.record_list = record_list

    def pid_search(record):
        """
        Get fedora PID from oai_dc wrapper.
        :param record: A single oai_dc record.
        :return: item's fedora PID.
        """
        pid = re.compile('fsu_[0-9]*')
        for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['oai_dc'])):
            match = pid.search(identifier.text)
            if match:
                return match.group().replace('_', ':')

#mods = MODS('dev/fsu_cookbooksandherbals.xml')
#for record in mods.record_list:
#    print(MODS.title_constructor(record))