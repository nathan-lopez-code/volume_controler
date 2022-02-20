import mediapipe as mp
import cv2


class HandTracking:

    def __init__(self, img_static=False, nb_hands=2, complexity=1,
                 min_confidence=0.5, max_confidence=0.5):
        self.img_static=img_static
        self.nb_hands = nb_hands
        self.complexity = complexity
        self.min_confidence = min_confidence
        self.max_confidence = max_confidence
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands()

    def detectingHand(self, img, draw=True):
        """detecting hand in img"""
        # transform image to the format color support by mediapipe
        imgTransform = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.detecting = self.hands.process(imgTransform)

        # let show if the program detected same thing with multi_hand_landmarks methode
        if self.detecting.multi_hand_landmarks:
            for hand in self.detecting.multi_hand_landmarks:
                # take all hand detected in image and shows it
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)

        return img

    def positionPoint(self, img, hand=0, point=0, draw=True, andPoint=False):
        listcoord = []
        pointcoord = []
        if self.detecting.multi_hand_landmarks:
            hand = self.detecting.multi_hand_landmarks[hand]
            # take the id point of the hand
            for mat, coord in enumerate(hand.landmark):
                height, width, chanel = img.shape
                # found the position of hand point mark in the image
                mat_x, mat_y = int(coord.x * width), int(coord.y*height)
                listcoord.append([mat, mat_x, mat_y])
                if draw:
                    cv2.circle(img, (mat_x, mat_y), 7, (244, 200, 0), cv2.FILLED)
                if mat == point:
                    pointcoord.append([mat_x, mat_y])
                    if draw:
                        cv2.circle(img, (mat_x, mat_y), 7, (245, 200, 0), cv2.FILLED)

        if andPoint:
            return listcoord, pointcoord
        else:
            return listcoord


def show(img, title="my capture video"):
    """this function alone to screening image"""
    cv2.imshow(title, img)
    cv2.waitKey(1)


def main():
    running = True
    vid = cv2.VideoCapture(0)
    # create on instance of the class hand tracking
    hand_detection = HandTracking()
    # the event loop
    while running:
        cool, img = vid.read()
        img = hand_detection.detectingHand(img, draw=False)
        listcoord, pointcoord = hand_detection.positionPoint(img, hand=1, point=4, draw=False)
        if len(listcoord) != 0 and len(pointcoord) != 0:
            print(listcoord[0])
            print("**************")
            print(pointcoord)

        # let show image
        show(img, title="hand tracking")


if __name__ == "__main__":
    main()
