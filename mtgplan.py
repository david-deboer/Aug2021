import json
from argparse import Namespace
import os


with open('hera_mtg_planning.json', 'r') as fp:
    mtg_availability = json.load(fp)

meetings = ['All-hands meeting', 'Analog', 'Pspec', 'pyuvsim/pyradiosky alternating',
            'Commissioning', 'Correlator', 'Site', 'pyuvdata', 'NRAO',
            'Analysis/Quality Metrics alternating', 'Imaging (biweekly)', 'Validation',
            'Machine learning', 'Theory Meets Data']

dow = {'Mon': '1', 'Tues': '2', 'Wed': '3', 'Thurs': '4', 'Fri': '5'}

MD = Namespace(pop={}, mtg={}, all_mtg={}, x={}, all_x={})

for person in mtg_availability.keys():
    for avail in mtg_availability[person]['available']:
        MD.pop.setdefault(avail, [])
        MD.pop[avail].append(person)
    for this_mtg in mtg_availability[person]['meetings']:
        MD.all_mtg.setdefault(this_mtg, [])
        MD.all_mtg[this_mtg].append(person)
        MD.mtg.setdefault(this_mtg, {})
        for avail in mtg_availability[person]['available']:
            MD.mtg[this_mtg].setdefault(avail, [])
            MD.mtg[this_mtg][avail].append(person)
    for this_mtg in mtg_availability[person]['x']:
        MD.all_x.setdefault(this_mtg, [])
        MD.all_x[this_mtg].append(person)
        MD.x.setdefault(this_mtg, {})
        for avail in mtg_availability[person]['available']:
            MD.x[this_mtg].setdefault(avail, [])
            MD.x[this_mtg][avail].append(person)

csv_file = 'results.csv'
if os.path.exists(csv_file):
    os.remove(csv_file)


def view(mtype='mtg', meeting='All-hands meeting',
         header=True, names='not-present', show=0, csv=True):
    ranked = {}
    if mtype == 'pop':
        this = MD.pop
        all = list(mtg_availability.keys())
    else:
        this = getattr(MD, mtype)[meeting]
        all = getattr(MD, 'all_'+mtype)[meeting]
    hdr = "{}-{}:  {}".format(mtype, meeting, ', '.join(all))
    if names:
        hdr += '\n{}<{}>'.format(24*' ', names)
    if header:
        print(hdr)
    for key, val in this.items():
        d, h = key.split()
        th = [int(x) for x in h.split(':')]
        this_key = "{:02d}_{}_{:02d}:{:02d}_{}".format(len(val), dow[d], th[0], th[1], key)
        ranked[this_key] = val
    this_len = len(all)
    if csv:
        fp = open(csv_file, 'a')
        # print('{},{},{},{}'.format(mtype, meeting, names, ','.join(all)), file=fp)
    for ordrk in sorted(list(ranked.keys()), reverse=True):
        n, _a, _b, sch = ordrk.split('_')
        if int(n) < show:
            continue
        csv_row = [mtype, meeting, n, this_len, sch.split()[0], sch.split()[1]]
        print('{} / {:02d} {:14s}'.format(n, this_len, sch), end='')
        if names == 'present':
            print('  {}'.format(', '.join(ranked[ordrk])))
            csv_row += ranked[ordrk]
        elif names == 'not-present':
            np = []
            for nm in all:
                if nm not in ranked[ordrk]:
                    np.append(nm)
            print('  {}'.format(', '.join(np)))
            csv_row += np
        else:
            print()
        if csv:
            row = ','.join([str(x) for x in csv_row])
            print('{}'.format(row), file=fp)
    if csv:
        fp.close()
    return ranked
