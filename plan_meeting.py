#! /usr/bin/env python
import mtgplan
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('meeting', nargs='?', help="Name of meeting.")
ap.add_argument('-g', '--groups', help="groups to use", default="regular,occasional")
ap.add_argument('--csv', help="Flag to write csv file(s) for selected meetings.",
                action='store_true')
ap.add_argument('--attendee-display', dest='attendee_display', help="attendee status to display",
                choices=['present', 'not-present'], default='not-present')
ap.add_argument('--show-meetings', dest='show_meetings', help="Just show meeting list and exit.",
                action='store_true')
ap.add_argument('--show-groups', dest='show_groups', help="Just show groups lists for "
                "selected meetings and exit.", action='store_true')
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
            x = mp.view(mtg, group, attendee_display=args.attendee_display, csv=args.csv)
            print("-------------------------------------------")

        if args.csv:
            mp.handle_file(mtg)
