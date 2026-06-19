/** API client for SkyLog backend */

import type { Flight, FlightCreate, DashboardStats } from "./types";

const API_BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error: ${response.status} ${error}`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  /** Get all flights */
  listFlights: () => request<Flight[]>("/flights"),

  /** Get a flight by ID */
  getFlight: (id: number) => request<Flight>(`/flights/${id}`),

  /** Create a new flight */
  createFlight: (flight: FlightCreate) =>
    request<Flight>("/flights", {
      method: "POST",
      body: JSON.stringify(flight),
    }),

  /** Update a flight */
  updateFlight: (id: number, flight: Partial<FlightCreate>) =>
    request<Flight>(`/flights/${id}`, {
      method: "PUT",
      body: JSON.stringify(flight),
    }),

  /** Delete a flight */
  deleteFlight: (id: number) =>
    request<void>(`/flights/${id}`, { method: "DELETE" }),

  /** Get dashboard stats */
  getDashboardStats: () => request<DashboardStats>("/dashboard/stats"),

  /** Health check */
  healthCheck: () => request<{ status: string }>("/health"),
};