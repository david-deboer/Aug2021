import mtgplan as mp

print(mp.meetings)

incl_names = 'not-present'  # vs 'present' or False
meeting = "All-hands meeting"  # see meetings in mtgplan.py

print("VIABLE (subjective; 'x' field in hera_mtg_planning.json)")
show_down_to = 12  # cut-off number
x = mp.view('x', meeting, header=True, names=incl_names, show=show_down_to)

print("-------------------------------------------")
print("SELF-SELECTED (from googlesheet; 'meetings' in hera_mtg_planning.json)")
show_down_to = 15  # cut-off number
m = mp.view('mtg', meeting, header=True, names=incl_names, show=show_down_to)

print("-------------------------------------------")
print("ALL (all from whenisgood)")
show_down_to = 23  # cut-off number
p = mp.view('pop', meeting, header=False, names=incl_names, show=show_down_to)

print("writing results.csv")
