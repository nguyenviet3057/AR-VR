import cv2
import mediapipe as mp
import time
import math
import pyautogui as pag
import os
import wave
import pyaudio
import speech_recognition as sr
from mutagen.mp3 import MP3
from threading import Thread
import threading

lst1 = ['break the rules', 'lovely', 'let me down slowly', 'bleeding love', 'someone you loved', 'what are words', 'we can\'t stop', '7 years', '2002', 'rockabye', 'saints', 'scared to be lonely', 'talk', 'treat you better', 'how to love', 'hero', 'how long', 'wolves', 'breathe', 'scars to your beautiful', 'savage love', 'locked away', 'melody', 'the river', 'the calling', 'fly away', 'save me', 'lonely together', 'shelter', 'faded', 'my heart', 'i do', 'double vision', 'the girl', 'one wish', 'bad liar', 'miss you more', 'redemption', 'knees', 'close to the sun', 'the ocean', 'pretty girl', 'i want you to know', 'walk through', 'fire', 'umbrella', 'end of time', 'the way i still love you', 'soul sister', 'trap queen', 'dusk till dawn', 'back to you', 'beautiful', 'different world', 'in the name of love', 'in your eyes', 'lily', 'lost control', 'memories', 'monsters', 'on my way', 'perfect', 'why do i']

lst2 = ['24h', 'bước qua mùa cô đơn', 'phải chăng em đã yêu', 'yêu một người có lẽ', 'đã lỡ yêu em nhiều', 'đi về nhà', 'gác lại âu lo', 'thanh xuân', 'trên tình bạn dưới tình yêu', 'tháng năm', 'một cú lừa', 'em không sai chúng ta sai', 'em bỏ hút thuốc chưa', 'ai đưa em về', 'cảm nắng', 'khó vẽ nụ cười', 'cô thắm không về', 'một phút', 'bạn tình ơi', 'bánh mì không', 'em ơi lên phố', 'sai lầm của anh', 'sao anh chưa về nhà', 'gió vẫn hát', 'bạc phận', 'hồng nhan', 'sao em vô tình', 'cưới nhau đi', 'cảm giác lúc ấy sẽ ra sao', 'anh ơi ở lại', 'đừng yêu nữa em mệt rồi', 'lạ lùng', 'cùng anh', 'bình yên nơi anh', 'buồn của anh', 'người lạ ơi', 'ánh nắng của anh']

endMusic = False
c = True

def PlayMusic(langType):
    lst = lst1 + lst2
    if langType == "en-EN":
        lst = lst1
        r = sr.Recognizer()
        mic = sr.Microphone()
        print(langType)
        print ('Speak now:')
    if langType == "vi-VN":
        lst = lst2
        r = sr.Recognizer()
        mic = sr.Microphone()
        print(langType)
        print ('Speak now:')

    global endMusic

    #Lặp n lần*
    while (not endMusic):

        print(endMusic)

        #Thu âm
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=1.0)
                r.phrase_threshold = 0.3
                r.pause_threshold = 0.6
                r.non_speaking_duration = 0.12
                audio = r.listen(source,10)
                
        except AssertionError:
            break

        #Kiểm tra khả năng Recognize: *thay đổi 'language' phù hợp
        check = -1
        try:
            rec = r.recognize_google(audio, language=langType, show_all=True)
        except sr.UnknownValueError:
            check = 0
        while check == 0:
            try:
                rec = r.recognize_google(audio, language=langType, show_all=True)
                check = 1
            except sr.UnknownValueError:
                print('RecError')
                check = 0

        #kiểm tra output
        print(rec)

        if rec != []:
        #Kiểm tra lst(list) trong rec(dict)
            check = 0
            for num1 in range(0,len(rec['alternative'])):
                for num2 in range(0,len(lst)):      
                    if lst[num2] in rec['alternative'][num1]['transcript'].lower():
                        # print('lst:',lst[num2].replace(' ','_')) #check
                        print(rec['alternative'][num1]['transcript'])
                        check = 1
                        os.startfile('F:\Python\Project\AR-VR\music\\' + lst[num2].replace(' ','_') + '.mp3')
                        file = MP3('F:\Python\Project\AR-VR\music\\' + lst[num2].replace(' ','_') + '.mp3')
                        duration = file.info.length
                        break
                if check == 1:
                    break
            if check == 0:
                # print('check == 0') #check
                for num1 in range(0,len(rec['alternative'])):
                    for num2 in range(0,len(lst)):
                        st = ''
                        ds = lst[num2].split(' ')
                        if len(ds)>2:
                            # print('len(ds): ' + str(len(ds)))
                            for i in range(0,len(ds)-2):
                                st += ds[i] + ' '
                            st += ds[len(ds)-2]
                        else:
                            # print('100000000')
                            st = ds[0]
                        if st in rec['alternative'][num1]['transcript'].lower():
                            # print('st:',st) #check
                            for num3 in range(0,len(lst)):
                                if st in lst[num3]:
                                    os.startfile('F:\Python\Project\AR-VR\music\\' + lst[num3].replace(' ','_') + '.mp3')
                                    file_mp3 = MP3('F:\Python\Project\AR-VR\music\\' + lst[num3].replace(' ','_') + '.mp3')
                                    duration = file_mp3.info.length
                                    break
                            break
                    break

            #Tạm dừng
        if check == 1:
            print(duration-10)
            time.sleep(duration-10)
            for num3 in range(0,10):
                print(10-num3,end=' | ')
                time.sleep(1)
            '''
            tts = gTTS(text='Chuyển bài hát',lang='vi')
            tts.save('notify.mp3')
            '''
        # os.system('start ting.mp3')
        time.sleep(1.5)
        print('------ Chuyển Bài Hát ------'.center(20))


