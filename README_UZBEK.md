# IELTS Mock Exam Platform - O'zbek tilida

Django MVT (Model-View-Template) arxitekturasi asosida qurilgan to'liq funksional IELTS mock imtihon platformasi.

## 🎯 Loyiha haqida

Bu platforma tashkilotlarga IELTS mock imtihonlarini yaratish, boshqarish va talabalar natijalarini tahlil qilish imkonini beradi. Talabalar ro'yxatdan o'tmasdan, faqat noyob link orqali imtihon topshira oladilar.

## ✨ Asosiy Xususiyatlar

### Tashkilotlar uchun (Admin)
- ✅ Ro'yxatdan o'tish va xavfsiz kirish
- ✅ Imtihonlarni yaratish, tahrirlash, o'chirish
- ✅ 4 xil savol turi (Ko'p tanlovli, Yozma, Tinglash, O'qish)
- ✅ Noyob linklar yaratish (muddati va foydalanish cheklovi bilan)
- ✅ Natijalarni ko'rish va batafsil tahlil
- ✅ CSV formatda eksport
- ✅ IELTS band score avtomatik hisobi
- ✅ Statistika va grafiklar

### Talabalar uchun (Ro'yxatsiz)
- ✅ Noyob link orqali kirish
- ✅ Oddiy ro'yxatdan o'tish formasi
- ✅ Taymer bilan imtihon topshirish
- ✅ Savollar orasida navigatsiya
- ✅ Avtomatik baholash
- ✅ Natijani darhol ko'rish
- ✅ To'g'ri/noto'g'ri javoblarni ko'rish

## 🛠️ Texnologiyalar

- **Backend**: Django 5.0 (MVT arxitekturasi)
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Database**: SQLite3 (development), PostgreSQL (production)
- **Auth**: Django Session Authentication
- **Icons**: Bootstrap Icons
- **Responsive**: Mobile-first dizayn

## 📦 O'rnatish

### 1. Loyihani yuklab olish

```bash
git clone <repository-url>
cd ielts-exam-system
```

### 2. Virtual muhit yaratish

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Database yaratish

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser yaratish

```bash
python manage.py createsuperuser
```

Ma'lumotlarni kiriting:
- Username: admin
- Email: admin@example.com
- Password: (xavfsiz parol)

### 6. Serverni ishga tushirish

```bash
python manage.py runserver
```

### 7. Brauzerda ochish

- **Asosiy sahifa**: http://localhost:8000/
- **Login**: http://localhost:8000/login/
- **Admin panel**: http://localhost:8000/admin/

## 📚 Foydalanish Qo'llanmasi

### Admin uchun

#### 1. Ro'yxatdan o'tish
1. http://localhost:8000/register/ sahifasiga o'ting
2. Tashkilot ma'lumotlarini kiriting
3. "Ro'yxatdan o'tish" tugmasini bosing

#### 2. Imtihon yaratish
1. Dashboard → "Yangi imtihon" tugmasini bosing
2. Imtihon nomi, tavsif va davomiyligini kiriting
3. "Saqlash" tugmasini bosing

#### 3. Savol qo'shish
1. Imtihon sahifasida "Savol qo'shish" tugmasini bosing
2. Savol turini tanlang:
   - **Ko'p tanlovli**: A, B, C, D variantlar bilan
   - **Yozma**: Matn kiritish uchun
   - **Tinglash**: Audio fayl URL bilan
   - **O'qish**: Matn asosida savol
3. Savol matnini va variantlarni kiriting
4. To'g'ri javobni belgilang
5. "Saqlash" tugmasini bosing

#### 4. Link yaratish
1. Imtihon sahifasida "Yangi link" tugmasini bosing
2. Amal qilish muddatini kiriting (kunlarda)
3. Maksimal foydalanish sonini kiriting (ixtiyoriy)
4. "Yaratish" tugmasini bosing
5. Linkni nusxalang va talabalar bilan ulashing

#### 5. Natijalarni ko'rish
1. "Natijalar" bo'limiga o'ting
2. Barcha natijalarni ko'ring
3. Batafsil ko'rish uchun "Ko'rish" tugmasini bosing
4. CSV eksport uchun "CSV eksport" tugmasini bosing

