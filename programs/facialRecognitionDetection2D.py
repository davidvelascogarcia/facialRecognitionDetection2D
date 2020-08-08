'''
  * ************************************************************
  *      Program: Facial Recognition Detection 2D Module
  *      Type: Python
  *      Author: David Velasco Garcia @davidvelascogarcia
  * ************************************************************
  *
  * | INPUT PORT                           | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /facialRecognitionDetection2D/img:i  | Input image                                             |
  *
  *
  * | OUTPUT PORT                          | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /facialRecognitionDetection2D/img:o  | Output image with facial detection                      |
  * | /facialRecognitionDetection2D/data:o | Output result, facial recognition data                  |
  * | /facialRecognitionDetection2D/coord:o| Output result, facial recognition coordinates           |
'''

# Libraries
import cv2
import datetime
import face_recognition
import numpy as np
import time
import yarp

print("")
print("")
print("**************************************************************************")
print("**************************************************************************")
print("                 Program: Facial Recognition Detector 2D                  ")
print("                     Author: David Velasco Garcia                         ")
print("                             @davidvelascogarcia                          ")
print("**************************************************************************")
print("**************************************************************************")

print("")
print("Starting system ...")
print("")

print("")
print("Loading facialRecognitionDetection2D module ...")
print("")

print("")
print("**************************************************************************")
print("YARP configuration:")
print("**************************************************************************")
print("")
print("Initializing YARP network ...")
print("")

# Init YARP Network
yarp.Network.init()

print("")
print("[INFO] Opening image input port with name /facialRecognitionDetection2D/img:i ...")
print("")

# Open input image port
facialRecognitionDetection2D_portIn = yarp.BufferedPortImageRgb()
facialRecognitionDetection2D_portNameIn = '/facialRecognitionDetection2D/img:i'
facialRecognitionDetection2D_portIn.open(facialRecognitionDetection2D_portNameIn)

print("")
print("[INFO] Opening image output port with name /facialRecognitionDetection2D/img:o ...")
print("")

# Open output image port
facialRecognitionDetection2D_portOut = yarp.Port()
facialRecognitionDetection2D_portNameOut = '/facialRecognitionDetection2D/img:o'
facialRecognitionDetection2D_portOut.open(facialRecognitionDetection2D_portNameOut)

print("")
print("[INFO] Opening data output port with name /facialRecognitionDetection2D/data:o ...")
print("")

# Open output data port
facialRecognitionDetection2D_portOutDet = yarp.Port()
facialRecognitionDetection2D_portNameOutDet = '/facialRecognitionDetection2D/data:o'
facialRecognitionDetection2D_portOutDet.open(facialRecognitionDetection2D_portNameOutDet)

print("")
print("[INFO] Opening data output port with name /facialRecognitionDetection2D/coord:o ...")
print("")

# Open output coordinates data port
facialRecognitionDetection2D_portOutCoord = yarp.Port()
facialRecognitionDetection2D_portNameOutCoord = '/facialRecognitionDetection2D/coord:o'
facialRecognitionDetection2D_portOutCoord.open(facialRecognitionDetection2D_portNameOutCoord)

# Create data bootle
outputBottleFacialRecognitionDetection2D = yarp.Bottle()

# Create coordinates bootle
coordinatesBottleFacialRecognitionDetection2D = yarp.Bottle()

# Image size
image_w = 640
image_h = 480

# Prepare input image buffer
in_buf_array = np.ones((image_h, image_w, 3), np.uint8)
in_buf_image = yarp.ImageRgb()
in_buf_image.resize(image_w, image_h)
in_buf_image.setExternal(in_buf_array.data, in_buf_array.shape[1], in_buf_array.shape[0])

# Prepare output image buffer
out_buf_image = yarp.ImageRgb()
out_buf_image.resize(image_w, image_h)
out_buf_array = np.zeros((image_h, image_w, 3), np.uint8)
out_buf_image.setExternal(out_buf_array.data, out_buf_array.shape[1], out_buf_array.shape[0])

print("")
print("[INFO] YARP network configured correctly.")
print("")

print("")
print("**************************************************************************")
print("Reading files database:")
print("**************************************************************************")
print("")
print("[INFO] Reading people files database at " + str(datetime.datetime.now()) + " ...")
print("")

loopControlPeopleFiles = 0

