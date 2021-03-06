#!/usr/bin/env python2.6
import sys
import os
import getpass

source = sys.argv[1]
destination = sys.argv[2]

def copyFiles(dir):
  os.system("srmmkdir  srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/" + getpass.getuser() + "/" + os.path.join(destination, dir)) 
  for item in os.listdir(os.path.join(os.getcwd(), dir)):
    item = os.path.join(dir, item)
    if(os.path.isfile(os.path.join(os.getcwd(), item))): 
      if(os.path.isfile("/pnfs/iihe/cms/store/user/tomc/" + os.path.join(destination, item))):
        print item + " exists"
        continue
      os.system("srmcp file:///" + os.path.join(os.getcwd(), item) + " srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/" + getpass.getuser() + "/" + os.path.join(destination, item)) 
    else: copyFiles(item)

copyFiles(source)
