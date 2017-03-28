import re
from lxml import etree

from pymods.constants import NAMESPACES
from pymods.exceptions import ElementNotFound


class Record(etree.ElementBase):

    def _init(self):
        super(etree.ElementBase, self).__init__()

    def abstract(self, elem=None):
        """
        Access mods:abstract elements and return a list of dicts:
        return: [{abstract displayLabel: abstract text}] or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}abstract'.format(NAMESPACES['mods'])) is not None:
            all_abstracts = []
            for abstract in record.iterfind('./{0}abstract'.format(NAMESPACES['mods'])):
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

    def classification(self, elem=None):
        """
        Access mods:classification element:
        return: [classification text, ... ] or None
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}classification'.format(NAMESPACES['mods'])) is not None:
            all_classifications = []
            for classification in record.iterfind('./{0}classification'.format(NAMESPACES['mods'])):
                all_classifications.append(classification.text)
            return all_classifications
        else:
            return None

    def collection(self, elem=None):
        """
        Retrieve archival collection metadata from mods:relatedItem[type="host"]:
        return: {'location': collection location, 'title': collection title, 'url': link to collection (if found)}
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}relatedItem'.format(NAMESPACES['mods'])) is not None:
            for related_item in record.iterfind('./{0}relatedItem'.format(NAMESPACES['mods'])):
                if 'type' in related_item.attrib.keys():
                    if 'host' == related_item.attrib['type']:
                        host_info = {}
                        if self.title_constructor(related_item) is not None:
                            host_title = self.title_constructor(related_item)[0]
                            host_info['title'] = host_title

                        if self.physical_location(related_item) is not None:
                            host_location = self.physical_location(related_item)[0]
                            host_info['location'] = host_location

                        if related_item.find('./{0}location/{0}url'.format(NAMESPACES['mods'])).text is not None:
                            host_info['url'] = related_item.find('./{0}location/{0}url'.format(NAMESPACES['mods'])).text

                        return host_info
        else:
            return None

    def date_constructor(self, elem=None):
        """
        Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate, and mods:dateOther underneath mods:originInfo. Other date-type elements are ignored:
        return: A date containing string or None.
        """
        date_list = ['{0}dateIssued'.format(NAMESPACES['mods']),
                     '{0}dateCreated'.format(NAMESPACES['mods']),
                     '{0}copyrightDate'.format(NAMESPACES['mods']),
                     '{0}dateOther'.format(NAMESPACES['mods'])]
        ignore_list = ['{0}place'.format(NAMESPACES['mods']),
                       '{0}publisher'.format(NAMESPACES['mods']),
                       '{0}dateCaptured'.format(NAMESPACES['mods']),
                       '{0}dateValid'.format(NAMESPACES['mods']),
                       '{0}dateModified'.format(NAMESPACES['mods']),
                       '{0}edition'.format(NAMESPACES['mods']),
                       '{0}issuance'.format(NAMESPACES['mods']),
                       '{0}frequency'.format(NAMESPACES['mods'])]
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}originInfo'.format(NAMESPACES['mods'])) is not None:
            origin_info = record.find('./{0}originInfo'.format(NAMESPACES['mods']))
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
        else:
            return None

    def digital_origin(self, elem=None):
        """
        Accesses mods:digitalOrigin element:
        return: element text or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}digitalOrigin'.format(NAMESPACES['mods'])) is not None:
            return record.find('.//{0}digitalOrigin'.format(NAMESPACES['mods'])).text
        else:
            return None

    def doi_search(self, elem=None):
        """
        Get DigiNole IID from MODS record:
        return: item's IID.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}identifier'.format(NAMESPACES['mods'])) is not None:
            for identifier in record.iterfind('.//{0}identifier'.format(NAMESPACES['mods'])):
                if 'type' in identifier.attrib is not None:
                    if 'DOI' == identifier.attrib['type']:
                        return identifier.text
        else:
            return None

    def edition(self, elem=None):
        """
        Accesses mods:edition element:
        return: element text or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}edition'.format(NAMESPACES['mods'])) is not None:
            return record.find('.//{0}edition'.format(NAMESPACES['mods'])).text
        else:
            return None

    def extent(self, elem=None):
        """
        Accesses mods:extent element:
        return: list of mods:extent texts or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}extent'.format(NAMESPACES['mods'])) is not None:
            all_extents = []
            for extent in record.iterfind('.//{0}extent'.format(NAMESPACES['mods'])):
                all_extents.append(extent.text)
            return all_extents
        else:
            return None

    def form(self, elem=None):
        """
        Accesses mods:physicalDescription/mods:form element:
        return: list of mods:form texts or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}physicalDescription/{0}form'.format(NAMESPACES['mods'])) is not None:
            all_forms = []
            for form in record.iterfind('./{0}physicalDescription/{0}form'.format(NAMESPACES['mods'])):
                all_forms.append(form.text)
            return all_forms
        else:
            return None

    def genre(self, elem=None):
        """
        Accesses mods:genre element:
        return: [ { 'term': , 'authority': , 'authorityURI': , 'valueURI': }, ] or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}genre'.format(NAMESPACES['mods'])) is not None:
            all_genres = []
            for genre in record.iterfind('./{0}genre'.format(NAMESPACES['mods'])):
                genre_elems = {}
                genre_elems['term'] = genre.text
                if 'authority' in genre.attrib.keys():
                    genre_elems['authority'] = genre.attrib['authority']
                if 'authorityURI' in genre.attrib.keys():
                    genre_elems['authorityURI'] = genre.attrib['authorityURI']
                if 'valueURI' in genre.attrib.keys():
                    genre_elems['valueURI'] = genre.attrib['valueURI']
                all_genres.append(genre_elems)
            return all_genres
        else:
            return None

    def geographic_code(self, elem=None):
        """
        Accesses mods:geographicCode element:
        return: list of mods:geographicCode texts or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}subject/{0}geographicCode'.format(NAMESPACES['mods'])) is not None:
            all_geocodes = []
            for geocode in record.iterfind('./{0}subject/{0}geographicCode'.format(NAMESPACES['mods'])):
                all_geocodes.append(geocode.text)
            return all_geocodes
        else:
            return None

    def issuance(self, elem=None):
        """
        Accesses mods:issuance element:
        return: list of mods:issuance texts or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}issuance'.format(NAMESPACES['mods'])) is not None:
            all_issuances = []
            for issuance in record.iterfind('.//{0}issuance'.format(NAMESPACES['mods'])):
                all_issuances.append(issuance.text)
            return all_issuances
        else:
            return None

    def language(self, elem=None):
        """
        Accesses mods:languageterm elements:
        :return: list of of dicts [{term-type: term}] or None.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}language'.format(NAMESPACES['mods'])) is not None:
            all_languages = []
            for language in record.iterfind('.//{0}language'.format(NAMESPACES['mods'])):
                languages = {}
                for term in language.iterchildren():
                    if 'type' in term.keys():
                        languages[term.attrib['type']] = term.text
                    else:
                        languages['untyped'] = term.text
                all_languages.append(languages)
            return all_languages
        else:
            return None

    def local_identifier(self, elem=None, type='IID'):
        """
        Get DigiNole IID from MODS record:
        return: item's IID.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}identifier'.format(NAMESPACES['mods'])) is not None:
            for identifier in record.iterfind('.//{0}identifier'.format(NAMESPACES['mods'])):
                if 'type' in identifier.attrib is not None:
                    if type == identifier.attrib['type']:
                        return identifier.text

    def _nameGen_(names, full_name):
        keys = []
        for key in names.keys():
            keys.append(key)
        if all(x in keys for x in ['family', 'given',
                                   'termsOfAddress', 'date']):
            full_name = full_name + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ', ' + \
                       names['date']
        elif all(x in keys for x in ['family', 'given', 'date']):
            full_name = full_name + names['family'] + ', ' + names['given'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'given', 'termsOfAddress']):
            full_name = full_name + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['family', 'termsOfAddress', 'date']):
            full_name = full_name + names['family'] + ', ' + names['termsOfAddress'] + ', ' + names['date']
        elif all(x in keys for x in ['given', 'termsOfAddress', 'date']):
            full_name = full_name + names['given'] + ', ' + names['termsOfAddress'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'given']):
            full_name = full_name + names['family'] + ', ' + names['given']
        elif all(x in keys for x in ['family', 'date']):
            full_name = full_name + names['family'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'termsOfAddress']):
            full_name = full_name + names['family'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['given', 'date']):
            full_name = full_name + names['given'] + ', ' + names['date']
        elif all(x in keys for x in ['given', 'termsOfAddress']):
            full_name = full_name + names['given'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['termsOfAddress', 'date']):
            full_name = full_name + ', ' + names['termsOfAddress'] + ', ' + names['date']
        elif 'date' in keys:
            full_name = full_name + ', ' + names['date']
        elif 'termsOfAddress' in keys:
            full_name = full_name + ', ' + names['termsOfAddress']
        return full_name

    def name_constructor(self, elem=None):
        """
        Accesses mods:name/mods:namePart elements and reconstructs names into LOC order:
        return: a list of strings.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}name'.format(NAMESPACES['mods'])) is not None:
            all_names = []
            for name in record.iterfind('./{0}name'.format(NAMESPACES['mods'])):
                full_name = name.attrib
                name_text = ""

                if name.find('./{0}namePart'.format(NAMESPACES['mods'])) is not None:

                    # Multipart name
                    if len(name.findall('./{0}namePart'.format(NAMESPACES['mods']))) > 1:
                        names = {}
                        for name_part in name.iterfind('./{0}namePart'.format(NAMESPACES['mods'])):

                            # Untyped nameParts
                            if 'type' not in name_part.attrib.keys():
                                name_text = name_text + ', ' + name_part.text
                                full_name['text'] = name_text.strip(', ')
                            # Typed nameParts
                            elif 'type' in name_part.attrib.keys():
                                names[name_part.attrib['type']] = name_part.text

                        if len(names) > 0:
                            full_name['text'] = Record._nameGen_(names, name_text.strip(', '))

                    # Single part name
                    else:
                        full_name['text'] = name_text + name.find(
                            './{0}namePart'.format(NAMESPACES['mods'])).text

                    # Roles
                    if name.find('./{0}role'.format(NAMESPACES['mods'])) is not None:
                        for role_term in name.iterfind('./{0}role/{0}roleTerm'.format(NAMESPACES['mods'])):
                            if role_term.attrib['type'] == 'code':
                                full_name['roleCode'] = role_term.text
                            elif role_term.attrib['type'] == 'text':
                                full_name['roleText'] = role_term.text

                    all_names.append(full_name)

            if len(all_names) == 0:
                return None
            else:
                return all_names
        else:
            return None

    def note(self, elem=None):
        """
        Access mods:note elements and return a list of dicts:
        return: [{note-type: note-text}, untyped-note-text]
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}note'.format(NAMESPACES['mods'])) is not None:
            all_notes = []
            for note in record.iterfind('./{0}note'.format(NAMESPACES['mods'])):
                if len(note.attrib) >= 1:
                    if 'type' in note.attrib.keys():
                        typed_note = {note.attrib['type']: note.text}
                        all_notes.append(typed_note)
                    elif 'displayLabel' in note.attrib.keys():
                        labeled_note = {note.attrib['displayLabel']: note.text}
                        all_notes.append(labeled_note)
                    else:
                        all_notes.append({'untyped': note.text})
                else:
                    all_notes.append({'untyped': note.text})
            return all_notes
        else:
            return None

    def physical_description_note(self, elem=None):
        """
        Access mods:physicalDescription/mods:note elements and return a list of text values:
        return: list of note text values.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}physicalDescription'.format(NAMESPACES['mods'])) is not None:
            for physical_description in record.iterfind('./{0}physicalDescription'.format(NAMESPACES['mods'])):
                all_notes = []
                for note in physical_description.iterfind('./{0}note'.format(NAMESPACES['mods'])):
                    all_notes.append(note.text)
            return all_notes
        else:
            return None

    def physical_location(self, elem=None):
        """
        Access mods:mods/mods:location/mods:physicalLocation and return text values.
        return: list of element text values.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}location/{0}physicalLocation'.format(NAMESPACES['mods'])) is not None:
            all_locations = []
            for location in record.iterfind('./{0}location/{0}physicalLocation'.format(NAMESPACES['mods'])):
                all_locations.append(location.text)
            return all_locations
        else:
            return None

    def pid_search(self, elem=None, prefix='fsu:'):
        """
        Get fedora PID from MODS record:
        return: item's fedora PID.
        """
        pid = re.compile(prefix)
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}identifier'.format(NAMESPACES['mods'])) is not None:
            for identifier in record.iterfind('.//{0}identifier'.format(NAMESPACES['mods'])):
                match = pid.search(identifier.text)
                if match:
                    return match.string
        else:
            return None

    def publication_place(self, elem=None):
        """
        Access mods:place and return a list of dicts:
        return: [{termType: termText}, {'untyped': termText}, ...]
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}place'.format(NAMESPACES['mods'])) is not None:
            all_places = []
            for place in record.iterfind('.//{0}place'.format(NAMESPACES['mods'])):
                places = {}
                for term in place.iterchildren():
                    if 'type' in term.attrib.keys():
                        places[term.attrib['type']] = term.text
                    else:
                        places['untyped'] = term.text
                all_places.append(places)
            return all_places
        else:
            return None

    def publisher(self, elem=None):
        """
        Access mods:publisher and return a list of text values:
        return: [publisher, ...]
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}publisher'.format(NAMESPACES['mods'])) is not None:
            all_publishers = []
            for publisher in record.iterfind('.//{0}publisher'.format(NAMESPACES['mods'])):
                all_publishers.append(publisher.text)
            return all_publishers
        else:
            return None

    def purl_search(self, elem=None):
        """
        Accesses record's Persistent URL from mods:mods/mods:location/mods:url:
        return: item PURL as string.
        """
        purl = re.compile('((http://purl)[\w\d:#@%/;$()~_?\+-=\\\.&]+)')
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}location/{0}url'.format(NAMESPACES['mods'])) is not None:
            for url in record.iterfind('./{0}location/{0}url'.format(NAMESPACES['mods'])):
                match = purl.search(url.text)
                if match:
                    return match.string
        else:
            return None

    def rights(self, elem=None):
        """
        Access mods:rights[type="use and reproduction|useAndReproduction" and return a dict:
        return: {'text': elementText, 'URI': rightsURI}
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}accessCondition'.format(NAMESPACES['mods'])) is not None:
            for access_condition in record.iterfind('.//{0}accessCondition'.format(NAMESPACES['mods'])):
                rights = {}
                if 'use and reproduction' or 'useAndReproduction' in access_condition.attrib['type']:
                    rights['text'] = access_condition.text
                    if '{http://www.w3.org/1999/xlink}href' in access_condition.attrib.keys():
                        rights['URI'] = access_condition.attrib['{http://www.w3.org/1999/xlink}href']
            return rights
        else:
            return None

    def _subject_parser_(subject):
        parts = ['authority', 'authorityURI', 'valueURI']
        if subject.tag == '{0}subject'.format(NAMESPACES['mods']):
            subject_parts = {'text': Record._subject_text_(subject)}
        else:
            subject_parts = {'type': subject.tag, 'term': subject.text}
        children = []
        for part in parts:
            if part in subject.attrib.keys():
                subject_parts.update({part: subject.attrib[part]})
            else:
                pass
        for child in subject.iterchildren():
            children.append(Record._subject_parser_(child))
        if len(children) > 0:
            subject_parts.update({'children': children})
        return subject_parts

    def subject(self, elem=None):
        """
        Access mods:subject elements and returns a list of dicts:
        return: [{'authority': , 'authorityURI': , 'valueURI': , children: {'type': child element name, 'term': text value}}, ... ]
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}subject'.format(NAMESPACES['mods'])) is not None:
            all_subjects = []
            for subject in record.iterfind('./{0}subject'.format(NAMESPACES['mods'])):
                if 'authority' in subject.attrib.keys():
                    if 'lcsh' or 'lctgm' or 'fast' == subject.attrib['authority'].lower():
                        all_subjects.append(Record._subject_parser_(subject))
                    elif 'naf' or 'lcnaf' == subject.attrib['authority'].lower():
                        if self.name_constructor(subject) is not None:
                            all_subjects.append(self.name_constructor(subject)[0])
                else:
                    all_subjects.append(Record._subject_parser_(subject))
            return all_subjects
        else:
            return None

    def _subject_text_(subject):
        subject_text = ""
        for child in subject:
            if child.tag == '{0}name'.format(NAMESPACES['mods']):
                subject_text = subject_text + '--' + Record.name_constructor(subject, elem=child.getparent())[0]['text']
            else:
                subject_text = subject_text + '--' + child.text
        return subject_text.strip(' -,.')

    def subject_constructor(self, elem=None):
        """
        Access mods:subject elements and parses text values into LOC double hyphenated complex headings
        return: A list of strings
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if self.subject(record) is not None:
            subject_text_list = []
            for subject in self.subject(record):
                subject_text_list.append(subject['text'])
            return subject_text_list
        else:
            return None

    def title_constructor(self, elem=None):
        """
        Accesses children of mods:titleInfo and return a list of titles in natural order:
        return: list of titles.
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('./{0}titleInfo'.format(NAMESPACES['mods'])) is not None:
            all_titles = []
            for title in record.iterfind('./{0}titleInfo'.format(NAMESPACES['mods'])):
                if title.find('./{0}nonSort'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}title'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])) is not None:
                    title_full = title.find('./{0}nonSort'.format(NAMESPACES['mods'])).text + ' ' + title.find(
                        './{0}title'.format(NAMESPACES['mods'])).text + ': ' + title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])).text
                elif title.find('./{0}nonSort'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}title'.format(NAMESPACES['mods'])) is not None:
                    title_full = title.find('./{0}nonSort'.format(NAMESPACES['mods'])).text + ' ' + title.find(
                        './{0}title'.format(NAMESPACES['mods'])).text
                elif title.find('./{0}title'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])) is not None:
                    title_full = title.find('./{0}title'.format(NAMESPACES['mods'])).text + ': ' + title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])).text
                else:
                    title_full = title.find('./{0}title'.format(NAMESPACES['mods'])).text
                all_titles.append(title_full)
            return all_titles
        else:
            return None

    def type_of_resource(self, elem=None):
        """
        Access mods:typeOfResource and return text value:
        return: text value or None
        """
        if elem is not None:
            record = elem
        else:
            record = self[0]
        if record.find('.//{0}typeOfResource'.format(NAMESPACES['mods'])) is not None:
            type_of_resource = record.find('.//{0}typeOfResource'.format(NAMESPACES['mods']))
            return type_of_resource.text
        else:
            return None

#    def _exists(self, elem):
#        if self[0].find(elem) is not None:
#            return True
#        else:
#            return None
#            #raise ElementNotFound
