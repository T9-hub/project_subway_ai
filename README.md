# 🎮 AI Game Controller for Subway Surfers (ICT Challenge)

โปรเจกต์นี้จัดทำขึ้นเพื่อ **การศึกษาและความบันเทิงเท่านั้น** โดยนำเทคโนโลยี Computer Vision (MediaPipe) มาประยุกต์ใช้ในการควบคุมเกมด้วยท่าทางร่างกาย (Body Pose)

---

## 📋 เกี่ยวกับโปรเจกต์
ระบบจะใช้กล้อง Webcam จับการเคลื่อนไหวของผู้เล่นเพื่อควบคุมเกม **Subway Surfers** (หรือเกมแนว Endless Runner อื่นๆ)
- **กระโดด (Jump)**: กระโดดเพื่อสั่งให้ตัวละครกระโดด
- **ย่อตัว (Crouch)**: ย่อตัวลงเพื่อสั่งให้ตัวละครกลิ้ง
- **เอียงซ้าย/ขวา (Left/Right)**: ขยับตัวไปทางซ้ายหรือขวาเพื่อเปลี่ยนเลน

---

## ⚙️ วิธีการติดตั้งและใช้งาน (Installation)

### 1. ดาวน์โหลดโปรเจกต์ (Clone)
```bash
git clone https://github.com/T9-hub/project_subway_ai.git
cd game_ict
```

### 2. สร้างจำลองสภาพแวดล้อม (Virtual Environment)
เพื่อป้องกันไม่ให้ Library ตีกัน แนะนำให้สร้าง env ใหม่ก่อนเริ่มใช้งาน:
```bash
# สร้าง Virtual Environment
python -m venv env

# เข้าใช้งาน env (Activate)
# สำหรับ Windows:
.\env\Scripts\activate
# (ถ้าสำเร็จ จะมีคำว่า (env) ขึ้นหน้าบรรทัด)
```

### 3. ติดตั้ง Library ที่จำเป็น
```bash
pip install -r requirements.txt
```

### 4. เริ่มเล่นเกม! 🚀
1. เปิดเกม Subway Surfers ใน Web Browser เตรียมไว้
2. รันคำสั่ง:
   ```bash
   python main.py
   ```
3. ยืนให้ห่างจากกล้องพอประมาณ ให้กล้องเห็นตั้งแต่ศีรษะถึงเอว
4. ทำท่า **"ประสานมือ" (Join Hands)** เพื่อเริ่มเกม

---

## 🕹️ การควบคุม (Controls)
*   **เริ่มเกม**: ประสานมือไว้ระดับอกค้างไว้สักครู่
*   **หยุดเกม (ชั่วคราว)**: กดปุ่ม `Esc`

---

## 🙏 เครดิตและที่มา (Credits)
ขอขอบคุณความรู้และแรงบันดาลใจจาก:
*   **Original Tutorial**: [Artificial Intelligence Project | Game Checkpoint](https://www.youtube.com/watch?v=Z2EGhplFOHs)

---
*Developed for ICT Challenge Project*
