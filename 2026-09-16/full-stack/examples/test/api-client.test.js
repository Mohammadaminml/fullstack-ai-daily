import assert from "node:assert/strict";
import test from "node:test";

import { getProperty, parseProperty } from "../api-client.js";

function fakeFetch(payload, { ok = true, status = 200 } = {}) {
  return async () => ({
    ok,
    status,
    async json() {
      return payload;
    },
  });
}

const validPayload = {
  id: 42,
  title: "آپارتمان دوخوابه",
  price: 12_500_000_000,
  city: { id: 1, name: "تهران" },
};

test("returns a normalized property for a valid contract", async () => {
  const result = await getProperty(42, fakeFetch(validPayload));

  assert.deepEqual(result, validPayload);
  assert.equal(Object.isFrozen(result), true);
});

test("accepts zero as a valid price boundary", () => {
  const result = parseProperty({ ...validPayload, price: 0 });
  assert.equal(result.price, 0);
});

test("rejects an explicit null price", () => {
  assert.throws(
    () => parseProperty({ ...validPayload, price: null }),
    /property\.price must be a finite number/,
  );
});

test("rejects a missing city object", () => {
  const { city: _city, ...withoutCity } = validPayload;
  assert.throws(() => parseProperty(withoutCity), /property\.city must be an object/);
});

test("reports an unsuccessful HTTP status", async () => {
  await assert.rejects(
    () => getProperty(42, fakeFetch({}, { ok: false, status: 404 })),
    /status 404/,
  );
});

test("rejects an invalid id before making a request", async () => {
  let called = false;
  const fetchFn = async () => {
    called = true;
    throw new Error("must not be called");
  };

  await assert.rejects(() => getProperty(0, fetchFn), /positive integer/);
  assert.equal(called, false);
});
