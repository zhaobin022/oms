#!/usr/bin/env python
import os,commands,math
def get_cpu_count():
    # initialize a grains dictionary
    grains = {}
    # Some code for logic that sets grains like
    grains['physical_cpu_count' ] = commands.getoutput('cat /proc/cpuinfo  | grep "physical id" | sort  | uniq  | wc -l')
    disk_list = commands.getoutput('fdisk -l | grep "^Disk /dev"|grep -v mapper  | cut -d " " -f 5').split('\n')
    disk_size = 0
    for d in disk_list:
        disk_size+=int(d)
    
    grains['disk' ] = '%dG' % (disk_size/1024/1024/1024)
    return grains


#print get_cpu_count()