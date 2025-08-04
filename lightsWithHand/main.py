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

#i=0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    RGB_Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_Frame)
    ptThumbx = 0
    ptThumby = 0
    ptIndexx = 0
    ptIndexy = 0
    dist = 0
    fingerDist = 0
    scaledDist = 0
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                if id == 0:
                    ptPalmx = landmark.x #* w)
                    ptPalmy = landmark.y#* h)
                    ptPalmz = landmark.z

                if id == 4:
                    ptThumbx = landmark.x #* w)
                    ptThumby = landmark.y#* h)
                    ptThumbz = landmark.z
                if id == 5:
                    ptUnderIndexx = landmark.x #* w)
                    ptUnderIndexy = landmark.y#* h)
                    ptUnderIndexz = landmark.z
                if id == 8:
                    ptIndexx = landmark.x #* w)
                    ptIndexy = landmark.y#* h)
                    ptIndexz = landmark.z
                

                    dist = math.sqrt((ptThumbx - ptIndexx)**2 + (ptThumby - ptIndexy)**2 + (ptThumbz - ptIndexz)**2)
                    handScale = math.sqrt((ptPalmx - ptUnderIndexx)**2 + (ptPalmy - ptUnderIndexy)**2 + (ptPalmz - ptUnderIndexz)**2)
                    fingerDist = dist/handScale

                    clamped = max(min(fingerDist,1.20),0.15)
                    scaledDist = 100 * ((clamped - 0.15)/(1.20 - 0.15)) 

                    print(str(fingerDist))
                    print(str(scaledDist))


        if dist>0:
            serialInst.write((str(scaledDist)+"\n").encode('utf-8'))
           
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
    cv2.line(img=frame, pt1=(int(ptThumbx*w),int(ptThumby*h)), pt2=(int(ptIndexx*w),int(ptIndexy*h)), color=(255,0,0), thickness=5, lineType=8, shift=0 )
    cv2.putText(frame, str(round(scaledDist,2)),(5,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
    cv2.imshow("Webcame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()