import cv2
import pyautogui
from time import time
from pose_utils import detectPose, pose_video
from game_controls import checkHandsJoined, checkLeftRight, checkJumpCrouch
import mediapipe as mp # import เพื่อใช้ PoseLandmark ใน main loop
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# เริ่มต้น VideoCapture เพื่ออ่านภาพจาก Webcam ( index 0 คือกล้อง default)
camera_video = cv2.VideoCapture(0)

# ปรับความละเอียด (Resolution) 
# 3 = width
# 4 = height
# ถ้าอยากได้ชัดๆ ให้แก้เป็น 1280, 960 
# ถ้าอยากได้ลื่นๆ ให้ใช้ 640, 480
camera_video.set(3,1280)
camera_video.set(4,960)

# สร้างหน้าต่างสำหรับแสดงผล
cv2.namedWindow('Subway Surfers with Pose Detection', cv2.WINDOW_NORMAL)
 
# ตัวแปรสำหรับคำนวณ FPS
time1 = 0

# ตัวแปรเก็บสถานะว่าเกมเริ่มหรือยัง
game_started = False   

# ตัวแปรเก็บสถานะแกน X (0=Left, 1=Center, 2=Right) เริ่มต้นที่ 1 (Center)
x_pos_index = 1

# ตัวแปรเก็บสถานะแกน Y (0=Crouch, 1=Standing, 2=Jump) เริ่มต้นที่ 1 (Standing)
y_pos_index = 1

# ตัวแปรเก็บค่า Y กลางตอนเริ่มเกม (ความสูงมาตรฐานของผู้เล่น)
MID_Y = None

# ตัวนับสำหรับตรวจสอบการประสานมือ (ต้องประสานค้างไว้แป๊บนึงถึงจะเริ่ม)
counter = 0
# ตัวนับสำหรับตรวจสอบการประสานมือ (ต้องประสานค้างไว้แป๊บนึงถึงจะเริ่ม)
counter = 0
num_of_frames = 10 # จำนวนเฟรมที่ต้องค้างไว้

# ฟังก์ชันสำหรับวาดตัวหนังสือด้วย PIL (เพื่อให้ได้ฟอนต์สวยๆ)
def put_text_modern(img, text, position, font_size, color, align="left"):
    # แปลง cv2 image (BGR) เป็น PIL image (RGB)
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    try:
        # พยายามโหลดฟอนต์มาตรฐาน Windows (Arial หรือ Segoe UI)
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # ถ้าหาไม่เจอใช้ default
        font = ImageFont.load_default()

    # คำนวณขนาดข้อความเพื่อจัดตำแหน่ง (ถ้าจำเป็น)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # วาดข้อความ (ทําขอบดำเล็กน้อยเพื่อให้อ่านง่าย)
    x, y = position
    if align == "right":
        x = x - text_width
    elif align == "center":
        x = x - (text_width / 2)

    # Shadow / Stroke
    draw.text((x+2, y+2), text, font=font, fill=(0,0,0)) 
    
    # Text
    draw.text((x, y), text, font=font, fill=color)
    
    # แปลงกลับเป็น cv2 image (BGR)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

print("Starting Camera... Press 'ESC' to exit.")

