#!/usr/bin/env python
#Tom Cornelis, 17/07/2012
import os
import re
import getpass
from xml.etree import ElementTree as ET
from optparse import OptionParser 
import subprocess

parser = OptionParser()
parser.add_option("-j", "--job", dest="jobs", default = "All", help="filter on job numbers")
parser.add_option("-s", "--secondFile", action="store_true", dest="secondFile", default = False, help="take the second file in crab.cfg")
parser.add_option("-f", "--force", action="store_true", dest="force", default = False, help="force, even if it was already copied earlier")
parser.add_option("-m", "--merge", action="store_true", dest="merge", default = False, help="merge, even if some xml files are missing")
parser.add_option("-t", "--test", action="store_true", dest="test", default = False, help="test")
(options, args) = parser.parse_args()

#Get crabdiri, user remote dir, username, output file name
crabDir = ""
total = 0
if not os.path.exists(".status.txt"): os.system("crab -status > .status.txt");
statusFile = open(".status.txt")
for line in statusFile:
  if 'working directory' in line: crabDir = re.search('crab_0_\d+_\d+', line).group(0)
  if 'Total Jobs' in line:
    for x in line.split():
      if x.isdigit(): total = int(x)

userRemoteDir = ""
outputFile = ""
crabCfgFile = open("crab.cfg")
for line in crabCfgFile:
  if 'user_remote_dir' in line and not 'check_user_remote_dir' in line: userRemoteDir = line.split('=')[-1].replace(' ','').strip()
  if 'output_file' in line: 
    outputFile = line.split('=')[-1].split(',')[0].replace(' ','').strip().replace('.root','')
    if options.secondFile: outputFile = line.split('=')[-1].split(',')[-1].replace(' ','').strip().replace('.root','')

userName = getpass.getuser();

print 'Username:\t\t' + userName
print 'Crab directory:\t\t' + crabDir
print 'User remote directory:\t' + userRemoteDir
print 'Outputfile to copy:\t' + outputFile + '.root'
print

#Make destination directory
tempdir = "/user/" + userName + "/public/temp/"
if not os.path.exists(tempdir + userRemoteDir + '/' + outputFile): os.makedirs(tempdir + userRemoteDir + '/' + outputFile)

#Make joblist
jobs = []
if options.jobs == "All": jobs = range(1, total+1)
else:
  for crabRange in options.jobs.split(','):
    i = int(crabRange.split('-')[0])
    j = int(crabRange.split('-')[-1])
    while i <= j:
      jobs.append(i)
      i+=1

#Start moving the jobs
notFound = total - len(jobs) 
for i in jobs:
  xml_file = "./" + crabDir + "/res/crab_fjr_" + format(i) + ".xml"
  if os.path.exists(xml_file):
    if options.test: continue
    tree = ET.parse(xml_file)
    allFiles = tree.getroot().findall("AnalysisFile")
    if allFiles == []: print "xml file of job " + format(i) + " is corrupted" 
    rootfile = allFiles[0].find("SurlForGrid").get("Value").split("/")[-1]
    if not outputFile in rootfile: rootfile = allFiles[1].find("SurlForGrid").get("Value").split("/")[-1]
    old = "srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/" + userName + "/" + userRemoteDir + "/" + rootfile
    new = "file:///" + tempdir + userRemoteDir + "/" + outputFile + "/" + rootfile
    if options.force or not os.path.exists(tempdir + userRemoteDir + "/" + outputFile + '/' + rootfile):
      print "Copy file " + rootfile
      if subprocess.call(["srmcp", old + " " + new], stdout=open(".srmcp.txt","w"), stderr=subprocess.STDOUT): 
        print "SRMCP ERROR"
        notFound += 1
  else:
    print xml_file + " does not exist"
    notFound += 1

print "MOVING DONE (" + format(notFound) + " files not found)"
print

#Merging of the files
if notFound == 0 or options.merge:
  if not options.test:
    (folders, dataset) = os.path.split(userRemoteDir)
    mergeddir = "/user/" + userName + "/public/merged/"
    print "Start merging... (will be saved in " + mergeddir + folders + ")"
    if not os.path.exists("/user/" + userName + "/public/merged/" + folders): os.makedirs("/user/" + userName + "/public/merged/" + folders)
    os.system("hadd " + mergeddir + folders + "/" + outputFile + "_" + dataset + ".root " + tempdir + userRemoteDir + "/" + outputFile + "/" + outputFile + "*.root")
    os.system("rm .status.txt")
    os.system("rm .srmcp.txt")
