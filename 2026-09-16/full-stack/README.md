# تست قرارداد API میان Frontend و Backend

## هدف یادگیری

در پایان می‌توانی مرز میان API و Frontend را با Test محافظت کنی، Payload خام را Validate و Normalize کنی و تغییرات ناسازگار Backend را پیش از Production تشخیص بدهی.

## پیش‌نیاز

- آشنایی با JavaScript، `async/await` و `fetch`
- Node.js 20 یا جدیدتر
- آشنایی مقدماتی با APIهای JSON

نمونه از Test Runner داخلی Node.js استفاده می‌کند و Package خارجی ندارد.

## 1. Contract چیست؟

Contract توافق میان Producer و Consumer است. برای مثال Frontend انتظار دارد Endpoint زیر:

```http
GET /api/properties/42
```

Payload زیر را برگرداند:

```json
{
  "id": 42,
  "title": "آپارتمان دوخوابه",
  "price": 12500000000,
  "city": { "id": 1, "name": "تهران" }
}
```

اگر Backend نام `price` را به `amount` تغییر دهد یا در Production مقدار `null` برگرداند، TypeScript به‌تنهایی جلوی خطای Runtime را نمی‌گیرد؛ چون Response شبکه در زمان اجرا وارد برنامه می‌شود.

## 2. مرز ورودی را Validate کن

به‌جای استفادهٔ مستقیم از JSON، آن را از یک Parser عبور بده:

```js
const raw = await response.json();
return parseProperty(raw);
```

Parser باید حداقل فیلدهای ضروری و نوع آن‌ها را بررسی کند. در پروژهٔ بزرگ می‌توان از Schema Library استفاده کرد، اما نمونهٔ امروز منطق اصلی را بدون Dependency نشان می‌دهد.

## 3. بین Missing و Null تفاوت بگذار

این سه حالت یکسان نیستند:

```json
{}
{ "price": null }
{ "price": 0 }
```

- Missing می‌تواند نشانهٔ تغییر Contract باشد.
- `null` ممکن است در Domain مجاز یا خطا باشد.
- `0` یک Number معتبر است و نباید با شرط Truthy حذف شود.

در نمونه، `price` باید Number نامنفی باشد و `null` پذیرفته نمی‌شود.

## 4. API Client را قابل Test طراحی کن

به‌جای استفادهٔ مستقیم از `globalThis.fetch`، آن را Inject کن:

```js
export async function getProperty(id, fetchFn = globalThis.fetch) {
  // ...
}
```

در Test یک Fake کوچک می‌سازیم. نتیجه: Test سریع، قطعی و بدون نیاز به Backend واقعی اجرا می‌شود.

## 5. چه سناریوهایی باید Test شوند؟

حداقل این چهار مسیر را پوشش بده:

1. Payload معتبر
2. فیلد ضروری `null` یا Missing
3. Status ناموفق مانند `404` یا `500`
4. `id` ورودی نامعتبر

فایل [`api-client.test.js`](./examples/test/api-client.test.js) همهٔ این مسیرها را پوشش می‌دهد.

## 6. اجرا

```bash
cd 2026-09-16/full-stack/examples
npm test
```

اجرای Watch Mode:

```bash
npm run test:watch
```

## 7. جایگاه این Test در معماری

- Unit Test: Parser و منطق Client را سریع بررسی می‌کند.
- Contract Test: شکل Response مورد انتظار Consumer را ثبت می‌کند.
- Integration Test: API واقعی و زیرساخت را کنار هم بررسی می‌کند.
- End-to-End Test: جریان کاربر در UI را می‌سنجد.

نمونهٔ امروز یک Consumer-side Contract Test سبک است؛ جایگزین Integration یا End-to-End Test نیست.

## نکات مهم

- Error شامل Context مفید باشد، اما Token یا دادهٔ حساس را Log نکن.
- Contract را بر اساس نیاز واقعی Consumer تعریف کن، نه تمام فیلدهای Response.
- Test باید مقدار `0`، رشتهٔ خالی مجاز و مرزهای Domain را آگاهانه بررسی کند.
- Response Type در TypeScript تضمین Runtime ایجاد نمی‌کند.
- تغییر اختیاری به اجباری یا تغییر نوع فیلد معمولاً Breaking Change است.

## اشتباهات رایج

- Cast کردن Response با `as Property` بدون Validation
- Mock کردن آن‌قدر زیاد که Parser واقعی هرگز اجرا نشود
- فقط Test کردن Happy Path
- یکی دانستن `null`، `undefined` و `0`
- وابسته کردن Unit Test به شبکه یا Database

## ادامه

- [دفترچه تقلب](./CHEATSHEET.md)
- [تمرین‌ها](./EXERCISES.md)
- [نمونهٔ قابل اجرا](./examples/api-client.js)
