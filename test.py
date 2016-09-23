#!/usr/bin/env python3
from lxml import etree
from pymods import mods, fsudl, oai_dc

for record in mods.load('fsu_cookbooksandherbals.xml'):
    for publisher in mods.abstract(record):
        print(fsudl.pid_search(record), ':', publisher)
