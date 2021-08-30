import json
# import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from math import sqrt


with open('meetings.json', 'r') as fp:
    meeting_info = json.load(fp)

meetings = list(meeting_info['meetings'].keys())

with open('polls/whenisgood.json', 'r') as fp:
    whenisgood = json.load(fp)

# This is the self-select meeting attendence form
selfpoll_file = pd.read_csv('polls/MeetingChangeQuery.csv')
selfpoll = {}
for i, name in enumerate(selfpoll_file['Name']):
    last_name = name.split()[-1]
    selfpoll[last_name] = selfpoll_file.iloc[i]

# This is the value of the color that indicates availability
available_color = [0.4745098, 0.9529412, 0.2901961]
day_size = 142  # size of box in x-dim
border_day = int(0.1 * day_size / 2.0)
time_size = 32  # size of box in y-dim
border_time = int(0.15 * time_size / 2.0)
gap = 5
days = {
         '1Mon': 1459,
         '2Tues': -1, '3Wed': -1, '4Thurs': -1, '5Fri': -1
}
hours = {
          '07:00': 600,
          '07:30': -1, '08:00': -1, '08:30': -1, '09:00': -1, '09:30': -1, '10:00': -1,
          '10:30': -1, '11:00': -1, '11:30': -1, '12:00': -1, '12:30': -1, '13:00': -1,
          '13:30': -1, '14:00': -1, '14:30': -1, '15:00': -1, '15:30': -1, '16:00': -1,
          '16:30': -1, '17:00': -1, '17:30': -1, '18:00': -1, '18:30': -1
}
for i, dy in enumerate(sorted(days.keys())):
    days[dy] = days['1Mon'] + i * (day_size + gap)
for i, hr in enumerate(sorted(hours.keys())):
    hours[hr] = hours['07:00'] + i * (time_size + gap)
_days = sorted(list(days.keys()))
_hours = sorted(list(hours.keys()))


def clrdist(c, ref):
    d = 0.0
    for i in range(3):
        d += (c[i] - ref[i])**2
    return (sqrt(d))


# Check people in both polls
for pn in whenisgood.values():
    if pn not in selfpoll.keys():
        print("{} not in google poll".format(pn))
for pn in selfpoll.keys():
    if pn not in whenisgood.values():
        print("{} not in whenisgood".format(pn))

# # Step through grid in images
testing = False
full_responses = {}
for fn, pn in whenisgood.items():
    if testing and pn != testing:
        continue
    full_responses[pn] = {}
    for grp in meeting_info['groups'].keys():
        full_responses[pn][grp] = []

    if pn in selfpoll.keys():
        for self_mtg in selfpoll[pn].keys():
            for _mtg in meetings:
                if _mtg in self_mtg:
                    if isinstance(selfpoll[pn][self_mtg], str):
                        if 'regular' in selfpoll[pn][self_mtg]:
                            full_responses[pn]['regular'].append(_mtg)
                        elif 'occasional' in selfpoll[pn][self_mtg]:
                            full_responses[pn]['occasional'].append(_mtg)

    img = mpimg.imread('polls/' + fn)
    if testing:
        import numpy as np
        test_img = np.zeros(np.shape(img)[0:2])
    for hr in _hours:
        for dy in _days:
            h = hours[hr]
            d = days[dy]
            dcmin = 100.0
            for _y in range(border_time, time_size-border_time):
                for _x in range(border_day, day_size-border_day):
                    dval = d + _x
                    hval = h + _y
                    clr = img[hval, dval]
                    dc = clrdist(clr, available_color)
                    # test_img[hval, dval] = int(dc < 0.01)
                    if dc < dcmin:
                        this_clr = clr
                        dcmin = dc
            td = clrdist(this_clr, available_color)
            if testing:
                for _y in range(time_size):
                    for _x in range(day_size):
                        dval = d + _x
                        hval = h + _y
                        test_img[hval, dval] = int(td < 0.01)
                print("{:10s}".format(str(td < 0.01)), end=' ')
                print("{:.6f} {}  {}".format(td, dcmin, this_clr), end='')
            if td < 0.01:
                full_responses[pn]['available'].append("{} {}".format(dy[1:], hr))
        if testing:
            print()

    with open('full_responses.json', 'w') as fp:
        json.dump(full_responses, fp, indent=4)
