import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

class VirtualMouse:
    def __init__(self):
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Camera dimensions
        self.cam_width, self.cam_height = 640, 480
        
        # Smoothing factor for cursor movement
        self.smoothing = 7
        self.prev_x, self.prev_y = 0, 0
        
        # Click detection variables
        self.click_threshold = 40
        self.click_cooldown = 0.5
        self.last_click_time = 0
        
        # Disable pyautogui failsafe
        pyautogui.FAILSAFE = False
        
    def get_landmark_position(self, landmarks, landmark_id):
        """Get normalized position of a specific landmark"""
        landmark = landmarks.landmark[landmark_id]
        return landmark.x, landmark.y
    
    def calculate_distance(self, point1, point2):
        """Calculate distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def smooth_movement(self, x, y):
        """Apply smoothing to cursor movement"""
        smooth_x = self.prev_x + (x - self.prev_x) / self.smoothing
        smooth_y = self.prev_y + (y - self.prev_y) / self.smoothing
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return int(smooth_x), int(smooth_y)    

    def run(self):
        """Main loop for virtual mouse"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_height)
        
        print("Virtual Mouse Started!")
        print("Controls:")
        print("- Move your index finger to control cursor")
        print("- Bring thumb and index finger close together to click")
        print("- Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process hand landmarks
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Get key landmarks
                    index_tip = self.get_landmark_position(hand_landmarks, 8)  # Index finger tip
                    thumb_tip = self.get_landmark_position(hand_landmarks, 4)  # Thumb tip
                    
                    # Convert to screen coordinates
                    screen_x = int(index_tip[0] * self.screen_width)
                    screen_y = int(index_tip[1] * self.screen_height)
                    
                    # Apply smoothing
                    smooth_x, smooth_y = self.smooth_movement(screen_x, screen_y)
                    
                    # Move cursor
                    pyautogui.moveTo(smooth_x, smooth_y)
                    
                    # Calculate distance between thumb and index finger for click detection
                    distance = self.calculate_distance(thumb_tip, index_tip)
                    distance_pixels = distance * self.cam_width
                    
                    # Click detection
                    current_time = time.time()
                    if (distance_pixels < self.click_threshold and 
                        current_time - self.last_click_time > self.click_cooldown):
                        pyautogui.click()
                        self.last_click_time = current_time
                        print("Click detected!")
                    
                    # Visual feedback
                    cv2.circle(frame, 
                             (int(index_tip[0] * self.cam_width), 
                              int(index_tip[1] * self.cam_height)), 
                             10, (0, 255, 0), -1)
                    
                    cv2.circle(frame, 
                             (int(thumb_tip[0] * self.cam_width), 
                              int(thumb_tip[1] * self.cam_height)), 
                             10, (255, 0, 0), -1)
                    
                    # Show click status
                    if distance_pixels < self.click_threshold:
                        cv2.putText(frame, "CLICKING", (50, 50), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display frame
            cv2.imshow('Virtual Mouse', frame)
            
            # Exit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    virtual_mouse = VirtualMouse()
    virtual_mouse.run()