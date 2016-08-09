from lxml import etree
import re

'''
Elements to add 2016-02-11:


    originInfo
        dates
        publisher
        place of pub
        issuance

    physDesc
        extent
        notes

    abstract

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
def mods_note(mods_record, nameSpace_dict):
    allNotes = []
    for note in mods_record.iterfind('./{%s}note' % nameSpace_dict['mods']):
        allNotes.append(note.text)
    return allNotes


def mods_digitalOrigin(mods_record, nameSpace_dict):
    if mods_record.find('.//{%s}digitalOrigin' % nameSpace_dict['mods']) is not None:
        return mods_record.find('.//{%s}digitalOrigin' % nameSpace_dict['mods']).text
    else:
        return None


def mods_language(mods_record, nameSpace_dict):
    allLanguages = []
    if mods_record.find('.//{%s}language' % nameSpace_dict['mods']) is not None:
        for language in mods_record.iterfind('.//{%s}language' % nameSpace_dict['mods']):
            languages = {}
            for term in language.iterchildren():
                languages[term.attrib['type']] = term.text
            allLanguages.append(languages)
        return allLanguages
    else:
        return None


def mods_genre_text(mods_record, nameSpace_dict):
    if mods_record.find('.//{%s}genre' % nameSpace_dict['mods']) is not None:
        genre = mods_record.find('.//{%s}genre' % nameSpace_dict['mods'])
        return genre.text
    else:
        return None

def mods_genre_URIs(mods_record, nameSpace_dict):
    genreURIs = []
    for genre_elem in mods_record.iterfind('.//{%s}genre' % nameSpace_dict['mods']):
        if len(genre_elem.attrib) >= 1:
            genreURI = {}
            for key in genre_elem.attrib.keys():
                genreURI[key] = genre_elem.attrib[key]
            genreURIs.append(genreURI)
    return genreURIs
  

def mods_typeOfResource(mods_record, nameSpace_dict):
    if mods_record.find('.//{%s}typeOfResource' % nameSpace_dict['mods']) is not None:
        typeOfResource = mods_record.find('.//{%s}typeOfResource' % nameSpace_dict['mods'])
        return typeOfResource.text
    else:
        return None


def nameGen(names, fullName):
    keys = []
    for key in names.keys():
        keys.append(key)
    if all(x in keys for x in ['family', 'given', 'termsOfAddress', 'date']):
        fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ' ' + names[
            'date']
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


def mods_name_generator(mods_record, nameSpace_dict):
    allNames = []
    for name in mods_record.iterfind('./{%s}name' % nameSpace_dict['mods']):
        fullName = ""
        if len(name.findall('./{%s}namePart' % nameSpace_dict['mods'])) > 1:
            # Multipart name
            names = {}
            for namePart in name.findall('./{%s}namePart' % nameSpace_dict['mods']):
                if 'type' not in namePart.attrib.keys():
                    fullName = namePart.text
                elif 'type' in namePart.attrib.keys():
                    names[namePart.attrib['type']] = namePart.text
            fullName = nameGen(names, fullName)
        else:
            # Single part name
            fullName = fullName + name.find('./{%s}namePart' % nameSpace_dict['mods']).text
        allNames.append(fullName)
        return allNames


def mods_title_generator(mods_record, nameSpace_dict):
    allTitles = []
    for title in mods_record.iterfind('.//{%s}titleInfo' % nameSpace_dict['mods']):
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


def mods_date_generator(mods_record, nameSpace_dict):
    if mods_record.find('./{%s}originInfo/{%s}copyrightDate' % (
    nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
        date = mods_record.find(
            './{%s}originInfo/{%s}copyrightDate' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
    elif mods_record.find(
                    './{%s}originInfo/{%s}dateCreated' % (nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
        date = mods_record.find(
            './{%s}originInfo/{%s}dateCreated' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
    elif mods_record.find(
                    './{%s}originInfo/{%s}dateIssued' % (nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
        date = mods_record.find(
            './{%s}originInfo/{%s}dateIssued' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
    elif mods_record.find(
                    './{%s}originInfo/{%s}dateOther' % (nameSpace_dict['mods'], nameSpace_dict['mods'])) is not None:
        date = mods_record.find(
            './{%s}originInfo/{%s}dateOther' % (nameSpace_dict['mods'], nameSpace_dict['mods'])).text
    else:
        date = "No date"
    return date


def fsudl_purl_search(mods_record, nameSpace_dict):
    purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
    for url in mods_record.iterfind('./{%s}location/{%s}url' % (nameSpace_dict['mods'], nameSpace_dict['mods'])):
        match = purl.search(url.text)
        if match:
            return match.group()


def fsudl_pid_search(mods_record, nameSpace_dict):
    pid = re.compile('fsu:[0-9]*')
    for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
        match = pid.search(identifier.text)
        if match:
            return match.group()


def mods_subject_generator(mods_record, nameSpace_dict):
    allSubjects = []
    for subject in mods_record.iterfind('.//{%s}subject' % nameSpace_dict['mods']):
        fullSubject = []
        for subjectTerm in subject:
            fullSubject.append(subjectTerm.text)
        if fullSubject:
            allSubjects.append(fullSubject)
    return allSubjects
