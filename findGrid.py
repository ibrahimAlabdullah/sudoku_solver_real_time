import cv2
import numpy as np
import solveMyS
import myNetowrk
#***************************************** biggest contour ****************************************************#

def cornerContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 *peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    if biggest.size != 0:
        biggest = sortCorner(biggest)
        #print(biggest)
        return biggest
        top_left = biggest[0][0]
        top_right = biggest[1][0]
        #bot_left = biggest[2][0]
        bot_right = biggest[3][0]

        if bot_right[1] - top_right[1] == 0:
            return []
        if not (0.95 < ((top_right[0] - top_left[0]) / (bot_right[1] - top_right[1])) < 1.05):
            return []
        return biggest

    return []

#***************************************** sort numbers ****************************************************#

def sortCorner(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew
#***************************************** predict numbers ****************************************************#
cls = myNetowrk.classify()

def getMyPredict(boxes):
    result = []
    for img in boxes:
        img = cv2.resize(img, (28, 28))
       #hog = cv2.HOGDescriptor(winSize, blockSize,  blockStride, cellSize, nbins)
        hog = cv2.HOGDescriptor((img.shape[1], img.shape[0]), (4, 4),  (4, 4), (2, 2), 5)
        locations = []
        hist = hog.compute(img, None, None, locations)
        hist = np.asarray(hist)
        print(hist.shape)
        hist = hist.reshape(1, -1)
        result.append(cls.predict(hist))
    return result
#********************************** Display Numbers ******************************************************

def displayNumber(imgWarp):
    numbers = np.multiply(posArray, board)
    for i in range(0, 9):
        for j in range(0, 9):
            if numbers[i][j] != 0:
                X = (j + 1) * int(widthImg / 9) - 35
                Y = (i + 1) * int(heightImg / 9) - 10
                cv2.putText(imgWarp, str(numbers[i][j]), (X, Y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2,cv2.LINE_8)

    # cv2.imshow('solved image', img)
    # cv2.waitKey(0)

    pts2 = np.float32(biggest)
    pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgInvWarp = cv2.warpPerspective(imgWarp, matrix, (widthImg, heightImg))
    # cv2.imshow('inv', img)
    # cv2.waitKey(0)
    pts2 = np.array([[pts2[0][0], pts2[2][0], pts2[3][0], pts2[1][0]]], dtype=np.int32)
    cv2.fillPoly(originalImage, pts2, 0)
    img = cv2.add(imgInvWarp, originalImage)

    return img

#********************************** Start ******************************************************
mask = cv2.imread('grids/mask.jpg',0)
cap = cv2.VideoCapture(0)
#cap.set(3,1270)
#cap.set(4,720)
#cap.set(10,150)
while True:
    success, imga = cap.read()
    # cv2.imshow('sd' , img)
    # cv2.waitKey(0)

    img = cv2.imread("grids/1.jpg")
    img = cv2.resize(img,(450,450))
    widthImg = img.shape[0]
    heightImg = img.shape[1]
    imgBigContour = img.copy()
    imgContours = img.copy()
    originalImage = img.copy()
    #cv2.imshow('original' ,originalImage)
    #cv2.waitKey(0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)

    contour, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(imgContours, contour, -1, (0, 255, 0), 3)
    #cv2.imshow('contor' , imgContours)
    #cv2.waitKey(0)
    biggest = cornerContour(contour)
    #print(biggest)
    #cv2.drawContours(img, biggest, -1, (0, 0, 255), 25)
    #cv2.imshow("Corner Detect",imgBigContour)
    #cv2.waitKey(0)
    if  len(biggest) == 4:
        #cv2.drawContours(img, biggest, -1, (0, 0, 255), 25)
        pts1 = np.float32(biggest)
        pts2 = np.float32([ [0, 0] , [widthImg , 0 ] , [ 0, heightImg] , [heightImg, widthImg]  ])
        perspectiv = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(img,perspectiv,(widthImg, heightImg))
        #cv2.imshow('CropedImage', img)
        #cv2.waitKey(0)

        rows = np.vsplit(imgWarp, 9)
        boxes = []
        for row in rows:
            cols = np.hsplit(row, 9)
            for box in cols:
                boxes.append(box)


        smallImages = []
        for box in boxes :
            box = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
            _,box = cv2.threshold(box , 0 ,255 , cv2.THRESH_OTSU)
            box = cv2.bitwise_or(box , mask)
            smallImages.append(box)

        result = getMyPredict(smallImages)
        board = np.asarray(result)
        board = board.reshape(9,9)

        posArray = np.where(board > 0, 0, 1)
        #print(board)
        #print('\n')

        #if solveMyS.is_valid(board) == False:
            #print("Sorry! Invalid.")
        pl = solveMyS.try_with_possibilities(board)
        is_done = solveMyS.is_solved(board)
        if is_done == True:
            img = displayNumber(imgWarp)
        else:
            new_list = solveMyS.run_assumption(board, pl)
            if new_list != False:
                is_done = solveMyS.is_solved(new_list)
                #print('is solved ? - ', is_done)
                #print(new_list)
                if is_done == True:
                    img = displayNumber(imgWarp)
                #else:
                    #print("Unable to solve by traditional ways")

    img = cv2.resize(img , (600,600))
    cv2.imshow('original solved', img)
    #cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
