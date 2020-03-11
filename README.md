# BlindBot
BlindBot หุ่นยนต์นำทางคนตาบอด ใช้ร่วมกับ GPS

หุ่นยนต์ Blindbot
เป็นหุ่นยนต์เคลื่อนที่ตามตำแหน่งของ GPS โดยควบคุมผ่านโทรศัพท์มือถือ และบอร์ดคอมพิวเตอร์ที่อยู่ภายในตัวของหุ่นยนต์ 
หุ่นยนต์มีเซนเซอร์อัลตร้าโซนิคสำหรับสั่งให้หุ่นยนต์หยุดการเคลื่อนที่ และส่งเสียงแจ้งเตือน เมื่อมีวัตถุขวางอยู่ข้างหน้า
    หุ่นยนต์มีลักษณะการเคลื่อนที่แบบ Omni Directional คือสามารถเคลื่อนที่ได้ทุกทิศทาง
    หุ่นยนต์มีเซนเซอร์ Lidar สำหรับตรวจเช็ควัตถุและหลบหลีกสิ่งกีดขวาง

## สำหรับผู้ใช้งาน

การใช้งานหุ่นยนต์เริ่มจากการเปิดเครื่องโดยการกดปุ่มสวิตช์ด้านข้าง ซึ่งจะมีสวิตช์อยู่ 2 ตัวคือ เปิดปิดหุ่นยนต์ และ เปิดปิดระบบการเคลื่อนที่เฉพาะส่วน เพื่อไม่ให้หุ่นยนต์เคลื่อนที่ได้แต่ส่วนควบคุมยังทำงานอยู่
    เมื่อเปิดหุ่นยนต์แล้วโปรแกรมทั้งหมดจะทำงานอย่างอัตโนมัติ เมื่อพร้อมจะมีเสียงแจ้งเตือนดัง ปิ๊ปๆๆ จากนั้นหุ่นยนต์จะกระจายสัญญาณ HotSpot ออกมา ให้เราใช้โทรศัพท์มือถือเชื่อมต่อเข้าไป โดย SSID มีชื่อว่า Blindbot และ Password เป็น blindbot
    เมื่อเชื่อมต่อเสร็จแล้วก็ให้เปิดแอพพลิเคชั่น และสามารถใช้งานหุ่นยนต์ได้ทันที

## สำหรับผู้พัฒนา
    ผู้พัฒนาสามารถเชื่อมต่อเข้าไปยังตัวประมวลผลหุ่นยนต์ผ่าน SSH โดยมี 
    IP Address : 192.168.4.1
    Username : pi
    Password : blindbot

ไฟล์โปรแกรมทั้งหมดอยู่ใน Github สามารถดาวน์โหลดได้
https://github.com/SweiLz/BlindBot

ส่วนประกอบของโปรแกรมจะมีอยู่ 2 ส่วน
ส่วนที่อยู่ในตัวของหุ่นยนต์ Raspberry Pi 3
ส่วนที่อยู่ในโทรศัพท์ แอพแอนดรอย

โปรแกรมที่อยู่ในตัวหุ่นยนต์นั้นจะเขียนด้วยภาษา Python3 และมี Script สั่งการให้โปรแกรมหลักเริ่มทำงานเมื่อเปิดตัวหุ่นยนต์  ซึ่งในโปรแกรมนี้จะทำงานโดย แบ่งการทำงานเป็น 
ส่วนของการควบคุมการทำงานของหุ่นยนต์ 
ในส่วนการควบคุมการทำงานของหุ่นยนต์ก็จะแบ่งย่อยออกเป็น Thread ย่อยๆหลายๆตัว ประกอบไปด้วย 
Thread Buzzer สำหรับสั่งงานเสียง 
Thread Drive สำหรับควบคุมความเร็วการเคลื่อนที่ของล้อทั้ง 3 ล้อ
Thread GPS Ultrasonic สำหรับอ่านค่าตำแหน่ง GPS และค่าของ Ultrasonic
Thread IMU สำหรับหาทิศทางของสนามแม่เหล็ก Compass
Thread Control สำหรับควบคุมการทำงานให้ประสานกันทั้งหมด
Thread Lidar สำหรับอ่านค่า Lidar และนำมาประมวลผล
โปรแกรมหลักจะเริ่มจากการเปิดใช้งาน Thread
ทุกตัวและรอรับคำสั่งจากส่วนที่เป็นเซิฟเวอร์รอรับคำสั่งจากโทรศัพท์

ส่วนที่เป็นเซิฟเวอร์สำหรับเชื่อมต่อกับโทรศัพท์
    ในส่วนนี้จะเป็นเหมือน API ของตัวหุ่นยนต์โดยเราสามารถ GET POST มาที่ตัวหุ่นยนต์ผ่าน IP ของหุ่นยนต์ได้
หาก GET มาที่หุ่นยนต์ /201 หุ่นยนต์จะรีเทิร์นค่าตำแหน่ง GPS ออกไปให้เป็นไฟล์ Json
หาก GET มาที่หุ่นยนต์ /220 หุ่นยนต์จะเป็นการหยุดการเคลื่อนที่โดยทันที
หาร POST มาที่หุ่นยนต์ /221 และมี Argument เป็น Heading และ Speed หุ่นยนต์จะทำการเคลื่อนที่ไปยังทิศทางและความเร็วที่กำหนดให้นั้น


ในส่วนแอพที่อยู่ในโทรศัพท์แอนดรอยนั้นจะเขียนโดยใช้ App Inventor2 ไฟล์อยู่ใน Github ที่แปะไว้ นามสกุลเป็น .aia สามารถนำไปเปิดเพื่อแก้ไขได้
    แอพพลิเคชั้นนี้จะมีการแสดงตำแหน่งของหุ่นยนต์ และแผนที่ สามารถกำหนดพิกัดให้หุ่นยนต์เคลื่อนที่ไปได้ และสามารถเปลี่ยนโหมดได้โดยใช้ GPS ของโทรศัพท์มือถือ หรือ GPS ของตัวหุ่นยนต์ ลักษณะการทำงานก็จะเป็นการส่ง GET POST ไปยังตัวหุ่นยนต์ให้เคลื่อนที่ไปด้วยความเร็วกับทิศทางที่กำหนด
