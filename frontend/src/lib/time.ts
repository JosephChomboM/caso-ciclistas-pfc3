export function dateInLima(value: string): string {
  // SQLite conserva el instante UTC de la API sin sufijo de zona.
  const normalized =
    value.includes("T") && !/(Z|[+-]\d{2}:\d{2})$/i.test(value)
      ? `${value}Z`
      : value;
  return new Date(normalized).toLocaleDateString("es-PE", {
    timeZone: "America/Lima",
  });
}
