import json
SDOW = {'Mon': '5', 'Tues': '4', 'Wed': '3', 'Thurs': '2', 'Fri': '1'}


class MeetingPlanner:

    def __init__(self,
                 fnresponses='full_responses.json',  # Info from both polls
                 fninfo="meetings.json"):  # Overall meeting info
        """
        Read info and set up empty dictionaries.
        """
        with open(fninfo, 'r') as fp:
            self.info = json.load(fp)
        with open(fnresponses, 'r') as fp:
            self.team = json.load(fp)
        # Combine occasional = regular + occasional
        for pn, info in self.team.items():
            info['occasional'] += info['regular']

        self.meetings = {}
        self.planner = {}
        self.ranked = {}
        for mtg in self.info['meetings']:
            self.meetings[mtg] = {}
            self.planner[mtg] = {}
            for grp in self.info['groups'].keys():
                self.meetings[mtg][grp] = []
                self.planner[mtg][grp] = {}
        self.csv_fp = None

    def setup(self):
        """
        Populates the following class nested dictionaries:
            self.meetings
            self.planner
            self.ranked
        """
        for person, mtg_info in self.team.items():
            for mtg in self.info['meetings']:
                for grp in self.info['groups'].keys():
                    if grp == 'all' or mtg in mtg_info[grp]:
                        self.meetings[mtg][grp].append(person)
        for mtg in self.info['meetings']:
            for grp in self.info['groups'].keys():
                for person, mtg_info in self.team.items():
                    person_in_mtggrp = person in self.meetings[mtg][grp]
                    for available in mtg_info['available']:
                        if person_in_mtggrp:
                            self.planner[mtg][grp].setdefault(available, [])
                            self.planner[mtg][grp][available].append(person)
        for mtg in self.info['meetings']:
            self.ranked[mtg] = {}
            for grp in self.info['groups'].keys():
                self.ranked[mtg][grp] = {}
                for available, p_list in self.planner[mtg][grp].items():
                    dn, tm = available.split()
                    hr, mn = [99-int(x) for x in tm.split(':')]  # the 99/SDOW are for reverse sort
                    key = "{:03d}-{}-{:02d}-{:02d}".format(len(p_list), SDOW[dn], hr, mn)
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

    def view(self, meeting, group, attendee_display='not-present', csv=True):
        print("-----------------Viewing {} for {}.  Include names '{}'--------------"
              .format(meeting, group, attendee_display))
        if meeting not in self.info['meetings']:
            raise ValueError("{} not valid meeting".format(meeting))
        if group not in self.info['groups'].keys():
            raise ValueError("{} not valid group".format(group))
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
            names = get_name_list(available, full_group, attendee_display)
            print('{}  {:8s}  {}'.format(_t, _x, ', '.join(names)))
            if csv:
                print("{},{},{},{},{},{},{}".format(meeting, group,
                                                    this_time.split()[0], this_time.split()[1],
                                                    len(available), len(full_group),
                                                    ','.join(names)), file=self.csv_fp)


def get_name_list(this_list, full_list, attendee_display, truncate=12):
    names_list = []
    i = 0
    for nm in full_list:
        if i > truncate:
            names_list.append('.....')
            break
        if nm in this_list:
            if attendee_display == 'present':
                names_list.append(nm)
                i += 1
        else:
            if attendee_display == 'not-present':
                names_list.append(nm)
                i += 1
    return names_list
