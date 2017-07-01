#!/usr/bin/python

import os

import sys
import subprocess
import getopt
from utils.PermissionInfo import PermissionInfo
from utils.PermissionParser import PermissionParser
from utils.ProtectionLevelParser import ProtectionLevelParser

from configs.Constant import Constant as configs

#DBUG config
DEBUG = False
DEFAULT_SDK = configs.getDefSdkLv()

def usage():
    print 'USAGE:\n'
    print sys.argv[0]+' [-h | --help]\n'
    print sys.argv[0]+' [-d] [-l]  [-g]  [-t <target-sdk>] -i <path-to-apk>'
    print '\t-d: list all the protection level decription'
    print '\t-l: list all permissions'
    print '\t-g: group the use-permission by protection level'
    print '\t-t <target-sdk>: set the codebase target-sdk'

def getPermsDict(sdk_lv):
    xml= configs.getRes(sdk_lv)
    if xml is None:
        xml = base.getRes(DEFAULT_SDK)
    parser = PermissionParser(xml)
    return parser.getPermList()

def printUnknownPerm(perm):
    print " Permission"
    print "   Name: "+perm
    print "   Group: unknown"
    print "   Protection Level: unknown"

def main(argv):
    targetApk = ''
    sdkLevel = DEFAULT_SDK #defaul use Android N (7.1.1)
    err = False;
    groupByLevel = False
    listLevelDesc = False
    listAllPerms = False

    #getopt Ref: https://docs.python.org/2/library/getopt.html
    try:
        opts, args = getopt.getopt(sys.argv[1:],'dlghi:t:', ["help"] )

        for opt, arg in opts:
            if (DEBUG == True):
                print opt+": "+arg
            if (opt == '-t'):
                sdkLevel = arg
            elif (opt in ("-h", "--help")):
                usage()
                sys.exit()
            elif (opt == '-g'):
                groupByLevel = True
            elif (opt == '-d'):
                listLevelDesc = True
            elif (opt == '-l'):
                listAllPerms = True
            elif (opt == '-i'):
                targetApk = arg
            else:
                assert False, "unhandled option"

        permParser = ProtectionLevelParser()
        levels = permParser.parsingProtectionLevels()
        if (listLevelDesc == True):
            for lv in levels:
                print lv+':'
                print '\tValue: '+permParser.getProtectionLevelValue(lv)
                print '\tDescription: '+permParser.getProtectionLevelDesc(lv)
                print '\n'

        permissionsDict = getPermsDict(sdkLevel)

        if (listAllPerms == True):
            for perm in permissionsDict.values():
                perm.dump()

        if (targetApk is ''):
            print "No target APK file path!"
            sys.exit(2)

        out = subprocess.check_output("./utils/unpackApk.sh "+targetApk, shell=True)
        usePerms = {}
        for perm in out.split('\n'):
            if (DEBUG == True):
                print perm
            permInfo = permissionsDict.get(perm)
            usePerms[perm] = permInfo

        print '\n============================================================='
        print 'Permission Status'
        print 'TARGET APK:'+targetApk
        print '=============================================================\n'

        if (groupByLevel != True):
            #output use-permissions list
            for perm in usePerms.keys():
                info = usePerms[perm]
                if info is not None:
                    info.dump()
                else:
                    printUnknownPerm(perm)
        else:
            permsGroupByLv = {}
            unknownPerms = []
            for lv in levels:
                perms = []
                for permName in usePerms.keys():
                    permInfo = usePerms[permName]
                    if permInfo is None:
                        if permName is not '' and permName not in unknownPerms:
                            unknownPerms.append(permName)
                    elif lv in permInfo.protectionLevel:
                        perms.append(permName)
                permsGroupByLv[lv] = perms
            permsGroupByLv['unknown'] = unknownPerms

            #result output
            for level, perms in permsGroupByLv.items():
                if len(perms) is 0:
                    continue
                print "\n* "+level+" permissions:"
                for perm in perms:
                    if (level is 'unknown'):
                        printUnknownPerm(perm)
                    else:
                        usePerms[perm].dump()

    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

if __name__ == '__main__':
    if (DEBUG == True):
        print sys.argv
    if (len(sys.argv) < 2):
        usage()
    else:
        main(sys.argv)
