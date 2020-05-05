'''
 * ************************************************************
 *      Program: peopleData Module
 *      Type: Python
 *      Author: David Velasco Garcia @davidvelascogarcia
 * ************************************************************
 */
'''

# Libraries
import os
import numpy as np
import string
import sys

print("")
print("")
print("**************************************************************************")
print("updatePeopleData")
print("**************************************************************************")
print("")
print("Preparing and updating people labels ...")
print("")
print("**************************************************************************")
print("Processing:")
print("**************************************************************************")
print("")

loopControlFileExists = 0

while int(loopControlFileExists)==0:
    try:
        print("")
        print("Reading peopleFiles.txt ...")
        peopleFile = open("../resources/peopleFiles.txt", "rt")
        loopControlFileExists = 1
    except:
        print("")
        print("Sorry, peopleFiles.txt not founded, waiting 4 seconds to the next check ...")
        print("")
        time.sleep(4)

peopleFileUpdated = open("../resources/peopleData.txt", "wt")

# Clean image extension and to uppercase
print("")
print("Writing people labels ...")
for line in peopleFile:
	cleanNames=line.replace('.jpg', '')
	cleanNames=cleanNames.replace('.jpeg', '')
	cleanNames=cleanNames.replace('.giff', '')
	cleanNames=cleanNames.replace('.tiff', '')
	cleanNames=cleanNames.replace('.png', '')
	cleanNames=cleanNames.replace('.bmp', '')
	cleanNames=cleanNames.replace('.pdf', '')
	cleanNames=cleanNames.replace('database/', '')
	cleanNames=cleanNames.upper()
	peopleFileUpdated.write(cleanNames)

# Close files
peopleFile.close()
peopleFileUpdated.close()

print("")
print("People labels updated correctly")

print("")
print("")
print("**************************************************************************")
print("Program finished")
print("**************************************************************************")
print()
print("Press enter to close program ...")
exitProgram = input()
