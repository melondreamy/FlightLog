/** Flight types for SkyLog frontend */

export interface Flight {
  id: number;
  date: string;
  aircraft_type: string;
  aircraft_reg: string;
  departure: string;
  arrival: string;
  departure_time: string | null;
  arrival_time: string | null;
  total_time: number;
  night_time: number;
  pic_time: number;
  sic_time: number;
  dual_received: number;
  dual_given: number;
  actual_instrument: number;
  sim_instrument: number;
  approaches: number;
  pilot_in_command: string;
  remarks: string | null;
  landings_day: number;
  landings_night: number;
  cross_country: boolean;
  created_at: string;
}

export interface FlightCreate {
  date: string;
  aircraft_type: string;
  aircraft_reg: string;
  departure: string;
  arrival: string;
  departure_time?: string | null;
  arrival_time?: string | null;
  total_time: number;
  night_time?: number;
  pic_time?: number;
  sic_time?: number;
  dual_received?: number;
  dual_given?: number;
  actual_instrument?: number;
  sim_instrument?: number;
  approaches?: number;
  pilot_in_command: string;
  remarks?: string | null;
  landings_day?: number;
  landings_night?: number;
  cross_country?: boolean;
}

export interface DashboardStats {
  total_flights: number;
  total_hours: number;
  total_night_hours: number;
  total_pic_hours: number;
  total_sic_hours: number;
  total_instrument_hours: number;
  hours_last_30_days: number;
  total_landings: number;
  total_approaches: number;
  unique_aircraft: number;
}