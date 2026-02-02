import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

# เริ่มต้นคลาส mediapipe pose
mp_pose = mp.solutions.pose

# ตั้งค่าฟังก์ชัน Pose สำหรับภาพนิ่ง (ถ้าต้องการใช้)
pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=1)

# ตั้งค่าฟังก์ชัน Pose สำหรับวิดีโอ (ใช้สำหรับ webcam)
# model_complexity=0 (Lite) เร็วขึ้นมาก เหมาะกับคอมสเปคทั่้วไป
pose_video = mp_pose.Pose(static_image_mode=False, model_complexity=0, min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)

# เริ่มต้นคลาสสำหรับการวาดเส้น landmarks
mp_drawing = mp.solutions.drawing_utils 

def detectPose(image, pose, draw=False, display=False):
    '''
    ฟังก์ชันนี้ทำหน้าที่ตรวจจับท่าทาง (Pose Detection) ของคนที่เด่นที่สุดในภาพ
    
    Args:
        image:   ภาพ input ที่มีคนอยู่
        pose:    ฟังก์ชัน pose ของ mediapipe ที่ตั้งค่าไว้
        draw:    ค่า boolean (True/False) ถ้าเป็น True จะวาดเส้น landmarks ลงบนภาพ
        display: ค่า boolean (True/False) ถ้าเป็น True จะแสดงผลภาพ (ใช้สำหรับ debug)
    
    Returns:
        output_image: ภาพผลลัพธ์ที่มีการวาดเส้น landmarks (ถ้า draw=True)
        results:      ผลลัพธ์ของการตรวจจับ landmarks จาก mediapipe
    '''
    
    # สร้างสำเนาของภาพ input เพื่อไม่ให้กระทบภาพต้นฉบับ
    output_image = image.copy()
    
    # แปลงภาพจาก BGR (format ของ OpenCV) เป็น RGB (format ที่ MediaPipe ต้องการ)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # ทำการตรวจจับท่าทาง (Process the image)
    results = pose.process(imageRGB)
    
    # ตรวจสอบว่าเจอ landmarks หรือไม่ และดูว่าต้องวาดเส้นไหม
    if results.pose_landmarks and draw:
    
        # วาด Pose Landmarks ลงบนภาพ output_image
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                               thickness=3, circle_radius=3),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                               thickness=2, circle_radius=2))

    # ถ้าต้องการให้แสดงผลรูปภาพเลย (มักใช้ตอนทดสอบกับภาพนิ่ง)
    if display:
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    # ส่งค่าภาพผลลัพธ์และข้อมูล landmarks กลับไป
    return output_image, results
