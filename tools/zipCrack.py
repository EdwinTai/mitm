#!/usr/bin/python
# -*- coding: utf-8 -*-
import zipfile
import optparse
from threading import Thread


def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password.encode('ascii')) #這個地方要加encode，否則會出錯
        print('[+] Found password ' + password + '\n')
    except Exception as e:#加上列印exception，否則完全不知道為什麼密碼明明是對的，也不會顯示
      #print(e)
      pass


def main():
    parser = optparse.OptionParser("usage python zipCrack.py "+\
      "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',\
      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
      help='specify dictionary file')
    (options, args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        #print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()


if __name__ == '__main__':
    main()