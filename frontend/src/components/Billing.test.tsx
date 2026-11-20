import { fireEvent, render, screen } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import Billing from "./Billing";
import { api, downloadFavorites, type User } from "../api/client";

vi.mock("../api/client", () => ({ api: vi.fn(), downloadFavorites: vi.fn() }));
const plans = [
  { code: "free", name: "Comunidad", amount_centavos: 0, features: ["Mapa"] },
  {
    code: "plus",
    name: "CicloLima Plus",
    amount_centavos: 990,
    features: ["Exportación CSV"],
  },
];

it("lets a visitor inspect demo plans and requests login before a change", async () => {
  vi.mocked(api).mockResolvedValue({ plans });
  const login = vi.fn();
  render(<Billing user={null} onLogin={login} />);
  expect(await screen.findByText("CicloLima Plus")).toBeInTheDocument();
  fireEvent.click(
    screen.getAllByRole("button", { name: "Ingresar para probar" })[1],
  );
  expect(login).toHaveBeenCalledOnce();
  expect(api).not.toHaveBeenCalledWith(
    "/billing/subscription",
    expect.anything(),
  );
});

it("persists the selected demo plan and offers the personal CSV export", async () => {
  const user: User = {
    id: 1,
    alias: "Ana",
    email: "ana@example.com",
    district: "",
    role: "cyclist",
  };
  vi.mocked(api).mockImplementation(async (path, options) => {
    if (path === "/billing/plans") return { plans };
    if (path === "/billing/invoices") return [];
    return {
      plan_code: options?.method === "PUT" ? "plus" : "free",
      mode: "demo",
    };
  });
  render(<Billing user={user} onLogin={vi.fn()} />);
  const change = await screen.findByRole("button", {
    name: "Probar CicloLima Plus",
  });
  fireEvent.click(change);
  expect(
    await screen.findByText(/Cambiaste a CicloLima Plus/),
  ).toBeInTheDocument();
  fireEvent.click(
    screen.getByRole("button", { name: "Exportar mis favoritos" }),
  );
  expect(downloadFavorites).toHaveBeenCalledOnce();
});
