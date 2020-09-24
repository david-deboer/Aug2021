#! /usr/bin/env python
import mtgplan
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('meeting', help="Name of meeting unless None which does all",
                nargs='?', default=None)
ap.add_argument('--include-names', dest='incl_names', help="not-present or present",
                default='not-present')
ap.add_argument('--csv', help="Write csv file", action='store_true')
ap.add_argument('--groups', help="groups to use", default="convener,self,all")
ap.add_argument('--show-meetings', dest='show_meetings', help="Just show meeting list.",
                action='store_true')
ap.add_argument('--show-groups', dest='show_groups', help="Just show groups.",
                action='store_true')
args = ap.parse_args()

mp = mtgplan.MeetingPlanner()

if args.meeting is None:
    meeting_set = mp.info['meetings']
else:
    meeting_set = args.meeting.split(',')
args.groups = args.groups.split(',')
mp.setup()

if args.show_meetings:
    for mtg in meeting_set:
        print(mtg)
elif args.show_groups:
    for mtg in meeting_set:
        print("Groups for {}".format(mtg))
        for grp in args.groups:
            print("\t{}:  {}".format(grp, ', '.join(mp.meetings[mtg][grp])))
else:
    for mtg in meeting_set:
        print(mtg)
        if args.csv:
            mp.handle_file(mtg)

        for group in args.groups:
            print(mp.info['groups'][group])
            x = mp.view(mtg, group, names_shown_as=args.incl_names, csv=args.csv)
            print("-------------------------------------------")

        if args.csv:
            mp.handle_file(mtg)