#### 6. Statistika
1. "Statistika" bo'limiga o'ting
2. Umumiy statistikani ko'ring:
   - Jami talabalar
   - O'rtacha ball
   - Ball taqsimoti
   - Eng yaxshi natijalar

### Talaba uchun

#### 1. Imtihon boshlanishi
1. Admin tomonidan ulashilgan linkni oching
2. Ma'lumotlaringizni kiriting:
   - Ism
   - Familiya
   - Telefon raqam
   - Telegram username (ixtiyoriy)
   - Email (ixtiyoriy)
3. "Imtihonni boshlash" tugmasini bosing

#### 2. Imtihon topshirish
1. Taymer avtomatik boshlanadi
2. Savollarni o'qing va javob bering
3. O'ng tomonda savollar navigatsiyasi mavjud
4. Javob bergan savollar yashil rangda ko'rsatiladi
5. Barcha savollarga javob bergandan keyin "Imtihonni yakunlash" tugmasini bosing

#### 3. Natijani ko'rish
1. Imtihon tugagach natijangiz avtomatik ko'rsatiladi
2. Umumiy ball, foiz va IELTS band score ko'rsatiladi
3. Har bir savolning to'g'ri/noto'g'ri ekanligini ko'ring
4. Natijani chop etish mumkin

## 🎨 Savol Turlari

### 1. Ko'p tanlovli (Multiple Choice)
- A, B, C, D variantlar
- Avtomatik baholash
- Eng ko'p ishlatiladigan tur

### 2. Yozma (Writing)
- Matn kiritish maydoni
- Qo'lda baholash uchun saqlanadi
- Essay yoki qisqa javoblar uchun

### 3. Tinglash (Listening)
- Audio fayl URL
- Ko'p tanlovli javob
- IELTS listening section uchun

### 4. O'qish (Reading)
- Matn asosida savollar
- Ko'p tanlovli javob
- IELTS reading section uchun

## 📊 IELTS Band Score

Tizim avtomatik ravishda IELTS band score hisoblab beradi:

| Foiz | Band Score | Daraja |
|------|------------|--------|
| 90-100% | 9.0 | Expert |
| 80-89% | 8.0 | Very Good |
| 70-79% | 7.0 | Good |
| 60-69% | 6.0 | Competent |
| 50-59% | 5.0 | Modest |
| 40-49% | 4.0 | Limited |
| 30-39% | 3.0 | Extremely Limited |
| 20-29% | 2.0 | Intermittent |
| 10-19% | 1.0 | Non-user |
| 0-9% | 0.0 | Did not attempt |

## 🔐 Xavfsizlik

### Admin uchun
- ✅ Parollar hash qilingan (bcrypt)
- ✅ Session autentifikatsiya
- ✅ CSRF himoyasi
- ✅ XSS himoyasi
- ✅ SQL injection himoyasi (Django ORM)

### Imtihon uchun
- ✅ Copy-paste o'chirilgan
- ✅ Tab almashtirish kuzatiladi
- ✅ Vaqt tugaganda avtomatik yuboriladi
- ✅ Noyob tokenlar
- ✅ Link muddati va foydalanish cheklovi

## 🎯 Imtihon Xususiyatlari

### Taymer
- Imtihon boshlanganida avtomatik ishga tushadi
- Qolgan vaqt real-time ko'rsatiladi
- 5 daqiqa qolganda ogohlantiradi
- Vaqt tugaganda avtomatik yuboriladi
- Progress bar bilan vizual ko'rsatish

### Navigatsiya
- Barcha savollar ro'yxati
- Javob berilgan savollar belgilanadi
- Istalgan savolga tez o'tish
- Hozirgi savol ko'rsatiladi

### Anti-Cheat
- Copy-paste funksiyasi o'chirilgan
- Tab almashtirish kuzatiladi va hisoblanadi
- Ogohlantirish xabarlari
- Natijada tab switches soni ko'rsatiladi

## 📱 Responsive Dizayn

Platforma barcha qurilmalarda yaxshi ishlaydi:
- ✅ Desktop kompyuterlar
- ✅ Noutbuklar
- ✅ Planshetlar
- ✅ Smartfonlar

