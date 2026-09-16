# راهنمای انتشار در GitHub

پوشهٔ `2026-09-16` را در ریشهٔ Repository قرار بده و سپس:

```bash
git status
git pull --rebase origin main
git add 2026-09-16
git diff --cached --check
git diff --cached --stat
git commit -m "test: add API contract and RAG evaluation lessons for 2026-09-16"
git push origin main
```

اگر نام شاخهٔ اصلی `master` است، در دستورهای بالا `main` را با `master` جایگزین کن.

## کنترل محتوای Commit

```bash
git diff --cached
```

## مدیریت تعارض احتمالی Rebase

```bash
git status
# فایل‌های متعارض را اصلاح کن
git add <resolved-file>
git rebase --continue
```

برای برگشت به وضعیت قبل از Rebase:

```bash
git rebase --abort
```
