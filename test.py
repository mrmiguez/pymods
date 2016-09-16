#!/usr/bin/env python3
from lxml import etree
from pymods import mods, fsudl, oai_dc

for record in oai_dc.load('fsu_bepress_modern_etds.mods.xml'):
#    for subject in mods.subject_generator(record):
        print(oai_dc.pid_search(record))#, ':', subject)
