---
name: pelago-phone
description: Adapt the pelago Asia fishing-ground app for low-end phones used at sea. Use when changing the pelago globe, phone layout, touch gestures, frame rate, Thai fonts, workspace screens, or a deploy of this app.
---

# pelago phone baseline

Keep the current dark visual design. Do not invent accuracy claims, rescue numbers, or spot coordinates.

## Baseline the product is built for

1. สเปคฮาร์ดแวร์โดยเฉลี่ย (Baseline Hardware)

• ระบบปฏิบัติการ (OS): Android 10 ถึง Android 14 (พบ iOS รุ่นเก่าอย่าง iPhone 7/8/11 บ้างประปรายในกลุ่มไต้ก๋งหรือเจ้าของเรือ)
• หน่วยความจำ (RAM): 3 GB – 4 GB (รุ่นใหม่หน่อยจะได้ 6 GB แต่จะมีแอปพื้นหลังเปิดค้างไว้เยอะ)
• พื้นที่เก็บข้อมูล (Storage): 32 GB – 64 GB (มักใกล้เต็มจากรูปภาพ คลิปวิดีโอ และแอปแชท ทำให้พื้นที่ Cache ของเบราว์เซอร์มีจำกัด)
• ชิปเซ็ต (CPU/GPU): ระดับเริ่มต้น เช่น MediaTek Helio G-series (G35, G85), Unisoc หรือ Snapdragon 600-series รุ่นเก่า ซึ่งประมวลผลกราฟิก 3D หรือแอนิเมชันซับซ้อนได้ช้า
• หน้าจอ (Display): ขนาด 6.5 – 6.7 นิ้ว ความละเอียด HD+ (720 x 1600 พิกเซล) อัตรารีเฟรชหน้าจอ (Refresh Rate) ส่วนใหญ่เป็น 60Hz (รุ่นใหม่บางรุ่นอาจได้ 90Hz) และมักจะปรับความสว่างหน้าจอสูงสุดตลอดเวลาเพื่อสู้แสงแดดกลางทะเล ทำให้เครื่องร้อนง่ายและลดประสิทธิภาพ (Thermal Throttling) ลง

2. สภาพแวดล้อมการใช้งานและอินเทอร์เน็ต

• เครือข่าย: 4G สัญญาณไม่เสถียร (มักสลับไปมาระหว่าง 4G, 3G หรือเหลือขีดเดียวเมื่อออกห่างฝั่ง)
• เบราว์เซอร์: Google Chrome เป็นหลัก รองลงมาคือการเปิดลิงก์ผ่าน In-app Browser ของ LINE หรือ Facebook ซึ่งกิน RAM มากกว่าปกติ

## Rules

- Phone layout stays inside the viewport: header, map, and bottom bar do not overlap or push the globe off-screen. Touch targets are at least 44px.
- The satellite globe zooms with two fingers on the canvas. Browser page zoom must not scale the chrome.
- On a phone or `navigator.deviceMemory <= 4`, draw at most 30fps, cap the canvas at 1x, and skip the expensive glow pass. Desktop stays 60fps.
- Thai text uses installed faces (`Noto Sans Thai`, `Leelawadee UI`, `Thonburi`) via `lang="th"`. Do not add a render-blocking font download.
- Workspace screens scroll inside their own panel. Forms stack to full width on a phone.
- Deploy frontend changes to the existing Vercel project `pelago-asia` (https://pelago-asia.vercel.app).
