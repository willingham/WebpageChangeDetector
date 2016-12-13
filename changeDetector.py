##############################################
#
# Website Change Detector
# Author: Thomas Willingham
# Date: December 2016
#
#############################################
import urllib, difflib, subprocess, sys, time

# set these two lines
toAddress = "your@email.com" # the address an alert will be sent to
fromAddress = "alertsS@yourdomain.com" # the address an alert will come from
interval = 300 # time between checks (in seconds)

usage = "python changeDetector.py [-i intervalToCheckInSeconds] urlToMonitor"
if len(sys.argv) < 2 or sys.argv[1] == "-h":
    print(usage)
    exit(1)
elif len(sys.argv) == 2:
    url = sys.argv[1]
elif len(sys.argv) == 4 and sys.argv[1] == "-i":
    interval = int(sys.argv[2])
    url = sys.argv[3]
else:
    print(usage)
    exit(1)

f = urllib.urlopen(url)
with open("orig.html", "w+") as fil:
    fil.write(f.read()) # set the initial state of the website
print("Original State Set.")
while(1):
    f = urllib.urlopen(url)
    diff = difflib.unified_diff(f.read(), open("orig.html").read())
    x = ' '.join(diff)
    y = x.split(" ")
    if len(y) > 1:
        print("Change Detected!")
        command = 'echo "%s%s" | mailx -r %s %s' % ("Change detected on ", url, fromAddress, url)
        subprocess.call(command, shell=True)
        exit(0)
    else:
        print("No Change Detected. Now sleeping for " + str(interval) + " seconds.")
        time.sleep(interval)
