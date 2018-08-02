##################################################################
# Program: sharpie_mode.py                                       #
# Developer: Walt Moorhouse                                      #
# Developer Website: http://www.waltmoorhouse.com                #
# Date: August 1st, 2018                                         #
# Purpose: Make GCode sharpie safe, by limiting Z axis to min 0. #
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
                    if linePart.startswith('Z'):
                        z_coord = float(linePart[1:])
                        if z_coord < 0.0000:
                            z_coord = 0.0000;
                        outputFile.write('Z'+str(z_coord))
                    else:
                        outputFile.write(linePart)
                    outputFile.write(" ")          # We must add back the spaces between the lineParts.
                outputFile.write("\n")   # Write the modified go command.
                linesModified += 1

print "Lines modified: "+str(linesModified)
print "Lines skipped: "+str(linesSkipped)
