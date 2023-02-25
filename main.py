import re
import requests
import zipfile
import os
import subprocess
from shutil import rmtree

print("Getting Apple Music Beta Download Link")

url = "https://store.rg-adguard.net/api/GetFiles"
data = {"type": "ProductId", "url": "9PFHDD62MXS1", "ring": "WIF", "lang": "en-US"}

response = requests.post(url=url, data=data, timeout=10)

HTML = response.text.splitlines()


# Open text file response for testing purposes
# with open("reponse.html", 'r') as f:
#     HTML = f.readlines()
#     f.close()

finalURL = ""
for line in HTML:
    if "AppleInc.AppleMusicWin" in line and ".msixbundle" in line:
        url = re.match(r'.*\shref="(.*?)"\s.*', line)
        if url:
            finalURL = url.group(1)


print("Downloading MsixBundle... Please wait, this can take a few minutes")

download = requests.get(url=finalURL)
rawFile = download.content

print("Writing MSixBundle")

with open("AppleMusic.Msixbundle", 'wb') as f:
    f.write(rawFile)
    f.close()

print("Extracting required files")

zipFile = zipfile.ZipFile("AppleMusic.Msixbundle", 'r')
itemName = ""
for item in zipFile.namelist():
    if "x64" in item:
        itemName = item
        zipFile.extract(item)

zipFile = zipfile.ZipFile(itemName, 'r')
zipFile.extractall("./temp/")

with open("./temp/AppxManifest.xml", 'r') as f:
    manifest = f.readlines()
    f.close()

print("Modifying app to work on Windows 10")

for line in range(len(manifest)):
    if '<TargetDeviceFamily Name="Windows.Desktop"' in manifest[line]:
        manifest[line] = re.sub(r'MinVersion="10.\d+\.\d+\.\d+"', 'MinVersion="10.0.0.0"', manifest[line])

with open("./temp/AppxManifest.xml", 'w') as f:
    for line in manifest:
        f.write(line)
    f.close()

print("Removing unnecessary files. If any errors occur, it's probably okay")

os.remove("./temp/AppxBlockMap.xml")
os.remove("./temp/AppxSignature.p7x")
os.remove("./temp/[Content_Types].xml")
os.remove("./temp/AppxMetadata/CodeIntegrity.cat")
os.rmdir("./temp/AppxMetadata")

print("Installing app...")

subprocess.call('powershell.exe Add-AppxPackage -Register temp/AppxManifest.xml', shell=True)

print("Removing temporary files")

rmtree("./temp")
os.remove("./AppleMusic.Msixbundle")
os.remove("./" + itemName)

pp = input("Finished. Please press enter to exit.")
