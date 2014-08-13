#!/usr/bin/env
"""

This script is designed to be a supplemental tool for the Ramsey County Property
Records and Revenue Mapping Department.  We are tasked with keeping up-to-date
tax maps that were traditionally housed internally on mylar.  There has been a
shift towards digital storage so future tax maps will be presented on the county
website as a PDF.  This script assists in the creation of these maps by offering
options, such as, reducing the size a quarter section map to match the scale of
a half section map.  The script will also launch *.pdf templates with embedded
document level JavaScript that creates updated maps dynamically.

"""


import os
import shutil
import io
import sys
import getpass
import time
import glob
import linecache
import random
#import arcpy

try:
    import PyPDF2
except IOError:
    print 'PyPDF2 is not installed.'
    raw_input('PyPDF must be installed before running.')
    _exit()

try:
    import termcolor
except IOError:
    print_error('Termcolor is not installed.')
try:
    import colorama
except IOError:
    print_error('Colorama is not installed.')

#  Import necessary modules from libraries
from arcpy import env
from PyPDF2 import PdfFileReader, PdfFileWriter
from termcolor import colored
from colorama import init
init()

__author__ = "Chris Martin"
__credits__ = ["Chris Martin", "Aaron Thielen", "Michael Moore"]
__version__ = "1.1"
__maintainer__ = "Chris Martin"
__email__ = "cmartin616@gmail.com"
__status__ = "Development"

        
#  Prints error message as red text (in shell)
def print_error(text):
    print colored(text, 'red')

#  Validates the type of a given variable
def type_validate(value, type_check):
    try:
        type_check(value)
        return True
    except ValueError:
        return False

#  Validates the input depending on provided arguments.
def input_validated(msg, is_valid, type_check = None):
    while True:
        ans = raw_input(msg).lower()

        if type_check:
            if not type_validate(ans, type_check):
                print_error('You must enter a valid integer. Try again.\n')
                continue

        if is_valid(ans):
            break
        else:
            print_error('That is not a valid answer. Try again.\n') 
    return ans

#  Verifies a directory exists.  If not, creates it.
def dir_check(directory, y = None):
    if not os.path.isdir(directory):
        os.makedirs(directory)
        print colored(directory + ' was created.', 'green')
    #  Optional argument for testing purposes/feedback.
    if y == 'y':
        print colored('Valid directory','green')

#  Verifies the file exists.
def file_check(value, y = None, mess = None):
    while True:
        validateDir = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\input')
        filetest = os.path.normpath(validateDir +'\\' + value + '.pdf')
        if not os.path.isfile(filetest):
            print_error('\nNot a valid file.  Please try again.')
            #  Optional argument to return a provided error message.
            if mess != None:
                print_error(mess)
            value = raw_input("\nInput file name: ")
            continue
        else:
            return value
            break
    #  Optional argument for testing purposes/feedback.
    if y == 'y':    
        print 'Valid file'

#  Interface with user to request input and output file names.
def ask_file_name(run, method = None, mess = None, directory = None):
    while True:
        if run == 'resize1' or run == 'split1':
            if method == 'input':
                filename = raw_input("\nInput file name: ")
                file_check(filename,'', 'The file name must be 8 characters.  Do not include .pdf.')
                return filename.upper()
            else:
                filename = raw_input("\nOutput file name: ")
                return filename.upper()
        elif run == 'resize2':
            if method == 'inputleft':
                filename = raw_input("\nInput left file name: ")
                return filename.upper()
            if method == 'inputright':
                filename = raw_input("\nInput right file name: ")
                return filename.upper()
            else:
                filename = raw_input("\nOutput file name: ")
                return filename.upper()

#  Custom exit function
def _exit():
    print_error('\nNow exiting the program...')
    time.sleep(1)
    print_error('Goodbye!')
    time.sleep(1)
    sys.exit()

