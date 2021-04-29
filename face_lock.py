from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO

RELAY = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.output(RELAY,GPIO.LOW)

currentname = "unknown"
encodingsP = "encodings.pickle"
#The XML file I am using to help with identifying points with facial recognition
cascade = "haarcascade_frontalface_default.xml"

print("[INFO] Loading Files & Facial detection software...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

print("[INFO] Starting Video Display")

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

fps = FPS().start()

prevTime = 0
doorUnlock = True


while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    #Converts faces from BGR to Grayscale for face detection and from BGR to RGB for recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

   
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)


    # Box Coords
    
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    for encoding in encodings:

        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown" #if face is not recognized, then print Unknown

        
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            
            # to Unlock the door
            GPIO.output(RELAY,GPIO.LOW)
            prevTime = time.time()
            doorUnlock = True
            print("Door Unlocking...")

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            if currentname != name:
                currentname = name
                print(currentname)


        names.append(name)
        
        #Lock the door after 5 seconds
    if doorUnlock == True and time.time() - prevTime > 5:
        doorUnlock = False
        GPIO.output(RELAY,GPIO.HIGH)
        print("Door Locking...")

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (255, 0, 0), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()


fps.stop()
print("[INFO] Time Running: {:.2f}".format(fps.elapsed()))
print("[INFO] FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()