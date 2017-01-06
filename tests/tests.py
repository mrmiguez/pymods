import sys

sys.path.append('../')

from pymods import MODS, FSUDL, OAI



mods = OAI('C:\\Users\\mmiguez\\bin\pymods\\tests\\fsu_nap01.oai.mods.xml')

#print(mods.set_spec)

for record in mods.record_list:
    print(mods.pid_search())

#for record in mods.record_list:
#    print(mods.pid_search(record))

#for record in mods.record_list:
#    print(OAI.pid_search(mods, record))