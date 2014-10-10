#!/usr/bin/env python2.6

# crabStatus.py <options>
# Wrapper around crab -status which allows to use filters on output and easy resubmissions

import os
from optparse import OptionParser

#Option parser
parser = OptionParser()
parser.add_option("-n", "--noStatusCheck", action="store_false", dest="checkCrab", default = True, help="Crab status is not re-checked")
parser.add_option("-j", "--job", dest="jobs", default = "All", help="filter on job numbers")
parser.add_option("-s", "--search", dest="search", default="N", help="filter on status, action, exitcode or E_HOST")
parser.add_option("-b", "--blacklist", dest="blacklist", default="", help="blacklist E_HOST")
parser.add_option("-i", "--noinfo", action="store_false", dest="printInfo", default = True, help="Don't show exit codes and job summary")
parser.add_option("-k", "--kill", action="store_true", dest="kill", default = False, help="Kill the (selected) jobs")
parser.add_option("-r", "--resubmit", action="store_true", dest="resubmit", default = False, help="Resubmit the (selected) jobs")
parser.add_option("-f", "--forceResubmit", action="store_true", dest="forceResubmit", default = False, help="Force resubmit the (selected) jobs")
(options, args) = parser.parse_args()

if 'All' not in options.jobs: options.search = "All"

#function for changing python list to crab list
def jobsToCrabList(jobs):
  crabList = ""
  for i in jobs:
    if crabList == "": crabList = format(i) 
    else:
      pythonRange = crabList.split(',')[-1]
      last = pythonRange.split('-')[-1]
      if i == int(last) + 1: 
        if pythonRange.split('-')[0] == last: crabList += '-' + format(i)
        else: crabList = crabList.replace(last, format(i))
      else: crabList += "," + format(i)
  return crabList

#function for changing crab list to python list
def jobsToPythonList(jobs, total):
  if 'All' in jobs or 'all' in jobs: return range(1, total+1) 
  pythonList = []
  for crabRange in jobs.split(','):
    i = int(crabRange.split('-')[0])
    j = int(crabRange.split('-')[-1])
    while i <= j:
      pythonList.append(i)
      i+=1
  return pythonList

#Check crab status
if options.checkCrab: 
  print "Getting the crab status..."
  os.system("crab -status > .status.txt")

#Get total jobs
total = 0
statusFile = open(".status.txt")
for str in statusFile:
  if 'Total Jobs' in str: 
    for x in str.split(): 
      if x.isdigit(): total = int(x)

#Make search filters
noFilters = False
jobFilters = []
for search in options.search.split(','):
  if search == "All": noFilters = True
  else:
    print 'Searching for ' + search.replace('+'," AND ")
    filterWords = []
    for word in search.split('+'):
      filterWords.append(word)
    jobFilters.append(filterWords) 

myjobs = jobsToPythonList(options.jobs, total)
print 'Selecting jobs: ' + options.jobs


#Filter results
filteredJobs = []
abortedJobs = []
killFailedJobs = []
siteErrorJobs = []
cannotSubmitJobs = []
cannotSubmitJobs = []
cancelledJobs = []
infoPart = False
statusFile = open(".status.txt")
for line in statusFile:
  jobInfo = line.split()
  try:
    jobID = int(jobInfo[0])
    if jobID in myjobs:
      printLine = False
      for search in jobFilters:
        searchFound = True
        for word in search:
          if word not in jobInfo: searchFound = False
        if searchFound: printLine = True
      if printLine or noFilters:
        print line,
        filteredJobs.append(jobID)
    if 'Aborted' in jobInfo: abortedJobs.append(jobID)
    if '60317' in jobInfo: siteErrorJobs.append(jobID)
    if '60307' in jobInfo: siteErrorJobs.append(jobID)
    if '10030' in jobInfo: siteErrorJobs.append(jobID)
    if '10040' in jobInfo: siteErrorJobs.append(jobID)
    if '50115' in jobInfo: siteErrorJobs.append(jobID)
    if 'KillFailed' in jobInfo: killFailedJobs.append(jobID)
    if 'CannotSubmit' in jobInfo: cannotSubmitJobs.append(jobID)
    if 'Cancelled' in jobInfo: cancelledJobs.append(jobID)
  except:
    if "working directory" in line: 
      print "Crab working directory: " + jobInfo[2]
      print
      print "ID    END STATUS            ACTION       ExeExitCode JobExitCode E_HOST"
      print "----- --- ----------------- ------------  ---------- ----------- ---------"
    if "ExitCodes" in line or "Total Jobs" in line: 
      if options.printInfo and not infoPart: 
        infoPart = True 
        print
  if infoPart: print line,

jobList = jobsToCrabList(filteredJobs)
abortedList = jobsToCrabList(abortedJobs)
siteErrorList = jobsToCrabList(siteErrorJobs)
killFailedList = jobsToCrabList(killFailedJobs)
cannotSubmitList = jobsToCrabList(cannotSubmitJobs)
cancelledList = jobsToCrabList(cancelledJobs)

resubmitList = abortedList + "," + cancelledList
forceResubmitList = killFailedList + "," + cannotSubmitList + "," + siteErrorList

print "Jobs listed above: " + jobList
if options.kill and jobList != "": os.system("crab -kill " + jobList)
if options.resubmit and jobList != "": resubmitList = resubmitList + "," + jobList 
if options.forceResubmit and jobList != "": forceResubmitList = forceResubmitList + "," + jobList

if resubmitList[0] == ",": resubmitList = resubmitList[1:]
if resubmitList != "" and resubmitList[-1] == ",": resubmitList = resubmitList[:-1]
if forceResubmitList[0] == ",": forceResubmitList = forceResubmitList[1:]
if forceResubmitList != "" and forceResubmitList[-1] == ",": forceResubmitList = forceResubmitList[:-1]


if resubmitList != "":
  print "Resubmit of jobs: " + resubmitList
  if options.blacklist != "": os.system("crab -resubmit " + resubmitList + " -GRID.blacklist=" + options.blacklist)
  else: os.system("crab -resubmit " + resubmitList)


if forceResubmitList != "":
  print "ForceResubmit of jobs: " + forceResubmitList
  if options.blacklist != "": os.system("crab -forceResubmit " + forceResubmitList + " -GRID.blacklist=" + options.blacklist)
  else: os.system("crab -forceResubmit " + forceResubmitList)
