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
    lines = []
    try:
        with fileinput.FileInput(filename) as file:
            for line in file:
                if(line.replace('\n','') != ''):
                    lines.append(line.replace('\n',''))
    except FileNotFoundError:
        print("Error: File %s doesn't exists" % filename)
        sys.exit()
    except UnicodeDecodeError:
        pass
    return lines
def scan_dir(dir_name):
    scanned_files = []
    if(os.path.isfile(dir_name)):
        scanned_files.append(dir_name)
        return scanned_files
    elif(not(os.path.isdir(dir_name))):
        return scanned_files
    for subdir, dirs, files in os.walk(dir_name):
        for file in files:
            scanned_files.append( (os.path.join(subdir,file)))
    return scanned_files
def isLineFound(source,target):
    len_s = len(source) #so we don't recompute length of s on every iteration
    for i in range(len(target) - len_s+1):
        if(source == target[i:len_s+i]):
            return i
    else :
        return -1
def isStringFound(source_str, filename):
    with fileinput.FileInput(filename, inplace=False, backup='') as file:
        for line in file:
            if(line.find(source_str[0])>=0):
                return True
    return False
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
def doBackupDir(filenames):
    print("Backup is in progress...")
    for filename in filenames:
        doBackupFile(filename)
    print("Done backup!")

def getBackupFolderName(dest):
    backupDest = dest + '/backup'
    for i in range(1, 100):
        if os.path.exists(backupDest):
            backupDest = dest + '/backup_' + str(i)
        else:
            break
    return backupDest + '/'
def doBackupFile(filename, backupFolder):
    baseFolder = '/' if not('./' in os.path.dirname(filename)) else os.path.dirname(filename) + '/'
    backupFile = os.path.abspath(backupFolder) + baseFolder + os.path.basename(filename)
    backupDest = os.path.dirname(backupFile)
    if not os.path.exists(backupDest):
        os.makedirs(backupDest)
    copy(filename, backupFile)
def doMultipleLineSAR(filename, target_str, source_str, replace_str):
    linePtr = []
    pos = 0
    lineNo = isLineFound(source_str, target_str)
    while(lineNo >=0):
        pos = pos + lineNo + 1
        lineNo = isLineFound(source_str, target_str[pos:])
        linePtr.append(pos-1)
    for line in reversed(linePtr):
        target_str[line:line+len(source_str)] = replace_str
    target_str = '\n'.join(target_str)
    with open(filename, "w") as file:
        file.write(target_str)
def doSingleLineSAR(filename, source_str, replace_str):
    with fileinput.FileInput(filename, inplace=True, backup='') as file:
        for line in file:
            print(line.replace(source_str[0], replace_str[0]), end='')
def confirmation(source_str, replace_str, filenames):
    infoResponse = False
    backupResponse = False
    print('- - - - - - - - - - - - - - - - - - - - -')
    print("Old string: \n%s" % '\n'.join(source_str))
    print('- - - - - - - - - - - - - - - - - - - - -')
    print("New string: \n%s" % '\n'.join(replace_str))
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
        return infoResponse, backupResponse
    else:
        return infoResponse, backupResponse
def main():
    #check if arguments are valid
    if(not validArgs(sys.argv)):
        sys.exit()
    dir_name = sys.argv[1]
    old_string = sys.argv[2]
    new_string = sys.argv[3]
    file_ext = sys.argv[4]
    #scan for files to process
    scanned_files = scan_dir(dir_name)
    filenames = []
    if(not('/' in dir_name)):
        dir_name = dir_name + '/'
    backupDir = dir_name + BACKUPFOLDER
    backupFolder = ''
    for filename in scanned_files:
        if(file_ext == filename.split('.')[-1].lower()):
            filenames.append(filename)
    if(len(filenames) == 0):
        sys.exit("Couldn't find any file with extension `.%s`" % file_ext)
    #eliminate source file from target files
    if(not('./' in old_string)): #check if input filename is valid
        old_string = './' + old_string #if not, change it
    removeElementFromList(filenames, old_string) #if yes, remove it
    #eliminate backup files from target files
    backupFiles = scan_dir(backupDir)
    removeMultipleElementsFromList(filenames, backupFiles)
    origDir = os.path.realpath(dir_name).split('/')[-1] + '/' #name of basefolder
    backupFolder = getBackupFolderName(backupDir) + origDir
    #get string to search for and string to replace with
    source_str = readFile(old_string)
    replace_str = readFile(new_string)
    isInfoValid, needBackup = confirmation(source_str, replace_str, filenames)
    if(not(isInfoValid)):
        sys.exit()
    print("Modified files: ")
    for filename in filenames:
        #if there is only 1 line each in source_str and target_str, do search and replace line by line
        if(len(source_str) == 1 and len(replace_str) == 1):
            if (isStringFound(source_str, filename)):
                print(filename)
                if(needBackup):
                    doBackupFile(filename, backupFolder)
                doSingleLineSAR(filename, source_str, replace_str)
        #else do search and replace multiple line
        else:
            target_str = readFile(filename)
            numLine = isLineFound(source_str, target_str)
            if(numLine >= 0):
                print(filename)
                if(needBackup):
                    doBackupFile(filename, backupFolder)
                doMultipleLineSAR(filename, target_str, source_str, replace_str)
if __name__=="__main__":
    main()
