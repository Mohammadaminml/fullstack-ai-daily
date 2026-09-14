# راهنمای انتشار در GitHub

## ساخت Repository جدید

در GitHub یک Repository با نام پیشنهادی `fullstack-ai-daily` بسازید و گزینه ساخت خودکار README را غیرفعال کنید.

```bash
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fullstack-ai-daily.git
git add .
git commit -m "docs: add full-stack and AI lessons for 2026-09-14"
git push -u origin main
```

## افزودن این شماره به Repository موجود

پوشه `2026-09-14` را در ریشه Repository کپی کنید، سپس:

```bash
git pull --rebase origin main
git add 2026-09-14
git commit -m "docs: add full-stack and AI lessons for 2026-09-14"
git push origin main
```

اگر شاخه اصلی شما `master` است، در دستورات بالا `main` را با `master` جایگزین کنید.

