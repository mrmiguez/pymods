import sys

sys.path.append('../')

from pymods import MODS, FSUDL, OAI


mods = MODS('tests/fsu_nap01-1.xml')

#print(mods.nsroot)

#for record in mods.record_list:
#    print(mods.pid_search())

for record in mods.record_list:
    print(FSUDL.pid_search(record), MODS.geographic_code(record))

#for record in mods.record_list:
#    print(OAI.pid_search(mods, record))