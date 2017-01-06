import sys

sys.path.append('../')

from pymods import MODS, FSUDL, OAI


mods = OAI('fsu_nap01-1.xml')

#print(mods.nsroot)

#for record in mods.record_list:
#    print(mods.pid_search())

for record in mods.record_list:
    print(mods.pid_search(record), mods.oai_urn)

#for record in mods.record_list:
#    print(OAI.pid_search(mods, record))