# نظام إدارة ملفات المترشحين — EETFP-MPG
# Système de gestion des candidatures — EETFP-MPG

## الخطوات / Étapes

### 1. تعديل الإعدادات / Configuration
افتح ملف `config.py` وعدّل:
```python
IMAP_SERVER   = "mail.eetfp-mpg.mr"   # خادم البريد
EMAIL_ADDRESS = "eetfp-mpg@eetfp-mpg.mr"
PASSWORD      = "كلمة_المرور_الحقيقية"
```

> **ملاحظة:** الخادم عادةً يكون `mail.DOMAIN` أو `imap.DOMAIN`
> يمكن التحقق من إعدادات cPanel في قسم "Email Accounts" ← "Connect Devices"

---

### 2. تشغيل النظام / Lancement

**Windows — الطريقة السهلة:**
```
انقر مرتين على: LANCER.bat
```

**يدوياً / Manuellement:**
```powershell
# تثبيت المكتبات
pip install -r requirements.txt

# معالجة الرسائل (يعمل مرة واحدة أو عند التحديث)
python process_emails.py

# تشغيل لوحة التحكم
python app.py
```
ثم افتح المتصفح على: **http://localhost:5000**

---

### 3. هيكل الملفات / Structure
```
mpg-candidatures/
├── config.py           ← الإعدادات (تعديل هنا فقط)
├── process_emails.py   ← سكريبت معالجة البريد الإلكتروني
├── app.py              ← خادم الويب (Flask)
├── templates/
│   └── dashboard.html  ← واجهة لوحة التحكم
├── requirements.txt    ← المكتبات المطلوبة
├── LANCER.bat          ← ملف التشغيل السريع (Windows)
├── candidates.db       ← قاعدة البيانات (تُنشأ تلقائياً)
└── pieces_jointes/     ← المرفقات المحفوظة (تُنشأ تلقائياً)
    ├── email1@example.com/
    ├── email2@example.com/
    └── ...
```

---

### 4. ميزات لوحة التحكم / Fonctionnalités
- **بحث فوري** بالاسم أو البريد أو الموضوع
- **فلترة** حسب الحالة (مكتمل / جزئي / ناقص / فارغ) أو التخصص
- **إحصائيات** شاملة: إجمالي، مكررات، توزيع بالتخصص
- **تفاصيل** كل مترشح بنقرة واحدة: قائمة المرفقات، مواضيع الرسائل
- **تصدير CSV** لاستخدامه في Excel

---

### 5. ملاحظات تقنية
- النظام يُشغَّل **محلياً** على جهازك، لا يحتاج إنترنت بعد المعالجة
- يمكن إعادة تشغيل `process_emails.py` لاسترجاع رسائل جديدة (التحديث تراكمي)
- قاعدة البيانات SQLite تبقى محفوظة بين الجلسات
- المرفقات تُحفظ في مجلدات منظمة حسب البريد الإلكتروني

---

### 6. استكشاف الأخطاء / Dépannage

| الخطأ | الحل |
|-------|------|
| `Connection refused` | جرّب `imap.eetfp-mpg.mr` بدلاً من `mail.eetfp-mpg.mr` |
| `Login failed` | تحقق من كلمة المرور في config.py |
| `SSL error` | جرّب `USE_SSL = False` و`IMAP_PORT = 143` |
| `No module named flask` | شغّل `pip install flask` |

---

*EETFP-MPG — École d'Enseignement Technique et de Formation Professionnelle*
*Mines, Pétrole & Gaz — Nouakchott, Mauritanie*
