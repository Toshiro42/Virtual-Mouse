import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

smoothening = 5
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
click_threshold = 30 

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol = volume.GetVolumeRange()[:2]

smooth_vol = 0

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_label = "Left" if results.multi_handedness[idx].classification[0].label == "Left" else "Right"
            
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))
            
            landmarks = hand_landmarks.landmark
            index_x, index_y = int(landmarks[8].x * frame.shape[1]), int(landmarks[8].y * frame.shape[0])
            thumb_x, thumb_y = int(landmarks[4].x * frame.shape[1]), int(landmarks[4].y * frame.shape[0])
            middle_x, middle_y = int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])
            ring_x, ring_y = int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])
            pinky_x, pinky_y = int(landmarks[20].x * frame.shape[1]), int(landmarks[20].y * frame.shape[0])

            if hand_label == "Left":
                mouse_x = (index_x / frame.shape[1]) * screen_width
                mouse_y = (index_y / frame.shape[0]) * screen_height
                curr_x = prev_x + (mouse_x - prev_x) / smoothening
                curr_y = prev_y + (mouse_y - prev_y) / smoothening
                pyautogui.moveTo(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

                # Left Click
                if math.dist((thumb_x, thumb_y), (index_x, index_y)) < click_threshold:
                    pyautogui.click()
                    cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 230, 0), 2)

                # Right Click
                if math.dist((thumb_x, thumb_y), (middle_x, middle_y)) < click_threshold:
                    pyautogui.rightClick()
                    cv2.putText(frame, "Right Click", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Open On-Screen Keyboard
                if math.dist((thumb_x, thumb_y), (ring_x, ring_y)) < click_threshold:
                    pyautogui.hotkey('win', 'ctrl', 'o')
                    cv2.putText(frame, "Opening Keyboard", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Open some shit man Idk
                if math.dist((thumb_x, thumb_y), (pinky_x, pinky_y)) < click_threshold:
                    pyautogui.hotkey('win', '3',)
                    cv2.putText(frame, "Opening Brave", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)    

            # Right Hand (Volume Control)
            elif hand_label == "Right":
                volume_distance = math.dist((index_x, index_y), (thumb_x, thumb_y))
                vol_level = np.interp(volume_distance, [20, 150], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol_level, None)
                
                smooth_vol = smooth_vol + (vol_level - smooth_vol) / 10 
                display_volume = int((smooth_vol - min_vol) / (max_vol - min_vol) * 100)
                
                cv2.putText(frame, f'Volume: {display_volume}%', 
                            (50, 50), cv2.QT_FONT_NORMAL, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Virtual Mouse & Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
