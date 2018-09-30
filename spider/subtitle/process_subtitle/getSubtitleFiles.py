# coding:utf-8

import sys
import fnmatch
import os
import shutil
import zipfile

outBasePath = '/Users/bms/workspace/download/'
global cnt_i

def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)


def getFilesByType(inputPath, fileType):
    outPath = outBasePath + fileType
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    for filename in iterfindfiles(inputPath, "*." + fileType):
        global cnt_i
        cnt_i = cnt_i+1
        # newfilename = outPath + "/" + str(cnt_i) + "_" + os.path.basename(filename).replace(' ', '_')
        newfilename = outPath + "/" + str(cnt_i) + "_" + str(hash(os.path.basename(filename))) + '.' + fileType
        # print filename + "<===>" + newfilename
        shutil.move(filename, newfilename)
        if "rar" == fileType:
            os.system('cd ' + outPath + ' && unrar -Y x ' + newfilename)
        elif "zip" == fileType:
            # file_zip = zipfile.ZipFile(newfilename, 'r')
            # file_zip.extractall(outPath + "/" + str(cnt_i) + "_" + os.path.basename(filename))
            # file_zip.close()
            os.system('cd ' + outPath + ' && unzip -o -q ' + newfilename)

cnt_i = 0
getFilesByType(outBasePath + 'result', "rar")
getFilesByType(outBasePath + 'result', "zip")

cnt_i = 0
getFilesByType(outBasePath + 'rar', "srt")
getFilesByType(outBasePath + 'zip', "srt")

shutil.rmtree(outBasePath + 'result')
shutil.rmtree(outBasePath + 'rar')
shutil.rmtree(outBasePath + 'zip')

