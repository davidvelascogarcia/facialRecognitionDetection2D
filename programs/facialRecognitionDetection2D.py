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
print("Loading facialRecognitionDetection2D module ...")


print("")
print("")
print("**************************************************************************")
print("YARP configuration:")
print("**************************************************************************")
print("")
print("")
print("Initializing YARP network ...")

# Init YARP Network
yarp.Network.init()


print("")
print("[INFO] Opening image input port with name /facialRecognitionDetection2D/img:i ...")

# Open input image port
facialRecognitionDetection2D_portIn = yarp.BufferedPortImageRgb()
facialRecognitionDetection2D_portNameIn = '/facialRecognitionDetection2D/img:i'
facialRecognitionDetection2D_portIn.open(facialRecognitionDetection2D_portNameIn)

print("")
print("[INFO] Opening image output port with name /facialRecognitionDetection2D/img:o ...")

# Open output image port
facialRecognitionDetection2D_portOut = yarp.Port()
facialRecognitionDetection2D_portNameOut = '/facialRecognitionDetection2D/img:o'
facialRecognitionDetection2D_portOut.open(facialRecognitionDetection2D_portNameOut)

print("")
print("[INFO] Opening data output port with name /facialRecognitionDetection2D/data:o ...")

# Open output data port
facialRecognitionDetection2D_portOutDet = yarp.Port()
facialRecognitionDetection2D_portNameOutDet = '/facialRecognitionDetection2D/data:o'
facialRecognitionDetection2D_portOutDet.open(facialRecognitionDetection2D_portNameOutDet)

print("")
print("[INFO] Opening data output port with name /facialRecognitionDetection2D/coord:o ...")

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
print("")
print("**************************************************************************")
print("Reading files database:")
print("**************************************************************************")
print("")
print("Reading people files database ...")
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
        print("")
        time.sleep(4)

print("")
print("")
print("**************************************************************************")
print("Reading database:")
print("**************************************************************************")
print("")
print("Reading people name database ...")
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
        print("")
        time.sleep(4)

print("")
print("")
print("**************************************************************************")
print("Training models:")
print("**************************************************************************")
print("")
print("Training people database ...")
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

print("")
print("")
print("**************************************************************************")
print("Waiting for input image source:")
print("**************************************************************************")
print("")
print("")
print("Waiting input image source ...")
print("")

# Control loopControlReceiveImageSource
loopControlReceiveImageSource = 0

# Loop process
while int(loopControlReceiveImageSource) == 0:

    # Recieve image source
    frame = facialRecognitionDetection2D_portIn.read()

    print("")
    print("")
    print("**************************************************************************")
    print("Processing:")
    print("**************************************************************************")
    print("")
    print("Processing data ...")

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

            # Get time Detection
            timeDetection = datetime.datetime.now()

            # Print processed data
            print("")
            print("**************************************************************************")
            print("Resume:")
            print("**************************************************************************")
            print("")
            print("[RESULTS] Detection: "+ str(detectedPerson))
            print("[INFO] Coordinates:")
            print("X: ", x)
            print("Y: ", y)
            print("[INFO] Detection time: "+ str(timeDetection))

            # Sending processed detection
            outputBottleFacialRecognitionDetection2D.clear()
            outputBottleFacialRecognitionDetection2D.addString("Detection:")
            outputBottleFacialRecognitionDetection2D.addString(detectedPerson)
            outputBottleFacialRecognitionDetection2D.addString("Time:")
            outputBottleFacialRecognitionDetection2D.addString(str(timeDetection))
            facialRecognitionDetection2D_portOutDet.write(outputBottleFacialRecognitionDetection2D)

            # Sending coordinates detection
            coordinatesBottleFacialRecognitionDetection2D.clear()
            coordinatesBottleFacialRecognitionDetection2D.addString("X: ")
            coordinatesBottleFacialRecognitionDetection2D.addString(str(x))
            coordinatesBottleFacialRecognitionDetection2D.addString("Y: ")
            coordinatesBottleFacialRecognitionDetection2D.addString(str(y))
            facialRecognitionDetection2D_portOutCoord.write(coordinatesBottleFacialRecognitionDetection2D)

    else:

        # Update time detection
        timeDetection = datetime.datetime.now()

        # Sending processed detection if none detection
        outputBottleFacialRecognitionDetection2D.clear()
        outputBottleFacialRecognitionDetection2D.addString("Detection:")
        outputBottleFacialRecognitionDetection2D.addString(detectedPerson)
        outputBottleFacialRecognitionDetection2D.addString("Time:")
        outputBottleFacialRecognitionDetection2D.addString(str(timeDetection))
        facialRecognitionDetection2D_portOutDet.write(outputBottleFacialRecognitionDetection2D)

    # Sending processed image
    print("")
    print("[INFO] Sending processed image at " + str(timeDetection) + " ...")
    print("")
    out_buf_array[:,:] = in_buf_array
    facialRecognitionDetection2D_portOut.write(out_buf_image)

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
