import json


class MeetingPlanner:
    meetings = ['All-hands meeting', 'Analog', 'Pspec',
                'pyuvsim/pyradiosky alternating', 'Commissioning', 'Correlator',
                'Site', 'pyuvdata', 'NRAO', 'Analysis/Quality Metrics alternating',
                'Imaging (biweekly)', 'Validation', 'Machine learning',
                'Theory Meets Data', 'Instrument Modeling']
    dow = {'Mon': '1', 'Tues': '2', 'Wed': '3', 'Thurs': '4', 'Fri': '5'}
    all_mtypes = ['all', 'mtg', 'x']

    def __init__(self, fn='hera_mtg_planning.json'):
        self.fn = fn
        for mtype in self.all_mtypes:
            setattr(self, mtype, {})
            setattr(self, 'all_{}'.format(mtype), {})
        self.csv_fp = None

    def setup(self):
        with open(self.fn, 'r') as fp:
            self.mtg_availability = json.load(fp)
        for person in self.mtg_availability.keys():
            for avail in self.mtg_availability[person]['available']:
                self.all.setdefault(avail, [])
                self.all[avail].append(person)
            for this_mtg in self.mtg_availability[person]['meetings']:
                self.all_mtg.setdefault(this_mtg, [])
                self.all_mtg[this_mtg].append(person)
                self.mtg.setdefault(this_mtg, {})
                for avail in self.mtg_availability[person]['available']:
                    self.mtg[this_mtg].setdefault(avail, [])
                    self.mtg[this_mtg][avail].append(person)
            for this_mtg in self.mtg_availability[person]['x']:
                self.all_x.setdefault(this_mtg, [])
                self.all_x[this_mtg].append(person)
                self.x.setdefault(this_mtg, {})
                for avail in self.mtg_availability[person]['available']:
                    self.x[this_mtg].setdefault(avail, [])
                    self.x[this_mtg][avail].append(person)

    def reset_file(self, meeting):
        if self.csv_fp is None:
            meeting = meeting.replace('/', '')
            meeting = meeting.replace(' ', '')
            meeting = meeting.replace('(', '')
            meeting = meeting.replace(')', '')
            meeting = meeting.replace('-', '')
            self.mcsv = "{}.csv".format(meeting)
            self.csv_fp = open(self.mcsv, 'w')
            print("mtype,meeting,available,total,day,hour,not-present", file=self.csv_fp)
        else:
            self.csv_fp.close()
            print("Writing {}".format(self.mcsv))
            self.csv_fp = None

    def view(self, mtype='mtg', meeting='All-hands meeting',
             header=True, names='not-present', show=0, csv=True):
        if meeting not in self.meetings:
            raise ValueError("{} not valid meeting".format(meeting))
        ranked = {}
        if mtype == 'all':
            this = self.all
            all = list(self.mtg_availability.keys())
        else:
            this = getattr(self, mtype)[meeting]
            all = getattr(self, 'all_'+mtype)[meeting]
        hdr = "{}-{}:  {}".format(mtype, meeting, ', '.join(all))
        if names:
            hdr += '\n{}<{}>'.format(24*' ', names)
        if header:
            print(hdr)
        for key, val in this.items():
            d, h = key.split()
            th = [int(x) for x in h.split(':')]
            this_key = "{:02d}_{}_{:02d}:{:02d}_{}".format(len(val), self.dow[d], th[0], th[1], key)
            ranked[this_key] = val
        this_len = len(all)
        # if csv:
        #     print('{},{},{},{}'.format(mtype, meeting, names, ','.join(all)), file=self.csv_fp)
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
                print('{}'.format(row), file=self.csv_fp)
        return ranked
