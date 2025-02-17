import sys
import time
import os
import os.path

def reSpeed(path, fps):   
    
    fps = min(max(fps, 1) , 50)
    deviation=0.5
    interval = int(100 / fps)  
    

    try:
        if os.path.isfile(path):
            print("Loading file: ", path, " ...")
            file = open(path, "r+b")
        else:
            print("The file was not found")
            return(False)
        
        byte = file.read(3)
        
        if byte.decode() != "GIF":
            print("Not a .gif")
            return(False)
        
        file.seek(0)
        fullFile = file.read()
        file.close()
        
        targetOut = os.path.splitext(path)[0] + "_reSpeed_" + str(fps) + ".gif"
        for runOption in runOptions:
            if runOption == "-r":
                targetOut = path
        
        
        outFile = open(targetOut, "wb")
        outFile.write(fullFile)
        outFile.close()
        
        file = open(targetOut, "r+b")
        
        print("ReSpeeding '", path, "' to a speed of", fps, "FPS...")
        
        while byte:
            if byte == b'\x21':
                byte = file.read(1)
                if byte == b'\xF9':
                    byte = file.read(1)
                    if byte == b'\x04':
                        file.seek(1, os.SEEK_CUR)
                        deviation+=(100.0 / fps)-interval
                        file.write(int(interval+deviation).to_bytes(1, "little"))
                        if deviation>=1:
                            deviation=deviation-int(deviation)
                        
            byte = file.read(1)
    
    except Exception as e:
        print(e)
        file.close()
        return(False)
    
    
    file.close()
    
    for runOption in runOptions:
        if runOption == "-o":
            if sys.platform == "win32":
                os.startfile(targetOut)
    
    return(True)
    

fps = ""
targetFile = ""
runOptions = []

print("GIF ReSpeed")
print("Developed by LarsKDev")
print("modify by yuangBi")
print("Version 1.0.3 | 5 Mar 2022")
print("---------------------------")

if len(sys.argv) == 1:
    targetFile = input("Please specify the location of the .gif file")
elif len(sys.argv) > 1:
    targetFile = sys.argv[1]
    runOptions = sys.argv[2:]

if len(sys.argv) > 2:
    print("Running with additional arguments", runOptions)
    

while not isinstance(fps, int):
    try:
        fps = int(input("Please specify the new frame interval in frames per second: (GIF files only support up to 50 fps)"))
    except:
        print("Please enter a valid integer")
        
folderOption = False
for runOption in runOptions:
    if runOption == "-f":
        folderOption = True
        print("Converting all .gifs in folder...")
        if os.path.isdir(targetFile):
            targetFiles = os.listdir(targetFile)
            
            for f in targetFiles:
                reSpeed(targetFile + "/" + f, fps)
        else:
            print("Please specify a folder...")
            
            
if not folderOption:
    reSpeed(targetFile, fps)

time.sleep(2)

