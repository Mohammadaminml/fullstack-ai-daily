# تمرین‌های Full-Stack

## ۱. آسان — خطای Validation

یک Endpoint برای ساخت کاربر بنویسید که اگر `name` خالی بود پاسخ `400` با کد `VALIDATION_ERROR` برگرداند.

راهنما: از `Results.BadRequest(...)` و فیلد `details` استفاده کنید.

## ۲. متوسط — نمایش خطا در React

با استفاده از `apiRequest` یک تابع `loadUser(id)` بسازید. برای `USER_NOT_FOUND` پیام «کاربر وجود ندارد» و برای `NETWORK_ERROR` دکمه تلاش مجدد نمایش دهید.

راهنما: ابتدا `result.ok` و سپس `result.error.code` را بررسی کنید.

## ۳. چالشی — Refresh Token هم‌زمان

Wrapper را طوری توسعه دهید که در خطای `401` فقط یک بار Refresh Token انجام دهد؛ اگر چند Request هم‌زمان `401` شدند، همگی منتظر همان Promise بمانند.

راهنمای حل: یک متغیر ماژولی از نوع `Promise<boolean> | null` نگه دارید. قبل از Refresh بررسی کنید Promise فعال وجود دارد یا نه. از حلقه Retry بی‌نهایت جلوگیری کنید.

