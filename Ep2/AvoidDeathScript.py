#! python3

from PIL import ImageGrab, Image
import time, pyautogui, threading

backButtonPosX = 662
backButtonPosY = 604
backButtonWidth = 600
backButtonHeight = 60 #from screenshot

screenCenterX = 960 #half of the screen res

backButtonImage = Image.open('./backButton.bmp').load() #Open the image file saved with saveButtonImage() function

connectButtonX = 580
connectButtonY = 360 #from screenshot

failCounter = 0

failInterval = 5 #in seconds
checkInterval = 5 #in seconds

isConnected = 1
exitFlag = False

imageGray = Image.open('./imageGray.bmp').load()
imageRed = Image.open('./imageRed.bmp').load()

heartStartX = 704
heartXDistance = 24
heartCenterY = 820 #from screenshot

quitButtonY = 730 #from screenshot

#def saveButtonImage():
#    tempIm = ImageGrab.grab(bbox=(backButtonPosX, backButtonPosY, backButtonPosX + backButtonWidth, backButtonPosY + backButtonHeight))
#    tempIm.save('./backButton.bmp', 'bmp')
#Use this function to save the back button's image to the current folder.

def compareImage(imageA, imageB, width, height):
    difference = 0
    for x in range(0, int(width / 2)):
        for y in range(0, int(height / 2)):
            (rA, gA, bA) = imageA[x*2, y*2]
            (rB, gB, bB) = imageB[x*2, y*2]
            difference += ((rA - rB) ** 2) + ((gA - gB) ** 2) + ((bA - bB) ** 2)
    #print(difference)
    return difference
#the method used to compare the image is sum up the squre of difference of each px's RGB value.

def reconnect(shift):
    backButtonCenterY = backButtonPosY + backButtonHeight / 2 + shift
    pyautogui.moveTo(screenCenterX, backButtonCenterY, 0.5)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.moveTo(connectButtonX, connectButtonY, 0.5)
    time.sleep(0.1)
    pyautogui.click()
#this will move the cursor and click the buttons

def isDisconnected():
    for i in range(0, 60):
        tempIm = ImageGrab.grab(bbox=(backButtonPosX, backButtonPosY + i, backButtonPosX + backButtonWidth, backButtonPosY + backButtonHeight + i)).load()
        result = compareImage(backButtonImage, tempIm, backButtonWidth, backButtonHeight)
        if result < 8192:
            tempIm = None
            return i + 1
    tempIm = None
    return 0
#this will check if the back button is there, if it is there, how much it moved downward.

def compareImageSlow(imageA, imageB, width, height):
    difference = 0
    for x in range(0, width):
        for y in range(0, height):
            (rA, gA, bA) = imageA[x, y]
            (rB, gB, bB) = imageB[x, y]
            difference += ((rA - rB) ** 2) + ((gA - gB) ** 2) + ((bA - bB) ** 2)
    #print(difference)
    return difference

def checkHealth():
    health = 0
    healthLose = 0
    for i in range(0,10):
        tempIm = ImageGrab.grab(bbox=(i * heartXDistance + heartStartX, heartCenterY, i * heartXDistance + heartStartX + 2, heartCenterY + 2)).load()
        if compareImageSlow(imageRed, tempIm, 2, 2) <= 1024:
            health += 1
        if compareImageSlow(imageGray, tempIm, 2, 2) <= 1024:
            healthLose += 1
    #print('health:' + str(health))
    #print('healthLose:' + str(healthLose))
    if (health + healthLose) == 10:
        return health
    return 10

def disconnect():
    pyautogui.keyDown('esc')
    pyautogui.moveTo(screenCenterX, quitButtonY)
    time.sleep(0.01)
    pyautogui.keyUp('esc')
    time.sleep(0.1)
    pyautogui.click()

class threadHealthCheck (threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self)
    def run(self):
        global isConnected
        global exitFlag
        while not exitFlag:
            #print(isConnected)
            if isConnected == 1:
                if checkHealth() < 8:
                    disconnect()
                    isConnected = 0
                    exitFlag = True
                    failCounter = 9
                    print(time.strftime("Get attacked at %Y-%m-%d, %H:%M:%S, Disconnect.", time.localtime()))
                time.sleep(0.1)
            else:
                time.sleep(1)

def main():
    global exitFlag
    global failCounter
    failCounter = 0
    counter = 0

    healthChkThd = threadHealthCheck()
    healthChkThd.start()

    try:
        print('Auto AFK started, press Ctrl+C to quit.')
        while failCounter <= 5:
            buttonShift = isDisconnected()
            if buttonShift and failCounter <= 5:
                failCounter += 1
                isConnected = 0
                if failCounter > 5:
                    print('Failled to connect too many times.')
                    break #stop checking after five fails
                counter = 5
                print(time.strftime("Disconnected at %Y-%m-%d, %H:%M:%S", time.localtime()))
                time.sleep(1)
                print('Reconnect attempt #' + str(failCounter) + ', next attempt after ' + str(failCounter * failInterval) + ' seconds...')
                print('')
                reconnect(buttonShift)
                isConnected = 1
                time.sleep(failInterval * failCounter)
            elif counter > 0:
                counter -= 1
                time.sleep(checkInterval)
                if counter == 0:
                    failCounter = 0;
                    print('Fail counter reset.')# this reset the fail counter if successfully connect to the server for amount of time.
            else:
                time.sleep(checkInterval)
        exitFlag = True
        print('Press Ctrl+C to quit.')
        while True:
            pass
    except KeyboardInterrupt:
        print('Terminating...')
        time.sleep(0.5)

if __name__ == '__main__':
    main()
