export type User = {
  id: number;
  alias: string;
  email: string;
  district: string;
  role: string;
};
export type Cycleway = {
  id: number;
  name: string;
  district: string;
  condition: string;
  geometry: [number, number][];
  length_km: number;
  source: string;
  is_demo: boolean;
  updated_at: string;
};
export type Parking = {
  id: number;
  name: string;
  district: string;
  latitude: number;
  longitude: number;
  address: string;
  hours: string;
  rack_type: string;
  source: string;
  is_demo: boolean;
  updated_at: string;
};
export type Report = {
  id: number;
  cycleway_id: number;
  category: string;
  description: string;
  latitude: number;
  longitude: number;
  status: string;
  created_at: string;
};

let token: string | null = null;
export const session = {
  set: (value: string | null) => {
    token = value;
  },
};

export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body) headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  let response: Response;
  try {
    response = await fetch(`${import.meta.env.VITE_API_URL || ""}/api${path}`, {
      ...options,
      headers,
    });
  } catch {
    throw new Error(
      "No pudimos conectar. Comprueba tu conexión y vuelve a intentar.",
    );
  }
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(
      typeof body?.detail === "string"
        ? body.detail
        : "Revisa los datos e inténtalo nuevamente.",
    );
  }
  return response.status === 204 ? (undefined as T) : response.json();
}
