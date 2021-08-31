import json
import matplotlib.image as mpimg
import pandas as pd
from math import sqrt


testing = "DeBoer"  # set to name to see result of that name
clr_threshold = 0.05  # how close to the available color to be
border_size = 0.4  # fractional size of border


with open('meetings.json', 'r') as fp:
    meeting_info = json.load(fp)
meetings = list(meeting_info['meetings'].keys())

with open('polls/whenisgood.json', 'r') as fp:
    wig = json.load(fp)

# This is the self-select meeting attendence form
selfpoll_file = pd.read_csv('polls/MeetingChangeQuery.csv')
selfpoll = {}
for i, name in enumerate(selfpoll_file['Name']):
    last_name = name.split()[-1]
    selfpoll[last_name] = selfpoll_file.iloc[i]


def clrdist(c, ref):
    d = 0.0
    for i in range(3):
        d += (c[i] - ref[i])**2
    return (sqrt(d))


def mkpixpts(keys, start, step, gap):
    wp = {}
    for i, k in enumerate(keys):
        wp[k] = start + i * (step + gap)
    return wp


# Check people in both polls and seed responses with full list
responses = {}
for pn in wig['img'].keys():
    responses[pn] = {}
    if pn not in selfpoll.keys():
        print("{} not in google poll".format(pn))
for pn in selfpoll.keys():
    responses[pn] = {}
    if pn not in wig['img'].keys():
        print("{} not in whenisgood".format(pn))

# Read in google form data
for pn in selfpoll.keys():
    for grp in meeting_info['groups'].keys():
        responses[pn][grp] = []
    for self_mtg in selfpoll[pn].keys():
        for _mtg in meetings:
            if _mtg.lower() in self_mtg.lower():
                if isinstance(selfpoll[pn][self_mtg], str):
                    if 'regular' in selfpoll[pn][self_mtg]:
                        responses[pn]['regular'].append(_mtg)
                    elif 'occasional' in selfpoll[pn][self_mtg]:
                        responses[pn]['occasional'].append(_mtg)

# # Step through grid in images
for pn in responses.keys():  # pn is person name
    if testing and pn != testing:
        continue
    if pn not in wig['img'].keys():
        continue
    if isinstance(wig['img'][pn], dict):  # Assumes all values defined.
        data = wig['img'][pn]
        fn = 'polls/' + wig['img'][pn]['file']
    else:
        data = wig
        fn = 'polls/' + wig['img'][pn]
    days = mkpixpts(data['days'], data['early_day'], data['day_size'], data['gap'])
    times = mkpixpts(data['times'], data['early_time'], data['time_size'], data['gap'])
    border_day = int(border_size * data['day_size'] / 2.0)
    border_time = int(border_size * data['time_size'] / 2.0)
    responses[pn]['available'] = []

    img = mpimg.imread(fn)
    if testing:
        import numpy as np
        test_img = np.zeros(np.shape(img)[0:2])
        print(f"\nUsing {pn}")
        print("          ", end=' ')
        for dy in data['days']:
            print(f"{dy:10s}".format(dy), end=' ')
        print("\n           -----      -----      -----      -----      -----")

    for this_time in data['times']:
        tpix = times[this_time]
        if testing:
            print(f"{this_time:10s}", end=' ')
        for this_day in data['days']:
            dpix = days[this_day]
            for _y in range(border_time, data['time_size']-border_time):
                for _x in range(border_day, data['day_size']-border_day):
                    dval = dpix + _x
                    tval = tpix + _y
                    clr = img[tval, dval]
                    is_available = clrdist(clr, data['color']) < clr_threshold
                    if is_available:
                        break
            if testing:
                for _y in range(border_time, data['time_size']-border_time):
                    for _x in range(border_day, data['day_size']-border_day):
                        dval = dpix + _x
                        tval = tpix + _y
                        test_img[tval, dval] = int(is_available)
                print("{:10s}".format(str(is_available)), end=' ')
                # print("{:.6f} {}  {}".format(td, dcmin, this_clr), end='')
            if is_available:
                responses[pn]['available'].append("{} {}".format(this_day, this_time))
        if testing:
            print()

    if testing:
        import subprocess
        subprocess.call(f'open "{fn}"', shell=True)
    else:
        with open('full_responses.json', 'w') as fp:
            json.dump(responses, fp, indent=4)
