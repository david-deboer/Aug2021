import mtgplan as mp
# See list in mtgplan
meeting = "All-hands meeting"
print("GOTTA")  # This is from the googlesheet of meeting contributors
print(', '.join(mp.all_essential[meeting]))
mp.view(mp.essential[meeting])
print("-------------------------------------------")
print("SELF-SELECTED")
print(', '.join(mp.all_mtg_by_mtg[meeting]))
mp.view(mp.mtg_by_mtg[meeting])
print("-------------------------------------------")
print("ALL")
mp.view(mp.all_pop)
