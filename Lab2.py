#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import sys
import os
from pathlib import Path
import json, subprocess

class iodir:
    inp : str
    outp : str
    files : list
    def __init__(self,inp,outp,files):
        self.inp=inp
        self.outp=outp
        self.files=files # indexed files

#Define directories   
def setDir():
    name = "BBB.mp4"
    path =  Path.cwd() / "Data"#set path to Data folder
    #for each file in folder get input path (BBB.mp4)
    file_path= [ subp for subp in path.iterdir() if subp.match(name)]
    file_path.sort()
    files = [i for i in os.listdir(path) if i != '.DS_Store' and i != '.vscode' ]  # avoid random files
    files = [(s + 1, i) for (s, i) in enumerate(files)]#Make a enumerated list of the files in the folder
    return iodir(str(file_path[0]),path,files)

#Refresh list of files that can be updated due to one of the exercices
def refresh():
    files = [i for i in os.listdir(dyr.outp) if i != '.DS_Store' and i != '.vscode' ]  # ignore random files
    dyr.files = [(s + 1, i) for (s, i) in enumerate(files)]
    return("Done")

#print avaiable files in the folder
def print_files():
    refresh()
    for file in dyr.files:
            print('{} - {}'.format(file[0], file[1]))
    
#Split name and extension of a filename
def check_ext_name(name):
    split = name.split('.')
    #Check if there is extension
    if(len(split) > 1):
        file_extension = split.pop()
    else:
        file_extension = None

    return split[0],file_extension

#transcode command implementation
def ext_change(old,new):
    command = "ffmpeg -i {} -c:v libx264 -crf 18 -preset veryslow -c:a copy {}".format(old, new)
    os.system(command)

#Exercice 1
def one():
    options = ['duration','width','height','nb_frames','bit_rate','all']
    x = int(input(" What do you want to know about the input video?\n 0 - duration\n 1 - width\n 2 - height\n 3 - nb_frames\n 4 - bitrate\n 5 - all\n"))
    #If user wants to know all about the video we print in terminal json format of all data specs
    #If user wants to know an specific information of the video we only show it.
    if x == 5:
        command = "ffprobe -v quiet -print_format json -show_format -show_data -show_streams {}".format(
        dyr.inp)
        os.system(command)
    else:    
        command = "ffprobe -v error -select_streams v:0 -show_entries stream={} -of csv=s=x:p=0 {}".format(options[x], dyr.inp)
        #save output command into a variable
        out = subprocess.Popen(command.split(' '),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        print("The {} of the video is {}".format(options[x], str(stdout)))
    return "Done"

#Exercice 2
def two():
    print_files()
    x = int(input("Which file you want to rename?\n"))
    if x > len(dyr.files) or x < 1:#Check if user choise is valid or not
            print('This file does not exist in this folder.\n')
    else:
        name = str(input("Enter the new file name:\n"))
        name, ext = check_ext_name(name)#get name and extension from the user input
        old_file = list(dyr.files[x-1]).pop()#get filename to rename
        old_name, old_ext = check_ext_name(old_file)#get extension of user choise

        #If the user has entered an extension(either equal or new)
        if (old_ext!=ext and ext): 
            check = str(input("Are you sure about changing the extension? [y/n]\n"))
            if(check == 'y'):#If user wants to change the extension we transcode the file
                new_filename= dyr.outp / "{}.{}".format(name,ext)
                ext_change(dyr.outp / old_file,new_filename)
                remove = str(input("Do you want to remove the previous named file? [y/n]\n"))
                if (remove == 'y'): os.remove(dyr.outp /old_file)
            else:
                new_filename= dyr.outp / "{}.{}".format(name,old_ext)
                os.rename(dyr.outp/old_file,new_filename)
                
        else:
            new_filename= dyr.outp / "{}.{}".format(name,old_ext)
            os.rename(dyr.outp/old_file,new_filename)
    return

#Exercice 3
def three():
    print_files()
    x = int(input("Choose a file to change its resolution:\n"))
    if x > len(dyr.files) or x < 1:
            print('This file does not exist in this folder.\n')
    else:
        #get name and extension of the chosen file
        filename = list(dyr.files[x-1]).pop()
        name, ext = check_ext_name(filename)
        new_dim= str(input("Enter new resolution:\n"))
        #Check the format used by the user 
        new_dim = new_dim.split('x')
        #480p,720p dimensions format
        if len(new_dim) == 1:
            #ensure that the value is only numeric
            new_dim = new_dim[0].split('p')
            scale = "{}:-2".format(new_dim[0])
            command = "ffmpeg -i Data/{} -vf scale={} -c:v libx264 -crf 18 -preset veryslow -c:a copy Data/{}_{}.{}".format(
                    filename, scale, name, new_dim[0],ext)
            os.system(command)
        #160x480 dimensions format
        elif len(new_dim) == 2:
            scale = "{}:{}".format(new_dim[0],new_dim[1])
            command = "ffmpeg -i Data/{} -vf scale={} -c:v libx264 -crf 18 -preset veryslow -c:a copy Data/{}{}_{}.{}".format(
                filename, scale, name,new_dim[0],new_dim[1],ext)
            os.system(command)
        else:
            print("Non valid resolution\n")
    return

#Exercice 4
def four():
    print_files()
    x = int(input("Choose a file to transcode :\n"))
    if x > len(dyr.files) or x < 1:
            print('This file does not exist in this folder.\n')
    else:
        filename = list(dyr.files[x-1]).pop()#get filename of user choise
        name, ext = check_ext_name(filename)#get name and extension of user choise
        new_ext = str(input("Enter new extension:"))
        #Since we dont know if user will enter it as .jpg or as jpg we avoid errors by:
        new_ext=new_ext.split('.')[1]
        new_filename = name + '.' + str(new_ext)
        ext_change(dyr.outp/filename,dyr.outp /new_filename )
    return

def execall(argument):
    # Get the function from switcher dictionary
    func = switcher.get(argument, "nothing")
    # Execute the function
    return func()

switcher = {
        1: one,
        2: two,
        3: three,
        4: four
}

if __name__ == "__main__": 
    dyr=setDir()#set directories
    x = input("[1]Get video Information\n[2]Rename\n[3]Resize the video\n[4]Change codec\n")
    while not x=='5':
         execall(int(x))
         x = input("[1]Get video Information\n[2]Rename\n[3]Change Resolution\n[4]Change codec\n[5]Exit\n")
   