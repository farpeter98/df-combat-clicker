import pyautogui
import pyscreenshot
import time
import cv2
import numpy

# default window size on my system
dfWindowWidth = 1016
dfWindowHeight = 700
# center position (with topleft corner being 0,0) of the attack button with the above sizes
atkCenterX = 507
atkCenterY = 527
dfWindow = None

def setDFWindow():
    global dfWindow
    for window in pyautogui.getAllWindows():
        if (window.title == "" and window.height == dfWindowHeight and window.width == dfWindowWidth):
            dfWindow = window
            return
    # set window to None in case it was set previously
    dfWindow = None
    print("DragonFable window not found")

def compareImage(image, template, method = cv2.TM_CCORR_NORMED):
    result = cv2.matchTemplate(image, template, method)
    min_val, _, _, _ = cv2.minMaxLoc(result)
    return min_val

def snapshotToGrey(image):
    return cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2GRAY)

# abilities (excluding potions) are numbered from -7 to 7, 0 being attack
def clickAbility(number = 0):
    global isPlayerRound
    if dfWindow == None:
        print("Invalid ability click attempt")
        return 

    clickX = atkCenterX + dfWindow.topleft.x
    clickY = atkCenterY + dfWindow.topleft.y
    if number == 0:
        pyautogui.click(clickX, clickY)
        return

    # there are roughly 45 pixels between neighbouring abilities, 80 between the atk button and neighbouring abilities
    clickX += (numpy.sign(number) * 80) + (numpy.sign(number) * (abs(number) - 1) * 45)
    pyautogui.click(clickX, clickY)

def detectEnemyCount():
    # determine how many enemies there are based on hp
    topLeftX = 685 + dfWindow.topleft.x
    topLeftY = 640 + dfWindow.topleft.y
    bottomRightX = 726 + dfWindow.topleft.x
    bottomRightY = 654 + dfWindow.topleft.y
    snapshot = pyscreenshot.grab(bbox=(topLeftX, topLeftY, bottomRightX, bottomRightY))
    hp1val = compareImage(snapshotToGrey(snapshot), cv2.imread('patterns/hp1man.png', 0))
    hp2val = compareImage(snapshotToGrey(snapshot), cv2.imread('patterns/hp2man.png', 0))
    hp3val = compareImage(snapshotToGrey(snapshot), cv2.imread('patterns/hp3man.png', 0))
    max_value = max([hp1val, hp2val, hp3val])
    if max_value == hp1val:
        return 1
    elif max_value == hp2val:
        return 2
    else:
        return 3

def detectVictory():
    topLeftX = 340 + dfWindow.topleft.x
    topLeftY = 220 + dfWindow.topleft.y
    bottomRightX = 680 + dfWindow.topleft.x
    bottomRightY = 340 + dfWindow.topleft.y
    snapshot = pyscreenshot.grab(bbox=(topLeftX, topLeftY, bottomRightX, bottomRightY))
    min_val = compareImage(snapshotToGrey(snapshot), cv2.imread('patterns/hp1man.png', 0))
    return (min_val > 0.48 and min_val < 0.53)

def resolveCombat():
    # always start with Gambit
    clickAbility(-2)
    enemyCount = detectEnemyCount()
    # wait for Gambit animation
    time.sleep(1.5)

    # Cast ability and wait for animation to end    
    # Untangle vs solo
    if enemyCount == 1:
        clickAbility(7)
        time.sleep(4.5)
    # Dominance vs duo
    elif enemyCount == 2:
        clickAbility(2)
        time.sleep(4.5)
    # Soul Rip vs trio
    else:
        clickAbility(3)
        time.sleep(2.5)
    
    if not detectVictory():
        # Dragon attack
        clickAbility(2)
        time.sleep(2.5)
        # Player second round, can only happen vs duo or trio
        if not detectVictory():
            if enemyCount == 3:
                # Additional wait for enemy rounds
                time.sleep(2.5)
                clickAbility(2)
                time.sleep(3)
            else:
                # Wait for enemy to attack
                time.sleep(3)
                clickAbility(1)
                time.sleep(2)

def run():
    # Start quest and wait for it to start
    pyautogui.leftClick(690 + dfWindow.topleft.x, 275 + dfWindow.topleft.y)
    time.sleep(2.5)
    # P4WN enemies
    resolveCombat()
    # Get sicko rewards and loot, and accept them
    pyautogui.leftClick(520 + dfWindow.topleft.x, 430 + dfWindow.topleft.y)
    time.sleep(0.3)
    # Click close
    pyautogui.leftClick(520 + dfWindow.topleft.x, 530 + dfWindow.topleft.y)
    # Wait for data to get saved
    time.sleep(1)
    # Accept quest item reward
    pyautogui.leftClick(520 + dfWindow.topleft.x, 530 + dfWindow.topleft.y)
    # Wait to save again
    time.sleep(1.5)

def main():
    # A little time to switch tabs
    time.sleep(2)
    setDFWindow()
    counter = 0
    while True:
        run()
        counter += 1
        print("Defeated " + str(counter) + " total")

if __name__ == '__main__':
    main()