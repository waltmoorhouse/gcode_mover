##################################################################
# Program: gcode_center.py                                       #
# Developer: Walt Moorhouse                                      #
# Developer Website: http://www.waltmoorhouse.com                #
# Date: August 1st, 2018                                         #
# Purpose: Make GCode centered around X = 0, Y = 0.              #
##################################################################

import sys

#####################################################################
# Handle arguments and have a little fun with the User interaction. #
#####################################################################

argNum = len(sys.argv)
if argNum < 3:
    if argNum < 2:
        inputFilename = raw_input("Please enter the path to your input file, or press enter to exit: ")
        if len(inputFilename) == 0:
            exit(9)
    outputFilename = raw_input("Please enter the path to your output file, or press enter to exit: ")
    if len(outputFilename) == 0:
        exit(10)
else:
    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]

#############
# Calculate #
#############

minX = 9999999999.9999
minY = 9999999999.9999
maxX = -9999999999.9999
maxY = -9999999999.9999

with open(inputFilename) as inputFile:
    for line in inputFile:
        if line[0] == 'G':
            for linePart in line.split():
                if linePart.startswith('X'):
                    tmp_x_coord = float(linePart[1:])
                    if tmp_x_coord < minX:
                        minX = tmp_x_coord
                    if tmp_x_coord > maxX:
                        maxX = tmp_x_coord

                elif linePart.startswith('Y'):
                    tmp_y_coord = float(linePart[1:])
                    if tmp_y_coord < minY:
                        minY = tmp_y_coord
                    if tmp_y_coord > maxY:
                        maxY = tmp_y_coord

xOffset = ((maxX - minX) / 2) - maxX
yOffset = ((maxY - minY) / 2) - maxY

###########
# Process #
###########

linesModified = 0
linesSkipped = 0
with open(outputFilename, "w") as outputFile:
    with open(inputFilename) as inputFile:
        for line in inputFile:
            if line[0] != 'G':
                outputFile.write(line)     # If it isn't a Go command, just pass through.
                linesSkipped += 1
            else:
                for linePart in line.split():
                    if linePart.startswith('X'):
                        xCoord = float(linePart[1:])
                        outputFile.write('X'+str(xCoord + xOffset))
                    elif linePart.startswith('Y'):
                        yCoord = float(linePart[1:])
                        outputFile.write('Y'+str(yCoord + yOffset))
                    else:
                        outputFile.write(linePart)
                    outputFile.write(" ")          # We must add back the spaces between the lineParts.
                outputFile.write("\n")   # Write the modified go command.
                linesModified += 1

print "Lines modified: "+str(linesModified)
print "Lines skipped: "+str(linesSkipped)
print "X Offset: "+str(xOffset)
print "Y Offset: "+str(yOffset)
print "Previous min X: "+str(minX)
print "New min X: "+str(minX+xOffset)
print "Previous max X: "+str(maxX)
print "New max X: "+str(maxX+xOffset)
print "Previous min Y: "+str(minY)
print "New min Y: "+str(minY+yOffset)
print "Previous max Y: "+str(maxY)
print "New max Y: "+str(maxY+yOffset)
