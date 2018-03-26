import re
import sys

class AcLogAnalyzer:

    def __init__(self):
        self.lastLines = []
        self.races = []
        self.currentRace = None

        self.reRaceStart = re.compile('^(RACE), WaitTime')
        self.reSessionName = re.compile('^SENDING (session name) : (.*)$')
        self.reSessionTime = re.compile('^SENDING (session time) : ([0-9]+)')
        self.reSessionLaps = re.compile('^SENDING (session laps) : ([0-9]+)')
        self.reSendingCar = re.compile('^(SENDING CAR): ([0-9]+)')
        self.reSessionWeather = re.compile('^Sending (weather)\s+([0-9.]+)\s+([0-9.]+)')
        self.reSessionWind = re.compile('^Sending (wind)\s+([0-9.]+)\s+([0-9.]+)')
        self.reSendingRemoteTime = re.compile('^SENDING (remote time) : ')
        self.reLapCompletedStart = re.compile('^Car\.(onLapCompleted)$')
        self.reLapCompletedLap = re.compile('^(LAP) (.+)([0-9]+:[0-9]+:[0-9]+)$')
        self.reLapCompletedCuts = re.compile('^Result\.OnLapCompleted\. (Cuts): ([0-9]+)')
        self.reLapCompletedEnd = re.compile('^Car\.(onLapCompleted END)')
        self.reLapCompletedCar = re.compile('^([0-9]+)\)\s+(.+)\s+(BEST): ([0-9]+:[0-9]+:[0-9]+) (TOTAL): ([0-9]+:[0-9]+:[0-9]+) Laps:([0-9]+) SesID:([0-9]+) HasFinished:([a-z]+)$')
        self.reRaceOverPacket = re.compile('^(RACE OVER PACKET)')

    def feedline(self, line):
        self.lastLines.append(line)

        if self.reRaceStart.match(line):
            self.currentRace = {}
        else if self.reRaceOverPacket.match(line):
            self.races.append(self.currentRace)
            self.currentRace = None
            
        m = None
        #m = m or self.reRaceStart.match(line)
        m = m or self.reSessionName.match(line)
        #m = m or self.reSessionTime.match(line)
        #m = m or self.reSessionLaps.match(line)
        m = m or self.reSendingCar.match(line)
        m = m or self.reSessionWeather.match(line)
        m = m or self.reSessionWind.match(line)
        m = m or self.reSendingRemoteTime.match(line)
        #m = m or self.reLapCompletedStart.match(line)
        #m = m or self.reLapCompletedLap.match(line)
        #m = m or self.reLapCompletedCuts.match(line)
        #m = m or self.reLapCompletedEnd.match(line)
        #m = m or self.reLapCompletedCar.match(line)
        m = m or self.reRaceOverPacket.match(line)

        if m:
            print (m.groups())
            self.lastLines = []
        
def extractRacesFromLog(path):
    with open(path, 'r') as f:
        analyzer = AcLogAnalyzer()

        for line in f:
            analyzer.feedline(line)


extractRacesFromLog(sys.argv[1])