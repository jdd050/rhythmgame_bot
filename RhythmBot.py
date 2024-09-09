"""RhythmBot.py
This application can automate the rhythm game found in the fishing section of the game 'HoloCure'
"""

import cv2
import numpy as np
import mss
from tkinter.messagebox import showinfo
import pynput.keyboard as kb
import pynput.mouse as mouse

class Main:
    """Main
    - The main class of the program.
    - Contains all member functions and data.
    """
    # Initialize mouse and keyboard listeners/controllers
    def __init__(self):
        self.keyboard = kb.Controller()
        self.mouse_output = mouse.Controller()
        self.num_clicks = 0
        self.region = []
    
    # Logic to handle click inputs
    def on_click(self, x, y, button, pressed) -> bool:
        if pressed and self.num_clicks < 2:
            print(f"Mouse clicked at ({x}, {y}) with {button}")
            self.num_clicks += 1
            self.region.append((x,y))
            # Stop listener if 2 clicks have been registered
            if self.num_clicks >= 2:
                print("Two clicks have been registered. Stopping listener.")
                return False
            return True
    
    # Capture the region of the screen where the game is located
    def capture_screen_region(self):
        # Check that two points have been set
        if len(self.region) < 2:
            print("Insufficient region data, unable to capture.")
            return None
        
        # Calculate the bounding box for the screen capture
        x1, y1 = self.region[0]
        x2, y2 = self.region[1]
        bbox = {'top': min(y1, y2), 'left': min(x1, x2), 'width': abs(x2 - x1), 'height': abs(y2 - y1)}
        
        # Use mss to capture the specified region
        with mss.mss() as sct:
            screenshot = sct.grab(bbox)
            img = np.array(screenshot)
            return img
    
    
        # Analyze the captured image for shapes
    def analyze_shapes(self, img):
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to smooth edges
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Use Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours in the edged image
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze each contour to determine its shape
        for contour in contours:
            # Approximate the contour shape
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Determine the shape
            if len(approx) == 3:
                shape = "Triangle"
            elif len(approx) == 4:
                shape = "Rectangle"
            elif len(approx) > 4:
                shape = "Circle"
            else:
                shape = "Unknown"
            
            print(f"Detected shape: {shape}")
            # Perform actions based on detected shapes
    
    # Listen to 2 (two) mouse clicks to let the user determine where OpenCV should look for rhythm game
    def get_monitor_region(self):
        # Ask user for two locations on screen to determine region for OpenCV
        showinfo("Rhythm Game Location", "Please click two locations to form a rectangle around the rhythm game.")
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
        return 0
    
    # Set up OpenCV to analyze the region
    def setup_opencv(self):
        print(self.region)
        img = self.capture_screen_region()
        if img is not None:
            self.analyze_shapes(img)

instance = Main()
instance.get_monitor_region()
instance.setup_opencv()
