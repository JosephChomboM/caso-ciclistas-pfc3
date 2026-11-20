import { afterEach, expect, it, vi } from "vitest";
import { api, session } from "./client";

afterEach(() => {
  session.set(null);
  vi.unstubAllGlobals();
});
it("sends session only as an authorization header and handles 204", async () => {
  const fetcher = vi.fn().mockResolvedValue({ ok: true, status: 204 });
  vi.stubGlobal("fetch", fetcher);
  session.set("test-session");
  await api("/users/logout", { method: "POST" });
  expect(fetcher.mock.calls[0][1].headers.get("Authorization")).toBe(
    "Bearer test-session",
  );
});
it("shows recoverable network errors", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError()));
  await expect(api("/cycleways")).rejects.toThrow("Comprueba tu conexión");
});
it("handles validation errors without exposing object dumps", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      json: async () => ({ detail: [{ type: "invalid" }] }),
    }),
  );
  await expect(api("/users/register")).rejects.toThrow("Revisa los datos");
});
