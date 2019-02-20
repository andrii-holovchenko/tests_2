import psutil
import subprocess
import re
import time

file_num = 3
file_size = 4096
#free_space = 


# Detect local mounted disk
local_disk_mounts = []
partitions = psutil.disk_partitions(all=False)
pattern = re.compile(".*/dev/[h,s]d[a-z].*")
for p in partitions:
   if pattern.match(str(p)) and psutil.disk_usage(p.mountpoint).free > 1024:
        local_disk_mounts.append(p.mountpoint)

def run_dd(num, size, mount):
    for n in range(num):
        subprocess.check_output(['dd', 'if=/dev/zero', 'of=%sfile%s.txt' % (mount, n), 'count=1', 'bs=%s' % size ], stderr=subprocess.STDOUT)


start = time.time()
run_dd(file_num, file_size, local_disk_mounts[0])
end = time.time()

print("Time used: " + str(end - start))
