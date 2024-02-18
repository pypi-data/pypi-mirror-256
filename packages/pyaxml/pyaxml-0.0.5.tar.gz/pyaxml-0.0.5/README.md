# README


## GENERAL INFO


  Project: Library to modify AXML file  
  Author: Benoît Forgette alias MadSquirrel  
  License: GNU General Public License v3.0 and later  
  Version: v1.0  
  Date: 12-08-23  

## GOAL

  PyAxml is a full python tool to play with AXML (Android XML) files.
  This tool is useful to decode and encode AXML files and manipulate AXML files
  over a [Protocol Buffers](https://protobuf.dev/) object.
  It is designed to work with Python 3 only.
  Some examples of the use of the tool is provided with the project:
  - copymanifest.py that allow to decode and reencode the original file
  - replace_activity_name.py to change the name an activity and replace by an
  other
  
  If you want to see more example you can dig more on the project
  [apkpatcher](https://gitlab.com/MadSquirrels/mobile/apkpatcher) that use this
  library to add some useful permission and inject a library inside the target
  application.

  To have a better understanding about how is composed the AXML format a
  graphic is associated in drawio and svg format: format.drawio, format.drawio.svg

## USAGE

  You can use 2 samples:
  ```shell
  $ python examples/copymanifest.py code/tata2.xml test.xml
  ```
  to simply copy the AXML file to test.xml with reencoding
  
  The second sample can replace the name of an activity inside an
  AndroidManifest.xml:

  ```shell
  $ androaxml.py code/tata2.xml
    <manifest xmlns:android="http://schemas.android.com/apk/res/android" compileSdkVersion="30" compileSdkVersionCodename="11" package="exploit.intent" platformBuildVersionCode="30" platformBuildVersionName="11">
      <application>
        <activity android:name="app.activity"/>
      </application>
    </manifest>
  $ python examples/replace_activity_name.py code/tata2.xml test.xml app.activity app.test
  $ androaxml.py test.xml 
    <manifest xmlns:android="http://schemas.android.com/apk/res/android" compileSdkVersion="30" compileSdkVersionCodename="11" package="exploit.intent" platformBuildVersionCode="30" platformBuildVersionName="11">
      <application>
        <activity android:name="app.test"/>
      </application>
    </manifest>
  ```

## CHANGELOG

