#!/usr/bin/env python2.6

# mvstar 'something_*_*.txt' 'something_different_*_*.txt'
# Allows to use wildcards in the mv command

import fnmatch
import os
import sys 

source = sys.argv[1]
destination = sys.argv[2]

path_parts = source.split('/')
depth = source.count('/')
copyArguments = []

def getWildcards(wildcards, match, path):
  x = path.split('*', 1)
  nextPart = x[1].split('*')[0]
  if '' is not nextPart: wildcard = match[len(x[0]):].split(nextPart)[0]
  else: wildcard = match[len(x[0]):]
  wildcards.append(wildcard)
  if '*' in x[1]: getWildcards(wildcards, match[len(x[0])+len(wildcard):], x[1])

def fillWildcards(wildcards, path):
  newPath = path
  i = 0
  while '*' in newPath:
    newPath = newPath.replace('*', wildcards[i], 1)
    i = i+1
  return newPath

def lookIntoDir(path, i):
  for x in os.listdir(path):
    if fnmatch.fnmatch(x, path_parts[i]):
      if os.path.isdir(path+'/'+x) and i < depth: lookIntoDir(path+'/'+x, i+1)
      else: 
        wildcards = []
        getWildcards(wildcards, path+'/'+x, './'+source)
        newDest = fillWildcards(wildcards, destination)
        copyArguments.append('mv ' + path + '/' + x + ' ' + newDest)
        
def confirm(prompt, resp=False):
  prompt = '%s %s|%s: ' % (prompt, 'y', 'n')
  while True:
    ans = raw_input(prompt)
    if not ans: return resp
    if ans not in ['y', 'Y', 'n', 'N']:
      print 'please enter y or n.'
      continue
    if ans == 'y' or ans == 'Y': return True
    if ans == 'n' or ans == 'N': return False

lookIntoDir('.', 0)
for x in copyArguments: print x
if(confirm('Move these files?')):
  for x in copyArguments: os.system(x) 
