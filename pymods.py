import re
from lxml import etree

nameSpace_default = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 
                     'dc': 'http://purl.org/dc/elements/1.1/', 
                     'mods': 'http://www.loc.gov/mods/v3', 
                     'dcterms': 'http://purl.org/dc/terms'}

'''
Elements to add 2016-02-11:
    originInfo
        dates
    subject
        URI
        authority (& split by authority... i.e. colocate TGM, LCSH, & FAST)
        geographicCode
    realtedItem
    relatedItem (archival host collection)
        purl to finding aid
        collection title
    location - physical location
    recordInfo (??)
'''
class mods:
    '''
    class Error(Exception):
        pass
        
    class No_MODS_Error(Error):
        def __init__(self, expression, message):
            self.expression = expression
            self.message = message
    '''
    def load(input_file, nameSpace_dict=nameSpace_default):
        tree = etree.parse(input_file)
        root = tree.getroot()
        if len(root.findall('.//{%s}mods' % nameSpace_dict['mods'])) > 1:
            record_list = []
            for record in root.iterfind('.//{%s}mods' % nameSpace_dict['mods']):
                record_list.append(record)
            return record_list
        #elif len(root.findall('.//{%s}mods' % nameSpace_dict['mods'])) == 1:
        else:
            return root
#        else:
#            print('No MODS record detected.')    
        


    def abstract(record, nameSpace_dict=nameSpace_default):
        allAbstracts = []
        if record.find('./{%s}abstract' % nameSpace_default['mods']) is not None:
            for abstract in record.iterfind('./{%s}abstract' % nameSpace_dict['mods']):
                if len(abstract.attrib) >= 1:
                    if 'type' in abstract.attrib.keys():
                        typed_abstract = {abstract.attrib['type'] : abstract.text}
                        allAbstracts.append(typed_abstract)
                    elif 'displayLabel' in abstract.attrib.keys():
                        labeled_abstract = {abstract.attrib['displayLabel'] : abstract.text}
                        allAbstracts.append(labeled_abstract)
                    else:
                        allAbstracts.append(abstract.text)
                else:
                    allAbstracts.append(abstract.text)
        return allAbstracts


    def physicalDescription_note(record, nameSpace_dict=nameSpace_default):
        allNotes = []
        for physicalDescription in record.iterfind('./{%s}physicalDescription' % nameSpace_dict['mods']):
            for note in physicalDescription.iterfind('./{%s}note' % nameSpace_dict['mods']):
                allNotes.append(note.text)
        return allNotes


    def physicalLocation(record, nameSpace_dict=nameSpace_default):
        allLocations = []
        if record.find('.//{%s}physicalLocation' % nameSpace_dict['mods']) is not None:
            for location in record.iterfind('.//{%s}physicalLocation' % nameSpace_dict['mods']):
                allLocations.append(location.text)
        else:
            allLocations.append(None)
        return allLocations


    def extent(record, nameSpace_dict=nameSpace_default):
        allExtents = []
        if record.find('.//{%s}extent' % nameSpace_dict['mods']) is not None:
            for extent in record.iterfind('.//{%s}extent' % nameSpace_dict['mods']):
                allExtents.append(extent.text)
        else:
            allExtents.append('None')
        return allExtents


    def issuance(record, nameSpace_dict=nameSpace_default):
        allIssuances = []
        if record.find('.//{%s}issuance' % nameSpace_dict['mods']) is not None:
            for issuance in record.iterfind('.//{%s}issuance' % nameSpace_dict['mods']):
                allIssuances.append(issuance.text)
        else:
            allIssuances.append('None')
        return allIssuances


    def publication_place(record, nameSpace_dict=nameSpace_default):
        allPlaces = []
        if record.find('.//{%s}place' % nameSpace_dict['mods']) is not None:
            for place in record.iterfind('.//{%s}place' % nameSpace_dict['mods']):
                places = {}
                for term in place.iterchildren():
                    places[term.attrib['type']] = term.text
                allPlaces.append(places)
        else:
            allPlaces.append('None')
        return allPlaces

   
    def publisher(record, nameSpace_dict=nameSpace_default):
        allPublishers = []
        if record.find('.//{%s}publisher' % nameSpace_dict['mods']) is not None:
            for publisher in record.iterfind('.//{%s}publisher' % nameSpace_dict['mods']):
                allPublishers.append(publisher.text)
        else:
            allPublishers.append('None')
        return allPublishers


    def note(record, nameSpace_dict=nameSpace_default):
        allNotes = []
        for note in record.iterfind('./{%s}note' % nameSpace_dict['mods']):
            if len(note.attrib) >= 1:
                if 'type' in note.attrib.keys():
                    typed_note = {note.attrib['type'] : note.text}
                    allNotes.append(typed_note)
                elif 'displayLabel' in note.attrib.keys():
                    labeled_note = {note.attrib['displayLabel'] : note.text}
                    allNotes.append(labeled_note)
                else:
                    allNotes.append(note.text)
            else:
                allANotes.append(note.text)
        return allNotes


    def digitalOrigin(record, nameSpace_dict):
        if record.find('.//{%s}digitalOrigin' % nameSpace_dict['mods']) is not None:
            return record.find('.//{%s}digitalOrigin' % nameSpace_dict['mods']).text
        else:
            return None


    def language(record, nameSpace_dict=nameSpace_default):
        allLanguages = []
        if record.find('.//{%s}language' % nameSpace_dict['mods']) is not None:
            for language in record.iterfind('.//{%s}language' % nameSpace_dict['mods']):
                languages = {}
                for term in language.iterchildren():
                    languages[term.attrib['type']] = term.text
                allLanguages.append(languages)
            return allLanguages
        else:
            return None


    def genre_text(record, nameSpace_dict=nameSpace_default):
        if record.find('.//{%s}genre' % nameSpace_dict['mods']) is not None:
            genre = record.find('.//{%s}genre' % nameSpace_dict['mods'])
            return genre.text
        else:
            return None

    def genre_URIs(record, nameSpace_dict=nameSpace_default):
        genreURIs = []
        for genre_elem in record.iterfind('.//{%s}genre' % nameSpace_dict['mods']):
            if len(genre_elem.attrib) >= 1:
                genreURI = {}
                for key in genre_elem.attrib.keys():
                    genreURI[key] = genre_elem.attrib[key]
                genreURIs.append(genreURI)
        return genreURIs
      

    def typeOfResource(record, nameSpace_dict=nameSpace_default):
        if record.find('.//{%s}typeOfResource' % nameSpace_dict['mods']) is not None:
            typeOfResource = record.find('.//{%s}typeOfResource' % nameSpace_dict['mods'])
            return typeOfResource.text
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


    def name_generator(record, nameSpace_dict=nameSpace_default):
        allNames = []
        if len(record.findall('./{%s}name' % nameSpace_dict['mods'])) > 0:
            for name in record.iterfind('./{%s}name' % nameSpace_dict['mods']):
                fullName = ""
                if len(name.findall('./{%s}namePart' % nameSpace_dict['mods'])) > 1:
                    # Multipart name
                    names = {}
                    for namePart in name.findall('./{%s}namePart' % nameSpace_dict['mods']):
                        if 'type' not in namePart.attrib.keys():
                            fullName = namePart.text
                        elif 'type' in namePart.attrib.keys():
                            names[namePart.attrib['type']] = namePart.text
                    fullName = mods._nameGen_(names, fullName)
                else:
                    # Single part name
                    fullName = fullName + name.find('./{%s}namePart' % nameSpace_dict['mods']).text
                allNames.append(fullName)
            return allNames
        else:
            allNames.append('None')
            return allNames


    def title_generator(record, nameSpace_dict=nameSpace_default):
        allTitles = []
        for title in record.iterfind('.//{%s}titleInfo' % nameSpace_dict['mods']):
            if title.find('./{%s}nonSort' % nameSpace_dict['mods']) is not None and title.find(
                            './{%s}title' % nameSpace_dict['mods']) is not None and title.find(
                            './{%s}subTitle' % nameSpace_dict['mods']) is not None:
                titleFull = title.find('./{%s}nonSort' % nameSpace_dict['mods']).text + ' ' + title.find(
                    './{%s}title' % nameSpace_dict['mods']).text + ': ' + title.find(
                    './{%s}subTitle' % nameSpace_dict['mods']).text
            elif title.find('./{%s}nonSort' % nameSpace_dict['mods']) is not None and title.find(
                            './{%s}title' % nameSpace_dict['mods']) is not None:
                titleFull = title.find('./{%s}nonSort' % nameSpace_dict['mods']).text + ' ' + title.find(
                    './{%s}title' % nameSpace_dict['mods']).text
            else:
                titleFull = title.find('./{%s}title' % nameSpace_dict['mods']).text
            allTitles.append(titleFull)
        return allTitles


    def date_generator(record, nameSpace_dict=nameSpace_default):
        if record.find('./{%s}originInfo/{%s}copyrightDate' % (
        nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
            date = record.find(
                './{%s}originInfo/{%s}copyrightDate' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
        elif record.find(
                        './{%s}originInfo/{%s}dateCreated' % (nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
            date = record.find(
                './{%s}originInfo/{%s}dateCreated' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
        elif record.find(
                        './{%s}originInfo/{%s}dateIssued' % (nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
            date = record.find(
                './{%s}originInfo/{%s}dateIssued' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
        elif record.find(
                        './{%s}originInfo/{%s}dateOther' % (nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
            date = record.find(
                './{%s}originInfo/{%s}dateOther' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
        else:
            date = "No date"
        return date
        
    def subject_generator(record, nameSpace_dict=nameSpace_default):
        allSubjects = []
        for subject in record.iterfind('.//{%s}subject' % nameSpace_dict['mods']):
            fullSubject = []
            for subjectTerm in subject.iterchildren():
                fullSubject.append({subjectTerm.tag[28: ] : subjectTerm.text})
    #        if fullSubject:
    #            allSubjects.append(fullSubject)
            allSubjects.append(fullSubject)
        return allSubjects

class fsudl:
    
    def purl_search(mods_record, nameSpace_dict=nameSpace_default):
        purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
        for url in mods_record.iterfind('./{%s}location/{%s}url' % (nameSpace_dict['mods'], nameSpace_dict['mods'])):
            match = purl.search(url.text)
            if match:
                return match.group()


    def pid_search(mods_record, nameSpace_dict=nameSpace_default):
        pid = re.compile('fsu:[0-9]*')
        for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
            match = pid.search(identifier.text)
            if match:
                return match.group()
                
    def local_identifier(mods_record, nameSpace_dict=nameSpace_default):
        for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
            if 'type' in identifier.attrib is not None:
                if 'IID' == identifier.attrib['type']:
                    return identifier.text
                
                
class oai_dc:

    '''
    Some implementations of the OAI-PMH standard do not include the
    default namespace for oai_dc. A future release will include a test
    for inclusion of the default namespace,and add it to the file when
    not present.
    '''

    def load(input_file, nameSpace_dict=nameSpace_default):
        record_list = []
        tree = etree.parse(input_file)
        root = tree.getroot()
        for record in root.iterfind('.//{%s}record' % nameSpace_dict['oai_dc']):
            record_list.append(record)
        return record_list
    

    def pid_search(record, nameSpace_dict=nameSpace_default):
        pid = re.compile('fsu_[0-9]*')
        for identifier in record.iterfind('.//{%s}identifier' % nameSpace_dict['oai_dc']):
            match = pid.search(identifier.text)
            if match:
                return match.group().replace('_',':')
