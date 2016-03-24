import sys

def checkArg():
    if len(sys.argv) != 4:
        print("illegal argument")
        sys.exit(1)
    elif sys.argv[3] != "3G" and sys.argv[3] != "4G":
        print("unknown RAT")
        sys.exit(1)
    else:
        try:
            inp = int(sys.argv[2])
        except ValueError:
            print("argument #2 must be integer")
            sys.exit(1)

def getSiteNumber(managedObject):
    siteNumber = ""
    if RAT == "3G":
        idx = managedObject.find('WBTS-') + 5
    else:
        idx = managedObject.find('MRBTS-') + 6

    while ord(managedObject[idx]) >= 48 and ord(managedObject[idx]) <= 57:
        siteNumber += managedObject[idx]
        idx += 1

    return siteNumber


checkArg()

header = ""
inFileName = sys.argv[1]
splitNum = sys.argv[2]
RAT = sys.argv[3]
i = 0
siteCount = 0
fileNum = 1
fileEnd = False
siteNum = "0000"
firstLine = ""
fileContent = ""



if '.' in inFileName:
    OutFileName = inFileName.split('.')[0]
else:
    OutFileName = inFileName

with open(inFileName, 'r') as infile:
    for line in infile:
        if len(line) > 200:
            print("Forgot to Align file?")
            sys.exit(1)
            
        header += line
        if line == "</header>\n":
            break

    while fileEnd == False:
        with open(OutFileName + '_' + str(fileNum) + '.xml', 'w') as outfile:
            outfile.write(header)
            outfile.write(firstLine)
        
            for line in infile:
                if line.startswith('</cmData>'):
                    fileEnd = True
                    break
                
                if line.startswith('<managedObject'):
                    newSiteNum = getSiteNumber(line)
                    if newSiteNum != siteNum:
                        siteCount += 1
                        siteNum = newSiteNum

                    if siteCount > int(splitNum):
                        firstLine = line
                        break

                fileContent += line

            outfile.write(fileContent)
            outfile.write('</cmData>\n')
            outfile.write('</raml>')
            siteCount = 1
            fileNum += 1
            fileContent = ""

sys.exit(0)