# Control peopleFiles.txt exist and wait until exist
while int(loopControlPeopleFiles) == 0:
    try:
        # Read people file databate and create dynamic array
        peopleFile = open('../resources/peopleFiles.txt', 'r')
        peopleFileLines = peopleFile.readlines()

        countFiles = 0
        peopleFiles = []

        # Append files to array
        for peopleFileLine in peopleFileLines:

            print("Line " + str(countFiles) + ": " + str(peopleFileLine.strip()))
            countFiles = countFiles + 1
            sourceImg = "../database/" + peopleFileLine.strip()
            peopleFiles.append(sourceImg)

        # Print user files
        print("")
        print("**************************************************************************")
        print("Users database files:")
        print("**************************************************************************")
        print("")
        print("[INFO] Users database files:")
        print("")
        print(peopleFiles)

        loopControlPeopleFiles = 1

    except:
        print("")
        print("[ERROR] Sorry, peopleFiles.txt not founded, next check in 4 seconds.")
        print("")
        time.sleep(4)

print("")
print("**************************************************************************")
print("Reading database:")
print("**************************************************************************")
print("")
print("[INFO] Reading people name database at " + str(datetime.datetime.now()) + " ...")
print("")

loopControlPeopleData = 0

# Control peopleData.txt exist and wait until exist
while int(loopControlPeopleData) == 0:

    try:
        # Read people name databate and create dynamic array
        peopleDataFile = open('../resources/peopleData.txt', 'r')
        peopleDataFileLines = peopleDataFile.readlines()

        countDataFiles = 0
        peopleDataFiles = []

        # Append users to array
        for peopleDataFileLine in peopleDataFileLines:

            print("Line " + str(countDataFiles) + ": " + str(peopleDataFileLine.strip()))
            countDataFiles = countDataFiles + 1
            peopleDataFiles.append(peopleDataFileLine.strip())

        # Print user names
        print("")
        print("**************************************************************************")
        print("Users database:")
        print("**************************************************************************")
        print("")
        print("[INFO] Users database:")
        print("")
        print(peopleDataFiles)

        loopControlPeopleData = 1

    except:
        print("")
        print("[ERROR] Sorry, peopleData.txt not founded, next check in 4 seconds.")
        print("")
        time.sleep(4)

print("")
print("**************************************************************************")
print("Training models:")
print("**************************************************************************")
print("")
print("[INFO] Training people database at " + str(datetime.datetime.now()) + " ...")
print("")

peopleDetection = []
peopleDetectionEncoding = []
countPeopleFiles = 0

# Load to train all image files to database
for people in peopleFileLines:

    print("[INFO] Loading to database " + str(peopleFiles[countPeopleFiles]) + " ...")

    # Load image to array
    peopleDetection.append(face_recognition.load_image_file(peopleFiles[countPeopleFiles]))

    # Detect face and loac face to array
    peopleDetectionEncoding.append(face_recognition.face_encodings(peopleDetection[countPeopleFiles])[0])

    countPeopleFiles = countPeopleFiles + 1

# Append to array known faces
knownFacesEnconding = []
countKnownPeople = 0

for peopleKnown in peopleFileLines:
    knownFacesEnconding.append(peopleDetectionEncoding[countKnownPeople])
    countKnownPeople = countKnownPeople + 1

# Append to array known names
knownFacesNames = []
countPeopleNames = 0

for peopleKnownNames in peopleFileLines:
    knownFacesNames.append(peopleDataFiles[countPeopleNames])

    countPeopleNames = countPeopleNames + 1

# Control loopControlReceiveImageSource
loopControlReceiveImageSource = 0

