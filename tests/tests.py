import sys

sys.path.append('../')

from pymods import MODS, FSUDL

mods = MODS('fsu_nap01-1.xml')

for record in mods.record_list:
    if MODS.subject(record) is not None:
        for subject in MODS.subject(record):
            print(subject)
            #if subject['authority'] == ('naf' or 'lcnaf'):
            #    print( '\n' + FSUDL.pid_search(record), subject['text'])