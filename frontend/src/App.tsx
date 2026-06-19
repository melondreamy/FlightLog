import { useState, useEffect } from "react";
import Dashboard from "./pages/Dashboard";
import Logbook from "./pages/Logbook";
import EntryForm from "./pages/EntryForm";

type Page = "dashboard" | "logbook" | "add";

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>("dashboard");

  // Listen for custom navigate events from child components
  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail;
      if (detail === "add") setCurrentPage("add");
      else if (detail === "logbook") setCurrentPage("logbook");
      else if (detail === "dashboard") setCurrentPage("dashboard");
    };
    window.addEventListener("navigate", handler);
    return () => window.removeEventListener("navigate", handler);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <span className="text-2xl">✈️</span>
              <h1 className="text-xl font-bold text-gray-900">SkyLog</h1>
            </div>

            {/* Navigation */}
            <nav className="flex gap-1">
              <NavButton
                active={currentPage === "dashboard"}
                onClick={() => setCurrentPage("dashboard")}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                <span className="hidden sm:inline">Dashboard</span>
              </NavButton>
              <NavButton
                active={currentPage === "logbook"}
                onClick={() => setCurrentPage("logbook")}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="hidden sm:inline">Logbook</span>
              </NavButton>
              <NavButton
                active={currentPage === "add"}
                onClick={() => setCurrentPage("add")}
                highlight
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span className="hidden sm:inline">New Flight</span>
              </NavButton>
            </nav>
          </div>
        </div>
      </header>

      {/* Page Content */}
      <main className="animate-fade-in" key={currentPage}>
        {currentPage === "dashboard" && <Dashboard />}
        {currentPage === "logbook" && <Logbook />}
        {currentPage === "add" && <EntryForm />}
      </main>
    </div>
  );
}

function NavButton({
  active,
  onClick,
  children,
  highlight,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
  highlight?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
        active
          ? "bg-blue-100 text-blue-700"
          : highlight
            ? "text-blue-600 hover:text-blue-700 hover:bg-blue-50"
            : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
      }`}
    >
      {children}
    </button>
  );
}
