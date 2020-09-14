import json
# import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd


responses_file = pd.read_csv('MeetingResponses.csv')
responses = {}
for i, name in enumerate(responses_file['Name']):
    responses[name] = responses_file.iloc[i]
meetings = ['All-hands meeting', 'Analog', 'Pspec', 'pyuvsim/pyradiosky alternating',
            'Commissioning', 'Correlator', 'Site', 'pyuvdata', 'NRAO',
            'Analysis/Quality Metrics alternating', 'Imaging (biweekly)', 'Validation',
            'Machine learning', 'Theory Meets Data']

available_color = 1.737255
days = {
         1618: 'Mon',
         1768: 'Tues',
         1918: 'Wed',
         2066: 'Thurs',
         2216: 'Fri'
}
hours = {
          552: '7:00',
          590: '7:30',
          628: '8:00',
          666: '8:30',
          704: '9:00',
          742: '9:30',
          780: '10:00',
          818: '10:30',
          856: '11:00',
          894: '11:30',
          932: '12:00',
          970: '12:30',
          1008: '13:00',
          1046: '13:30',
          1084: '14:00',
          1122: '14:30',
          1160: '15:00',
          1198: '15:30',
          1236: '16:00',
          1274: '16:30',
          1312: '17:00',
          1350: '17:30',
          1388: '18:00',
          1426: '18:30'
}
_days = sorted(list(days.keys()))
_hours = sorted(list(hours.keys()))

# Make screen shot file to person dictionary
ssfiles = []
with open('ssfiles.txt', 'r') as fp:
    for line in fp:
        ssfiles.append(line.strip())
ssfiles = sorted(ssfiles)
people = []
with open('people.txt', 'r') as fp:
    for line in fp:
        people.append(line.strip())
files = {}
for fn, pn in zip(ssfiles, people):
    files[fn] = pn

# Check people
for pn in people:
    if pn not in responses.keys():
        print("{} not in responses".format(pn))
for pn in responses.keys():
    if pn not in people:
        print("{} not in responses".format(pn))

# Step through grid in images
testing = False
if testing:
    img = mpimg.imread(ssfiles[0])
    for h in _hours:
        for d in _days:
            clr = img[h, d]
            clr = clr[0] + clr[1] + clr[2]
            print(abs(clr - available_color) < 0.01, end=' ')
            # print("{:.6f}   ".format(clr), end='')
        print('\n')
else:
    mtg_data = {}
    full_responses = {}
    for fn, pn in files.items():
        mtg_list = []
        for mtg in meetings:
            if pn in responses.keys():
                if responses[pn][mtg] == 'Yes':
                    mtg_list.append(mtg)
        full_responses[pn] = {'meetings': mtg_list, 'available': []}
        img = mpimg.imread(fn)
        for d in _days:
            for h in _hours:
                clr = img[h, d]
                clr = clr[0] + clr[1] + clr[2]
                if abs(clr - available_color) < 0.01:
                    full_responses[pn]['available'].append("{} {}".format(days[d], hours[h]))

    with open('full_responses.json', 'w') as fp:
        json.dump(full_responses, fp, indent=4)
