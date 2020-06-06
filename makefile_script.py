#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Name       : makefile_script
# Function   : This scrip is used for makefile
# Enviroment : python 3.6.2
# Author     : Shibo Jiang
# Time       : 2017.11.17
# Version    : 0.1
# Notes      : None
#------------------------------------------------------------------------------
import os
import shutil
import time

global TARGET_FLODER
global ABS_PATH
global OS_SYSTEM
# config parameter
TARGET_FLODER = 'build_result'
ABS_PATH = os.path.join(os.path.abspath('.'), TARGET_FLODER)
OS_SYSTEM = 'windows'

#------------------------------------------------------------------------------
# Name     : CreatResultFolder
# Function : Used to creat bulid folder
# Input    :
# Output   :
# Notes    :
#--------------------------Function start--------------------------------------
def CreatResultFolder():
    # toal 4 floders needed created
    new_dir = [0, 0, 0, 0]
    C = 0
    H = 1
    CPP = 2
    S = 3

    new_dir[C] = os.path.join(ABS_PATH, 'files_c')
    new_dir[H] = os.path.join(ABS_PATH, 'files_h')
    new_dir[CPP] = os.path.join(ABS_PATH, 'files_cpp')
    new_dir[S] = os.path.join(ABS_PATH, 'files_s')

    #creat new folder in select_result
    if (os.path.split(ABS_PATH))[1] in os.listdir(os.path.abspath('.')):
        print('The folder ' + TARGET_FLODER
            + 'is exited, so not creating it.')
        for i in range(len(new_dir)):
            if (os.path.split(new_dir[i]))[1] in \
                        os.listdir(os.path.abspath(TARGET_FLODER)):
                print('The folder ' + (os.path.split(new_dir[i]))[1] 
                    + 'is exited, so not creating it.')
            else:
                os.mkdir(new_dir[i])
    else:
        os.mkdir(ABS_PATH)
        for i in range(len(new_dir)):
            os.mkdir(new_dir[i])
#--------------------------End of function-------------------------------------

