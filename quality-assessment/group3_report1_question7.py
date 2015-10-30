import subprocess
import sys

def findLongest(command):
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc.stdout.readline() # throw away first line
	longest = len(proc.stdout.readline())
	print longest

path = sys.argv[1] # file path for pass reads

# Winner of 2D
print "Longest read for template in passed reads:"
poretools_command = "poretools winner --type fwd " + path
findLongest(poretools_command)

# Winner of Template
print "Longest read for complement in passed reads:"
poretools_command = "poretools winner --type rev " + path
findLongest(poretools_command)

# Winner of Complement
print "Longest read for 2D in passed reads:"
poretools_command = "poretools winner --type 2D " + path
findLongest(poretools_command)