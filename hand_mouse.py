import cv2
import mediapipe as mp
import pyautogui
import random
import time
import util
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Initialize Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

prev_x, prev_y = 0, 0  # For smoothing mouse movement

def move_mouse(index_finger_tip):
    global prev_x, prev_y
    if index_finger_tip is not None:
        x = int(index_finger_tip[0] * screen_width)
        y = int(index_finger_tip[1] * screen_height)

        # Smoothing
        smooth_x = prev_x + (x - prev_x) * 0.2
        smooth_y = prev_y + (y - prev_y) * 0.2
        pyautogui.moveTo(smooth_x, smooth_y)

        prev_x, prev_y = smooth_x, smooth_y

def is_left_click(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
        thumb_index_dist > 50
    )

def is_screenshot(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        thumb_index_dist < 50
    )

def is_double_click(landmarks_list, thumb_index_dist):
    return (
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 100 and
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 100 and
        thumb_index_dist < 30
    )

def detect_gestures(frame, landmarks_list):
    if len(landmarks_list) >= 21:
        index_finger_tip = landmarks_list[8]  # Index finger tip landmark is ID 8
        thumb_index_dist = util.get_distance(landmarks_list[4], landmarks_list[5])

        # Always move mouse
        move_mouse(index_finger_tip)

        # Gestures
        if is_left_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            time.sleep(0.2)  # Prevent rapid clicking

        elif is_right_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            time.sleep(0.2)

        elif is_double_click(landmarks_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            time.sleep(0.2)

        elif is_screenshot(landmarks_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            time.sleep(0.5)  # Screenshot delay

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return
    print("✅ Webcam opened successfully!")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

            detect_gestures(frame, landmarks_list)

            cv2.imshow('Hand Mouse Controller', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("👋 Quitting...")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
