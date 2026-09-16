function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function requireNumber(value, path) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new TypeError(`${path} must be a finite number`);
  }
  return value;
}

function requireString(value, path) {
  if (typeof value !== "string" || value.trim() === "") {
    throw new TypeError(`${path} must be a non-empty string`);
  }
  return value;
}

export function parseProperty(value) {
  if (!isRecord(value)) {
    throw new TypeError("property must be an object");
  }
  if (!isRecord(value.city)) {
    throw new TypeError("property.city must be an object");
  }

  const price = requireNumber(value.price, "property.price");
  if (price < 0) {
    throw new RangeError("property.price must be non-negative");
  }

  return Object.freeze({
    id: requireNumber(value.id, "property.id"),
    title: requireString(value.title, "property.title"),
    price,
    city: Object.freeze({
      id: requireNumber(value.city.id, "property.city.id"),
      name: requireString(value.city.name, "property.city.name"),
    }),
  });
}

export async function getProperty(id, fetchFn = globalThis.fetch) {
  if (!Number.isInteger(id) || id <= 0) {
    throw new RangeError("id must be a positive integer");
  }

  const response = await fetchFn(`/api/properties/${id}`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Property request failed with status ${response.status}`);
  }

  return parseProperty(await response.json());
}
