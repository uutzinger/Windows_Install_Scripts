# Missing DLL

Once you build more complex python packages, the two main issues you will need to solve is 
* to find appropriate binaries and packages to include into your build and reference the appropraite directories and lib(s) 
* to make sure the dll dependencies that those packages need are met in your search path.

Although packages build the dlls they needs, the support libraries those packages depend on have their own externa dll dependencies. 

Sometimes your build loads with python 2 and not with python 3. 

There are a few ways trying to identify which dll is missing and preventing your package from loading. 

## LucasG Dependencies
Download the distribution files from https://github.com/lucasg/Dependencies and load the dlls, e.g. opencv_worldxxx.dll and examine the dependencies.

Apparently the following dlls dependency errors can be ignroed:
Recommended ignore dll missing list:
* API-MS-WIN-*.dll
* EXT-MS-WIN-*.dll
* IESHIMS.dll
* EMCLIENT.dll
* DEVICELOCKHELPERS.dll
* EFSCORE.DLL
* WPAXHOLDER.DLL

## Dependency Walker
A similar program to Dependencies is available at https://www.dependencywalker.com/. Its more than 10 years old.

## dumpbin
Dumpbin is part of Visual Studio Compiler installation.
If its not automatically found you will need to execute visual studio script in your command shell:
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
```

To find the dll s that your package uses you can can execute the following:
```
dumpbin C:\Python38\Lib\site-packages\cv2\python-3.8\cv2.cp38-win_amd64.pyd /IMPORTS | findstr dll
```
This lists all dlls your build is attempting to open. Make sure each dll listed is found in your CMD windows with:
```
where dllname_from_previous_output
```
This approach can take significant time, and is not guaranteed to find the culprit. 
You can automate this approachby piping the output ofthe first command to file ```dumbin ... > missing.bat``` Then edit missing.bat and add ```where ``` infront of each line. Then you can run missing.bat and it will let you know where an error occurs.

## procmon
[Procmon](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon) allows to monitor Windows file system activity.
I start python and procmon and stop procmon from monitoring. I clear its output. Then I start monitoring and type ```import package```  in python. 
As soon as the error appears I stop monitoring. Then I use find tool in procmon to locate python activity e.g. 
Find python.exe. I attempt to find the last python activity and then step backwards by locating activity that did not result in 
SUCCESS. There are many such activities. I can not say exactly how to navigate the FILE NOT FOUND or BUFFER OVERLOW activities 
to identify which ones caused the package to fail. The one that breaks your installation could be listed under an other task 
than python.exe as it could be a sub-component failing to load its dlls. The more components you activate in your build, 
the more such components can cause a fail.

## sys.path
In python run
```
import sys
sys.path
sys.path.append('C:\\opencv\\opencv_redist')
sys.path.append('C:\\gstreamer\\1.0\\x86_64\\bin')
sys.path.remove('C:\\Python38\\python38.zip')
```

## Cleaning a Previous Build
You can clean the build configurtion in cmake-gui by clearing the cache (Menu item). 
You can also clean previous builds by deleting the content of the build directory. 
If you modify the build with cmake or cmake-gui, it appears that only the necessary modules are rebuilt. 
If you can not complete an incremental build, start disabling features and when that does not help, 
you might need to clear the cache or start from scratch by deleting the build folder.

When you use
```
"C:\Program Files\CMake\bin\cmake.exe" --build C:\opencv\opencv\build --target install
```

the --target options of interest are 
```
install
uninstall
clean
help
```
