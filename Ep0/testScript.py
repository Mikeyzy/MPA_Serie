#! python3
from PIL import ImageGrab
from time import sleep
import win32api, pyautogui, random
#import packages

screenW = win32api.GetSystemMetrics(0)
screenH = win32api.GetSystemMetrics(1)
centerX = screenW / 2
centerY = screenH / 2
#get screen size and center pos

def printCenterPxColor():
    tempIm = ImageGrab.grab(bbox=(centerX, centerY, centerX + 1, centerY + 1)).load()
    print("Screen Center Color " + str(tempIm[0,0]))
#output center px color

def moveMouse():
    randomX = random.randint(100, screenW - 100)
    randomY = random.randint(100, screenH - 100)
    pyautogui.moveTo(randomX, randomY, 0.25)
    print("Moved to " + str(pyautogui.position()))
#randomly move the cursor

while True:
    printCenterPxColor()
    moveMouse()
    sleep(1)
    #infinite loop
