'''
 * ************************************************************
 *      Program: Facial Recognition Detection 2D Module
 *      Type: Python
 *      Author: David Velasco Garcia @davidvelascogarcia
 * ************************************************************
 */

/*
  *
  * | INPUT PORT                           | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /facialRecognitionDetection2D/img:i  | Input image             n                               |
  *
  *
  * | OUTPUT PORT                          | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /facialRecognitionDetection2D/img:o  | Output image with facial detection                      |
  * | /facialRecognitionDetection2D/data:o | Output result, facial recognition data                  |
  * | /facialRecognitionDetection2D/coord:o| Output result, facial recognition coordinates           |

  *
'''

# Libraries
import face_recognition
import cv2
import yarp
import numpy as np

print("**************************************************************************")
print("**************************************************************************")
print("                 Program: Facial Recognition Detector 2D                  ")
print("                     Author: David Velasco Garcia                         ")
print("                             @davidvelascogarcia                          ")
print("**************************************************************************")
print("**************************************************************************")

print("")
print("Starting system...")

print("")
print("Loading facialRecognitionDetection2D module...")

print("")
print("Initializing YARP network...")

# Init YARP Network
yarp.Network.init()


print("")
print("Opening image input port with name /facialRecognitionDetection2D/img:i...")

# Open input image port
faceRecognitionDetection2D_portIn = yarp.BufferedPortImageRgb()
faceRecognitionDetection2D_portNameIn = '/facialRecognitionDetection2D/img:i'
faceRecognitionDetection2D_portIn.open(faceRecognitionDetection2D_portNameIn)

print("")
print("Opening image output port with name /facialRecognitionDetection2D/img:o...")

# Open output image port
faceRecognitionDetection2D_portOut = yarp.Port()
faceRecognitionDetection2D_portNameOut = '/facialRecognitionDetection2D/img:o'
faceRecognitionDetection2D_portOut.open(faceRecognitionDetection2D_portNameOut)

print("")
print("Opening data output port with name /facialRecognitionDetection2D/data:o...")

# Open output data port
faceRecognitionDetection2D_portOutDet = yarp.Port()
faceRecognitionDetection2D_portNameOutDet = '/facialRecognitionDetection2D/data:o'
faceRecognitionDetection2D_portOutDet.open(faceRecognitionDetection2D_portNameOutDet)

print("")
print("Opening data output port with name /facialRecognitionDetection2D/coord:o...")

# Open output coordinates data port
faceRecognitionDetection2D_portOutCoord = yarp.Port()
faceRecognitionDetection2D_portNameOutCoord = '/facialRecognitionDetection2D/coord:o'
faceRecognitionDetection2D_portOutCoord.open(faceRecognitionDetection2D_portNameOutCoord)

# Create data bootle
cmd=yarp.Bottle()

# Create coordinates bootle
coordinates=yarp.Bottle()

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

# Read people file databate and create dynamic array
peopleFile = open('../resources/peopleFiles.txt', 'r')
peopleFileLines = peopleFile.readlines()

countFiles = 0
peopleFiles = []

print("")
print("Reading people files database...")
print("")

for peopleFileLine in peopleFileLines:
    print("Line {}: {}".format(countFiles, peopleFileLine.strip()))
    countFiles=countFiles+1
    sourceImg="../database/"+peopleFileLine.strip()
    peopleFiles.append(sourceImg)

print(peopleFiles)

# Read people name databate and create dynamic array
peopleDataFile = open('../resources/peopleData.txt', 'r')
peopleDataFileLines = peopleDataFile.readlines()

countDataFiles = 0
peopleDataFiles = []

print("")
print("Reading people name database...")
print("")

for peopleDataFileLine in peopleDataFileLines:
    print("Line {}: {}".format(countDataFiles, peopleDataFileLine.strip()))
    countDataFiles=countDataFiles+1
    peopleDataFiles.append(peopleDataFileLine.strip())


print(peopleDataFiles)

print("")
print("Training people database...")
print("")

peopleDetection = []
peopleDetectionEncoding = []
countArray = 0

for people in peopleFileLines:

    print(peopleFiles[countArray])
    peopleDetection.append(face_recognition.load_image_file(peopleFiles[countArray]))
    peopleDetectionEncoding.append(face_recognition.face_encodings(peopleDetection[countArray])[0])
    countArray = countArray + 1

known_face_encodings = []

countArray2 = 0

for peopleKnown in peopleFileLines:
    known_face_encodings.append(peopleDetectionEncoding[countArray2])
    countArray2 = countArray2 +1


known_face_names = []

countArray3 = 0
for peopleKnownNames in peopleFileLines:
    known_face_names.append(peopleDataFiles[countArray3])
    countArray3 = countArray3 +1

print("")
print ('Waiting input image source...')
print("")



# Loop process
while True:

    # Recieve image source
    frame = faceRecognitionDetection2D_portIn.read()

    # Buffer processed image
    in_buf_image.copy(frame)
    assert in_buf_array.__array_interface__['data'][0] == in_buf_image.getRawImage().__int__()

    # YARP -> OpenCV
    rgb_frame = in_buf_array[:, :, ::-1]

    # Load known people
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    name = "None"
    # Process image for detection
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        # Compare known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)


        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
           name = known_face_names[best_match_index]
        else:  
           name = "Unknown"

        # Paint processed image
        cv2.rectangle(in_buf_array, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(in_buf_array, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(in_buf_array, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Get people coordinates
        x=left
        y=480-bottom

        #cv2.imshow('Video', in_buf_array)

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

        # Print processed data
        print ("\n")
        print ('Detection:')
        print (name)
        print("\n")
        print("Coordinates:")
        print("X: ", x)
        print("Y: ", y)

        # Sending processed detection
        cmd.clear()
        cmd.addString("Detection:")
        cmd.addString(name)
        faceRecognitionDetection2D_portOutDet.write(cmd)

        # Sending coordinates detection
        coordinates.clear()
        coordinates.addString("X: ")
        coordinates.addString(str(x))
        coordinates.addString("Y: ")
        coordinates.addString(str(y))
        faceRecognitionDetection2D_portOutCoord.write(coordinates)

        # Sending processed image
    print ('Sending processed image...')
    out_buf_array[:,:] = in_buf_array
    faceRecognitionDetection2D_portOut.write(out_buf_image)

print ('Closing ports...')
faceRecognitionDetection2D_portIn.close()
faceRecognitionDetection2D_portOut.close()
faceRecognitionDetection2D_portOutDet.close()
faceRecognitionDetection2D_portOutCoord.close()
#cv2.destroyAllWindows()
