#!/usr/bin/env python3
from lxml import etree
from pymods import mods, fsudl

tree = etree.parse('fsu_cookbooksandherbals.xml')
root = tree.getroot()
for record in root.iterfind('.//{%s}mods' % 'http://www.loc.gov/mods/v3'):
#    if pymods.mods_note(record, NS) is not None:
    for subject in mods.subject_generator(record):
        print(fsudl.pid_search(record), ':', subject)
