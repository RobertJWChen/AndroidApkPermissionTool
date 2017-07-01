#!/usr/bin/python

class PermissionInfo:
    #permName
    #permGroup
    #protectionLevel
    def __init__(self, permName, permGroup, protectionLevel):
        self.permName = permName
        if (permGroup is None):
            self.permGroup = ''
        else:
            self.permGroup = permGroup
        self.protectionLevel = protectionLevel

    def dump(self):
        print " Permission"
        print "   Name: "+self.permName
        print "   Group: "+self.permGroup
        print "   Protection Level: "+self.protectionLevel
        

if __name__ == '__main__':
    permInfo = PermissionInfo('com.perm.test1', 'com.perm.testgroup1', 'normal');
    permInfo.dump()
