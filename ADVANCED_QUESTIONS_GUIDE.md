# Advanced IELTS Question System - Qo'llanma

## ✅ Yangi Xususiyatlar

### 16 xil IELTS Savol Turi

#### 1. Multiple Choice (Single Answer)
- **Modul**: Reading / Listening
- **Interface**: Radio buttons
- **To'ldirish**: Savol + 4 ta variant (A, B, C, D) + To'g'ri javob

#### 2. Multiple Choice (Multiple Answers)
- **Modul**: Reading / Listening
- **Interface**: Checkboxes
- **To'ldirish**: Savol + 4 ta variant + Bir nechta to'g'ri javob

#### 3. True / False / Not Given
- **Modul**: Reading
- **Interface**: Radio buttons (3 variant)
- **To'ldirish**: Statement + To'g'ri javob (TRUE/FALSE/NOT GIVEN)

#### 4. Yes / No / Not Given
- **Modul**: Reading
- **Interface**: Radio buttons (3 variant)
- **To'ldirish**: Statement + To'g'ri javob (YES/NO/NOT GIVEN)

#### 5. Sentence Completion
- **Modul**: Reading / Listening
- **Interface**: Text input
- **To'ldirish**: Jumla (_____ bilan) + To'g'ri javob + So'zlar cheklovi

#### 6. Diagram Label Completion
- **Modul**: Reading / Listening
- **Interface**: Image + Input fields
- **To'ldirish**: Rasm yuklash + Labellar soni + Har bir label uchun javob
- **File Upload**: ✅ Rasm yuklash mumkin

#### 7. Short Answer Questions
- **Modul**: Reading / Listening
- **Interface**: Text input
- **To'ldirish**: Savol + To'g'ri javob + So'zlar cheklovi

#### 8. Writing Task
- **Modul**: Writing
- **Interface**: Textarea
- **To'ldirish**: Topshiriq matni + Minimal so'zlar soni
- **Baholash**: Qo'lda

## 🎯 Savol Qo'shish Jarayoni

### 1. Asosiy Ma'lumotlar
```
Module: Reading / Listening / Writing / Speaking
Savol turi: 16 ta turdan birini tanlang
Ko'rsatmalar: "Choose the correct answer" kabi
Tartib: Savol raqami
Ball: Har bir savol uchun ball
```

### 2. Listening uchun Audio
```
Audio fayl yuklash: MP3, WAV, OGG
yoki Audio URL: YouTube, SoundCloud, va boshqalar
Boshlanish vaqti: Soniyalarda (ixtiyoriy)
Tugash vaqti: Soniyalarda (ixtiyoriy)
```

### 3. Diagram uchun Rasm
```
Rasm yuklash: JPG, PNG, GIF
yoki Rasm URL: Tashqi manba
Labellar soni: 1-10 ta
Har bir label uchun to'g'ri javob
```

## 📊 Content JSON Strukturasi

### MCQ Single
```json
{
  "question": "What is the main idea?",
  "options": {
    "A": "Option 1",
    "B": "Option 2",
    "C": "Option 3",
    "D": "Option 4"
  }
}
```

### True/False/Not Given
```json
{
  "statement": "The earth is flat."
}
```

### Sentence Completion
```json
{
  "sentence": "The process begins with _____.",
  "word_limit": 3
}
```

### Diagram Labeling
```json
{
  "labels": [
    {"id": 1, "answer": "heart"},
    {"id": 2, "answer": "lungs"},
    {"id": 3, "answer": "liver"}
  ]
}
```

### Short Answer
```json
{
  "question": "What is the capital of France?",
  "word_limit": 3
}
```

## 🎨 Dynamic Interface

### Savol Turi Tanlanganda
1. Interface avtomatik o'zgaradi
2. Kerakli maydonlar ko'rsatiladi
3. Validatsiya qo'shiladi

### Module Tanlanganda
- **Listening** tanlansa → Audio section ko'rsatiladi
- **Reading** tanlansa → Audio section yashiriladi

## 📁 File Upload

### Audio Fayllar
- **Format**: MP3, WAV, OGG, M4A
- **Maksimal hajm**: 10MB
- **Saqlash**: `media/audio/`
- **Foydalanish**: Listening questions uchun

### Rasm Fayllar
- **Format**: JPG, PNG, GIF, SVG
- **Maksimal hajm**: 10MB
- **Saqlash**: `media/images/`
- **Foydalanish**: Diagram labeling uchun

## ✅ Baholash Tizimi

### Avtomatik Baholash
- Multiple Choice (Single/Multiple)
- True/False/Not Given
- Yes/No/Not Given
- Sentence Completion
- Diagram Labeling
- Short Answer

### Qo'lda Baholash
- Writing Tasks

### Baholash Qoidalari
1. **Case-insensitive**: "Paris" = "paris" = "PARIS"
2. **Trim spaces**: " Paris " = "Paris"
3. **Partial scoring**: Multiple answers uchun
4. **Word limit**: So'zlar soni tekshiriladi

## 🚀 Foydalanish

### 1. Imtihon Yaratish
```
Dashboard → Yangi imtihon → Ma'lumotlarni kiriting
```

### 2. Savol Qo'shish
```
Imtihon → Savol qo'shish → Turi tanlang → To'ldiring
```

### 3. Audio/Rasm Yuklash
```
Module: Listening tanlang
Audio fayl yuklash → Faylni tanlang
yoki Audio URL kiriting
```

### 4. Diagram Yaratish
```
Turi: Diagram Label Completion
Rasm yuklash → Faylni tanlang
Labellar soni: 5
Har bir label uchun javob kiriting
```

## 📝 Misollar

### Reading - MCQ Single
```
Module: Reading
Type: Multiple Choice (Single Answer)
Instruction: Choose the correct answer
Question: What is the main purpose of the passage?
A: To inform
B: To persuade
C: To entertain
D: To describe
Correct Answer: A
```

### Listening - Sentence Completion
```
Module: Listening
Type: Sentence Completion
Instruction: Complete the sentences below
Audio: Upload MP3 file
Sentence: The lecture starts at _____.
Correct Answer: 9 o'clock
Word Limit: 3
```

### Reading - Diagram Labeling
```
Module: Reading
Type: Diagram Label Completion
Instruction: Label the diagram
Image: Upload diagram.png
Labels: 3
Label 1: heart
Label 2: lungs
Label 3: liver
```

## 🎯 Keyingi Qadamlar

1. ✅ Serverni ishga tushiring
2. ✅ Imtihon yarating
3. ✅ Turli xil savollar qo'shing
4. ✅ Audio/rasm yuklang
5. ✅ Test qiling

## 📞 Yordam

Savollar yoki muammolar bo'lsa:
- Bu faylni o'qing
- README_UZBEK.md ni ko'ring
- Test qiling va feedback bering

**Omad tilaymiz! 🚀**
