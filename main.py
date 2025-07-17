import cv2
#pip install mediapipe
import mediapipe as mp
import math
#pip install pyserial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino #: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM"+str(com)):
        use = "COM"+ str(com)
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

cap = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

i=0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    RGB_Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_Frame)
    pt1x = 0
    pt1y = 0
    pt2x = 0
    pt2y = 0
    dist = 0
    oldDist = 0
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                if id == 4:
                    pt1x = int(landmark.x * w)
                    pt1y = int(landmark.y * h)
                if id == 8:
                    pt2x = int(landmark.x * w)
                    pt2y = int(landmark.y * h)
                    side1 = pt1x - pt2x
                    side2 = pt1y - pt2y
                    if side1<0:
                        side1 = -side1

                    if side2<0:
                        side2 = -side2

                    if side2 == 0:
                        dist = side1
                    elif side1 == 0:
                        dist = side2
                    else:
                        dist = math.sqrt((side1*side1)+(side2*side2))
        if dist>0:
            serialInst.write((str(dist)+"\n").encode('utf-8'))
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
    cv2.line(img=frame, pt1=(pt1x,pt1y), pt2=(pt2x,pt2y), color=(255,0,0), thickness=5, lineType=8, shift=0 )
    cv2.imshow("Webcame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()