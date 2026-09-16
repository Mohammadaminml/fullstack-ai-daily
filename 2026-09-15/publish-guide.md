# راهنمای انتشار در GitHub

فرض شده Repository قبلاً Clone شده و پوشهٔ `2026-09-15` را در ریشهٔ آن قرار داده‌ای.

```bash
git status
git pull --rebase origin main
git add 2026-09-15
git diff --cached --check
git commit -m "docs: add SQL performance and RAG retrieval lessons for 2026-09-15"
git push origin main
```

اگر شاخهٔ اصلی Repository تو `master` است، به‌جای `main` از `master` استفاده کن.

## بررسی قبل از Commit

```bash
git diff --cached --stat
git diff --cached
```

اگر هنگام `pull --rebase` تعارض ایجاد شد، فایل‌ها را اصلاح کن و سپس:

```bash
git add <resolved-file>
git rebase --continue
```

برای لغو امن Rebase:

```bash
git rebase --abort
```
