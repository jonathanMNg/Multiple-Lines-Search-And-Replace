# Author: Jonathan Nguyen
# Published: 05/19/2018
import os, sys, fileinput
from shutil import copy
#Define constants
ARGV_LEN = 5
PROGRAM_NAME = "search_and_replace.py"
ARGV_1 = "target[file|dir]"
ARGV_2 = "search-string[file]"
ARGV_3 = "replace_string[file]"
ARGV_4 = "file_ext[php|txt|html]"
BACKUPFOLDER = "SAR_backup"

def readFile(filename):
    lines = ''
    try:
        with fileinput.FileInput(filename) as file:
            for line in file:
                    lines = lines + line
    except FileNotFoundError:
        print("Error: File %s doesn't exists" % filename)
        sys.exit()
    except UnicodeDecodeError:
        pass
    return lines
def scan_dir(dir_name, list):
    scanned_files = []
    if(os.path.isfile(dir_name)):
        scanned_files.append(dir_name)
        return scanned_files
    elif(not(os.path.isdir(dir_name))):
        return scanned_files
    else:
        if(list=='all'):
            for subdir, dirs, files in os.walk(dir_name):
                for file in files:
                    scanned_files.append( (os.path.join(subdir,file)))
        elif(list=='dir'):
            for file in os.listdir(dir_name):
                if(os.path.isdir(dir_name+'/'+file)):
                    file = file + '/'
                scanned_files.append(file)
    return scanned_files
def getDirname(path, root):
    rootLen = len(os.path.abspath(root).split('/'))
    pathLen = len(os.path.abspath(path).split('/'))
    return '/'.join(os.path.abspath(path).split('/')[rootLen-1:pathLen-1]) + '/'
def sortByType(filename):
    if filename[-1] == '/':
        return filename[-1] + filename
    else:
        return filename
def removeElementFromList(l, val):
    if(val in l):
        l.remove(val)
        return True
    else:
        return False
def removeMultipleElementsFromList(l, vals):
    removedFilesCount = 0
    for val in vals:
        if(removeElementFromList(l, val)):
            removedFilesCount = removedFilesCount + 1
    return removedFilesCount

def validArgs(argv):
    valid = True
    if(len(sys.argv) != ARGV_LEN):
        print("Error: Invalid arguments")
        print("Usage: python3 %s %s %s %s" % (PROGRAM_NAME, ARGV_1, ARGV_2, ARGV_3))
        valid = False
    return valid
def getBackupFolderName(dest):
    backupDest = dest + 'backup'
    for i in range(1, 100):
        if os.path.exists(backupDest):
            backupDest = dest + 'backup_' + str(i)
        else:
            break
    return backupDest + '/'
def doBackupFile(filename, backupFolder):
    root = '/'.join(os.path.abspath(backupFolder).split('/')[:-3])
    baseFolder = getDirname(filename, root)
    if(baseFolder == backupFolder.split('/')[-2] + '/'):
        baseFolder = ''
    backupFile = backupFolder + baseFolder + os.path.basename(filename)
    backupDest = os.path.dirname(backupFile)
    if not os.path.exists(backupDest):
        os.makedirs(backupDest)
    copy(filename, backupFile)
def confirmation(source_str, replace_str, filenames):
    infoResponse = False
    backupResponse = False
    print('- - - - - - - - - - - - - - - - - - - - -')
    print("Old string: \n%s" % source_str)
    print('- - - - - - - - - - - - - - - - - - - - -')
    print("New string: \n%s" % replace_str)
    print('- - - - - - - - - - - - - - - - - - - - -')
    print("Target files: \n%s" % '\n'.join(filenames))
    print('- - - - - - - - - - - - - - - - - - - - -')
    isCorrect = input("Are these information all correct? (y/N) ")
    if(isCorrect.strip().lower() == 'y'):
        infoResponse = True
    elif(isCorrect.strip().lower() != 'n'):
        print("Invalid input")
        return infoResponse, backupResponse
    else:
        print("Please make your changes and run the program again!")
        return infoResponse, backupResponse
    print('- - - - - - - - - - - - - - - - - - - - -')
    isBackup = input("Do you want to create a backup for the modified files? (y/N) ")
    if(isBackup.strip().lower() == 'y'):
        backupResponse = True
        return infoResponse, backupResponse
    elif(isBackup.strip().lower() != 'n'):
        print("Invalid input")
        infoResponse = False
        return infoResponse, backupResponse
    else:
        return infoResponse, backupResponse
def main():
    #check if arguments are valid
    if(not validArgs(sys.argv)):
        sys.exit()
    dir_name = os.path.relpath(sys.argv[1]) + '/'
    old_string = os.path.relpath(sys.argv[2])
    new_string = os.path.relpath(sys.argv[3])
    file_ext = sys.argv[4]
    #scan for files to process
    scanned_files = scan_dir(dir_name, list='all')
    scanned_dir = scan_dir(dir_name, list='dir')
    #sort the scanned dir by type and alphabet order
    scanned_dir.sort(key=sortByType)
    filenames = []
    backupDir = dir_name + BACKUPFOLDER + '/'
    backupFolder = ''
    for filename in scanned_files:
        if(file_ext == filename.split('.')[-1].lower()):
            filenames.append(filename)
    if(len(filenames) == 0):
        sys.exit("Couldn't find any file with extension `.%s`" % file_ext)
    #eliminate source file from target files
    removeElementFromList(filenames, old_string) #if yes, remove it
    #eliminate backup files from target files
    backupFiles = scan_dir(backupDir, list='all')
    removeMultipleElementsFromList(filenames, backupFiles) #remove backup folder from target files
    origDir = os.path.realpath(dir_name).split('/')[-1] #name of basefolder
    backupFolder = getBackupFolderName(backupDir) + origDir + '/'
    #get string to search for and string to replace with
    source_str = readFile(old_string).strip()
    replace_str = readFile(new_string).strip()
    isInfoValid, needBackup = confirmation(source_str, replace_str, scanned_dir)
    if(not(isInfoValid)):
        sys.exit()
    print("Modified files: ")
    for filename in filenames:
        tmpFile = readFile(filename)
        if(tmpFile.find(source_str) >= 0):
            print(filename)
            if(needBackup):
                doBackupFile(filename, backupFolder)
            tmpFile = tmpFile.replace(source_str, replace_str)
            with open(filename, "w") as file:
                file.write(tmpFile)

if __name__=="__main__":
    main()