pag.PAUSE = 0
pag.FAILSAFE = False

cap = cv2.VideoCapture(0) #Use "http://192.168.101.33:8080/video" for streaming from smartphone
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('P','I','M','1'))
cap.set(3,1920)
cap.set(4,1080)
cap.set(5,60)

mpHands = mp.solutions.hands #Start using hands tracking module // using mp.solutions.hands /.Hands /.process(img) /.multi_hand_landmarks /.landmark
hands = mpHands.Hands(static_image_mode=False,
               max_num_hands=1,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

TIMES = 0
pPosX = [0,0,0,0,0,0,0,0,80,0,0,0,80,0,0,0,0,0,0,0,0]
pPosY = [0,0,0,0,0,0,0,0,80,0,0,0,80,0,0,0,0,0,0,0,0]
cPosX = [0,0,0,0,0,0,0,0,80,0,0,0,80,0,0,0,0,0,0,0,0]
cPosY = [0,0,0,0,0,0,0,0,80,0,0,0,80,0,0,0,0,0,0,0,0]
check = False
compare = 0
near = 0
down = 0 #Counter for only choosing once per time
downMouse = 0
dX = 0
dY = 0
desWindow = 0

displayMenu = 0

onPlaying = 0

onChange = [0,0]
countChange = 0
pTime = time.time()
accept = 0 #Counter remove double click bugs

while True:
    check = False
    # closeHand = 1
    success, img = cap.read()
    img = cv2.flip(img, 1)

    h, w, c = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    if results.multi_hand_landmarks:
        closeHand = 1
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                
                #Decrease all the coordinates' oscillation
                for i in range(21):
                    if id == i:
                        cPosX[i] = int(lm.x*w)
                        cPosY[i] = int(lm.y*h)
                
                #Check if closeHand = True/False
                for i in range(2,5,1):
                    if cPosY[i*4]-cPosY[i*4-3] < 0:
                        closeHand = 0
                
                for i in range(21):
                    if abs(cPosX[i]-pPosX[i])>5 and abs(cPosY[i]-pPosY[i])>5:
                        if compare == 0:
                            dX = cPosX[4]-pPosX[4]
                            dY = cPosY[4]-pPosY[4]
                            compare = 1
                        check = True
                        break
                if check == False:
                    if compare == 1:
                        compare = 0
                    for i in range(21):
                        if id == i:
                            lm.x = pPosX[i]/w
                            lm.y = pPosY[i]/h
                        
                if check == True:
                    for i in range(21):
                        pPosX[i] = cPosX[i]
                        pPosY[i] = cPosY[i]
    
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    else:
        closeHand = 2

    if abs(pPosX[4]-pPosX[8])>=70 or abs(pPosY[4]-pPosY[8])>=70:
        # print("CHECK")
        cTime = time.time()
    if cTime != pTime:
        accept = 1
    else:
        accept = 0

    #Move mouse if not mouse control function
    # if displayMenu not in [21,22,111,121]:
    #     pag.moveTo(int((cPosX[4]+cPosX[8])/2),int((cPosY[4]+cPosY[8])/2))

    '''
        #Select Selections
    '''    
    #Selection 1
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(150,750) and cPosY[8] in range(100,200) and displayMenu == 0:
        if down == 0 and accept == 1:
            print("Play music")
            displayMenu = 1
            down = 1
            accept = 0
    else:
        down = 0
    #Selection 2
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(150,750) and cPosY[8] in range(250,350):
        if down == 0 and accept == 1 and displayMenu == 0:
            print("Control mouse")
            displayMenu = 2
            down = 1
            accept = 0
    else:
        down = 0


    '''
        #PLay musics
    '''
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(400,600) and cPosY[8] in range(250,350) and displayMenu == 1:
        if down == 0 and accept == 1:
            print("Play US-UK music")
            onPlaying = 1
            displayMenu = 11
            down = 1
            accept = 0
    else:
        down = 0
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(680,880) and cPosY[8] in range(250,350) and displayMenu == 1:
        if down == 0 and accept == 1:
            print("Play VN music")
            onPlaying = 1
            displayMenu = 12
            down = 1
            accept = 0
    else:
        down = 0
    #Need to seperate from above if because of display menu bug
    if displayMenu == 11:
        playMusic = threading.Thread(target=PlayMusic, args=("en-EN",)) #Remember this bug (easy to fix but spend so much time)
        playMusic.start()
        displayMenu = 111
    if displayMenu == 12:
        playMusic = threading.Thread(target=PlayMusic, args=("vi-VN",))
        playMusic.start()
        displayMenu = 121

    '''
        #{-}Auto return Main menu from Control mouse function choice{-}#
    '''
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(400,600) and cPosY[8] in range(250,350) and displayMenu == 2:
        if down == 0 and accept == 1:
            print("Hold")
            displayMenu = 21
            down = 1
            accept = 0
    else:
        down = 0
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(680,880) and cPosY[8] in range(250,350) and displayMenu == 2:
        if down == 0 and accept == 1:
            print("Auto")
            displayMenu = 22
            down = 1
            accept = 0
    else:
        down = 0
    '''
        #-Control mouse
    '''
    if displayMenu in [111,121] and closeHand == 1:
        print("Closed hand while playing music")
    if displayMenu in [21,22,111,121] and closeHand == 0:
        displayMenu = 21
        if abs(pPosX[4]-pPosX[8])<60 and abs(pPosY[4]-pPosY[8])<60:
            # print("MOVED")
            cMouX, cMouY = pag.position()

            if near == 0:
                fPosX = pPosX[4]-cMouX
                fPosY = pPosY[4]-cMouY
                near = 1

            if check == 1:
                pag.move(cPosX[4]-cMouX-fPosX,pPosY[4]-cMouY-fPosY) #??? if we set fPosX(Y) = pPosX(y)[4] only, then use pag.move(cPosX[4]-cMouX-(fPosX-cMouX),pPosY[4]-cMouY-(fPosY-cMouY)), the result is DIFFERENT - remember this to check later
        else:
            near = 0
        if abs(pPosX[4]-pPosX[12])<70 and abs(pPosY[4]-pPosY[12])<70:
            if downMouse == 0:
                # print("DOWN")
                pag.mouseDown()
                downMouse = 1 #Check later - Forgot this bug (from "down=1" to "downMouse=1")
        else:
            # print("UP")
            downMouse = 0
            pag.mouseUp()
    #Go back from Control mouse function (Hold -and- Auto)
    if displayMenu == 21 and closeHand == 1:
        print("Main menu")
        displayMenu = 0
        desWindow = 0 #Missing this line will appear a bug when do the second Control mouse function
    if displayMenu == 22 and closeHand != 0:
        print("Main menu")
        displayMenu = 0
        desWindow = 0 #Missing this line will appear a bug when do the second Control mouse function
    
    '''
        #Show FPS
        # cTime = time.time()
        # fps = 1/(cTime-pTime)
        # pTime = cTime
        # cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,255), 2)

        #Make fullscreen "Hand Tracking" window
        # cv2.namedWindow("Hand Tracking", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Hand Tracking",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    '''
    
    '''
        #Draw Selections
    '''
    if displayMenu == 0:
        cv2.rectangle(img, (150,100), (750,200), (0,255,0), 2)
        cv2.putText(img, "Voice command: Play music", (200,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
        cv2.rectangle(img, (150,250), (750,350), (0,255,0), 2)
        cv2.putText(img, "Hand tracking: Move mouse", (200,300), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
    if displayMenu == 1:
        cv2.rectangle(img, (400,250), (600,350), (0,255,255), 2)
        cv2.putText(img, "US-UK", (450,320), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
        cv2.rectangle(img, (680,250), (880,350), (0,255,255), 2)
        cv2.putText(img, "VPOP", (730,320), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
    if displayMenu == 2:
        cv2.rectangle(img, (400,250), (600,350), (0,255,255), 2)
        cv2.putText(img, "Hold", (450,320), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
        cv2.rectangle(img, (680,250), (880,350), (0,255,255), 2)
        cv2.putText(img, "Auto", (730,320), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)


    #Backward Selection
    if displayMenu in [1,11,12,111,121,2]:
        cv2.rectangle(img, (540,450), (700,510), (255,255,255), -1)
        cv2.putText(img, "Back", (580,490), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(540,700) and cPosY[8] in range(450,510):
        if down == 0 and accept == 1 and displayMenu == 1:
            print("Go back from Play music")
            # time.sleep(0.1)
            displayMenu = 0
            down = 1
            accept = 0
        if down == 0 and accept == 1 and displayMenu == 11:
            print("Go back from Play US-Uk music")
            # time.sleep(0.1)
            displayMenu = 1
            down = 1
            accept = 0
        if down == 0 and accept == 1 and displayMenu == 12:
            print("Go back from Play VN music")
            # time.sleep(0.1)
            displayMenu = 1
            down = 1
            accept = 0
        if down == 0 and accept == 1 and onPlaying == 1:
            # endMusic = True #NOT WORK
            os.system("TASKKILL /IM mpc-hc64.exe")
            playMusic.join(0.1)
            onPlaying = 0
            print("Go back from PLaying US-UK/VN music")
            endMusic = True
            print(endMusic)
            # time.sleep(0.5)
            displayMenu = 1
            down = 1
            accept = 0
        if down == 0 and accept == 1 and displayMenu == 2:
            print("Go back from Control mouse")
            # time.sleep(0.1)
            displayMenu = 0
            down = 1
            accept = 0
    else:
        down = 0

    #End Program #--->Note<---#
    if displayMenu == 0:
        cv2.rectangle(img, (150,400), (550,500), (255,255,255), -1)
        cv2.putText(img, "END PROGRAM", (200,470), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 3)
    if abs(pPosX[4]-pPosX[8])<70 and abs(pPosY[4]-pPosY[8])<70 and cPosX[8] in range(150,550) and cPosY[8] in range(400,500) and displayMenu == 0:
        print("End program")
        cv2.destroyAllWindows()
        #NEED to mute microphone for 10s instead of Speech recognition bug
        break

    #Hide/Show Hand tracking window when 2nd function selected
    if displayMenu in [21,22] and desWindow == 0:
        cv2.destroyWindow("Hand Tracking")
        desWindow = 1
    if displayMenu not in [21,22]:
        cv2.namedWindow("Hand Tracking", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Hand Tracking",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Hand Tracking", img) #show the result image
        
    #Check double click bugs
    if countChange == 0:
        onChange[0] = displayMenu
        countChange = 1
    else:
        onChange[1] = displayMenu
        countChange = 0
    if onChange[0] != onChange[1]:
        # print("CHANGE")
        pTime = time.time()
        cTime = pTime

    #-->Bug<--#May fixed
    # for i in range(10):
    #     endMusic - True
    endMusic = False
    # print(threading.enumerate())
    
    cv2.waitKey(1) #Necessary to run Hand tracking window
    if cv2.waitKey(5) & 0xFF == 27: #wait for input keyboard to end the program
        break
cap.release() #close the program
