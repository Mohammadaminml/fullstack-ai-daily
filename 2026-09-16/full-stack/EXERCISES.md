# تمرین‌های API Contract Testing

## تمرین 1 — آسان

یک Test اضافه کن که `price: 0` را معتبر بداند.

راهنمای حل: Payload معتبر بساز، `getProperty` را اجرا کن و با `assert.equal(result.price, 0)` نتیجه را بررسی کن.

## تمرین 2 — متوسط

فیلد اختیاری `description` را اضافه کن. اگر Missing یا `null` بود، خروجی `null` باشد؛ در غیر این صورت فقط String پذیرفته شود.

پاسخ کوتاه:

```js
const description = value.description == null ? null : requireString(value.description, "description");
```

برای Numberها از `== null` استفاده نکن مگر اینکه هر دو حالت Missing و Null واقعاً یک معنی داشته باشند.

## تمرین 3 — چالشی

یک Test Integration بنویس که Contract را مقابل یک Server محلی اجرا کند و پس از Test حتماً Server را ببندد.

راهنمای حل: از `node:http` برای ساخت Server روی Port تصادفی استفاده کن، آدرس را به Client بده، Test را در `try` اجرا کن و در `finally` از `server.close()` استفاده کن. مسیرهای `200` و `500` را جداگانه بررسی کن.
