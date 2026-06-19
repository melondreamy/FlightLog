import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Flight } from "../api/types";

const PAGE_SIZE = 15;

export default function Logbook() {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);

  useEffect(() => {
    api.listFlights().then(setFlights).catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="p-8 text-center animate-fade-in">
        <div className="inline-flex items-center gap-2 bg-red-100 text-red-700 px-4 py-3 rounded-lg">
          <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Failed to load flights: {error}</span>
        </div>
      </div>
    );
  }

  // Filter by search term
  const q = search.toLowerCase().trim();
  const filtered = q
    ? flights.filter(
        (f) =>
          f.aircraft_type.toLowerCase().includes(q) ||
          f.aircraft_reg.toLowerCase().includes(q) ||
          f.departure.toLowerCase().includes(q) ||
          f.arrival.toLowerCase().includes(q) ||
          f.pilot_in_command.toLowerCase().includes(q) ||
          (f.remarks && f.remarks.toLowerCase().includes(q))
      )
    : flights;

  // Paginate
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(page, totalPages - 1);
  const paged = filtered.slice(safePage * PAGE_SIZE, (safePage + 1) * PAGE_SIZE);

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this flight record?")) return;
    try {
      await api.deleteFlight(id);
      setFlights((prev) => prev.filter((f) => f.id !== id));
    } catch (err) {
      alert(`Failed to delete: ${err instanceof Error ? err.message : "Unknown error"}`);
    }
  };

  // Empty state — no flights at all
  if (flights.length === 0) {
    return (
      <div className="p-8 text-center animate-fade-in">
        <div className="max-w-md mx-auto py-16">
          <div className="text-6xl mb-4">📖</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">No flights logged yet</h2>
          <p className="text-gray-500 mb-6">
            Ready for takeoff? Add your first flight to get started.
          </p>
          <button
            onClick={() => window.dispatchEvent(new CustomEvent("navigate", { detail: "add" }))}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors btn-primary"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Your First Flight
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Logbook</h1>
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
              fill="none" viewBox="0 0 24 24" stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search flights..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(0); }}
              className="pl-9 pr-3 py-2 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-48 sm:w-56"
            />
          </div>

          {/* Add flight button */}
          <button
            onClick={() => window.dispatchEvent(new CustomEvent("navigate", { detail: "add" }))}
            className="inline-flex items-center gap-1.5 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors btn-primary whitespace-nowrap"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Flight
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
        {filtered.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <p className="text-lg">No flights match your search.</p>
            <button
              onClick={() => { setSearch(""); setPage(0); }}
              className="text-sm text-blue-600 hover:text-blue-700 mt-2 underline"
            >
              Clear search
            </button>
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b-2 border-gray-200 bg-gray-50">
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600">Date</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600">Aircraft</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600">From</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600">To</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600">Duration</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600">PIC</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-600 w-16">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {paged.map((flight, idx) => (
                    <tr
                      key={flight.id}
                      className="border-b border-gray-100 hover:bg-gray-50 logbook-row"
                      style={{ animationDelay: `${idx * 30}ms` }}
                    >
                      <td className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">{flight.date}</td>
                      <td className="px-4 py-3 text-sm whitespace-nowrap">
                        <span className="text-gray-900 font-medium">{flight.aircraft_type}</span>
                        <span className="text-gray-400 ml-1 text-xs">({flight.aircraft_reg})</span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">{flight.departure}</td>
                      <td className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">{flight.arrival}</td>
                      <td className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">{flight.total_time.toFixed(1)}h</td>
                      <td className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">{flight.pilot_in_command}</td>
                      <td className="px-4 py-3 row-actions whitespace-nowrap">
                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => alert("Edit: Implement edit navigation")}
                            className="p-1.5 rounded-md text-gray-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                            title="Edit flight"
                          >
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => handleDelete(flight.id)}
                            className="p-1.5 rounded-md text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                            title="Delete flight"
                          >
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-t border-gray-200 text-sm text-gray-600">
                <span>
                  Showing {safePage * PAGE_SIZE + 1}–{Math.min((safePage + 1) * PAGE_SIZE, filtered.length)} of{" "}
                  {filtered.length} flights
                </span>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setPage((p) => Math.max(0, p - 1))}
                    disabled={safePage === 0}
                    className="px-3 py-1.5 rounded-md hover:bg-gray-200 disabled:opacity-30 disabled:hover:bg-transparent transition-colors"
                  >
                    ‹ Prev
                  </button>
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    const start = Math.max(0, Math.min(safePage - 2, totalPages - 5));
                    const pg = start + i;
                    return (
                      <button
                        key={pg}
                        onClick={() => setPage(pg)}
                        className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
                          pg === safePage
                            ? "bg-blue-600 text-white"
                            : "hover:bg-gray-200 text-gray-700"
                        }`}
                      >
                        {pg + 1}
                      </button>
                    );
                  })}
                  <button
                    onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                    disabled={safePage >= totalPages - 1}
                    className="px-3 py-1.5 rounded-md hover:bg-gray-200 disabled:opacity-30 disabled:hover:bg-transparent transition-colors"
                  >
                    Next ›
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
