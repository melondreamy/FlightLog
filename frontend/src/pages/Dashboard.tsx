import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { DashboardStats, Flight } from "../api/types";

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentFlights, setRecentFlights] = useState<Flight[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.getDashboardStats(),
      api.listFlights(),
    ])
      .then(([statsData, flightsData]) => {
        setStats(statsData);
        setRecentFlights(flightsData.slice(0, 5));
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="p-8 text-center animate-fade-in">
        <div className="inline-flex items-center gap-2 bg-red-100 text-red-700 px-4 py-3 rounded-lg">
          <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Failed to load dashboard: {error}</span>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-8 max-w-4xl mx-auto animate-fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
              <div className="skeleton h-4 w-24 mb-3" />
              <div className="skeleton h-8 w-20" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  // If no flights logged
  if (stats.total_flights === 0) {
    return (
      <div className="p-4 sm:p-8 max-w-4xl mx-auto animate-fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
        <div className="text-center py-16">
          {/* Aviation icon */}
          <div className="text-6xl mb-4">✈️</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">Welcome to SkyLog!</h2>
          <p className="text-gray-500 mb-6">
            Your flight data will appear here once you start logging.
          </p>
          <button
            onClick={() => window.dispatchEvent(new CustomEvent("navigate", { detail: "add" }))}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors btn-primary"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Log Your First Flight
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-8 max-w-4xl mx-auto animate-fade-in">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <StatCard label="Total Flights" value={stats.total_flights} />
        <StatCard label="Total Hours" value={`${stats.total_hours.toFixed(1)}h`} />
        <StatCard label="PIC Hours" value={`${stats.total_pic_hours.toFixed(1)}h`} />
        <StatCard label="SIC Hours" value={`${stats.total_sic_hours.toFixed(1)}h`} />
        <StatCard label="Night Hours" value={`${stats.total_night_hours.toFixed(1)}h`} />
        <StatCard label="Instrument Hours" value={`${stats.total_instrument_hours.toFixed(1)}h`} />
        <StatCard label="Hours (Last 30 Days)" value={`${stats.hours_last_30_days.toFixed(1)}h`} />
        <StatCard label="Total Landings" value={stats.total_landings} />
        <StatCard label="Instrument Approaches" value={stats.total_approaches} />
        <StatCard label="Unique Aircraft" value={stats.unique_aircraft} />
      </div>

      {/* Recent Flights Section */}
      {recentFlights.length > 0 && (
        <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden animate-slide-up">
          <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Recent Flights</h2>
            <button
              onClick={() => window.dispatchEvent(new CustomEvent("navigate", { detail: "logbook" }))}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              View All →
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">Date</th>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">Aircraft</th>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">From → To</th>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">Duration</th>
                  <th className="px-6 py-3 text-sm font-semibold text-gray-600">PIC</th>
                </tr>
              </thead>
              <tbody>
                {recentFlights.map((flight, idx) => (
                  <tr
                    key={flight.id}
                    className="border-b border-gray-50 hover:bg-gray-50 logbook-row"
                    style={{ animationDelay: `${idx * 50}ms` }}
                  >
                    <td className="px-6 py-3 text-sm text-gray-900">{flight.date}</td>
                    <td className="px-6 py-3 text-sm">
                      <span className="text-gray-900">{flight.aircraft_type}</span>
                      <span className="text-gray-500 ml-1 text-xs">({flight.aircraft_reg})</span>
                    </td>
                    <td className="px-6 py-3 text-sm text-gray-900">{flight.departure} → {flight.arrival}</td>
                    <td className="px-6 py-3 text-sm text-gray-900">{flight.total_time.toFixed(1)}h</td>
                    <td className="px-6 py-3 text-sm text-gray-900">{flight.pilot_in_command}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({
  label,
  value,
  icon,
}: {
  label: string;
  value: number | string;
  icon?: string;
}) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 stat-card animate-slide-up">
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium text-gray-500 uppercase tracking-wide">{label}</p>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
    </div>
  );
}
