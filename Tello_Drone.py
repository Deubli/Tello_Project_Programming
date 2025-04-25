import djitellopy
import cv2
import pygame
import time
import threading
import logging
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600, 400))
tello = djitellopy.Tello()
tello.connect()

control = False

forback = 0
leftright = 0
yaw = 0
updown = 0

back = False
left = False
forward = False
right = False

color = 0

red_lower = np.array([17, 15, 100], np.uint8)
red_upper = np.array([50, 56, 200], np.uint8)
blue_lower = np.array([86, 31, 4], np.uint8)
blue_upper = np.array([220, 88, 50], np.uint8)
yellow_lower = np.array([25, 146, 190], np.uint8)
yellow_upper = np.array([62, 174, 250], np.uint8)
orange_lower = np.array([15, 50, 200], np.uint8)
orange_upper = np.array([25, 100, 255], np.uint8)
green_lower = np.array([50, 50, 0], np.uint8)
green_upper = np.array([70, 255, 100], np.uint8)
purple_lower = np.array([120, 50, 100], np.uint8)
purple_upper = np.array([150, 150, 255], np.uint8)
def redDet():
    image = tello.get_frame_read().frame
    mask = cv2.inRange(tello.get_frame_read().frame, red_lower, red_upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    hasRed = np.sum(mask)
    if hasRed > 0:
        print('Red detected!')
    cv2.imshow("images", np.hstack([image, output]))
    
def blueDet():
    image = tello.get_frame_read().frame
    mask = cv2.inRange(tello.get_frame_read().frame, blue_lower, blue_upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    hasRed = np.sum(mask)
    if hasRed > 0:
        print('Blue detected!')
    cv2.imshow("images", np.hstack([image, output]))
def yellowDet():
    image = tello.get_frame_read().frame
    mask = cv2.inRange(tello.get_frame_read().frame, yellow_lower, yellow_upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    hasRed = np.sum(mask)
    if hasRed > 0:
        print('Yellow detected!')
    cv2.imshow("images", np.hstack([image, output]))
def orangeDet():
    image = cv2.cvtColor(tello.get_frame_read().frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(tello.get_frame_read().frame, orange_lower, orange_upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    hasRed = np.sum(mask)
    print(hasRed)
    if hasRed > 0:
        print('Orange detected!')
    cv2.imshow("images", np.hstack([image, output]))
def greenDet():
    image = cv2.cvtColor(tello.get_frame_read().frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(tello.get_frame_read().frame, green_lower, green_upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    hasRed = np.sum(mask)
    print(hasRed)
    if hasRed > 0:
        print('Green detected!')
    cv2.imshow("images", np.hstack([image, output]))
def purpleDet():
    image = cv2.cvtColor(tello.get_frame_read().frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(tello.get_frame_read().frame, purple_lower, purple_upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    hasRed = np.sum(mask)
    print(hasRed)
    if hasRed > 0:
        print('Purple detected!')
    cv2.imshow("images", np.hstack([image, output]))
tello.LOGGER.setLevel(logging.WARNING)
print("Battery:" + str(tello.get_battery()))
tello.streamon()
def move():
    while True:
        if(control == True):
            tello.send_rc_control(leftright, forback, updown, yaw)
def camera():
    while True:
        cv2.imshow("Video", tello.get_frame_read().frame)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
moveThr = threading.Thread(target=move)
cameraThr = threading.Thread(target=camera)
moveThr.start()
cameraThr.start()
while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if(e.key == pygame.K_w):
                forback = 25
                forward = True
            elif(e.key == pygame.K_a):
                leftright = -25
                left = True

            elif(e.key == pygame.K_s):
                forback = -25
                back = True
            elif(e.key == pygame.K_d):
                leftright = 25
                right = True
            elif(e.key == pygame.K_LEFT):
                yaw = -75
            elif(e.key == pygame.K_RIGHT):
                yaw = 75
            elif(e.key == pygame.K_DOWN):
                updown = -65
            elif(e.key == pygame.K_UP):
                updown = 65
            elif(e.key == pygame.K_SPACE):
                tello.takeoff()
                control = True
            elif(e.key == pygame.K_LCTRL):
                tello.land()
                control = False
            elif(e.key == pygame.K_BACKSPACE):
                tello.emergency()
                control = False
            elif(e.key == pygame.K_l):
                color += 1
                print(color)
            elif(e.key == pygame.K_k):
                color -= 1
                print(color)
            elif(e.key == pygame.K_f):
                print("A")
                if(color == 0):
                    redDet()
                if(color == 1):
                    blueDet()
                if(color == 2):
                    yellowDet()
                if(color == 3):
                    orangeDet()
                if(color == 4):
                    greenDet()
                if(color == 5):
                    purpleDet()
        elif e.type == pygame.KEYUP:
            if(e.key == pygame.K_w):
                forward = False
                if(back != True):
                    forback = 0
            elif(e.key == pygame.K_a):
                left = False
                if(right != True):
                    leftright = 0
            elif(e.key == pygame.K_s):
                back = False
                if(forward != True):
                    forback = 0
            elif(e.key == pygame.K_d):
                leftright = 0
                right = False
                if(left != True):
                    leftright = 0
            elif(e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT):
                yaw = 0
            elif(e.key == pygame.K_UP or e.key == pygame.K_DOWN):
                updown = 0
