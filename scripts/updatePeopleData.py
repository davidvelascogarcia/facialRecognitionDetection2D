'''
 * ************************************************************
 *      Program: peopleData Module
 *      Type: Python
 *      Author: David Velasco Garcia @davidvelascogarcia
 * ************************************************************
'''

# Libraries
import datetime
import os
import numpy as np
import string
import sys

print("")
print("**************************************************************************")
print("Updating people data labels:")
print("**************************************************************************")
print("")
print("[INFO] Preparing and updating people labels at " + str(datetime.datetime.now()) + " ...")
print("")

print("")
print("**************************************************************************")
print("Processing input people date labels:")
print("**************************************************************************")
print("")

loopControlFileExists = 0

while int(loopControlFileExists)==0:
    try:
        print("")
        print("[INFO] Reading peopleFiles.txt at " + str(datetime.datetime.now()) + " ...")
        print("")

        peopleFile = open("../resources/peopleFiles.txt", "rt")

        loopControlFileExists = 1

    except:
        print("")
        print("[ERROR] Sorry, peopleFiles.txt not founded, waiting 4 seconds to the next check ...")
        print("")
        time.sleep(4)

peopleFileUpdated = open("../resources/peopleData.txt", "wt")

# Clean image extension and to uppercase
print("")
print("[INFO] Writing people labels at " + str(datetime.datetime.now()) + " ...")
print("")

for line in peopleFile:

	cleanNames = line.replace('.jpg', '')
	cleanNames = cleanNames.replace('.jpeg', '')
	cleanNames = cleanNames.replace('.giff', '')
	cleanNames = cleanNames.replace('.tiff', '')
	cleanNames = cleanNames.replace('.png', '')
	cleanNames = cleanNames.replace('.bmp', '')
	cleanNames = cleanNames.replace('.pdf', '')
	cleanNames = cleanNames.replace('database/', '')
	cleanNames = cleanNames.upper()
	peopleFileUpdated.write(cleanNames)

# Close files
peopleFile.close()
peopleFileUpdated.close()

print("")
print("[INFO] People labels updated correctlyat " + str(datetime.datetime.now()) + ".")
print("")

print("")
print("")
print("**************************************************************************")
print("Program finished")
print("**************************************************************************")
print("")
print("[INFO] Press enter to close program ...")
print("")

exitProgram = input()
