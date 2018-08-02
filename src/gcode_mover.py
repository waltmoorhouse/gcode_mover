#######################################################
# Program: gcode_mover.py                             #
# Developer: Walt Moorhouse                           #
# Developer Website: http://www.waltmoorhouse.com     #
# Date: August 1st, 2018                              #
# Purpose: Move a 3D GCode Path in 1 to 3 dimensions. #
#######################################################

import os
import sys
import random

####################
# Define Constants #
####################

COMMENT_TEXT = "(This object was edited with gcode_mover.py)\n"
EXIT_STRING = "The board you are standing on suddenly launches into the air, tossing your screaming soon to be " \
              "corpse into the foggy depths of the chasm, leaving behind only the fading echos of your screams."

#####################################################################
# Handle arguments and have a little fun with the User interaction. #
#####################################################################

argNum = len(sys.argv)
if argNum < 3:
    print "You approach a locked gate. On the rusty gate there is sign that says, ONLY THOSE WITH GCODE FILES MAY PASS."
    if argNum < 2:
        inputFilename = raw_input("Please enter the path to your input file, "
                                  "or press enter to slowly back away from the gate: ")
        if len(inputFilename) == 0:
            exit(9)
    outputFilename = raw_input("Please enter the path to your output file, "
                               "or press enter to slowly back away from the gate: ")
    if len(outputFilename) == 0:
        exit(10)
else:
    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]
try:
    test = open(outputFilename, "w+")
    test.write(COMMENT_TEXT)
    test.close()

    if os.access(inputFilename, os.R_OK):
        print "The lock pops open and the rusty gate swings open."
    else:
        print "The gate won't budge, so you step away to inspect your input file and make sure the gate can read it."
        exit(11)
except IOError:
    print "The gate won't budge, so you step away to inspect your output directory permissions."
    exit(12)

if argNum == 6:
    x_amount = float(sys.argv[3])
    y_amount = float(sys.argv[4])
    z_amount = float(sys.argv[5])
    bk_phrases = ["Meh. You're no fun! Go on across.", "Well, SOMEONE is in a hurry.", "Watch out for Swallows!",
                  "I should install a kiosk and retire.", "Too busy looking at their phones to talk to me. Shameful.",
                  "I get lonely here with just the bridge for company, you know."]
    print "BRIDGEKEEPER: " + bk_phrases[random.randint(0, len(bk_phrases))]
else:
    print "You go through the now unlocked gate and approach an ancient bridge across a foggy chasm with no discernable bottom."
    print "A withered old bridgekeeper that looks as though he may have started the day they built it approaches you... slowly."
    print "BRIDGEKEEPER: Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other file he see."
    print "You bravely step up and say: Ask me the questions, bridgekeeper. I am not afraid."
    if argNum > 3:
        x_amount_input = sys.argv[3]
        print "BRIDGEKEEPER: What!..."
        print "You interrupt: Move the path " + x_amount_input + " units along the X axis"
        print "BRIDGEKEEPER: Huh? Well ok then."
    else:
        x_amount_input = raw_input("BRIDGEKEEPER: What!... is the amount you want to move the path along the X axis? ")
    try:
        x_amount = float(x_amount_input)
    except (ValueError, TypeError):
        print EXIT_STRING
        exit(13)
    if argNum > 4:
        y_amount_input = sys.argv[4]
        print "BRIDGEKEEPER: What!..."
        print "You interrupt: Move the path " + y_amount_input + " units along the Y axis"
        print "BRIDGEKEEPER: Will you at least let me finish the question?"
    else:
        y_amount_input = raw_input("BRIDGEKEEPER: What!... is the amount you want to move the path along the Y axis? ")
    try:
        y_amount = float(y_amount_input)
    except (ValueError, TypeError):
        print EXIT_STRING
        exit(13)
    z_amount_input = raw_input("BRIDGEKEEPER: What!... is the amount you want to move the path along the Z axis? ")
    try:
        z_amount = float(z_amount_input)
    except (ValueError, TypeError):
        print EXIT_STRING
        exit(14)

##############################################################
# Now that we have a file and some values, let's process it. #
##############################################################

linesModified = 0
linesSkipped = 0
with open(outputFilename, "w") as outputFile:
    with open(inputFilename) as inputFile:
        for line in inputFile:
            if line != COMMENT_TEXT:        # Don't put multiple copies of this if we edit multiple times.
                if line[0] != 'G':
                    outputFile.write(line)     # If it isn't a Go command, just pass through.
                    linesSkipped += 1
                else:
                    for linePart in line.split():
                        if linePart.startswith('X'):
                            outputFile.write('X'+str(float(linePart[1:]) + x_amount))
                        elif linePart.startswith('Y'):
                            outputFile.write('Y'+str(float(linePart[1:]) + y_amount))
                        elif linePart.startswith('Z'):
                            outputFile.write('Z'+str(float(linePart[1:]) + z_amount))
                        else:
                            outputFile.write(linePart)
                        outputFile.write(" ")          # We must add back the spaces between the lineParts.
                    outputFile.write("\n")   # Write the modified go command.
                    linesModified += 1

print "* You have successfully made it across the Bridge of Death, your files intact. *"
print "Lines modified: "+str(linesModified)
print "Lines skipped: "+str(linesSkipped)
