#!/usr/bin/env python3
from lxml import etree
from pymods import mods, fsudl, oai_dc

for record in mods.load('fsu_cookbooksandherbals.xml'):
#    for iid in fsudl.local_identifier(record):
    print(fsudl.pid_search(record), ':', fsudl.local_identifier(record))
