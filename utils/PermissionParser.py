#!/usr/bin/python

import os
import urllib, urllib2

from bs4 import BeautifulSoup
from PermissionInfo import PermissionInfo

#DBUG config
DEBUG = False

class PermissionParser:

    mTargetUrl = ''
    mPermGroups = []

    def __init__(self, xmlUrl):
        self.mTargetUrl = xmlUrl

    def getPermList(self):
        print('Get Permission List from '+self.mTargetUrl)
        fileHandler = urllib2.urlopen(self.mTargetUrl).read().decode('utf-8')
        soup = BeautifulSoup(fileHandler, "xml")
        permList = {}
        for p in soup.findAll('permission'):
            name = p['android:name']
            group = p.get('android:permissionGroup')
            if ((group is not None) and (group not in self.mPermGroups)):
                self.mPermGroups.append(group)                
            protection = p['android:protectionLevel']
            pInfo = PermissionInfo(name, group, protection)
            permList[name] = pInfo
            if DEBUG is True:
                print p
                print p.attrs
                pInfo.dump()
        return permList

def test():
    DEF_URL="https://raw.githubusercontent.com/android/platform_frameworks_base/master/core/res/AndroidManifest.xml"
    permsParser = PermissionParser(DEF_URL)
    permList = permsParser.getPermList()
    # print out all the permissions info
    for perm in permList.values():
        perm.dump()
        print "------"
    print "permissions#: %d\n" % len(permList)
    for permGroup in permsParser.mPermGroups:
        print permGroup
    print "permission groups #: %d\n" % len(permsParser.mPermGroups)
if __name__ == '__main__':
    test()