#  Creates and/or edits PDF file.
def handle_file(filename):
    fIn1 = file(os.path.join(dir1, filename), 'rb')
    inp1 = PdfFileReader(fIn1)
    for i, p in enumerate(inp1.pages):
        output = PdfFileWriter()
        first_letter = filename[0].lower()
        new_filename, page_num = PAGE_MAPPING[(first_letter, i)]
        fileout = filename[1:-4] + new_filename
        page = inp1.getPage(page_num)
        print fileout, 'was created.'

        output.addPage(page)
        outputStream = file(os.path.join(user, dirIn, fileout),"wb")
        output.write(outputStream)
        outputStream.close()
    fIn1.close()

#  Reduces a single or two PDF files by half.
def resize_file(filename, filename2 = None):
    output = PdfFileWriter()

    fIn1 = file(os.path.join(inputDir,filename), 'rb')

    inp1 = PdfFileReader(fIn1)
    p1 = inp1.getPage(0)
    p1.scale(.5,.5)
    output.addPage(p1)
    
    if filename2 is not None:
        fIn2 = file(os.path.join(inputDir,filename2), 'rb')
        inp2 = PdfFileReader(fIn2)
        p2 = inp2.getPage(0)
        p2.scale(.50,.50)
        output.addPage(p2)

    outputStream = file(os.path.join(validateDir,str(fileout) + '.pdf'),"wb")
    output.write(outputStream)
    outputStream.close()
    fIn1.close()

#  Adds every PDF in a directory to a list
def get_all_pdfs(directory):
    pdfs = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            pdfs.append(filename)
    if not pdfs:
        print_error('No PDFs were found.')
    return pdfs

#  Verifies all PDFs have the proper naming convention
def check_pdf_names(pdfs):
    valid = []

    for i in pdfs:
        if i.endswith('.pdf'):
            if i[0].lower() == 'n' or i[0].lower() == 's':
                valid.append(i)
    if not valid:
        print_error('There are no PDFs in this directory that meet the proper naming convention.\n')
    return valid

#  Checks if library exists in Python directory.  If not, copies necessary files.
def configure_libs(lib):
    directory = os.path.normpath('C:\Python27\ArcGIS10.2\Lib'+lib)
    store = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\script\Libraries'+lib)
    if not os.path.isdir(directory):
        shutil.copytree(store,directory)
        print colored(directory + ' was created.', 'green')

