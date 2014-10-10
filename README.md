scripts
=======

 * **checkLHE.py <lhe-file>** 
   Checks lhe-file for missing event tags and blank lines 
   Returns number of events

 * **copySRM.py <source> <destination>** 
   Copy the source directory (relative path) to a destination on Brussels T2 (path relative to /pnfs/iihe/cms/store/user/$USER)
   (Need voms-proxy-init to work)

 * **cpstar 'something\_\*\_\*.txt' 'something\_\*\_different\_\*.txt'**  
   Allows to use wildcards in the cp command  
   Destination/source should be quoted and could be both relative or absolute  

 * **crabStatus.py <options>**  
   Wrapper around crab -status which allows to use filters on output and easy resubmissions  
   -j \<jobs\> select on jobs  
   -s \<search\> select on status, host, exit code,...  
   -k kill selected jobs  
   -r resubmit of jobs  
   -f forceResubmit of jobs  
   -b blacklist T2  

 * **mvstar 'something\_\*\_\*.txt' 'something\_\*\_different\_\*.txt'**  
   Allows to use wildcards in the mv command  
   Destination/source should be quoted and could be both relative or absolute  

 * **removeExcept <files>**  
  Removes everyhing in this folder except the specified files  


