#!/usr/bin/env python3
from lxml import etree
from pymods import mods, fsudl

NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
tree = etree.parse('fsu_cookbooksandherbals.xml')
root = tree.getroot()
for record in root.iterfind('.//{%s}mods' % NS['mods']):
#    if pymods.mods_note(record, NS) is not None:
    for subject in mods.subject_generator(record, NS):
        print(fsudl.pid_search(record, NS), ':', subject)
