import sys
import os
import json


# This script checks if the tool is already installed. If it isn't,
# then it installs the script in the directory specified into the conf.json file.


'''
    required command-line utilities:
        - sudo
        - chmod
        - cp
        - mkdir
'''



# install the utility by creating the root directory and any other necessary file
def install_utility():
    uid, gid = (os.getuid(), os.getgid())
    if not os.path.exists(installdir):
        sudo_command("mkdir " + installdir)
    if not os.path.exists(installdir+"/"+toolname):
        sudo_command("mkdir " + (installdir+"/"+toolname))

    sudo_command("chown " + str(uid)+":"+str(gid) + " " + (installdir+"/"+toolname))

    write_to(pathnames_to_compress)                            # creates the pathnames file
    write_to(backup_locations, (default_dir+"\n"))             # creates the localdirs file
    write_to(remote_hosts_file, (ip_port+"\n"))                # creates the rhosts file

    sudo_command("sudo cp -R conf "+installdir+"/"+toolname+"/")           # copy the configuration file and directory into the installation directory
    os.system("chmod +x backuper && sudo cp backuper /usr/local/bin")   # copy the script to the user's bin path

# read the default backup directory from stdin.
def read_default_localdir():
    print "Enter an existing directory where you want to store your backups:"
    default_dir = sys.stdin.readline().replace("\n","")
    while(not os.path.exists(default_dir) or not os.path.isdir(default_dir) or not can_write_to(default_dir)):
        if not os.path.exists(default_dir):
            print "[*] The directory you provided does not exist!"
        else:
            print "[*] Directory exists but no write privileges. Obtain them or"
        print "Enter another directory pathname: "
        default_dir = sys.stdin.readline().replace("\n", "")


    default_dir = os.path.abspath(default_dir)
    if default_dir[-1] != '/':
        default_dir = default_dir + '/'
    return default_dir

# read an IP address and a port number from stdin. they've to be submitted
# with the following format: IP:port
def read_default_ipport():
    print "You want to set a remote host:port (default is No)? [Y/N]"
    ans = sys.stdin.readline()
    if ans in ["y","Y","yes","Yes","YES"]:
        print "Enter IP:port: "
        ip_port = sys.stdin.readline().replace("\n", "")
        while(not validate_ipv4_port(ip_port)):
            print "Enter an IP:port: "
            ip_port = sys.stdin.readline().replace("\n", "")
    else:
        return ""
    return ip_port

# return True if the username that runs this script
# can write to the dir directory
def can_write_to(dir):
    return (os.access(dir, os.W_OK) and os.access(dir, os.X_OK))

# write stuffs into filename
# if stuffs is None, then this method creates filename and then terminates.
def write_to(filename, stuffs=None):
    f = open(filename, "w")
    if stuffs != None:
        f.write(stuffs)
    f.close()

# tries to execute the given command line utility
# with root privileges. Naturally, it may require a password.
def sudo_command(cmd):
    os.system("sudo " + cmd)


# return True if the directory that would be created AND the python executable
# already exists. Otherwise it returns False
def is_already_installed(installdir, toolname):
    if(os.path.exists(installdir+"/"+toolname) or os.path.exists("/usr/local/bin/"+toolname)):
        return True
    return False

# returns True if the input string represents an integer,
# otherwise returns False.
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# validate a 'decimal-formatted' IPv4 address
def isvalid_ipv4(ip):
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not RepresentsInt(x):
            print "not an int"
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

# validate an (IP,port) pair format
def validate_ipv4_port(ip_port):
    r = ip_port.split(":")
    if len(r) != 2 or not (RepresentsInt(r[1]) and 1 <= int(r[1]) <= 65535) or not isvalid_ipv4(r[0]):
        return False
    return True



###############################
#           MAIN
###############################

# parses the JSON configuration file
data = json.loads(open('conf/conf.json').read())
installdir = data["installation_dir"]
toolname = data["tool_name"]
backup_locations = installdir+"/"+toolname+"/"+data['backup_location']
pathnames_to_compress = installdir+"/"+toolname+"/"+data['pathnames_to_compress']
remote_hosts_file = installdir+"/"+toolname+"/"+data['remote_hosts_file']

# check if the tool is already installed.
# if it's installed, then quit.
if(is_already_installed(installdir, toolname)):
    print "[*] ALREADY INSTALLED"
    print "[*] In order to uninstall the utility, just run the uninstall.sh script"
    sys.exit(3)
print "[*] Tool not installed yet"


default_dir = read_default_localdir()   # read the default brackup directory
ip_port = read_default_ipport()         # read the default IP:port pair, only if the user wants to
if ip_port == "":
    print "No remote host stored"

print "\n[*] Installing the utility.. this may take a while..."
install_utility()
print "\n[*] Tool installed successfully!!"
