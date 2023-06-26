#Feed this script your fixpack and it will move it to the correct location and explode it for you - conforms to Python 2.6.6
#This assumes you are running this on v8 or higher. <= v7 has a separate set of instructions and comes up rarely enough to not code in
import sys, os, subprocess, traceback, pwd, grp
from os.path import expanduser

if len(sys.argv) != 2: #make sure the command only has two entries (not including the python command)
	print('RUN FAILED')
	print('Proper usage: python fixpack_deploy.py fixpackfile.jar')
	sys.exit(0)
	
homedirectory_path = expanduser("~") #grab /home/yourusername path
print('Grabbing home path.')

if os.path.isfile(homedirectory_path + '/' + sys.argv[1]) != True: #check if /home/home_folder/fixpackfile.jar exists
	print("The given path does not exist, please try again.")
	sys.exit(0)

print('Check for fixpack location. -- PASSED')
	
jar_in_homedirectory_path = homedirectory_path + '/' + sys.argv[1] #set /home/home_folder/fixpackfile.jar as var

dir_list = os.listdir('/usr/local/jive/applications') #has only ever caught 3 in my tests
dir_list.remove('saasagent') #one of the three, not needed
dir_list.remove('template') #one of the three, not needed

if len(dir_list) != 1:
	print('Too many items in dir_list, this should never be hit') #if somehow a site has more than three folders in /usr/local/jive/applications
	sys.exit(0)

if os.path.isdir('/usr/local/jive/applications/%s/application/WEB-INF/classes' % dir_list[0]) != True: #check if /usr/local/jive/applications/installation_name/application/WEB-INF/classes exists
	print("Incorrect installation name. Found under \"Name\" on JCA page if hosted, or is supposed to be \"sbs\" on cloud")
	sys.exit(0)

wd = os.getcwd()
os.chdir("/usr/local/jive/applications/%s/application/WEB-INF/classes" % dir_list[0]) #cd to the path where you need to be
	
print('Check for correct installation name path. -- PASSED')

potential_oldfile = '/tmp/%s' % sys.argv[1] #set var for /tmp/fixpackfile.jar

try:
	if os.path.isfile(potential_oldfile) == True: #if jar you are preparing to copy already exists in /tmp/ then remove it. Prevents applying outdated fixpacks?
		print("Removing %s" % potential_oldfile)
		delete_oldjar = subprocess.call(['sudo', 'rm', '-f', '%s' % potential_oldfile])
except Exception:
	print('Removing %s -- FAILED' % potential_oldfile)
	traceback.format_exc()
print('Target path for jar is clear.')

try:
	subprocess.call(['cp', '%s' % jar_in_homedirectory_path, '/tmp']) #cp /home/home_folder/fixpackfile.jar /tmp/
except Exception:
	print('Copy to /tmp/ -- FAILED')
	traceback.format_exc()
	
print('Copied jar into /tmp/')

try:
	os.system('sudo -u jive /usr/local/jive/java/bin/jar xvf %s' % potential_oldfile) #runs as the 'jive' user for the exploded file permissions to be correct
except Exception:
	print('Exploded jar -- FAILED')
	traceback.format_exc() #print the trace
	sys.exit(0)
print('Exploded jar -- PASSED')
os.chdir(wd) #cd ~
print('JOB SUCCESSFUL!')