#------------------------------------------------------------------------------
# Name     : SelectFiles
# Function : Used for selecting *.c *.h *.cpp *.s files
# Input    :
# Output   :
# Notes    :
#--------------------------Function start--------------------------------------
def SelectFiles():
    # judge os system
    global SEPARATOR
    if 'windows' == OS_SYSTEM:
        SEPARATOR = '\\'
    elif 'linux' == OS_SYSTEM:
        SEPARATOR = '/' 

    # #judge whether folder is exist,and creat a stand folder
    # folder_number = 0
    # temp_path = abs_path
    # exclude_path = [abs_path]
    # while 1:
    #     if (os.path.split(abs_path))[1] in os.listdir(os.path.abspath('.')):
    #         folder_number = folder_number + 1
    #         abs_path = temp_path + '_' + str(folder_number)
    #         exclude_path.append(abs_path)
    #     else:
    #         break

    #delete older folder and creat new
    # if (os.path.split(ABS_PATH))[1] in os.listdir(os.path.abspath('.')):
    #     shutil.rmtree(ABS_PATH)

    #search files function
    def FindFiles(path, search, default_result, exclude = None):
        for x_path in os.listdir(path):
            if x_path != exclude:
                x_path = os.path.join(path, x_path)
                if os.path.isdir(x_path):
                    FindFiles(x_path, search, default_result, exclude = None)
                elif (os.path.splitext(x_path)[1]).lower() == search:
                    default_result.append(x_path)

    #find .h files and store the path in a list
    H_FILES = ['0']
    FindFiles(os.path.abspath('.'), '.h', H_FILES, TARGET_FLODER)
    #find .c files and store the path in a list
    C_FILES = ['0']
    FindFiles(os.path.abspath('.'), '.c', C_FILES, TARGET_FLODER)
    #find .cpp files and store the path in a list
    CPP_FILES = ['0']
    FindFiles(os.path.abspath('.'), '.cpp', CPP_FILES, TARGET_FLODER)
    #find .s files and store the path in a list
    S_FILES = ['0']
    FindFiles(os.path.abspath('.'), '.s', S_FILES, TARGET_FLODER)

    # toal 4 floders needed created
    new_dir = [0, 0, 0, 0]
    C = 0
    H = 1
    CPP = 2
    S = 3

    new_dir[C] = os.path.join(ABS_PATH, 'files_c')
    new_dir[H] = os.path.join(ABS_PATH, 'files_h')
    new_dir[CPP] = os.path.join(ABS_PATH, 'files_cpp')
    new_dir[S] = os.path.join(ABS_PATH, 'files_s')

    #creat new folder in select_result
    if (os.path.split(ABS_PATH))[1] in os.listdir(os.path.abspath('.')):
        pass
    else:
        os.mkdir(ABS_PATH)
        for i in range(len(new_dir)):
            os.mkdir(new_dir[i])

    #function copy files to folder
    repeat_name_file = []
    modify_file = []
    def CopyFiles(src, target, repeat_report, modify_report):
        src_file_name = ['0']
        if len(src) > 1:
            for x_file in src:
                # judge whether files is repeat
                if os.path.split(x_file)[1] in src_file_name:
                    repeat_report.append(x_file)
                else:
                    src_file_name.append(os.path.split(x_file)[1])
                    # judge whether files modified before copy files
                    if (os.path.split(x_file))[1] in os.listdir(target):
                        temp_file = os.path.join(target, \
                                    os.path.split(x_file)[1])
                        time1 = time.ctime(os.stat(x_file).st_mtime)
                        time2 = time.ctime(os.stat(temp_file).st_mtime)
                        if time1 != time2:
                            modify_report.append(x_file)
                            shutil.copy2(x_file, target)
                    else:
                        shutil.copy2(x_file, target)

    #copy .h files to the folder named files_h
    CopyFiles(H_FILES[1:], new_dir[H], repeat_name_file, modify_file)
    #copy .c files to the folder named files_c
    CopyFiles(C_FILES[1:], new_dir[C], repeat_name_file, modify_file)
    #copy .cpp files to the folder named files_cpp
    CopyFiles(CPP_FILES[1:], new_dir[CPP], repeat_name_file, modify_file)
    #copy .s files to the folder named files_s
    CopyFiles(S_FILES[1:], new_dir[S], repeat_name_file, modify_file)

    #write sourcefiles name to file with makefile fromate
    def WriteSrcName(path, file, src_files):
        target_file =os.path.join(path, file)
        #src_files = os.listdir(src_path)
        with open(target_file, 'w', encoding='utf-8') as f:
            for file_name in src_files:
                f.write('$(TOP)' + SEPARATOR
                + file_name + '\n')
                # + os.path.split(path)[1] + SEPARATOR 
                # + os.path.split(src_path)[1] + SEPARATOR
                # + file_name + '   ' + SEPARATOR + '\n')

    #store the name to a file
    C_LIST   = 'c_list.txt'
    H_LIST   = 'h_list.txt'
    CPP_LIST = 'cpp_list.txt'
    S_LIST   = 's_list.txt'
    WriteSrcName(ABS_PATH, C_LIST, C_FILES[1:])
    WriteSrcName(ABS_PATH, H_LIST, H_FILES[1:])
    WriteSrcName(ABS_PATH, CPP_LIST, CPP_FILES[1:])
    WriteSrcName(ABS_PATH, S_LIST, S_FILES[1:])

    #report
    if len(repeat_name_file) > 0:
        print('Error!!!\n  These files have duplicate names \
    and are not copied to result floder,please handle it.\n \
    Make will stop until this error is fixed! - \n')
        if type(repeat_name_file).__name__ == 'list':
            for x_file in repeat_name_file:
                print(x_file)
        else:
            print(repeat_name_file)
    if len(modify_file) > 0:
        print('These files are modified and have \
    copied to result floder.- \n')
        if type(repeat_name_file).__name__ == 'list':
            for x_file in modify_file:
                print(x_file)
        else:
            print(modify_file)
#--------------------------End of function-------------------------------------

#------------------------------------------------------------------------------
# Name     : DeleteResult
# Function : Used to creat bulid folder
# Input    :
# Output   :
# Notes    :
#--------------------------Function start--------------------------------------
def DeleteResult():
    #delete older folder and creat new
    if (os.path.split(ABS_PATH))[1] in os.listdir(os.path.abspath('.')):
        shutil.rmtree(ABS_PATH)
    else:
        print('No ' + TARGET_FLODER + ' folder exited.')
#--------------------------End of function-------------------------------------

# First creat bulid folder
CreatResultFolder()
# Then copy source files to build folder
SelectFiles()


#-End of file------------------------------------------------------------------