# Loop process
while int(loopControlReceiveImageSource) == 0:

    try:
        print("")
        print("**************************************************************************")
        print("Waiting for input image source:")
        print("**************************************************************************")
        print("")
        print("[INFO] Waiting input image source at " + str(datetime.datetime.now()) + " ...")
        print("")

        # Recieve image source
        frame = facialRecognitionDetection2D_portIn.read()

        print("")
        print("**************************************************************************")
        print("Processing input image:")
        print("**************************************************************************")
        print("")
        print("[INFO] Processing input image at " + str(datetime.datetime.now()) + " ...")
        print("")

        # Buffer processed image
        in_buf_image.copy(frame)
        assert in_buf_array.__array_interface__['data'][0] == in_buf_image.getRawImage().__int__()

        # YARP -> OpenCV
        rgbFrame = in_buf_array[:, :, ::-1]

        # Detect faces in rgbFrame
        faceLocations = face_recognition.face_locations(rgbFrame)

        # Encode face detected
        faceEncodings = face_recognition.face_encodings(rgbFrame, faceLocations)

        # Pre-configure detected name as "None"
        detectedPerson = "None"

        # If faces has been detected
        if str(faceLocations) != "[]":

            # Process image with faces detected
            for (top, right, bottom, left), faceEncoding in zip(faceLocations, faceEncodings):

                # Compare faceEncoding with known faces
                faceMatches = face_recognition.compare_faces(knownFacesEnconding, faceEncoding)

                # Compare faceEncoding with known faces to get distance
                faceMatchesDistance = face_recognition.face_distance(knownFacesEnconding, faceEncoding)

                # Extract index match
                bestMatchIndex = np.argmin(faceMatchesDistance)

                # If detected person is in database get name
                if faceMatches[bestMatchIndex]:
                   detectedPerson = knownFacesNames[bestMatchIndex]

                # If isn´t in database is "Unknown"
                else:
                   detectedPerson = "Unknown"

                # Paint processed image
                # Paint rectange in detected face
                cv2.rectangle(in_buf_array, (left, top), (right, bottom), (0, 0, 255), 2)

                # Paint rectangle to put name
                cv2.rectangle(in_buf_array, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                # Paint name
                cv2.putText(in_buf_array, detectedPerson, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

                # Get people coordinates
                x = left
                y = 480 - bottom

                # Print processed data
                print("")
                print("**************************************************************************")
                print("Resume results:")
                print("**************************************************************************")
                print("")
                print("[RESULTS] facialRecognitionDetection2D results:")
                print("")
                print("[DETECTION] Facial recognition detection: " + str(detectedPerson))
                print("[COORDINATES] Coordinates: X:" + str(x) + ", Y: " + str(y))
                print("[DATE] Detection time: " + str(datetime.datetime.now()))
                print("")

                # Sending processed facialRecognitionDetection2D detection
                outputBottleFacialRecognitionDetection2D.clear()
                outputBottleFacialRecognitionDetection2D.addString("DETECTION:")
                outputBottleFacialRecognitionDetection2D.addString(detectedPerson)
                outputBottleFacialRecognitionDetection2D.addString("DATE:")
                outputBottleFacialRecognitionDetection2D.addString(str(datetime.datetime.now()))
                facialRecognitionDetection2D_portOutDet.write(outputBottleFacialRecognitionDetection2D)

                # Sending coordinates detection
                coordinatesBottleFacialRecognitionDetection2D.clear()
                coordinatesBottleFacialRecognitionDetection2D.addString("COORDINATES:")
                coordinatesBottleFacialRecognitionDetection2D.addString("X: " + str(x) + ", Y: " + str(y))
                coordinatesBottleFacialRecognitionDetection2D.addString("DATE:")
                coordinatesBottleFacialRecognitionDetection2D.addString(str(datetime.datetime.now()))
                facialRecognitionDetection2D_portOutCoord.write(coordinatesBottleFacialRecognitionDetection2D)

        else:
            # Sending processed detection if none detection
            outputBottleFacialRecognitionDetection2D.clear()
            outputBottleFacialRecognitionDetection2D.addString("DETECTION:")
            outputBottleFacialRecognitionDetection2D.addString(detectedPerson)
            outputBottleFacialRecognitionDetection2D.addString("DATE:")
            outputBottleFacialRecognitionDetection2D.addString(str(datetime.datetime.now()))
            facialRecognitionDetection2D_portOutDet.write(outputBottleFacialRecognitionDetection2D)

        # Sending processed image
        print("")
        print("[INFO] Sending processed image at " + str(datetime.datetime.now()) + " ...")
        print("")

        out_buf_array[:,:] = in_buf_array
        facialRecognitionDetection2D_portOut.write(out_buf_image)

    except:
        print("")
        print("[ERROR] Empty frame.")
        print("")

# Close ports
print("[INFO[ Closing ports ...")
facialRecognitionDetection2D_portIn.close()
facialRecognitionDetection2D_portOut.close()
facialRecognitionDetection2D_portOutDet.close()
facialRecognitionDetection2D_portOutCoord.close()

# Close files
peopleFile.close()
peopleDataFile.close()

print("")
print("")
print("**************************************************************************")
print("Program finished")
print("**************************************************************************")
print("")
print("facialRecognitionDetection2D program finished correctly. ")
print("")
