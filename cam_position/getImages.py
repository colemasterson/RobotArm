import cv2


cap = cv2.VideoCapture(6)

num = 0

while cap.isOpened():

    succes, img = cap.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('C:/Users/maste/RobotArm/cam_position/calis/camX/image' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img 1',img)