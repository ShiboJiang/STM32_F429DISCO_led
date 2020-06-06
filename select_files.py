#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Function   : This scrip is used for selecting *.c *.h *.cpp *.s files
# Enviroment : python 3.6.2
# Author     : Shibo Jiang
# Time       : 2017.11.13
# Version    : 0.3
# Notes      : None
#------------------------------------------------------------------------------
import os
import shutil

#creat folder named 'select_result' to store select results
target_floder = 'select_result'
abs_path = os.path.join(os.path.abspath('.'), target_floder)

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
if (os.path.split(abs_path))[1] in os.listdir(os.path.abspath('.')):
    shutil.rmtree(abs_path)

#search files function
def find_files(path, search, default_result, exclude = None):
    for x_path in os.listdir(path):
        if x_path != exclude:
            x_path = os.path.join(path, x_path)
            if os.path.isdir(x_path):
                find_files(x_path, search, default_result, exclude = None)
            elif (os.path.splitext(x_path)[1]).lower() == search:
                default_result.append(x_path)

#find .h files and store the path in a list
h_files = ['0']
find_files(os.path.abspath('.'), '.h', h_files)

#find .c files and store the path in a list
c_files = ['0']
find_files(os.path.abspath('.'), '.c', c_files)

#find .cpp files and store the path in a list
cpp_files = ['0']
find_files(os.path.abspath('.'), '.cpp', cpp_files)

#find .s files and store the path in a list
s_files = ['0']
find_files(os.path.abspath('.'), '.s', s_files)

#creat new folder in select_result
os.mkdir(abs_path)

# toal 4 floders needed created
new_dir = [0, 0, 0, 0]
C = 0
H = 1
CPP = 2
S = 3

new_dir[C] = os.path.join(abs_path, 'files_c')
new_dir[H] = os.path.join(abs_path, 'files_h')
new_dir[CPP] = os.path.join(abs_path, 'files_cpp')
new_dir[S] = os.path.join(abs_path, 'files_s')

for i in range(len(new_dir)):
    os.mkdir(new_dir[i])

repeat_name_file = []       
#copy .h files to the folder named files_h
if len(h_files) > 1:
    for x_file in h_files[1:]:
        if (os.path.split(x_file))[1] in os.listdir(new_dir[H]):
            repeat_name_file.append(x_file)
        else:
            shutil.copy(x_file, new_dir[H])

#copy .c files to the folder named files_c
if len(c_files) > 1:
    for x_file in c_files[1:]:
        if (os.path.split(x_file))[1] in os.listdir(new_dir[C]):
            repeat_name_file.append(x_file)
        else:
            shutil.copy(x_file, new_dir[C])

#copy .cpp files to the folder named files_cpp
if len(cpp_files) > 1:
    for x_file in cpp_files[1:]:
        if (os.path.split(x_file))[1] in os.listdir(new_dir[CPP]):
            repeat_name_file.append(x_file)
        else:
            shutil.copy(x_file, new_dir[CPP])

#copy .s files to the folder named files_s
if len(s_files) > 1:
    for x_file in s_files[1:]:
        if (os.path.split(x_file))[1] in os.listdir(new_dir[S]):
            repeat_name_file.append(x_file)
        else:
            shutil.copy(x_file, new_dir[S])


#write sourcefiles name to file with makefile fromate
def write_src_name(path, file, src_path):
    target_file =os.path.join(path, file)
    src_files = os.listdir(src_path)
    with open(target_file, 'w', encoding='utf-8') as f:
        for file_name in src_files:
            f.write('$(TOP)\\' 
            + os.path.split(path)[1] + '\\' 
            + os.path.split(src_path)[1] + '\\'
            + file_name + '   ' + '\\' + '\n')

#store the name to a file
src_file = 'src.txt'
write_src_name(abs_path, src_file, new_dir[C])

#report files need rename
if len(repeat_name_file) > 0:
    print('These files have duplicate names and are not \
copied to result floder.- \n' + str(repeat_name_file))

#-End of file------------------------------------------------------------------
# change test