'''
 * ************************************************************
 *      Program: peopleData Module
 *      Type: Python
 *      Author: David Velasco Garcia @davidvelascogarcia
 * ************************************************************
 */
'''

# Libraries
import os, sys, string
import numpy as np


print("")
print("")
print("**************************************************************************")
print("Processing")
print("**************************************************************************")
print("")
print("Preparing files ...")

peopleFile = open("../resources/peopleFiles.txt", "rt")
peopleFileUpdated = open("../resources/peopleData.txt", "wt")

# Clean image extension and to uppercase
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
	
peopleFile.close()
peopleFileUpdated.close()

print("")
print("")
print("**************************************************************************")
print("Program finished")
print("**************************************************************************")

