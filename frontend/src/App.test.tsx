import { fireEvent, render, screen } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import App from "./App";

vi.mock("./components/MapCanvas", () => ({
  default: () => <div>Mapa de prueba</div>,
}));
vi.mock("./components/Account", () => ({
  default: ({ onUser }: { onUser: (user: object) => void }) => (
    <button
      onClick={() =>
        onUser({
          id: 1,
          alias: "Ana",
          email: "ana@example.com",
          district: "",
          role: "cyclist",
        })
      }
    >
      Entrar de prueba
    </button>
  ),
}));
vi.mock("./api/client", () => ({
  api: vi.fn(async (path: string) => {
    if (path === "/parking")
      return [
        {
          id: 1,
          name: "Parking demostración",
          district: "Barranco",
          latitude: -12.1,
          longitude: -77,
          is_demo: true,
          source: "Demo",
          updated_at: "2026-11-19",
        },
      ];
    return [];
  }),
}));

it("recovers from an empty favorites filter when clearing filters", async () => {
  render(<App />);
  fireEvent.click(screen.getByRole("button", { name: "Ingresar" }));
  fireEvent.click(screen.getByRole("button", { name: "Entrar de prueba" }));
  fireEvent.click(screen.getByRole("button", { name: "Estacionamientos" }));
  expect(await screen.findByText("Parking demostración")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("checkbox", { name: "Solo mis favoritos" }));
  expect(screen.getByText("No encontramos coincidencias")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Limpiar filtros" }));
  expect(screen.getByText("Parking demostración")).toBeInTheDocument();
  expect(
    screen.getByRole("checkbox", { name: "Solo mis favoritos" }),
  ).not.toBeChecked();
});