#  Returns length (in lines) of input text file
def file_len(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#  Easter egg for coworker
def easter_egg_AT():
    quotelist = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\script\previous versions\solaire.txt')
    file_length = file_len(quotelist)
    num = random.randint(1,file_length)
    quote = linecache.getline(quotelist, num)
    user = os.environ.get('USERNAME')
    if user == 'aaron.thielen':
        print '\n\n'
        print_error(quote)

#  Hard coded server directories
user = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction')
inputDir = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\input')
backupDir = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\backup')
validateDir = os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\validate')

#Ensure libraries are in the proper location
configure_libs('\\PyPDF2-master')
configure_libs('\\termcolor-1.1.0')
configure_libs('\\colorama-0.2.7')

#Install libraries if not present?
#
#
#
#
#
#
#
#
#
#
#


#Default variable for looping the program in order to draw a line when beginning again.
count = 0

#Page mapping for file name creation wheos.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction')n splitting PDFs
PAGE_MAPPING = {
    ('n',0): ('1.pdf', 1),
    ('n',1): ('2.pdf', 0),
    ('s',0): ('3.pdf', 0),
    ('s',1): ('4.pdf', 1),
}

#Easter Egg for coworker
easter_egg_AT()

#Introductory statement
print colored('\n---------------------------------------------------------------------------', 'yellow')
print colored('\n             Welcome to the Ramsey County Section Map script.', 'yellow')

print colored('\n---------------------------------------------------------------------------\n', 'yellow')
print 'This script offers the several options of handling quarter and half section \n\
scanned PDFs.  Please make a selection when you are ready to begin. \n'

while True:
    
    if count >0:
        print '\n---------------------------------------------------------------------------\n'

    version = 'a'
    running = True

    #Version A is the simplified menu version
    while version == 'a':
        running = True
        simple = input_validated('Which of the following processes do you need? \n\n\
          a) Resize a quarter section\n\
          b) Create a new half section map (PDF)\n\
          c) Create a new quarter section map (PDF)\n\
          d) Complex Menu (old version, more options)\n\
          e) Exit the program\n\n\
        ....  ', lambda x: x in ('a', 'b', 'c', 'd', 'e', 'exit'))

        if simple.lower() == 'a':
            run = 'resize1'
            break
        elif simple.lower() == 'b':
            run = 'halfmap'
            break
        elif simple.lower() == 'c':
            run = 'quartermap'
            break
        elif simple.lower() == 'd':
            version = 'b'
            break
        else:
            run = 'exit'
            break

    #Version B is a more complex menu with alternate options
    while version == 'b':

        selection = input_validated('Which of the following processes do you need? \n\n\
          a) Resize quarter sections\n\
          b) Create a new section map (PDF)\n\
          c) Separate a 2-page PDF into individual documents\n\
          d) Change default directory\n\
          e) Backup Utility\n\
          f) Previous Menu (Simple Version)\n\
          g) Exit the program\n\n\
        ....  ', lambda x: x in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'exit'))


        if selection.lower() == 'a':
            proc = input_validated('\nWhich of the following resize operations do you need? \n\n\
          a) Resize and merge two quarter sections\n\
          b) Resize a single quarter section \n\
          c) Return to the previous menu\n\
        ....  ', lambda x: x in ('a', 'b', 'c'))
            if proc == 'a':
                run = 'resize2'
                break
            elif proc == 'b':
                run = 'resize1'
                break
            elif proc == 'c':
                run = 'previous'
                break

        elif selection.lower() == 'b':
            proc = input_validated('\nWhich of the following size maps do you need? \n\n\
          a) Create new quarter section PDF\n\
          b) Create a new half section PDF\n\
          c) Return to the previous menu\n\
        ....  ', lambda x: x in ('a', 'b', 'c'))
            if proc == 'a':
                run = 'quartermap'
                break
            elif proc == 'b':
                run = 'halfmap'
                break
            elif proc == 'c':
                run = 'previous'
                break

        elif selection.lower() == 'c':
            proc = input_validated('\nWhich of the following splitting operations do you need? \n\n\
          a) Split a single PDF\n\
          b) Split a directory of PDFs\n\
          c) Return to the previous menu\n\
        ....  ', lambda x: x in ('a', 'b', 'c'))
            if proc == 'a':
                run = 'split1'
                break
            elif proc == 'b':
                run = 'splitdir'
                break
            elif proc == 'c':
                run = 'previous'
                break
                
        elif selection.lower() == 'd':
            run = 'changedir'
            break

        elif selection.lower() == 'e':
            run = 'backup'
            break

        elif selection.lower() == 'f':
            version ='a'
            running = False
            break

        else:
            run = 'exit'
            break

    #Running is True by default but menu switching sets Running to False, so it returns to the beginning of the script.
    if running == True:
        
        #  Resize and merge two quarter sections
        if run == 'resize2':                 
            while True:
                
                file1 = ask_file_name('resize2', 'inputleft')
                file2 = ask_file_name('resize2', 'inputright')
                fileout = ask_file_name('resize2', 'output')

                dir1 = os.path.join(str(inputDir), str(file1) +'.pdf')
                dir2 = os.path.join(str(inputDir), str(file2) +'.pdf')         
                backup1 = os.path.join(str(backupDir), str(file1) + '.pdf')
                backup2 = os.path.join(str(backupDir), str(file2) + '.pdf')

                resize_file(dir1,dir2)

                print ""

                if file1 != '0000' and file2 != '0000':
                    shutil.move(dir1, backup1)
                    print dir1, "has been successfully moved to the backup folder.\n"
                    shutil.move(dir2, backup2)
                    print dir2, "has been successfully moved to the backup folder.\n"
                elif file1 == '0000':
                    shutil.move(dir2, backup2)
                    print dir2, "has been successfully moved to the backup folder.\n"
                elif file2 == '0000':
                    shutil.move(dir1, backup1)
                    print dir1, "has been successfully moved to the backup folder.\n"

        #  Resize a single quarter section
        elif run == 'resize1':

            file1 = ask_file_name('resize1', 'input', '', inputDir)
            fileout = ask_file_name('resize1', 'output')
            input1 = str(file1) + '.pdf'
            dir1 = os.path.join(inputDir, input1)
            backup1 = os.path.join(backupDir, str(file1) + '.pdf')

            resize_file(input1)

            try:
                shutil.move(dir1, backup1)
                print input1, "has been successfully moved to the backup folder.\n"
            except:
                print_error('\nThe PDF you entered is opened elsewhere.  The file was not backed up.')
                print "Please move your scanned PDF from /input to /backup or run the backup utility.\n\n  Press enter to continue  ....  "
                print raw_input('')
                continue     
            
                    
        #  Open the quarter section template
        elif run == 'quartermap':
            print "Opening the PDF.\n"
            os.startfile(os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\templates\template_quarter.pdf'))

            
        #  Opening the half section template
        elif run == 'halfmap':
            print "Opening the PDF.\n"
            os.startfile(os.path.normpath(r'\\isvfs4\rr\shared\valuation\mapping\HalfSectionMapsProduction\templates\template_half.pdf'))


        #  Splitting a document
        elif run == 'split1':
            file1 = raw_input("\nInput file name: ")
            dir1 = os.path.join(inputDir, str(file1) +'.pdf')
            backup1 = os.path.join(dir1,'backup/')
            handle_file(dir1)    
            shutil.move(dir1, backup1)
            print dir1, 'has been successfully moved to the backup folder.\n'


        #  Splitting a directory of documents
        elif run == 'splitdir':
            dirIn = raw_input("\nInput directory: ")
            dir1 = os.path.join(dirIn)
            pdfs = check_pdf_names(get_all_pdfs(dir1))
            
            backup1 = os.path.join(dir1,'backup/' )

            for filename in pdfs:
                handle_file(filename)
                dirOut = os.path.join(dir1, filename)
                shutil.move(dirOut, backup1)
                print filename, 'has been successfully moved to the backup folder.\n'

            if not pdfs:
                print '\nPress enter to return to the previous menu.'
                raw_input()
                run = 'previous'


        #  change default directory
        elif run == 'changedir':
            print '\nYour default directory:\n\n', user, '\n\nIf this is not correct, please press \'n\' to enter a new directory.\n\
    Otherwise, press enter to continue.\n\
      ....  '
            def_dir = raw_input()
            if def_dir.lower() == 'n':
                user = raw_input('Please enter a new default directory\n\  ....  ')
                print 'Your new default directory: \n',user,'\nPress enter to continue.\n\
      ....  '
                raw_input()

        #  executes custom exit function
        elif run == 'exit':
            _exit()

        #  returns to the previous menu
        elif run == 'previous':
            print '\n---------------------------------------------------------------------------\n'
            continue

        #  creates backup files of the input folder.  Used when in-function backup fails because file is open elsewhere.
        elif run == 'backup':
            for file in glob.glob(os.path.normpath(inputDir + '\*.pdf')):
                filestart = str(file).find('input\\')
                fileend = str(file).find('.pdf', filestart)
                result = str(file)[filestart+6:fileend]
                name = result + '.pdf'
                
                try:
                    shutil.move(file, backupDir)
                    print '\n', name, 'has been successfully moved to the backup folder.\n'
                except:
                    print '\n', name,'is opened elsewhere.  Please close the file and run the utility again.'
                    print raw_input('\nPress enter to contine  ....  ')
                    continue     

    count+=1


#Bugs:
#---------


#List of things to add:
#---------
# gui
# arcpy functionality?
