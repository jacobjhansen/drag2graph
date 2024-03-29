import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as plticker
import datetime
import csv
import sys
import matplotlib.dates as mdates

class channel(object):
    def __init__(self,identifier): 
        assert type(identifier) is str, "Given channel identifier is not a string: %r" % identifier
        self.identifier = identifier
        self.readingList = list()

    def addReading(self, reading):
        self.readingList.append(reading)

    def returnReadings(self):
        return self.readingList

class reading(object):
    def __init__(self,timestamp,value):
        # TODO Assert timestamp
        # TODO Assert value
        self.timestamp = timestamp
        self.value = value

dataFile = sys.argv[1]

# For TESTING
# dataFile = 'dataq013.csv'

channelList = []

with open(dataFile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    hasDateTime = False
    line_count = 1
    for row in csv_reader:
        if line_count <= 7:
             pass
        if line_count == 8:
            for column in row:
                if column == 'Local Date and Time':
                    hasDateTime = True
                elif column != '':
                    currentChannel = channel(column)
                    channelList.append(currentChannel)
        if line_count > 8:
            break
        line_count += 1
        
    for row in csv_reader:
        if line_count > 8:
            for i in range(1,(len(channelList)+1)):
                rawTime = row[0]
                readingTime = datetime.datetime.strptime(rawTime, "%Y-%m-%d %H:%M:%S")
                readingValue = row[i]
                currentReading = reading(readingTime,readingValue)
                channelList[(i-1)].addReading(currentReading)


#plt.plot(xaxis,yaxis)
#plt.gcf().autofmt_xdate()#plt.show()
#plt.gcf().autofmt_xdate()

fig = plt.figure()
fig.subplots_adjust(hspace=0.9, wspace=0.4)
for i in range(1, 4):
    ax = fig.add_subplot(3, 1, i)

    xaxis = []
    yaxis = []

    for item in channelList[i-1].returnReadings():
        xaxis.append(item.timestamp)
        yaxis.append(item.value)

    ax.set_title(str(channelList[i-1].identifier))
    ax.plot(xaxis,yaxis)
    

plt.show()
