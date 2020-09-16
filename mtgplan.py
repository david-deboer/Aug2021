import json

with open('hera_mtg_planning.json', 'r') as fp:
    mtg = json.load(fp)

meetings = ['All-hands meeting', 'Analog', 'Pspec', 'pyuvsim/pyradiosky alternating',
            'Commissioning', 'Correlator', 'Site', 'pyuvdata', 'NRAO',
            'Analysis/Quality Metrics alternating', 'Imaging (biweekly)', 'Validation',
            'Machine learning', 'Theory Meets Data']

dow = {'Mon': '1', 'Tues': '2', 'Wed': '3', 'Thurs': '4', 'Fri': '5'}

num_all = len(list(mtg.keys()))
all_pop = {}
mtg_by_mtg = {}
all_mtg_by_mtg = {}
essential = {}
all_essential = {}
for pn in mtg.keys():
    for avail in mtg[pn]['available']:
        all_pop.setdefault(avail, [])
        all_pop[avail].append(pn)
    for this_mtg in mtg[pn]['meetings']:
        all_mtg_by_mtg.setdefault(this_mtg, [])
        all_mtg_by_mtg[this_mtg].append(pn)
        mtg_by_mtg.setdefault(this_mtg, {})
        for avail in mtg[pn]['available']:
            mtg_by_mtg[this_mtg].setdefault(avail, [])
            mtg_by_mtg[this_mtg][avail].append(pn)
    for this_mtg in mtg[pn]['x']:
        all_essential.setdefault(this_mtg, [])
        all_essential[this_mtg].append(pn)
        essential.setdefault(this_mtg, {})
        for avail in mtg[pn]['available']:
            essential[this_mtg].setdefault(avail, [])
            essential[this_mtg][avail].append(pn)


def view(this_one=mtg_by_mtg['All-hands meeting'], Nplan=-1, include_names=True, cull=0):
    ranked = {}
    for key, val in this_one.items():
        d, h = key.split()
        th = [int(x) for x in h.split(':')]
        this_key = "{:02d}_{}_{:02d}:{:02d}_{}".format(len(val), dow[d], th[0], th[1], key)
        ranked[this_key] = val

    for ordrk in sorted(list(ranked.keys()), reverse=True):
        n, _a, _b, sch = ordrk.split('_')
        if int(n) < cull:
            continue
        if Nplan > 0:
            print('{} / {:02d} {:14s}'.format(n, Nplan, sch))
        else:
            print('{} {:14s}'.format(n, sch))
        if include_names:
            print('  {}'.format(', '.join(ranked[ordrk])))
