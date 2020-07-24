def parseDiff(diffFile, outputDir):
    allDiffs = open(diffFile, "r")
    curFile = "placeholder"
    sign = "Find a functionally"
    count = 0
    for line in allDiffs:
        if line.startswith(sign):
            if(curFile != "placeholder"):
                curFile.close()
            fileName = line[line.index(":") + 1:-2]
            filePath = outputDir + fileName + ".diff"
            curFile = open(filePath, "w")
        curFile.write(line)
    if(curFile != "placeholder"):
        curFile.close()


parseDiff("../res/android-4.4_r1_android-5.0.0_r1.diff",
          "../res/split/android-4.4_r1_android-5.0.0_r1/all/")
