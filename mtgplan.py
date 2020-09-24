import json
DOW = {'Mon': '5', 'Tues': '4', 'Wed': '3', 'Thurs': '2', 'Fri': '1'}


class MeetingPlanner:

    def __init__(self, fn='hera_mtg_planning.json', info_fn="meeting_info.json"):
        """
        Reads info and sets up empty dictionaries
        """
        self.fn = fn
        with open(info_fn, 'r') as fp:
            self.info = json.load(fp)
        self.meetings = {}
        self.planner = {}
        self.ranked = {}
        for mtg in self.info['meetings']:
            self.meetings[mtg] = {}
            self.planner[mtg] = {}
            for grp in self.info['groups']:
                self.meetings[mtg][grp] = []
                self.planner[mtg][grp] = {}
        self.csv_fp = None

    def setup(self):
        """
        Produces the following class nested dictionaries:
            self.team
            self.meetings
            self.planner
            self.ranked
        """
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
        for mtg in self.info['meetings']:
            self.ranked[mtg] = {}
            for grp in self.info['groups']:
                self.ranked[mtg][grp] = {}
                for available, p_list in self.planner[mtg][grp].items():
                    dn, tm = available.split()
                    hr, mn = [99-int(x) for x in tm.split(':')]  # the 99/DOW are for reverse sort
                    key = "{:03d}-{}-{:02d}-{:02d}".format(len(p_list), DOW[dn], hr, mn)
                    self.ranked[mtg][grp][key] = available

    def handle_file(self, meeting):
        if meeting not in self.info['meetings']:
            raise ValueError("{} not valid meeting".format(meeting))
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

    def view(self, meeting, group, names_shown_as='not-present', csv=True):
        if meeting not in self.info['meetings']:
            raise ValueError("{} not valid meeting".format(meeting))
        if group not in self.info['groups']:
            raise ValueError("{} not valid group".format(meeting))
        if csv and self.csv_fp is None:
            print("No csv file open - not writing")
            csv = False
        ranked_order = sorted(list(self.ranked[meeting][group].keys()), reverse=True)
        full_group = self.meetings[meeting][group]
        for ro in ranked_order:
            this_time = self.ranked[meeting][group][ro]
            available = self.planner[meeting][group][this_time]
            _x = "{:>3s} /{:>3s}".format(str(len(available)), str(len(full_group)))
            _t = "{:5s} {:>5s}".format(this_time.split()[0], this_time.split()[1])
            names = get_name_list(available, full_group, names_shown_as)
            print('{}  {:8s}  {}'.format(_t, _x, ', '.join(names)))
            if csv:
                print("{},{},{},{},{},{},{}".format(meeting, group,
                                                    this_time.split()[0], this_time.split()[1],
                                                    len(available), len(full_group)), file=self.csv_fp)  # noqa


def get_name_list(this_list, full_list, names_shown_as):
    if names_shown_as == 'present':
        return this_list
    names_list = []
    for nm in full_list:
        if nm not in this_list:
            names_list.append(nm)
    return names_list