# วนลูปตราบเท่าที่กล้องยังทำงาน
while camera_video.isOpened():
    
    # อ่านภาพจากกล้อง
    ok, frame = camera_video.read()
    
    if not ok:
        continue
    
    # พลิกภาพแนวนอนให้เหมือนกระจก (Selfie view)
    frame = cv2.flip(frame, 1)
    
    frame_height, frame_width, _ = frame.shape
    
    # ตรวจจับท่าทาง (Pose Detection)
    # ถ้าเกมเริ่มแล้ว เราอาจจะไม่ต้องวาดเส้น landmark ตลอดเวลาก็ได้ แต่ในที่นี้ set draw=game_started 
    # หมายความว่าถ้าเกมเริ่ม จะวาดเส้น แต่ถ้าเกมยังไม่เริ่ม อาจจะยังไม่วาด (ตามโค้ดต้นฉบับ)
    # แต่จริงๆ วาดตลอดก็ได้ เพื่อให้เห็นว่ากล้องจับเจอไหม
    frame, results = detectPose(frame, pose_video, draw=True)
    
    # ถ้าเจอ Landmarks
    if results.pose_landmarks:
        
        # -----------------------------------------------------
        # ส่วนควบคุมเกมเมื่อเกมเริ่มแล้ว
        # -----------------------------------------------------
        if game_started:
            
            # 1. ควบคุมซ้าย-ขวา (Horizontal)
            frame, horizontal_position = checkLeftRight(frame, results, draw=True)
            
            # ถ้าขยับไปทางซ้าย (และยังไม่ได้อยู่ซ้ายสุด)
            if (horizontal_position=='Left' and x_pos_index!=0) or (horizontal_position=='Center' and x_pos_index==2):
                pyautogui.press('left') # กดปุ่มลูกศรซ้าย
                x_pos_index -= 1       

            # ถ้าขยับไปทางขวา (และยังไม่ได้อยู่ขวาสุด)
            elif (horizontal_position=='Right' and x_pos_index!=2) or (horizontal_position=='Center' and x_pos_index==0):
                pyautogui.press('right') # กดปุ่มลูกศรขวา
                x_pos_index += 1
            
            # 2. ควบคุมกระโดด-ย่อตัว (Vertical)
            if MID_Y:
                frame, posture = checkJumpCrouch(frame, results, MID_Y, draw=True)
                
                # ถ้ากระโดด
                if posture == 'Jumping' and y_pos_index == 1:
                    pyautogui.press('up') # กดปุ่มลูกศรขึ้น
                    y_pos_index += 1 

                # ถ้าย่อตัว
                elif posture == 'Crouching' and y_pos_index == 1:
                    pyautogui.press('down') # กดปุ่มลูกศรลง
                    y_pos_index -= 1
                
                # ถ้ากลับมายืนตรง
                elif posture == 'Standing' and y_pos_index != 1:
                    y_pos_index = 1
        
        # -----------------------------------------------------
        # ส่วนหน้าจอรอเริ่มเกม (Waiting Screen)
        # -----------------------------------------------------
        else:

            # cv2.putText(frame, 'JOIN BOTH HANDS TO START.', (5, frame_height - 10), cv2.FONT_HERSHEY_PLAIN,
            #             2, (0, 255, 0), 3)
            frame = put_text_modern(frame, "JOIN HANDS TO START", (frame_width//2, frame_height//2), 35, (0, 255, 0), align="center")
        
        # -----------------------------------------------------
        # ตรวจสอบคำสั่งเริ่มเกม (Join Hands)
        # -----------------------------------------------------
        if checkHandsJoined(frame, results)[1] == 'Hands Joined':
            counter += 1
            if counter == num_of_frames:
                # ถ้ายังไม่เริ่มเกม -> เริ่มเกม
                if not(game_started):
                    game_started = True
                    
                    # บันทึกความสูงไหล่ตอนเริ่มเกม เพื่อใช้เป็นค่ากลาง
                    left_y = int(results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y * frame_height)
                    right_y = int(results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y * frame_height)
                    MID_Y = abs(right_y + left_y) // 2

                    # จำลองการคลิกเมาส์เพื่อกดปุ่ม Play ในเกมหน้าเว็บ (ปรับพิกัด x,y ตามหน้าจอจริงถ้าจำเป็น)
                    # pyautogui.click(x=1300, y=800, button='left') 
                    # หรือกด Spacebar แทนถ้าเกมรองรับ
                    pyautogui.press('space')

                # ถ้าเกมเริ่มแล้ว -> Resume หรือแก้สถานะตาย
                else:
                    pyautogui.press('space')
                
                counter = 0
        else:
            counter = 0
            
    else:
        counter = 0
        
    # -----------------------------------------------------
    # คำนวณและแสดง FPS
    # -----------------------------------------------------
    # คำนวณและแสดง FPS
    # -----------------------------------------------------
    time2 = time()
    if (time2 - time1) > 0:
        frames_per_second = 1.0 / (time2 - time1)
        # แสดง FPS แบบเดิม (ง่ายและเร็ว) หรือเปลี่ยนเป็น Modern ก็ได้
        cv2.putText(frame, 'FPS: {}'.format(int(frames_per_second)), (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
        frame = put_text_modern(frame, f"FPS: {int(frames_per_second)}", (10, 10), 20, (0, 255, 0))
    time1 = time2

    # -----------------------------------------------------
    # แสดงชื่อเกมมุมขวาบน (GAME SUBWAY ICT CHALLENGE)
    # สีน้ำเงิน (Blue): (50, 100, 255) -> PIL ใช้ (R,G,B)
    # สีชมพู (Pink): (255, 50, 200)
    # -----------------------------------------------------
    # -----------------------------------------------------
    # แสดงชื่อเกมมุมขวาบน
    # แก้ขนาดตัวอักษรตรงเลข 25 (เดิม 30) 
    frame = put_text_modern(frame, "GAME SUBWAY", (frame_width - 10, 10), 25, (50, 100, 255), align="right")
    frame = put_text_modern(frame, "ICT CHALLENGE", (frame_width - 10, 45), 25, (255, 50, 200), align="right")

    
    # แสดงผลออกจอ
    cv2.imshow('Subway Surfers with Pose Detection', frame)
    
    # กด ESC เพื่อออกจากโปรแกรม
    k = cv2.waitKey(1) & 0xFF    
    if(k == 27):
        break

# คืนทรัพยากร
camera_video.release()
cv2.destroyAllWindows()
