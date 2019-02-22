# tests_2

# prog1.py 
Usage:

Create 3 files with size of 10 MB:
./prog1.py -n 3 -s 10 -m 1

List local mount points with free space more than 1000 MB:
./prog1.py -l -m 100

# prog2.py

Usage:
./prog2.py command hosts

Execute command 'ls -1' on hosts vm1 and vm2
./prog2.py ls -1 -l vm1 vm2
