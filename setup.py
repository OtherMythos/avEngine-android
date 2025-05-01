#!/usr/bin/python3

import argparse
import shutil
from pathlib import Path

def createAssetsDir(enginePath, depsPath, scriptPath):
    assetsDirPath = scriptPath / "app/src/main/assets"
    if assetsDirPath.exists() and assetsDirPath.is_dir():
        print("%s already exists, skipping" % str(assetsDirPath))
        return

    assetsDirPath.mkdir(parents=True)

    shutil.copytree(enginePath / "setup/essential", assetsDirPath / "essential")

    shutil.copytree(depsPath / "ogre2/share/OGRE/Media/Hlms", assetsDirPath / "Hlms")
    shutil.copytree(depsPath / "colibri/data/Hlms/Colibri", assetsDirPath / "Hlms/Colibri")

    print("Copied %s" % str(assetsDirPath / "essential"))

def createDependenciesCopy(enginePath, depsPath, scriptPath):
    #Create a symlink if the necessary permissions are available.
    #Windows devices require the user to be administer or certain permissions to exist in order to create symlinks.
    #TODO if on windows fallback to copying.

    depsDirPath = scriptPath / "app/src/main/Dependencies"
    if depsDirPath.exists():
        print("%s already exists, skipping" % str(depsDirPath))
        return

    depsDirPath.symlink_to(depsPath, target_is_directory=True)

    print("Copied %s" % str(depsDirPath))

def copySDLFiles(enginePath, depsPath, scriptPath):
    #Copy the files over from SDL2 in the dependencies dir
    SDL2JavaPath = scriptPath / "app/src/main/java"
    if SDL2JavaPath.exists():
        print("%s already exists, skipping" % str(SDL2JavaPath))
        return

    shutil.copytree(depsPath / "SDL2/java", SDL2JavaPath)

    targetFile = SDL2JavaPath / "org/libsdl/app/SDLActivity.java"
    with open(targetFile,'r') as file:
        filedata = file.read()
        filedata = filedata.replace("\"SDL2\",", "\"av\",")
        filedata = filedata.replace("\"main\"", "//\"main\"")
    with open(targetFile,'w') as file:
        file.write(filedata)

    print("Copied %s" % str(SDL2JavaPath))

def main():
    helpText = '''A script to setup the avEngine for android builds.
    Certain files need to be moved into place to allow this android project to be built correctly.
    '''

    parser = argparse.ArgumentParser(description = helpText)
    parser.add_argument("dependencies", type=str, nargs='?', help="Path to the built avEngine dependencies.")
    args = parser.parse_args()

    if args.dependencies is None:
        print("Please provide a path to the avEngine dependencies.")
        return

    depsPath = Path(args.dependencies)
    if not depsPath.exists() or depsPath.is_file():
        print("Provided dependencies path %s does not exist or is not useable" % str(depsPath))
        return

    #Assuming the symlink cloned the engine correctly.
    enginePath = Path("./app/src/main/avEngine").resolve()
    scriptPath = Path(__file__).parent
    depsPath = depsPath.resolve()

    createAssetsDir(enginePath, depsPath, scriptPath)
    createDependenciesCopy(enginePath, depsPath, scriptPath)
    copySDLFiles(enginePath, depsPath, scriptPath)

if __name__ == "__main__":
    main()
