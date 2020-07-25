import random
import os
import shutil


def parseDiff(diffFile, outputDir):
    allDiffs = open(diffFile, "r")
    curFile = "placeholder"
    sign = "Find a functionally"
    count = 0
    while True:
        # for line in allDiffs:
        line = allDiffs.readline()
        if(line == ''):
            break
        if line.startswith(sign):
            if(curFile != "placeholder"):
                curFile.close()
            fileName = line[line.index(":") + 1:-2]
            filePath = outputDir + fileName + ".diff"
            curFile = open(filePath, "w")

        curFile.write(line)
    if(curFile != "placeholder"):
        curFile.close()


def writeToFile(filePath, fileContent):
    curFile = open(filePath, "w")
    curFile.write(fileContent)
    curFile.close()


def shouldFilter(modifiers):
    isPublic = False
    isHiddenOrInternal = False
    for modifier in modifiers:
        if modifier == "public":
            isPublic = True
        if modifier == "hidden" or modifier == "internal":
            isHiddenOrInternal = True
    res = not(isPublic) or isHiddenOrInternal
    return res


def parseDiffAndFilter(diffFile, outputDir):
    allDiffs = open(diffFile, "r")
    newFunctionSign = "Find a functionally"
    modifierUpdatedSign = "Method Updated"
    modifierSign = "Method Modifier"
    modifier = []
    curFileContent = ""
    curFileName = ""
    filterFlag = True
    count = 0
    while True:
        # for line in allDiffs:
        line = allDiffs.readline()

        if(line == ''):
            if(not(filterFlag)):
                curFilePath = outputDir + curFileName + ".diff"
                writeToFile(curFilePath, curFileContent)
                count += 1
            break

        if line.startswith(newFunctionSign):
            curFilePath = outputDir + curFileName + ".diff"
            if(not(filterFlag)):
                writeToFile(curFilePath, curFileContent)
                count += 1
            filterFlag = False
            curFileContent = ""
            modifier = []
            curFileName = line[line.index(":") + 1:-2]

        if line.startswith(modifierSign):
            modifier = line[line.index(":") + 1:-2].split()
            filterFlag = filterFlag or shouldFilter(modifier)

        if line.startswith(modifierUpdatedSign):
            filterFlag = True

        curFileContent += line


def cleanDir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


cleanDir("../res/split/android-4.4_r1_android-5.0.0_r1/all/")

parseDiffAndFilter("../res/android-4.4_r1_android-5.0.0_r1.diff",
                   "../res/split/android-4.4_r1_android-5.0.0_r1/all/")
