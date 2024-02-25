# importing necessary modules
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(1)  # Set your camera appropriately by changing count Ex: 0


# defining a class for hand tracking
class handDetector():
    # initializing class
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(self.detectionCon), self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils

    # find hand and draw landmarks
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

        return img


while True:
    ret, img = cap.read()

    hand = handDetector()
    img = hand.findHands(img)

    cv2.imshow("Detecting", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()