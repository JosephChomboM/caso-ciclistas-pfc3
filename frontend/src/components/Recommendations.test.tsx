import { fireEvent, render, screen } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import Recommendations from "./Recommendations";
import { api } from "../api/client";

vi.mock("../api/client", () => ({ api: vi.fn() }));

it("submits preferences and selects a suggested route for the map", async () => {
  const cycleway = {
    id: 7,
    name: "Paseo ilustrativo",
    district: "Barranco",
    length_km: 2,
  };
  vi.mocked(api).mockResolvedValue([
    {
      cycleway,
      match_score: 85,
      published_reports: 1,
      reasons: ["Datos académicos"],
    },
  ]);
  const select = vi.fn();
  render(<Recommendations districts={["Barranco"]} onSelect={select} />);
  fireEvent.change(screen.getByLabelText("Distrito"), {
    target: { value: "Barranco" },
  });
  fireEvent.click(
    screen.getByRole("button", { name: "Encontrar sugerencias" }),
  );
  expect(await screen.findByText("Paseo ilustrativo")).toBeInTheDocument();
  expect(api).toHaveBeenCalledWith(
    "/cycleways/recommendations?target_km=3&district=Barranco",
  );
  fireEvent.click(screen.getByRole("button", { name: /Ver en el mapa/ }));
  expect(select).toHaveBeenCalledWith(cycleway);
});

it("shows a recoverable error when recommendations cannot load", async () => {
  vi.mocked(api).mockRejectedValue(new Error("No se pudo conectar"));
  render(<Recommendations districts={[]} onSelect={vi.fn()} />);
  fireEvent.click(
    screen.getByRole("button", { name: "Encontrar sugerencias" }),
  );
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "No se pudo conectar",
  );
  expect(
    screen.getByRole("button", { name: "Encontrar sugerencias" }),
  ).toBeEnabled();
});
