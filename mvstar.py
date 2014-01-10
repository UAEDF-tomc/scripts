#!/usr/bin/env python2.6

# cpstar 'something_*_*.txt' 'something_different_*_*.txt'
# Allows to use wildcards in the cp command

import fnmatch
import os
import sys 
import getpass

def makePathAbsolute(path):
  if path[0] == '~': 
    if path[1] == '/': path = path.replace('~', '/user/' + getpass.getuser(),1)
    else: path = path.replace('~', '/user/',1)
  if path[0] != '/': path = os.getcwd() + '/' + path
  return path

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
    if i < len(wildcards): newPath = newPath.replace('*', wildcards[i], 1)
    else: 
      print 'To many wildcards in destination'
      exit(1)
    i = i+1
  return newPath

def lookIntoDir(head, tail, destination, copyArguments):
  middle = tail.split('/')[0] 
  for item in os.listdir(head):
    if fnmatch.fnmatch(item, middle):
      path = os.path.join(head, item)
      leftOver = tail[len(middle)+1:]
      if os.path.isdir(path) and leftOver: lookIntoDir(path, leftOver, destination, copyArguments)
      else: 
        if not leftOver:
          wildcards = []
          getWildcards(wildcards, path, source)
          newDest = fillWildcards(wildcards, destination)
          if os.path.isdir(path): copyArguments.append('mv -r ' + path + ' ' + newDest)
          else: copyArguments.append('mv ' + path + ' ' + newDest)
        
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

source = makePathAbsolute(sys.argv[1])
destination = makePathAbsolute(sys.argv[2])
copyArguments = []
lookIntoDir('/', source[1:], destination, copyArguments)
for x in copyArguments: print x
if(confirm('Move these files?')):
  for x in copyArguments: os.system(x) 
