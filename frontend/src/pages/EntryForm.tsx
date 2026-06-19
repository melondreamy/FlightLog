import { useState } from "react";
import { api } from "../api/client";

interface FormState {
  date: string;
  aircraft_type: string;
  aircraft_reg: string;
  departure: string;
  arrival: string;
  departure_time: string;
  arrival_time: string;
  total_time: string;
  night_time: string;
  pilot_in_command: string;
  remarks: string;
  landings_day: string;
  landings_night: string;
  cross_country: boolean;
}

const initialForm = (): FormState => ({
  date: new Date().toISOString().split("T")[0],
  aircraft_type: "",
  aircraft_reg: "",
  departure: "",
  arrival: "",
  departure_time: "",
  arrival_time: "",
  total_time: "",
  night_time: "0",
  pilot_in_command: "",
  remarks: "",
  landings_day: "0",
  landings_night: "0",
  cross_country: false,
});

export default function EntryForm() {
  const [form, setForm] = useState<FormState>(initialForm());
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = type === "checkbox" ? (e.target as HTMLInputElement).checked : undefined;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    // Clear error on change
    if (errors[name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
  };

  const validate = (): boolean => {
    const errs: Record<string, string> = {};
    if (!form.date) errs.date = "Date is required";
    if (!form.aircraft_type.trim()) errs.aircraft_type = "Required";
    if (!form.aircraft_reg.trim()) errs.aircraft_reg = "Required";
    if (!form.departure.trim()) errs.departure = "Required";
    if (!form.arrival.trim()) errs.arrival = "Required";
    if (!form.pilot_in_command.trim()) errs.pilot_in_command = "Required";
    if (!form.total_time || parseFloat(form.total_time) <= 0) errs.total_time = "Must be > 0";
    if (form.night_time && parseFloat(form.night_time) < 0) errs.night_time = "Cannot be negative";
    if (form.night_time && form.total_time && parseFloat(form.night_time) > parseFloat(form.total_time)) {
      errs.night_time = "Cannot exceed total time";
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    setMessage(null);

    try {
      await api.createFlight({
        date: form.date,
        aircraft_type: form.aircraft_type.trim(),
        aircraft_reg: form.aircraft_reg.trim().toUpperCase(),
        departure: form.departure.trim().toUpperCase(),
        arrival: form.arrival.trim().toUpperCase(),
        departure_time: form.departure_time || null,
        arrival_time: form.arrival_time || null,
        total_time: parseFloat(form.total_time),
        night_time: parseFloat(form.night_time) || 0,
      setMessage({ type: "success", text: "Flight logged successfully!" });
      setForm(initialForm());
      setErrors({});
    } catch (err) {
      setMessage({
        type: "error",
        text: `Error: ${err instanceof Error ? err.message : "Unknown error"}`,
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-4 sm:p-8 max-w-2xl mx-auto animate-fade-in">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Log New Flight</h1>

      {/* Alert */}
      {message && (
        <div
          className={`flex items-center gap-2 p-3 rounded-lg mb-4 animate-slide-up ${
            message.type === "error" ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
          }`}
        >
          {message.type === "success" ? (
            <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          ) : (
            <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          )}
          <span className="text-sm">{message.text}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field
            label="Date"
            name="date"
            type="date"
            value={form.date}
            onChange={handleChange}
            required
            error={errors.date}
          />
          <Field
            label="Pilot in Command"
            name="pilot_in_command"
            value={form.pilot_in_command}
            onChange={handleChange}
            required
            placeholder="e.g. John Doe"
            error={errors.pilot_in_command}
          />
          <Field
            label="Aircraft Type"
            name="aircraft_type"
            value={form.aircraft_type}
            onChange={handleChange}
            required
            placeholder="e.g. Cessna 172"
            error={errors.aircraft_type}
          />
          <Field
            label="Aircraft Registration"
            name="aircraft_reg"
            value={form.aircraft_reg}
            onChange={handleChange}
            required
            placeholder="e.g. N123AB"
            error={errors.aircraft_reg}
          />
          <Field
            label="Departure (ICAO)"
            name="departure"
            value={form.departure}
            onChange={handleChange}
            required
            placeholder="e.g. KLAX"
            error={errors.departure}
          />
          <Field
            label="Arrival (ICAO)"
            name="arrival"
            value={form.arrival}
            onChange={handleChange}
            required
            placeholder="e.g. KCRQ"
            error={errors.arrival}
          />
          <Field
            label="Departure Time"
            name="departure_time"
            type="time"
            value={form.departure_time}
            onChange={handleChange}
          />
          <Field
            label="Arrival Time"
            name="arrival_time"
            type="time"
            value={form.arrival_time}
            onChange={handleChange}
          />
          <Field
            label="Total Time (hours)"
            name="total_time"
            type="number"
            step="0.1"
            min="0"
            value={form.total_time}
            onChange={handleChange}
            required
            placeholder="e.g. 1.5"
            error={errors.total_time}
          />
          <Field
            label="Night Time (hours)"
            name="night_time"
            type="number"
            step="0.1"
            min="0"
            value={form.night_time}
            onChange={handleChange}
            placeholder="e.g. 0.5"
            error={errors.night_time}
          />
          <Field
            label="Day Landings"
            name="landings_day"
            type="number"
            min="0"
            value={form.landings_day}
            onChange={handleChange}
          />
          <Field
            label="Night Landings"
            name="landings_night"
            type="number"
            min="0"
            value={form.landings_night}
            onChange={handleChange}
          />
        </div>

        {/* Cross Country Checkbox */}
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            name="cross_country"
            id="cross_country"
            checked={form.cross_country}
            onChange={handleChange}
            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <label htmlFor="cross_country" className="text-sm text-gray-700 select-none">
            Cross Country
          </label>
        </div>

        {/* Remarks */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Remarks</label>
          <textarea
            name="remarks"
            value={form.remarks}
            onChange={handleChange}
            rows={3}
            placeholder="VFR flight, smooth conditions, etc."
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400 resize-none"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={saving}
          className="w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors btn-primary flex items-center justify-center gap-2"
        >
          {saving ? (
            <>
              <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Saving...
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Log Flight
            </>
          )}
        </button>
      </form>
    </div>
  );
}

function Field({
  label,
  name,
  type = "text",
  value,
  onChange,
  required,
  step,
  min,
  placeholder,
  error,
}: {
  label: string;
  name: string;
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  required?: boolean;
  step?: string;
  min?: string;
  placeholder?: string;
  error?: string;
}) {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        step={step}
        min={min}
        placeholder={placeholder}
        className={`w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 transition-colors placeholder:text-gray-400 ${
          error
            ? "border-red-400 focus:ring-red-500"
            : "border-gray-300 focus:ring-blue-500"
        }`}
      />
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}
