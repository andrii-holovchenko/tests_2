#!/usr/bin/python

import argparse
import psutil
import subprocess
import re
import time
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int, help="Number of files to create")
parser.add_argument("-s", "--size", type=int, help="Size of file to create in MB")
parser.add_argument("-m", dest='min_free', type=int, help="Minimum disk free space in MB")
parser.add_argument("-l", dest="list",  action='store_true', help="List available mount points. Should be used with \'-m\' option")

# Detect local mounted disk
def local_disk_mounts(min_free):
    local_disk_mounts = []
    partitions = psutil.disk_partitions(all=False)
    pattern = re.compile(".*/dev/(mapper|[h,s]d[a-z]).*")
    for p in partitions:
        # psutil.disk_usage returns values in bytes
        if pattern.match(str(p)) and psutil.disk_usage(p.mountpoint).free > (min_free * 1024 * 1024):
            local_disk_mounts.append(p.mountpoint)
    if local_disk_mounts:
        return local_disk_mounts
    else:
        print "No available local mounted disks with %s MB free space" % min_free
        exit()

def run_dd(num, size, mount):
    try:
        subprocess.check_output(['dd', 'if=/dev/zero', 'of=%sfile%s.txt' % (mount, num), 'status=none', 'count=1', 'bs=%s' % (size * 1024 * 1024)])
        print('File \'%sfile%s.txt\' created succefully! Size: %s MB' % (mount, num, size))
    except subprocess.CalledProcessError as e:
        print "Error code:", e.returncode, e.output

def list_disks():
    if local_disk_mounts(min_free):
        print "List of available mounted disks with minimum %s MB free space:" % min_free
        print '\n'.join([i for i in local_disk_mounts(min_free)])

if __name__ == '__main__':

    args = parser.parse_args()
    file_num = args.number
    file_size = args.size
    min_free = args.min_free
    
    start = time.time()
    if args.list and min_free:
        list_disks()
        exit()
    elif args.list and not min_free:
        print "Option \'-l\' cant be use\'d without \'-m\' option!"
        exit()

    if args.number and args.size:
        if local_disk_mounts(min_free):
            print "Available disks:"
            print ','.join(local_disk_mounts(min_free))
            try:
                mount_point = raw_input('Please choose a disk you want to write on or \'ctrl+c\' for exit: ')
                while mount_point not in (local_disk_mounts(min_free)):
                    print "Wrong input!"
                    print "Available disks:"
                    print ','.join(local_disk_mounts(min_free))
                    mount_point = raw_input('Please choose a disk you want to write on or \'ctrl+c\' for exit: ')
            except KeyboardInterrupt:
                print('\nInterrupted. Exit the program.')
                exit()
            processes = []
            for i in range(file_num):
                p = multiprocessing.Process(target=run_dd, args=(i, file_size, mount_point,))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
                if process.exitcode != 0:
                    '%s exitcode = %s' % (process.name, process.exitcode)
    print('Time used {} seconds'.format(time.time() - start))

