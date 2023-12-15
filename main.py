import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import os

detector = PoseDetector()
cap = cv2.VideoCapture("videos/1.mp4")

imgList = os.listdir("images")

tshritNo = 0

widthShirt = 440
heightShirt = 580

# fixRatio = 262/190
# shirtRatioHightWidth = 580/440

buttonLeft = cv2.imread("button.png", cv2.IMREAD_UNCHANGED)
buttonRight = cv2.flip(buttonLeft, 1)
counterRight = 0
selectionSpeed = 10
counterLeft = 0

while True:

    success, img = cap.read()
    tshirt = cv2.imread("images/"+imgList[tshritNo], cv2.IMREAD_UNCHANGED)
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(
        img, draw=True, bboxWithHands=False)

    if lmList:

        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        lm10 = lmList[10][0:2]
        lm23 = lmList[23][0:2]

        # widthOfTishrt = int((lm11[0]-lm12[0])*fixRatio)

        # tshirt = cv2.resize(
        #     tshirt, (widthOfTishrt, int(widthOfTishrt*shirtRatioHightWidth)))

        widthOfTishrt = int(
            (((lm11[0]-lm12[0])/widthShirt) * (lm11[0]-lm12[0]))+(lm11[0]-lm12[0]))

        tshirt = cv2.resize(
            tshirt, (widthOfTishrt, int(lm23[1]-lm11[1]+80)))

        # currentScale = (lm11[0] - lm12[0]) / 190

        # offset = int(44 * currentScale), int(48 * currentScale)

        # img = cvzone.overlayPNG(
        #     img, tshirt, (lm12[0] - offset[0], lm12[1] - offset[1]))

        # print(int((lm12[1]-lm10[1])*2/3))
        x = int((lm12[1]-lm10[1])*2/3)
        y = int((lm12[1]-lm10[1])*1/3)
        img = cvzone.overlayPNG(
            img, tshirt, (lm12[0]-x, lm12[1]-y))

    cvzone.overlayPNG(img, buttonRight, (100, 250))
    cvzone.overlayPNG(img, buttonLeft, (1100, 250))

    if lmList[16][0] < 300:
        counterRight += 1
        cv2.ellipse(img, (160, 310), (66, 66), 0, 0,
                    counterRight * selectionSpeed, (0, 255, 0), 20)

        if (counterRight*selectionSpeed > 360):
            counterRight = 0
            if (len(imgList) > tshritNo+1):
                tshritNo += 1

    elif lmList[15][0] > 1000:
        counterLeft += 1
        cv2.ellipse(img, (1160, 310), (66, 66), 0, 0,
                    counterLeft * selectionSpeed, (0, 255, 0), 20)

        if (counterLeft*selectionSpeed > 360):
            counterLeft = 0
            if (tshritNo > 0):
                tshritNo -= 1
    else:
        counterRight = 0
        counterLeft = 0
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
