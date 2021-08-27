import win32gui, win32ui, win32con, win32api
import time
import sys


def getDFWindow():
    return win32gui.FindWindow(None, "Adobe Flash Player 32,0,0,465")

def click(handle, x, y):
    if handle == 0:
        print("Window not set")
        return

    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, 0, lParam)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

def clickSpikes(handle):
    click(handle, 230, 460)
    time.sleep(3)

def moveTop(handle):
    click(handle, 220, 350)

def moveBottom(handle):
    click(handle, 200, 420)

def startWave(handle):
    click(handle, 600, 400)
    time.sleep(3)

def getScreengrabBuffer(handle, left, top, right, bot):
    if handle == 0:
        print("Window not set")
        return

    width = right-left
    height = bot-top

    hdc = win32gui.GetWindowDC(handle)
    srcdc = win32ui.CreateDCFromHandle(hdc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    buffer = bmp.GetBitmapBits(True)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(handle, hdc)
    win32gui.DeleteObject(bmp.GetHandle())

    return buffer

def isCorrectPlatform(handle):
    if handle == 0:
        print("Window not set")
        return

    buffer = getScreengrabBuffer(handle, 190, 90, 220, 105)
    for val in buffer:
        if val != 255:
            return False
    return True

def isRareWave(handle):
    if handle == 0:
        print("Window not set")
        return
    
    buffer = getScreengrabBuffer(handle, 390, 330, 400, 340)
    i = 0
    while i < len(buffer):
        if buffer[i] != 166:
            return False
        i = i + 1
        if buffer[i] != 206:
            return False
        i = i + 1
        if buffer[i] != 234:
            return False
        i = i + 1
        if buffer[i] != 255:
            return False
        i = i + 1
    return True

def clickContinue(handle):
    click(handle, 390, 380)
    time.sleep(1)

def clickClose(handle):
    click(handle, 390, 460)

def finishWave(handle):
    clickClose(handle)
    #print("Closed end")
    time.sleep(1)
    clickClose(handle)
    #print("Got medal")
    time.sleep(3)

def defeatEnemy(handle):
    if isCorrectPlatform(handle):
        clickSpikes(handle)
        clickContinue(handle)
        return

    moveTop(handle)
    time.sleep(0.5)
    if isCorrectPlatform(handle):
        clickSpikes(handle)
        return
    
    moveBottom(handle)
    time.sleep(0.5)
    clickSpikes(handle)
    return

def defeatWave(handle):
    print("Wave started")
    #print("Enemy #1")
    defeatEnemy(handle)
    time.sleep(1)
    clickContinue(handle)
    if(isRareWave(handle)):
        print("Rare wave")
        finishWave(handle)
        return
    for _ in range(4):
        time.sleep(1)
        #print("Enemy #" + str(i + 2))
        defeatEnemy(handle)
        clickContinue(handle)
    finishWave(handle)

def main():
    medals = int(sys.argv[1])
    dfWind = getDFWindow()
    while medals < 9999:
        startWave(dfWind)
        defeatWave(dfWind)
        medals = medals + 1
        print("Total medals: " + str(medals))

if __name__ == '__main__':
    main()
