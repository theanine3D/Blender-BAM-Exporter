# Blender-BAM-Exporter
Blender addon for exporting Panda3D "BAM" files.

## Installation
To install the addon into Blender, press the green "Code" button above and choose Download ZIP. The resulting ZIP file can be installed via the Install button in the Blender addon preferences.

## Setup
This addon is a wrapper for the "[blend2bam](https://github.com/Moguri/blend2bam)" CLI tool. You must first install that tool via the same Python installation you're using with Panda3D. After installing blend2bam with pip, you must then open the Blender addon preferences and add the full absolute path to the Panda3D Python executable.

If you installed Panda3D via the SDK, the path will likely be somewhere in C:\Panda3D-x.xx.xx-x64\python (at least on Windows)
If using the Anaconda distribution of Python, look in C:\ProgramData\Anaconda (on Windows)

![image](https://user-images.githubusercontent.com/88953117/234090186-fd363cbc-f718-463a-8519-b8455dda9150.png)
