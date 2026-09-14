export type ApiErrorBody = {
  code: string;
  message: string;
  details?: Record<string, string[]>;
};

type ApiEnvelope<T> = {
  success: boolean;
  data: T | null;
  error: ApiErrorBody | null;
  traceId: string;
};

export type ApiResult<T> =
  | { ok: true; data: T; status: number; traceId: string }
  | {
      ok: false;
      status: number;
      error: ApiErrorBody & { traceId?: string };
    };

export async function apiRequest<T>(
  url: string,
  init: RequestInit = {},
  timeoutMs = 10_000,
): Promise<ApiResult<T>> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(init.body ? { "Content-Type": "application/json" } : {}),
        ...init.headers,
      },
      signal: controller.signal,
    });

    const contentType = response.headers.get("content-type") ?? "";
    const body = contentType.includes("application/json")
      ? ((await response.json()) as ApiEnvelope<T>)
      : null;

    if (!response.ok || !body?.success || body.data === null) {
      return {
        ok: false,
        status: response.status,
        error: {
          code: body?.error?.code ?? "HTTP_ERROR",
          message: body?.error?.message ?? `Request failed (${response.status})`,
          details: body?.error?.details,
          traceId: body?.traceId,
        },
      };
    }

    return {
      ok: true,
      data: body.data,
      status: response.status,
      traceId: body.traceId,
    };
  } catch (error) {
    const timedOut = error instanceof DOMException && error.name === "AbortError";
    return {
      ok: false,
      status: 0,
      error: {
        code: timedOut ? "TIMEOUT" : "NETWORK_ERROR",
        message: timedOut
          ? "مهلت درخواست به پایان رسید."
          : "ارتباط با سرور برقرار نشد.",
      },
    };
  } finally {
    clearTimeout(timeout);
  }
}

