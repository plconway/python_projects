import pandas as p
import plotly.express as px
import plotly.graph_objects as go
import pprint

figure = px.line(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16],
                 labels={'x': 'X Axis',
                         'y': 'Y Axis'},
                 title='My First Chart')
# figure.show()

# line.startswith('From ') is a better solution
#

data = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
for line in open('mbox.txt'):
    line = line.rstrip()
    if 'X-DSPAM-Processed: Mon' in line:
        data['Monday'] = data['Monday'] + 1
    elif 'X-DSPAM-Processed: Tue' in line:
        data['Tuesday'] = data['Tuesday'] + 1
    elif 'X-DSPAM-Processed: Wed' in line:
        data['Wednesday'] = data['Wednesday'] + 1
    elif 'X-DSPAM-Processed: Thu' in line:
        data['Thursday'] = data['Thursday'] + 1
    elif 'X-DSPAM-Processed: Fri' in line:
        data['Friday'] = data['Friday'] + 1
    elif 'X-DSPAM-Processed: Sat' in line:
        data['Saturday'] = data['Saturday'] + 1
    elif 'X-DSPAM-Processed: Sun' in line:
        data['Sunday'] = data['Sunday'] + 1

barchart = px.bar(x=data.keys(),
                  y=data.values(),
                  labels={'x': 'Day of the Week', 'y': 'Emails Sent'},
                  title='Emails Sent by Day of the Week')
barchart.show()

print(data.values())
