#!/usr/bin/env python
caption = """
#######################################################
# Python Music Player
# By Benjamin Urquhart
# VERSION: 2.5

This player is designed to play music on a Raspberry Pi,
but can be used on Windows and OSX.
OSX support is limited.

Doumentation is in the README file
#######################################################
"""
version = '2.5'
revision = '0'
log_cache = [] # The log() function hasn't been defined yet, so this is where the logs go for now
log_cache.append("Starting preload...")
#######################################################
log_cache.append("Defining variables...")
kill = False
threadUse = False
stop = False
skip = False
pause = False
play = False
debug = False
select = 0
current = ""
amount = 0
played = []
playlist = []
check = ""
width = 800
height = 600
console = False
text = ""
songNum = 1
app = None
url = "https://benjaminurquhart.dynu.net"
#######################################################
log_cache.append("Importing sys...")
# In order to parse arguments, we need to import the sys module early
import sys
try:
    argv = sys.argv
    if "-v" in argv or "--verbose" in argv:
        debug = True
    if "-f" in argv or "--file" in argv:
        current = str(argv[len(argv) - 1])
    if "-c" in argv or "--console" in argv:
        console = True
    if "--help" in argv or "-h" in argv:
	print 'Plays music in the "Music" folder within the current directory\n'
	print "Usage: " + sys.argv[0] + " [-hvc] [-f <filepath>]"
	print "Options: "
	print "\t -h, --help\t Displays this help text"
	print "\t -v, --verbose\t Displays extra information"
	print "\t -c, --console\t Disables Pygame screen (text-only mode)"
        print "\t -f, --file\t Plays the file at the filepath specified"
        print "\nExamples: \n\t " + sys.argv[0] + " -v -c -f /sample/file/path/foo.bar"
        print "\t " + sys.argv[0] + " -f foo.bar"
        kill = True
except:
    pass
if kill:
    exit()
######################################################
log_cache.append("Importing datetime...")
import datetime
log_cache.append("Importing urllib...")
import urllib
log_cache.append("Importing urllib2...")
import urllib2
log_cache.append("Importing os...")
import os
log_cache.append("Importing string...")
import string
log_cache.append("Importing tarfile...")
import tarfile
log_cache.append("Importing subprocess...")
import subprocess
log_cache.append("Importing threading...")
import threading
log_cache.append("Importing sleep from module time...")
from time import sleep
log_cache.append("Importing randint from random module...")
from random import randint
mod = "traceback"
try:
    log_cache.append("Trying to import " + mod + "...")
    import traceback
    mod = "requests"
    log_cache.append("Trying to import " + mod + "...")
    import requests
    #mod = "spin_mod"
    #log_cache.append("Trying to import " + mod + "...")
    #import spin_mod as spin
except ImportError:
    log_cache.append("Unable to import " + mod)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    log_cache.append(''.join(line for line in lines))
log_cache.append("Done preloading")
#####################################################
# For some reason, the DDNS address above doesn't work in my house
# The following lines will determine if the local address should be used instead
log_cache.append("Checking for dev mode...")

try:
    urllib.urlopen("http://localhost/devmode")
    log_cache.append("Setting URL to localhost...")
    url = "http://localhost"
    debug = True
    log_cache.append("Done")
except:
    log_cache.append("URL not changed")
log_cache.append("Done URL checking")
log_cache.append("Starting...")
######################################################
#                                                    ############
print "Starting Python Music Player " + version + "." + revision + "..."
#spin.setText("Starting Python Music Player " + version + "." + revision) #
#                                                    ############
######################################################
#spin.start()
log_cache.append("Defining functions...")
class FuncThread(threading.Thread):
    def __init__(self,target,*args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)
log_cache.append("Defined threading class FuncThread")
######################################################
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
log_cache.append("Defined mkdir()")
######################################################
def touch(path):
    with open(path, 'a'):
        os.utime(path, None)
log_cache.append("Defined touch()")
######################################################
# The shutdown process
def shutdown():
    kill = True
    bcast("\n")
    bcast("Stopping...")
    try:
        pygame.mixer.music.stop()
    except:
        pass
    log("Shutdown success")
    log_file.close()
    latest_log.close()
    if console == False:
        try:
            app.stop()
        except:
            pass
    #spin.stop()
    pygame.quit()
    quit()
log_cache.append("Defined shutdown()")
######################################################
# Custom logging function
def log(string):
    try:
	#if debug and not spin.getStop():
	    #spin.setText(string)
        #elif debug:
	if debug:
            print "[Debug]: " + string
	log_file.write("[Logger]: ")
        log_file.write(string)
        log_file.write("\n")
    except:
        pass
    try:
        latest_log.write("[Logger]: " + string + "\n")
    except:
        #log_cache.append("[Logger]: " + string + "\n")
        pass
