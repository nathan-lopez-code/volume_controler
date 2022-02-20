
def main():
    """ An main function of our application """
    width = 700
    heigth = 500
    run = True
    handD = HandTracking(min_confidence=0.7, max_confidence=0.9)
    vid = cv2.VideoCapture(0)
    vid.set(3, width), vid.set(4, heigth)       # change default dimension
    while run:
        succes, img = vid.read()
        img = handD.detectingHand(img, draw=False)
        listcoord = handD.positionPoint(img, draw=False)
        if len(listcoord) != 0:
            #print(listcoord[8], listcoord[4])
            x1, y1 = listcoord[4][1], listcoord[4][2]
            x2, y2 = listcoord[8][1], listcoord[8][2]
            cx, cy = (x1+x2)//2, (y1+y2)//2

            cv2.circle(img, (x1, y1), 7, (255, 0, 128), cv2.FILLED)
            cv2.circle(img, (x2, y2), 7, (255, 0, 128), cv2.FILLED)
            cv2.circle(img, (cx, cy), 5, (255, 0, 128), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (160, 160, 160), 2)

            dist = hypot(x2-x1, y2-y1)
            print(dist)

            if dist < 30:
                cv2.circle(img, (cx, cy), 5, (102, 102, 255), cv2.FILLED)

        show(img, "volume controler")

if __name__ == "__main__":

    from handTracking import HandTracking, show
    import mediapipe as mp
    import cv2
    from math import hypot
    from ctypes import cast, POINTER
    #from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, 7, None)

    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #     volume.GetMute()
    #     volume.GetMasterVolumeLevel()
    print(volume.GetVolumeRange())
    #     volume.SetMasterVolumeLevel(-20.0, None)
    #     main()
