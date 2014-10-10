#!/usr/bin/env python

# removeExcept <files>
# Removes everyhing in this folder except the specified files

import os
import shutil
import sys
import fnmatch

keep = [os.path.join(os.getcwd(), item) for item in sys.argv[1:]]
for file in keep: 
  if not file == os.getcwd(): keep.append(os.path.dirname(file))

for root, dirs, files in os.walk(os.getcwd()):
  if not root in keep: continue
  for f in files:
    if not os.path.join(root, f) in keep: os.unlink(os.path.join(root, f))
  for d in dirs:
    if not os.path.join(root, d) in keep: shutil.rmtree(os.path.join(root, d))
