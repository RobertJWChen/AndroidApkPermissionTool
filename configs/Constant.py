#!/usr/bin/python

class Constant:
    @staticmethod
    def getDefSdkLv():
        return '26'

    @staticmethod
    def getRes(lv):
        SDK={
            '26':'https://raw.githubusercontent.com/android/platform_frameworks_base/oreo-dev/core/res/AndroidManifest.xml',
            '25':'https://raw.githubusercontent.com/android/platform_frameworks_base/nougat-mr1-dev/core/res/AndroidManifest.xml',
            '24':'https://raw.githubusercontent.com/android/platform_frameworks_base/nougat-dev/core/res/AndroidManifest.xml',
            '23':'https://raw.githubusercontent.com/android/platform_frameworks_base/marshmallow-dev/core/res/AndroidManifest.xml',
            '22':'https://raw.githubusercontent.com/android/platform_frameworks_base/lollipop-mr1-dev/core/res/AndroidManifest.xml',
            '19':'https://raw.githubusercontent.com/android/platform_frameworks_base/kitkat-dev/core/res/AndroidManifest.xml'
        }
        return SDK.get(lv)
