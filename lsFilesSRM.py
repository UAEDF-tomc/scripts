#!/usr/bin/env python
#Tom Cornelis, 16/01/2012
import os
import re
import sys
from optparse import OptionParser

def ls(directory, search = ".*", user = "tomc", doPrint = True):
  userdir = "srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/" + user + "/"
  if directory == "": 
    try: directory = open(".lastls.txt").readline()
    except:
      print "Give a directory"
      return
  f = open(".lastls.txt","w")
  f.write(directory)

  offset = 0 
  condition = True
  files = []
  while condition:
    os.system("srmls -offset=" + format(offset) + " -count=1000 " + userdir + directory + " >& .ls.txt")
    offset += 1000
    lsfile = open(".ls.txt")
    countFiles = 0
    for line in lsfile:
      if 'root' in line: 
        countFiles += 1
        file = re.split(directory + "/", line)[-1]
        match = re.search(search, file)
        if match: files.append(match.group())
    if countFiles < 1000: condition = False
    lsfile.close()

  def sortWithNumbers(str):
    pieces = re.split(r'(\d+)', str)
    pieces[1::2] = map(int, pieces[1::2])
    return pieces 

  if doPrint: 
    for file in sorted(files, key=sortWithNumbers): print file
  return sorted(files, key=sortWithNumbers) 


if __name__ == "__main__": 
  parser = OptionParser()
  parser.add_option("-d", "--directory", dest="directory", default="", help="directory")
  parser.add_option("-s", "--search", dest="search", default="Tuple.*root", help="search")
  parser.add_option("-u", "--user", dest="user", default="tomc")
  parser.add_option("-n", action="store_false", dest="SRMCheck", default=True)
  (options, args) = parser.parse_args()

  ls(options.directory, options.search)