## 📁 Loyiha Strukturasi

```
ielts-exam-system/
├── organizations/              # Tashkilotlar (Admin)
│   ├── models.py              # Organization User modeli
│   ├── views_mvt.py           # Login, Register, Dashboard
│   ├── forms.py               # Django forms
│   ├── urls_mvt.py            # URL routing
│   ├── admin.py               # Admin panel
│   └── templates/             # HTML templates
│       ├── login.html
│       ├── register.html
│       └── dashboard.html
├── exams/                     # Imtihonlar
│   ├── models.py              # Exam, Question, ExamLink
│   ├── views_mvt.py           # CRUD views
│   ├── forms.py               # Django forms
│   ├── urls_mvt.py            # URL routing
│   ├── admin.py               # Admin panel
│   └── templates/             # HTML templates
│       ├── exam_list.html
│       ├── exam_detail.html
│       ├── exam_form.html
│       ├── exam_start.html
│       ├── exam_take.html
│       └── question_form.html
├── students/                  # Talabalar
│   ├── models.py              # Student modeli
│   ├── forms.py               # Registration form
│   └── admin.py               # Admin panel
├── results/                   # Natijalar
│   ├── models.py              # Result modeli
│   ├── views_mvt.py           # Results, Analytics
│   ├── urls_mvt.py            # URL routing
│   ├── admin.py               # Admin panel
│   └── templates/             # HTML templates
│       ├── results_list.html
│       ├── result_detail.html
│       └── analytics.html
├── templates/                 # Umumiy templates
│   └── base.html              # Base template
├── static/                    # Static fayllar
│   ├── css/
│   │   └── style.css          # Custom CSS
│   └── js/                    # JavaScript
├── ielts_platform/            # Asosiy loyiha
│   ├── settings.py            # Django sozlamalari
│   ├── urls.py                # Asosiy URL routing
│   └── wsgi.py                # WSGI config
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management
├── requirements.txt           # Python kutubxonalari
├── README_MVT.md              # MVT qo'llanma
├── README_UZBEK.md            # O'zbek tilida qo'llanma
├── SETUP_GUIDE.md             # O'rnatish qo'llanmasi
└── QUICK_START.txt            # Tezkor boshlash
```

## 🚀 Production Deployment

### 1. Sozlamalarni o'zgartirish

`.env` faylida:
```env
DEBUG=False
SECRET_KEY=your-very-strong-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Static fayllarni to'plash

```bash
python manage.py collectstatic --noinput
```

### 3. Gunicorn bilan ishga tushirish

```bash
gunicorn ielts_platform.wsgi:application --bind 0.0.0.0:8000
```

### 4. Nginx konfiguratsiyasi

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 Muammolarni hal qilish

### Migratsiya xatolari
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static fayllar yuklanmayapti
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Admin panel ochilmayapti
```bash
python manage.py createsuperuser
```

## 📞 Yordam va Qo'llab-quvvatlash

Savollar yoki muammolar bo'lsa:
1. SETUP_GUIDE.md faylini o'qing
2. Admin panel orqali test qiling
3. Django loglarini tekshiring
4. GitHub Issues orqali murojaat qiling

## 📝 Litsenziya

MIT License - Bepul foydalanish va o'zgartirish mumkin

## 👨‍💻 Muallif

IELTS Mock Exam Platform - Django MVT Architecture

## 🎉 Xulosa

Bu platforma to'liq ishga tayyor va quyidagi barcha funksiyalarni qo'llab-quvvatlaydi:

✅ Tashkilot ro'yxatdan o'tishi va kirishi
✅ Imtihonlar CRUD (Create, Read, Update, Delete)
✅ 4 xil savol turi
✅ Noyob linklar yaratish
✅ Talabalar ro'yxatsiz imtihon topshirishi
✅ Avtomatik baholash
✅ Natijalar va batafsil statistika
✅ CSV eksport
✅ IELTS band score hisobi
✅ Responsive dizayn
✅ Anti-cheat xususiyatlari
✅ Taymer va avtomatik yuborish

**Omad tilaymiz va muvaffaqiyatli imtihonlar! 🚀📚**
