#!/usr/bin/python

import os
import urllib, urllib2

from bs4 import BeautifulSoup
from PermissionInfo import PermissionInfo

#DBUG config
DEBUG = False

class ProtectionLevelParser:

    mTargetPath = 'https://developer.android.com/reference/android/R.attr.html#protectionLevel'
    mProtectionLevelVal = {}
    mProtectionLevelDesc = {}

    def parsingProtectionLevels(self):
        print('Get Permission Protection Level List from '+self.mTargetPath)
        req = urllib2.urlopen(self.mTargetPath)
        soup = BeautifulSoup(req.read().decode('utf-8'), "html.parser")
        divs = soup.find_all('div', {'class':'api apilevel-1', 'id':None})
        for div in divs:
            titles = div.find_all('h3', 'api-name')
            targetDivFound = False
            for title in titles:
                if (title.string == 'protectionLevel'):
                    targetFound = True
                    rows = div.find_all('tr')
                    for row in rows[1:]:
                    #roll out the the table title row
                        cols = row.find_all('td')
                        levelName = cols[0].string
                        levelVal =  cols[1].string
                        levelDesc = ''
                        if cols[2].string is None:
                            for content in cols[2].contents:
                                levelDesc += content.string
                        else:
                            levelDesc = cols[2].string
                        self.mProtectionLevelVal[levelName] = levelVal
                        self.mProtectionLevelDesc[levelName] = levelDesc.replace('\n','')
                    break
            if targetDivFound is True:
                break
        # return the whole protection level list
        return self.mProtectionLevelVal.keys()

    def getProtectionLevelValue(self, name):
        return self.mProtectionLevelVal[name]

    def getProtectionLevelDesc(self, name):
        return self.mProtectionLevelDesc[name]

def test():
    permsProtLvParser = ProtectionLevelParser()
    protectLevels = permsProtLvParser.parsingProtectionLevels()
    print 'TOTAL %d protection level definitions' % len(protectLevels)
    for level in protectLevels:
        print level+':'
        print '\tValue: '+permsProtLvParser.getProtectionLevelValue(level)
        print '\tDescription: '+permsProtLvParser.getProtectionLevelDesc(level)
        print '\n'

if __name__ == '__main__':
    test()
