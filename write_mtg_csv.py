#! /usr/bin/env python
import mtgplan
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('meeting', help="Name of meeting unless None", nargs='?', default=None)
ap.add_argument('--include-names', dest='incl_names', help="not-present, present or none",
                default='not-present')
ap.add_argument('--csv', help="Write csv file", action='store_true')
ap.add_argument('--mtype', help="mtypes", default="x,mtg,all")
args = ap.parse_args()

mp = mtgplan.MeetingPlanner()
mp.setup()
print("=====================================================")
print("=====================================================")

show = {'All-hands meeting':
        {'x': [12, True], 'mtg': [12, True], 'all': [23, False]},
        'Other':
        {'x': [0, True], 'mtg': [0, True], 'all': [23, True]}
        }

mtypes = {'x': "VIABLE (subjective; 'x' field in hera_mtg_planning.json)",
          'mtg': "SELF-SELECTED (from googlesheet; 'meetings' in hera_mtg_planning.json)",
          'all': "ALL (all from whenisgood)"}
args.mtype = args.mtype.split(',')

if args.meeting is None:
    meeting_set = mp.meetings
else:
    meeting_set = args.meeting.split(',')

for meeting in meeting_set:
    print(meeting)
    if args.csv:
        mp.reset_file(meeting)

    for mtype in args.mtype:
        print(mtypes[mtype])
        show_down_to = show[meeting][mtype][0]\
            if meeting in show.keys() else show['Other'][mtype][0]
        show_header = show[meeting][mtype][1]\
            if meeting in show.keys() else show['Other'][mtype][1]
        x = mp.view(mtype, meeting, header=show_header, names=args.incl_names, show=show_down_to)
        print("-------------------------------------------")

    if args.csv:
        mp.reset_file(meeting)
