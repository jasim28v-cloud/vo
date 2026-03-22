const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();

// إعدادات المنفذ (Port) ليتناسب مع Render تلقائياً
const PORT = process.env.PORT || 3000;

// تفعيل مشاركة الموارد وتنسيق البيانات
app.use(cors());
app.use(express.json());

// تشغيل ملفات الموقع (HTML, CSS, JS) من المجلد الرئيسي
app.use(express.static(path.join(__dirname, '.')));

// نقطة فحص للتأكد أن المحرك يعمل بنجاح
app.get('/status', (req, res) => {
    res.json({ 
        message: "Universal Engine is Live! 🚀",
        status: "Running v99" 
    });
});

// تشغيل السيرفر
app.listen(PORT, () => {
    console.log(Server is flying on port ${PORT} 🚀🌑);
});
