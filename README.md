# Apple Music Preview Installer
This is a quick script I hacked together to make it easier to install and update Apple Music Preview on Windows 10

# Building
You can either run it as a python file using python main.py, or you can build it into an exe file using PyInstaller.

To do this follow these steps:
  1. Install python 3
  2. Open cmd as admin
  3. Run `python -m pip install PyInstaller` to install PyInstaller
  4. Run `pyinstaller main.spec`
  5. The exe will be found in the dist folder
