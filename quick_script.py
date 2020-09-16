import mtgplan as mp
# See list in mtgplan
incl_names = True
meeting = "All-hands meeting"  # see meetings in mtgplan.py

print("VIABLE (subjective; 'x' field in hera_mtg_planning.json)")
print(', '.join(mp.all_essential[meeting]))
show_down_to = 12  # cut-off number
mp.view(mp.essential[meeting], len(mp.all_essential[meeting]), incl_names, show_down_to)

print("-------------------------------------------")
print("SELF-SELECTED (from googlesheet; 'meetings' in hera_mtg_planning.json)")
print(', '.join(mp.all_mtg_by_mtg[meeting]))
show_down_to = 15  # cut-off number
mp.view(mp.mtg_by_mtg[meeting], len(mp.all_mtg_by_mtg[meeting]), incl_names, show_down_to)

print("-------------------------------------------")
print("ALL (all from whenisgood)")
show_down_to = 23  # cut-off number
mp.view(mp.all_pop, mp.num_all, incl_names, show_down_to)
