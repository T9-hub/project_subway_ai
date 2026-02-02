import cv2
from math import hypot
import mediapipe as mp

# เริ่มต้นคลาส mediapipe pose เพื่อใช้ landmark constants
mp_pose = mp.solutions.pose

def checkHandsJoined(image, results, draw=False, display=False):
    '''
    ฟังก์ชันตรวจสอบว่ามือของผู้เล่นประสานกันหรือไม่ (ใช้สำหรับเริ่มเกม/Resume เกม)
    
    Args:
        image:   ภาพ input
        results: ผลลัพธ์จาก mediapipe pose detection
        draw:    ถ้า True จะวาดสถานะลงบนภาพ
        display: ถ้า True จะแสดงผลภาพ (debug)
    
    Returns:
        output_image: ภาพผลลัพธ์
        hand_status:  ข้อความสถานะ ('Hands Joined' หรือ 'Hands Not Joined')
    '''
    
    height, width, _ = image.shape
    output_image = image.copy()
    
    # หาพิกัดข้อมือซ้าย (Left Wrist)
    left_wrist_landmark = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width,
                          results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)

    # หาพิกัดข้อมือขวา (Right Wrist)
    right_wrist_landmark = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width,
                           results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)
    
    # คำนวณระยะห่างระหว่างข้อมือทั้งสอง (Euclidean distance)
    euclidean_distance = int(hypot(left_wrist_landmark[0] - right_wrist_landmark[0],
                                   left_wrist_landmark[1] - right_wrist_landmark[1]))
    
    # ถ้าค่าระยะห่างน้อยกว่า 130 ถือว่ามือประสานกัน
    if euclidean_distance < 130:
        hand_status = 'Hands Joined'
        color = (0, 255, 0) # สีเขียว
    else:
        hand_status = 'Hands Not Joined'
        color = (0, 0, 255) # สีแดง
        
    # วาดข้อความสถานะและระยะห่างบนภาพ
    if draw:
        cv2.putText(output_image, hand_status, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        cv2.putText(output_image, f'Distance: {euclidean_distance}', (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        
    return output_image, hand_status

def checkLeftRight(image, results, draw=False, display=False):
    '''
    ฟังก์ชันตรวจสอบตำแหน่งของคนในแนวแกน X (ซ้าย, กลาง, ขวา)
    เพื่อใช้ควบคุมการเคลื่อนที่ซ้าย-ขวาในเกม
    '''
    
    horizontal_position = None
    height, width, _ = image.shape
    output_image = image.copy()
    
    # หาพิกัดไอน์แกน X ของไหล่ขวา (Right Shoulder)
    left_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)

    # หาพิกัดในแกน X ของไหล่ซ้าย (Left Shoulder)
    right_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)
    
    # ตรวจสอบตำแหน่งเทียบกับกึ่งกลางภาพ (width // 2)
    
    # หากทั้งสองไหล่อยู่ทางซ้ายของเส้นกลาง
    if (right_x <= width//2 and left_x <= width//2):
        horizontal_position = 'Left'

    # หากทั้งสองไหล่อยู่ทางขวาของเส้นกลาง
    elif (right_x >= width//2 and left_x >= width//2):
        horizontal_position = 'Right'
    
    # หากไหล่คร่อมเส้นกลาง (ตัวอยู่ตรงกลาง)
    elif (right_x >= width//2 and left_x <= width//2):
        horizontal_position = 'Center'
        
    if draw:
        # ตรงนี้คือส่วนแสดงคำว่า Left / Right / Center
        # ใช้ cv2.FONT_HERSHEY_PLAIN (ฟอนต์มาตรฐานของ OpenCV)
        # ถ้าอยากเปลี่ยนเป็นแบบ Modern ต้องเอาจัวแปร put_text_modern เข้ามาทำในนี้แทนครับ
        cv2.putText(output_image, horizontal_position, (5, height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.line(output_image, (width//2, 0), (width//2, height), (255, 255, 255), 2)
        
    return output_image, horizontal_position

def checkJumpCrouch(image, results, MID_Y=250, draw=False, display=False):
    '''
    ฟังก์ชันตรวจสอบท่าทางแนวตั้ง (กระโดด, ย่อตัว, หรือยืนตรง)
    โดยเทียบกับค่า MID_Y ที่เก็บไว้ตอนเริ่มเกม
    '''
    
    height, width, _ = image.shape
    output_image = image.copy()
    
    # หาพิกัดแกน Y ของไหล่สองข้าง
    left_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)
    right_y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)

    # หาจุดกึ่งกลางความสูงของไหล่ปัจจุบัน
    actual_mid_y = abs(right_y + left_y) // 2
    
    # กำหนดขอบเขตบนและล่างสำหรับการตัดสินใจ
    lower_bound = MID_Y - 15  # ถ้ายกไหล่สูงกว่านี้ (ค่า y น้อยกว่า) = กระโดด
    upper_bound = MID_Y + 100 # ถ้าย่อไหล่ต่ำกว่านี้ (ค่า y มากกว่า) = ย่อตัว
    
    if (actual_mid_y < lower_bound):
        posture = 'Jumping'
    elif (actual_mid_y > upper_bound):
        posture = 'Crouching'
    else:
        posture = 'Standing'
        
    if draw:
        # ตรงนี้คือส่วนแสดงคำว่า Jumping / Crouching / Standing
        cv2.putText(output_image, posture, (5, height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.line(output_image, (0, MID_Y),(width, MID_Y),(255, 255, 255), 2)
        
    return output_image, posture


