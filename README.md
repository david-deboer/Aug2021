## This assists in finding times for meetings.

The data are in the file "full_responses.json".  It is taken from the following:
 - whenisgood poll in the "available" key
 - google form for the "regular" and "occasional" keys (groups)
 
 If you wish to look at a particular set of people for a meeting, edit the full_responses.json file "convener" key and add your meeting name.
 
 There is a script call "plan_meeting.py" that will show the results for a given meeting/group

usage: plan_meeting.py [-h] [-g GROUPS] [--csv] [--attendee-display {present,not-present}] [--show-meetings] [--show-groups] [meeting]

positional arguments:
  meeting               Name of meeting.

optional arguments:
  -h, --help            show this help message and exit
  -g GROUPS, --groups GROUPS
                        groups to use
  --csv                 Flag to write csv file(s) for selected meetings.
  --attendee-display {present,not-present}
                        attendee status to display
  --show-meetings       Just show meeting list and exit.
  --show-groups         Just show groups lists for selected meetings and exit.

Note that the following folks didn't complete both, so some data are missing.
    Parsons not in google poll
    Morales not in google poll
    Dai not in google poll
    Nhan not in whenisgood
    Robnett not in whenisgood
    Storer not in whenisgood
    Kim not in whenisgood
    Kocz not in whenisgood
    Garsden not in whenisgood


