# coding:utf-8

import sys
import os
import chardet


outBasePath = '/Users/bms/workspace/download/'


def getCharsetAndConv(sourceDirs, encodeType = 'utf-8'):
    for root, dirs, files in os.walk(sourceDirs):
        for file in files:
            file_path = root + '/' + file
            f = open(file_path, 'r')
            data = f.read()
            f.close()

            encoding = chardet.detect(data)["encoding"]
            print "== ", file_path, "\n\tencoding: " , encoding
            if encoding not in ("UTF-8-SIG", "UTF-16LE", "utf-8", "ascii"):
                try:
                    gb_content = data.decode('gb18030')
                    gb_content.encode(encodeType)
                    with open(file_path, 'w') as f:
                        f.write(gb_content.encode(encodeType))
                except:
                    print "==== will remove except file: ", file_path
                    os.remove(file_path)


getCharsetAndConv(outBasePath + 'srt')