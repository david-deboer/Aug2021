import json
DOW = {'Mon': '1', 'Tues': '2', 'Wed': '3', 'Thurs': '4', 'Fri': '5'}


class MeetingPlanner:

    def __init__(self, fn='hera_mtg_planning.json', info_fn="meeting_info.json"):
        self.fn = fn
        with open(info_fn, 'r') as fp:
            self.info = json.load(fp)
        self.meetings = {}
        self.planner = {}
        for mtg in self.info['meetings']:
            self.meetings[mtg] = {}
            self.planner[mtg] = {}
            for grp in self.info['groups']:
                self.meetings[mtg][grp] = []
                self.planner[mtg][grp] = {}
        self.csv_fp = None

    def setup(self):
        with open(self.fn, 'r') as fp:
            self.team = json.load(fp)
        for person, mtg_info in self.team.items():
            for mtg in self.info['meetings']:
                for grp in self.info['groups']:
                    if grp == 'all' or mtg in mtg_info[grp]:
                        self.meetings[mtg][grp].append(person)
        for mtg in self.info['meetings']:
            for grp in self.info['groups']:
                for person, mtg_info in self.team.items():
                    person_in_mtggrp = person in self.meetings[mtg][grp]
                    for available in mtg_info['available']:
                        if person_in_mtggrp:
                            self.planner[mtg][grp].setdefault(available, [])
                            self.planner[mtg][grp][available].append(person)

    def reset_file(self, meeting):
        if self.csv_fp is None:
            meeting = meeting.replace('/', '')
            meeting = meeting.replace(' ', '')
            meeting = meeting.replace('(', '')
            meeting = meeting.replace(')', '')
            meeting = meeting.replace('-', '')
            self.mcsv = "{}.csv".format(meeting)
            self.csv_fp = open(self.mcsv, 'w')
            print("group,meeting,available,total,day,hour,not-present", file=self.csv_fp)
        else:
            self.csv_fp.close()
            print("Writing {}".format(self.mcsv))
            self.csv_fp = None

    def view(self, group='meetings', meeting='All-hands meeting',
             header=True, names='not-present', show=0, csv=True):
        if meeting not in self.info['meetings']:
            raise ValueError("{} not valid meeting".format(meeting))
        if group not in self.info['groups']:
            raise ValueError("{} not valid group".format(group))
        ranked = {}
        hdr = "{}-{}:  {}".format(group, meeting, ', '.join(self.meetings[meeting][group]))
        if names:
            hdr += '\n{}<{}>'.format(24*' ', names)
        if header:
            print(hdr)
        for key, val in this.items():
            d, h = key.split()
            th = [int(x) for x in h.split(':')]
            this_key = "{:02d}_{}_{:02d}:{:02d}_{}".format(len(val), DOW[d], th[0], th[1], key)
            ranked[this_key] = val
        this_len = len(all)
        # if csv:
        #     print('{},{},{},{}'.format(group, meeting, names, ','.join(all)), file=self.csv_fp)
        for ordrk in sorted(list(ranked.keys()), reverse=True):
            n, _a, _b, sch = ordrk.split('_')
            if int(n) < show:
                continue
            csv_row = [group, meeting, n, this_len, sch.split()[0], sch.split()[1]]
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
