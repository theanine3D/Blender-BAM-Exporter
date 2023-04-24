# Blender-BAM-Exporter
Blender addon for exporting Panda3D "BAM" files. For Blender 3.0 and higher. Not related to the [older addon](https://github.com/tobspr/Panda3D-Bam-Exporter) for Blender 2.7x.

![image](https://user-images.githubusercontent.com/88953117/234097061-e53c0eca-93bf-4ee5-bf7d-9b55262ab46b.png)

## Installation
To install the addon into Blender, press the green "Code" button above and choose Download ZIP. The resulting ZIP file can be installed via the Install button in the Blender addon preferences.

## Setup
This addon is a wrapper for the "[blend2bam](https://github.com/Moguri/blend2bam)" CLI tool. You must first install that tool with pip in the same Python installation you're using with Panda3D. After installing blend2bam with pip, you must then open the Blender addon preferences and add the full absolute path to the Panda3D Python executable.

![image](https://user-images.githubusercontent.com/88953117/234090186-fd363cbc-f718-463a-8519-b8455dda9150.png)

If you installed Python via the Panda3D SDK, the path will likely be somewhere in C:\Panda3D-x.xx.xx-x64\python (at least on Windows)

If using the Anaconda distribution of Python, look in your C:\ProgramData\anaconda folder (on Windows)

## Known Issues
The "Selected Only" export option currently has no effect, as the feature still needs more testing.
