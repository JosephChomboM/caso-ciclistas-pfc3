import { expect, it } from "vitest";
import { dateInLima } from "./time";

it("keeps a late Lima evening on its local calendar date across UTC midnight", () => {
  expect(dateInLima("2026-11-20T04:30:00Z")).toBe("19/11/2026");
  expect(dateInLima("2026-11-20T04:30:00")).toBe("19/11/2026");
  expect(dateInLima("2026-11-20T05:30:00Z")).toBe("20/11/2026");
});
