#! python3

from PIL import ImageGrab, Image
import time, pyautogui

backButtonPosX = 662
backButtonPosY = 604
backButtonWidth = 600
backButtonHeight = 60
backButtonCenterX = 960 #half of the screen res

backButtonImage = Image.open('./backButton.png').load() #Open the image file saved with saveButtonImage() function

connectButtonX = 580
connectButtonY = 360

failInterval = 5 #in seconds
checkInterval = 5 #in seconds

#def saveButtonImage():
#    tempIm = ImageGrab.grab(bbox=(backButtonPosX, backButtonPosY, backButtonPosX + backButtonWidth, backButtonPosY + backButtonHeight))
#    tempIm.save('./backButton.png', 'png')
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
    pyautogui.moveTo(backButtonCenterX, backButtonCenterY, 0.5)
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
            #print(i)
            return i + 1
    tempIm = None
    return 0
#this will check if the back button is there, if it is there, how much it moved downward.

def main():
    failCounter = 0
    counter = 0
    try:
        print('Auto AFK started, press Ctrl+C to quit.')
        while failCounter <= 5:
            buttonShift = isDisconnected()
            if buttonShift and failCounter <= 5:
                failCounter += 1
                if failCounter > 5:
                    break #stop checking after five fails
                counter = 5
                print(time.strftime("Disconnected at %Y-%m-%d, %H:%M:%S", time.localtime()))
                time.sleep(1)
                print('Reconnect attempt #' + str(failCounter) + ', next attempt after ' + str(failCounter * failInterval) + ' seconds...')
                print('')
                reconnect(buttonShift)
                time.sleep(failInterval * failCounter)
            elif counter > 0:
                counter -= 1
                time.sleep(checkInterval)
                if counter == 0:
                    failCounter = 0;
                    print('Fail counter reset.')# this reset the fail counter if successfully connect to the server for amount of time.
            else:
                time.sleep(checkInterval)
        print('Failled to connect too many times.')
        print('Press Ctrl+C to quit.')
        while True:
            pass
    except KeyboardInterrupt:
        print('Terminating...')
        time.sleep(0.5)

if __name__ == '__main__':
    main()
