import mtgplan as mp
print("GOTTA")
print(', '.join(mp.all_essential['All-hands meeting']))  
mp.view(mp.essential['All-hands meeting'])
print("SELF-SELECTED")
print(', '.join(mp.all_mtg_by_mtg['All-hands meeting']))   
mp.view(mp.mtg_by_mtg['All-hands meeting'])
print("ALL")
mp.view(mp.all_pop)