log_cache.append("Defined log()")
######################################################
def LogErr():
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        log('')
        log(''.join(line for line in lines))
        if debug:
            bcast(''.join(line for line in lines), True)
    except:
        pass
log_cache.append("Defined LogErr()")
######################################################
def getKill():
    return kill
log_cache.append("Defined getKill()")
######################################################
def bcast(string, err=False):
    try:
	#if not spin.getStop():
	    #spin.setText(string)
        #elif err:
	if err:
            print "[Error]: " + string
        else:
            print "[Player]: " + string
    except:
        pass
log_cache.append("Defined bcast()")
######################################################
def updater():
    log('Update requested; attempting...')
    if update == 0:
        bcast('No update found.')
        log('No update found')
    else:
        bcast('Attempting to retrive tarball...')
        try:
            log('Connecting to ' + url +'...')
            try:
                r = requests.get('http://' + url)
                status = r.status_code
            except:
                status = 200
                LogErr()
            if int(status) == 200:
                try:
                    bcast('Downloading...')
                    urllib.urlretrieve(url + '/python/downloads/player/music-player-' + str(ver) + '.tar.gz', 'music-player-' + str(ver) + '.tar.gz')
                except:
                    LogErr()
                    raise IOError
                bcast('Installing...')
                log('Download success')
                log('Will now attempt to install update')
                try:
                    mkdir('update')
                    os.rename("music-player-" + str(ver) + ".tar.gz", 'update/update.tar.gz')
                    os.chdir('update')
                    tar = tarfile.open("update.tar.gz")
                    tar.extractall()
                    tar.close()
                    os.remove('update.tar.gz')
                    os.chdir('..')
                    log('Success!')
                    log("Attempting to copy over...")
                    try:
                        os.rename("updater/player.py","player.py")
                        bcast("Done!")
                        bcast("Changes will take place next run")
                    except:
                        LogErr()
                        bcast("Auto update failed")
                        bcast("Please copy the 'player.py' file from the 'update' folder")
                except:
                    LogErr()
                    bcast('Installation failed')
            else:
                bcast('Server is down')
                raise IOError
        except:
            LogErr()
            bcast('Download failed')
log_cache.append("Defined updater()")
######################################################
# To control the player remotely (Don't use)
def server():
    try:
        import socket
        HOST = socket.gethostname()
        PORT = 9000
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            LogErr()
            try:
                s.close()
            except:
                LogErr()
                pass
        s.listen(2)
        print 'Started control server on ' + HOST + ':' + str(PORT)
    except:
        print "Couldn't create control server"
        LogErr()
log_cache.append("Defined server()")
######################################################
# Get news updates
def news():
    log("Getting news")
    try:
        news = urllib2.urlopen(url + "/news.txt")
        news = news.read()
        if news == '':
            bcast("No News")
            log("No News")
        else:
            bcast(news)
            log(news)
    except:
        LogErr()
        bcast("Couldn't get news updates", True)
log_cache.append("Defined news()")
######################################################
def control(option=""):
    threadUse = True
    if option == "":
        option = raw_input("> ")
    try:
        option = option.replace("\n", '')
        option = option.lower()
        if option == 'quit' or option == 'stop':
            shutdown()
            #stop = True
            #shutdown()
        elif option == 'skip':
            #skip = True
            pygame.mixer.music.stop()
        elif option == 'update':
            #update = True
            try:
                app.addLabel("status","Getting update...")
            except:
                LogErr()
                pass
            updater()
        # Play/Pause indev
        elif option == 'pause':
            #pause = True
            pygame.mixer.music.pause()
            bcast('Paused')
        elif option == 'play':
            #play = True
            pygame.mixer.music.unpause()
            bcast("Playing")
        elif option == '':
            option = ''
        elif option == 'debug':
            if debug == True:
                print "Debug mode disabled"
                debug = False
            elif debug == False:
                print "Debug mode enabled"
                debug = True
        elif option == "news":
            news()
        else:
            bcast("Invalid command: " + option)
    except:
        LogErr()
    sleep(0.1)
    threadUse = False
log_cache.append("Defined control()")
###################################################
# This is leftover from the pygame screen era
def control2(pause):
    try:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event == pygame.K_d:
                    print "Debug"
                    if debug:
                        debug = False
                    else:
                        debug = True
                if event.key == pygame.K_SPACE or event.key == pygame.K_F11:
                    bcast("Pause")
                    if pause == True:
                        pygame.mixer.music.play()
                        pause = False
                    elif pause == False:
                        pygame.mixer.music.pause()
                        pause = True
                if event.key == pygame.K_u:
                    bcast("Update")
                    updater()
                if event.key == pygame.K_F12:
                    bcast("Skip")
                    pygame.mixer.music.stop()
                if event.key == pygame.K_F10 or event.key == pygame.K_q:
                    bcast("Quit")
                    shutdown()
    except:
        LogErr()
    sleep(0.2)
    return pause
