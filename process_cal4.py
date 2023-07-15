"""Assignment 4 process_cal4.py Andrei Mazilescu V00796396 (code from my A2 is used)"""
import datetime
import re

class Event:
    """Event class used to create Event objects for use in process_cal"""

    def __init__(self, start, end, loc, summ, until, rrule):
        """Event constructor: Takes in values for an event and constructs an event."""
        
        self.start = start
        self.end = end
        self.loc = loc
        self.summ = summ
        self.until = until
        self.rrule = rrule
        
class process_cal:
    """process_cal: Reads input from a file line by line and creates events, returns a string formatted as per assignment requirements"""

    def __init__(self, file):
        """process_cal constructor: takes in a filename, reads file, makes events from file, checks for repeaing events
        then sorts those events and puts them in a list"""

        lines = self.readfile(file)
        self.events = self.makeEvent(lines)
        self.rrule()
        self.eventslist = sorted(self.events, key=lambda i: i.start)


    def readfile(self, file):
        """opens and reads file, returns list of lines (Copied from A2)"""

        read = open(file)
        lines = read.readlines()

        return lines

    def makeEvent(self, lines):
        """goes through list of lines, checks for variables used for an event,
        creates an Event and then stores the event in a list, returns list of events
        (Adapted from A2)"""

        eventlist = []
        rrulefound = False

        for line in lines:
            
            if line.startswith("DTSTART:"):
                start = re.search(r"DTSTART:((.+T.+))", line)
                dtstart = datetime.datetime.strptime(start.group(1), '%Y%m%dT%H%M%S')

            if line.startswith("DTEND:"):
                end = re.search(r"DTEND:((.+T.+))", line)
                dtend = datetime.datetime.strptime(end.group(1), '%Y%m%dT%H%M%S')

            if line.startswith("LOCATION:"):
                loc = re.search(r"LOCATION:((.+))", line)
                if loc:
                    loc = loc.group(1)
                #if no string is found for location makes location empty
                else:
                    loc = ""

            if line.startswith("SUMMARY:"):
                summ = re.search(r"SUMMARY:((.+))", line)
                summ = summ.group(1)

            if line.startswith("RRULE:"):
                until = re.search(r"UNTIL=((.+T.+));", line)
                until = datetime.datetime.strptime(until.group(1), '%Y%m%dT%H%M%S')
                rrule = True
                rrulefound = True
                

            if line.startswith("END:VEVEN"):            
               
                if rrulefound == False:
                    rrule = False
                    until = ""

                eventlist.append(Event(dtstart, dtend, loc, summ, until, rrule))
                rrulefound = False
            
        return eventlist

    def rrule(self):
        """Goes through event list, for each event that is repeating, calls rruleincrement to add
        new events to list (Adapted from A2)"""
        
        count = len(self.events)

        for i in range(count):

            if self.events[i].rrule:
                self.rruleincrement(self.events[i])

        

    def rruleincrement(self, rrevent):
        """Creates and appends events to list, adds a week to each new event, stops when
        UNTIL date is reached (Adapted from A2)"""
        
        start = rrevent.start
        end = rrevent.end

        while start + datetime.timedelta(days=7) < rrevent.until:
            
            start += datetime.timedelta(days=7)
            end += datetime.timedelta(days=7)
            self.events.append(Event(start, end, rrevent.loc, rrevent.summ, rrevent.until, False))


    def get_events_for_day(self, day):
        """Takes a datetime object and checks to see if any events for that date exist, returns
        a formated string if found and returns None otherwise. If event is found Date of event 
        is added to the string and then the corresponding times, summaries and locations of events
        occuring on the same date (Formats copied from A2)"""

        found = False
        eventstring = ""

        for event in self.eventslist:

            if event.start.date() == day.date():

                eventstring = ""
                found = True
                date = event.start.strftime("%B %d, %Y (%a)")
                eventstring += (date + "\n")

                for i in range(len(date)):

                    eventstring += ("-")

                break

            else:
                eventstring = None

        if found == True:

            for event in self.eventslist:

                if event.start.date() == day.date():

                    starttime = event.start.strftime("%I:%M %p")
                    endtime = event.end.strftime("%I:%M %p")

                    if starttime[0] == "0":

                        starttime = starttime.replace('0', ' ', 1)

                    if endtime[0] == "0":

                        endtime = endtime.replace('0', ' ', 1)

                    eventstring += ("\n" + starttime + " to " + endtime + ": " + event.summ + " {{" + event.loc + "}}")

        return eventstring