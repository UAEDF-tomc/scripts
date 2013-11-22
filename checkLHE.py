#!/usr/bin/env python2.6

# checkLHE.py <lhe-file>
# Checks lhe-file for missing event tags and blank lines

import sys

with open(sys.argv[1], 'r') as file:
  eventBlock = False
  events = 0
  lineNumber = 0
  for line in file:
    lineNumber += 1
    if not line.strip(): print "Error: blank line (" + str(lineNumber) + ")"; exit(1)
    if "<event>" in line: 
      if eventBlock: print "Error: missing </event> tag before line " + str(lineNumber); exit(1)
      eventBlock = True
      events += 1
    if "</event>" in line:
      if not eventBlock: print "Error: missing <event> tag before line " + str(lineNumber); exit(1)
      eventBlock = False
    if "</LesHouchesEvents>" in line and eventBlock: print "Error: missing </event> tag before line " + str(lineNumber); exit(1)
  print str(events) + " events in file"
