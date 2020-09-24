#! /usr/bin/env python
import mtgplan
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('meeting', help="Name of meeting unless None which does all",
                nargs='?', default=None)
ap.add_argument('--include-names', dest='incl_names', help="not-present or present",
                default='not-present')
ap.add_argument('--csv', help="Write csv file", action='store_true')
ap.add_argument('--groups', help="groups to use", default="x,meetings,all")
args = ap.parse_args()

mp = mtgplan.MeetingPlanner()
mp.setup()

group_desc = {'x': "VIABLE (subjective; 'x' field in hera_mtg_planning.json)",
              'meetings': "SELF-SELECTED (from googlesheet; 'meetings' in hera_mtg_planning.json)",
              'all': "ALL (all from whenisgood)"}
args.groups = args.groups.split(',')

if args.meeting is None:
    meeting_set = mp.info['meetings']
else:
    meeting_set = args.meeting.split(',')

for meeting in meeting_set:
    print(meeting)
    if args.csv:
        mp.handle_file(meeting)

    for group in args.groups:
        print(group_desc[group])
        x = mp.view(meeting, group, names_shown_as=args.incl_names, csv=args.csv)
        print("-------------------------------------------")

    if args.csv:
        mp.handle_file(meeting)