log_cache.append("Defined control2()")
######################################################
log_cache.append("Done defining main functions")
log_cache.append("Creating logfile...")
mkdir('logs')
time = datetime.datetime.now()
time = str(time).replace(":",";")
try:
    latest_log = open("./logs/latest.log", "w")
    log_file = open("./logs/" + str(time), "w")
except:
    LogErr()
    bcast("Failed to create log")
log_cache.append("Dumping log_cache...")
log("Showing cached log messages...")
for i in log_cache:
    log(i)
log("Defining more functions...")
######################################################
def getFile():
    return log_file
log("Defined getFile()")
######################################################
def getReport():
    return "Dummy Text"
log("Defined getReport()")
######################################################
def getKilled():
    return kill
log("Defined getKilled()")
######################################################
def playAll(playThis=None):
    # Check the Music folder for tracks
    songNum = 1
    sound_data = os.listdir('./Music')
    playlist = []
    try:
	for i in sound_data:
	    playlist.append(i)
	i = 0
	amount = len(playlist)
	log(str(amount) + " Songs found")
	if amount == 0:
	    bcast('No music found!')
	    shutdown()
	bcast("Number of songs: " + str(amount))
	played = []
        # Play the music
	while i < amount:
	    select = randint(0, amount - 1)
	    #if not playThis == None or not playThis == "":
                #current = playThis
                #playlist = [playThis]
	    #else:
		#current = playlist[select]
		#current = current.replace("\n", "")
	    current = playlist[select]
	    if current not in played:
                # Try to load the track
		bcast("Now Playing: " + current + " (" + str(songNum) + " out of " + str(amount) + ")")
		log("Song " + str(songNum) + " out of " + str(amount))
		try:
		    log("Loading '" + current + "'")
		    pygame.mixer.music.load("./Music/" + current)
		    log('Now Playing: ' + current)
		except:
		    bcast("Couldn't play " + current)
                # Play loaded track
		pygame.mixer.music.play()
                # Take user input for controlling player
		while pygame.mixer.music.get_busy():
                    if console:
                        control()
                    if getKilled():
                        played = playlist
                        pygame.mixer.music.stop()
                        i = amount - 1
                        shutdown()
			break
                if not current in played:
		    played.append(current)
		    i = i + 1
		sleep(0.2)
		songNum = songNum + 1
	bcast("All songs have been played!")
	log('All songs have been played')
	shutdown()
    except:
	LogErr()
	shutdown()
log("Defined playAll()")
log("Done defining additional functions")
######################################################
#Bug reporter (BETA)
log("Trying to send a bug report (if it exists)")
try:
    crash_test = open(".iscrashed","r")
    crashed = crash_test.readline()
    crashed = crashed.replace("\n","")
    crash_test.close()
    if crashed == "true":
	bcast("The player crashed")
	bcast("Sending crash report to server")
	log("A crash has been detected. Sending report to server...")
	urllib.urlopen(url + "/crashreporter.php?version=" + version + "&revision=" + revision + "&report=" + getReport())
	bcast("Report sent")
except:
    LogErr()
    touch(".iscrashed")
######################################################
tmp = open(".iscrashed","w")
tmp.write("false")
tmp.close()
######################################################
#Looking for third party dependencies...
#spin.stop()
log("Importing pygame. This is a non-statndard module in python and may need to be installed")
try:
    import pygame
    from pygame.locals import *
