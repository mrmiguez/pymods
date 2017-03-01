import sys

sys.path.append('../')

from pymods import MODS, FSUDL, OAI


mods = MODS('tests/fsu_nap01-1.xml')

#print(mods.nsroot)

#for record in mods.record_list:
#    print(mods.pid_search())

for record in mods.record_list:
    try:
        for name in MODS.name_constructor(record):
            print(name)
    except TypeError:
        pass

#for record in mods.record_list:
#    print(OAI.pid_search(mods, record))