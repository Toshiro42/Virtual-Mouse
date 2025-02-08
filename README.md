# Virtual-Mouse
This project utilizes MediaPipe's hand tracking to control the mouse cursor and system volume using hand gestures. The left hand is used for mouse functions such as movement and clicks, while the right hand adjusts the system volume by modifying the distance between the index finger and thumb.
Features

Mouse Control (Left Hand):

1. Move the cursor by moving the index finger.

2. Left-click by bringing the thumb and index finger together.

3. Right-click by bringing the thumb and middle finger together.

4. Open the on-screen keyboard by bringing the thumb and ring finger together.

Volume Control (Right Hand):

1. Adjust the system volume by changing the distance between the index finger and thumb.

2. Smooth transition of volume level display.

Requirements

1. Python 3.x

2. OpenCV (cv2)

3. MediaPipe (mediapipe)

4. PyAutoGUI (pyautogui)

5. NumPy (numpy)

6. Pycaw (pycaw) for audio control

Installation

Run the following command to install dependencies:

--> pip install opencv-python mediapipe pyautogui numpy pycaw comtypes

Usage

Run the script:

--> python hand_tracking_mouse.py

Controls:

Move the left hand’s index finger to move the cursor.

Tap the left-hand thumb and index finger to left-click.

Tap the left-hand thumb and middle finger to right-click.

Use the right-hand index finger and thumb to control the volume.

Troubleshooting

If the camera freezes, ensure your webcam is working properly and restart the script.

If volume control is not smooth, adjust the smoothing factor in the code.

Ensure proper lighting for accurate hand detection.

License

This project is open-source and can be modified or distributed freely.

Author

Developed by SUYASH YOGI  