except ImportError:
    LogErr()
    old_junk = """
    bcast("Missing dependency: " + dep)
    if dep == "appjar":
        bcast('Getting appjar...')
        log("Getting appjar...")
        urllib.urlretrieve("http://" + url + "/appJar.tar.gz","appJar.tar.gz")
        tar = tarfile.open("appJar.tar.gz")
        tar.extractall()
        tar.close()
        os.remove("appJar.tar.gz")
        bcast("Done!")
        log("Done!")
        bcast("Attempting to load appjar...")
        log("Importing appjar...")
        try:
            from appJar import gui
            log("Success!")
            bcast("Success!")
        except ImportError:
            LogErr()
            bcast("Failed :(")
            shutdown()
        pass"""
    try:
        #spin.setText("Getting pygame...")
	#spin.start()
	bcast("Getting pygame...")
        log('Pygame missing; getting installer')
        osv = sys.platform
        if osv == 'win32':
            urllib.urlretrieve('https://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi', 'pygame-1.9.1.msi')
        elif osv == 'darwin':
            urllib.urlretrieve('https://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg', 'pygame-mac.dmg')
            log('Success!')
        elif osv == 'linux2' or osv == 'cygwin' or osv == 'linux3':
            bcast('You are using linux or cygwin')
            bcast("Use the command 'sudo pip install pygame' to install pygame")
            log(osv + ' detected; pip installer recommended')
        else:
            bcast('Unrecognized os: ' + osv)
        try:
            if os.uname()[4][:3] == 'arm':
                log("CPU architecture: " + os.uname()[4][:3])
                bcast("ARM processor architecture detected. Trying to get ARM-compiled pygame package...")
                urllib.urlretrieve(url + '/pygame.tar.gz', 'pygame.tar.gz')
                tar = tarfile.open("pygame.tar.gz")
                tar.extractall()
                tar.close()
                os.remove('pygame.tar.gz')
        except:
            LogErr()
            bcast("Failed to get pygame for ARM")
            shutdown()
        bcast('Please run the installer that has been dropped into the ' + os.path.dirname(os.getcwd()) + ' folder')
    except:
        bcast('Failed to get pygame')
        bcast("Please install the 'pygame' module manually at pygame.org")
        LogErr()
        shutdown()
    shutdown()
#spin.stop()
try:
    if console == False:
        log("Importing AppJar (another non-standard module)")
        from appJar import gui
        #app = gui("Music Player")
except ImportError:
    LogErr()
    bcast("AppJar could not be imported")
    bcast("This is required for the GUI to work")
    option = raw_input("Install? (yes/no): ")
    if option.lower() == "yes" or option.lower() == "y":
        try:
            bcast("Installing AppJar...")
            log("Downloading AppJar...")
            urllib.urlretrieve(url + "/appJar.tar.gz", "appJar.tar.gz")
            log("Extracting archive...")
            tarfile.open("appJar.tar.gz")
            tarfile.extractall()
            tarfile.close()
            os.remove("appJar.tar.gz")
            log("Done!")
            from appJar import gui
            #app = gui("Music Player")
        except:
            LogErr()
            bcast("Unable to download and install AppJar")
            bcast("The GUI will now be disabled")
            console = True
    elif option.lower() == "no" or option.lower() == "n":
        bcast("GUI will now be disabled.")
        bcast("You will be prompted again on next run")
    else:
        bcast("Invalid option: " + option)
        bcast("AppJar will not be installed")
#######################################################
# Load pygame module
try:
    pygame.init()
    pygame.mixer.init()
    #pygame.font.init()
    log('Pygame initialized')
except:
    bcast("Couldn't run pygame.init()", True)
    log("pygame.init() failed")
    LogErr()
######################################################
# Checking for updates...
update = 0
try:
    log('Checking for updates...')
    log('Getting info from ' + url)
    ver = urllib2.urlopen(url + '/version.txt')
    rev = urllib2.urlopen(url + '/rev.txt')
    ver = ver.read()
    rev = rev.read()
    log("Version from server: " + ver)
    log("Revision from server: " + rev)
    log("Installed version: " + version)
    log("Installed revision: " + revision)
    if float(ver) > float(version):
        log('Update found!')
        bcast("Python Music Player " + ver + " is availible")
        bcast("Type update at the prompt to download")
        update = 1
    elif float(ver) < float(version):
        log('Indev vesion in use')
        bcast('Indev version in use')
    elif int(rev) > int(revision) and float(ver) == float(version):
        log('New revision found!')
        bcast('Revision ' + str(rev) + ' is availible')
        bcast('Type update at the prompt to download')
        update = 1
    elif float(ver) == float(version):
        log('No update found')
        bcast('No update found')
except:
    bcast('Failed to check for updates', True)
    LogErr()
    log('Update check failed')
######################################################
mkdir('Music')
log("Player starting...")
news()
######################################################
try:
    if console == False:
        app = gui("Music Player")
        buttons = ["stop","play","pause","skip"]
	num = 0
        if update == 1:
            buttons.append("update")
        for i in buttons:
            app.addButton(i,control,0,num)
            num = num + 1
	app.addLabel("Loading...")
        num = 0
except:
    bcast("Display error, console mode active", True)
    log("Display error")
    LogErr()
    console = True
######################################################
log("Player started")
try:
    #player_engine.__init__("backend")
    backend = FuncThread(playAll,current)
    backend.start()
    if console == False:
        app.go()
except:
    LogErr()
    bcast("Failed to initialize backend")
    shutdown()
######################################################
