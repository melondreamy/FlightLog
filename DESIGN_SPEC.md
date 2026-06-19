# SkyLog — UI/UX Design Specification

> **Version:** 1.0  
> **Author:** Designer (agent-designer)  
> **Date:** 2026-06-18  
> **Stack:** React 19 + TypeScript + Vite + Tailwind CSS 4

---

## 1. Design System

### 1.1 Color Palette

| Token | Tailwind | Hex | Usage |
|-------|----------|-----|-------|
| Primary | `blue-600` | `#2563eb` | Buttons, links, active states |
| Primary Light | `blue-100` | `#dbeafe` | Active nav button bg |
| Primary Dark | `blue-700` | `#1d4ed8` | Button hover |
| Surface | `white` | `#ffffff` | Cards, header, table rows |
| Background | `gray-50` | `#f9fafb` | Page background |
| Border | `gray-200` | `#e5e7eb` | Table borders, card borders |
| Border Input | `gray-300` | `#d1d5db` | Form input borders |
| Text Primary | `gray-900` | `#111827` | Headings, primary text |
| Text Secondary | `gray-600` | `#4b5563` | Body text, labels |
| Text Muted | `gray-500` | `#6b7280` | Placeholder, hints |
| Success | `green-100`/`green-700` | — | Success messages |
| Error | `red-100`/`red-600` | — | Error messages, validation |
| Accent (aviation) | `sky-500` | `#0ea5e9` | Icons, highlights |

### 1.2 Typography

| Element | Class | Size | Weight |
|---------|-------|------|--------|
| Page heading | `text-3xl font-bold` | 30px / 1.2 | 700 |
| Card heading | `text-sm font-medium uppercase tracking-wide` | 14px / 1 | 500 |
| Card value | `text-3xl font-bold` | 30px / 1.2 | 700 |
| Table header | `text-sm font-semibold` | 14px / 1 | 600 |
| Table cell | `text-sm` (default) | 14px / 1 | 400 |
| Form label | `text-sm font-medium` | 14px / 1.25 | 500 |
| Form input | `text-sm` | 14px / 1.5 | 400 |
| Nav button | `text-sm font-medium` | 14px / 1 | 500 |

**Font Family:** System UI stack (default in Tailwind): `ui-sans-serif, system-ui, -apple-system, sans-serif`.

### 1.3 Spacing Grid

- Page padding: `p-4 sm:p-8` (16px → 32px)
- Content max-width: `max-w-4xl` (Dashboard), `max-w-6xl` (Logbook), `max-w-2xl` (Entry Form)
- Card padding: `p-6`
- Card gap: `gap-4`
- Section margin-bottom: `mb-6`

### 1.4 Shadows & Border Radius

| Component | Border Radius | Shadow |
|-----------|--------------|--------|
| Cards | `rounded-xl` (12px) | `shadow-md` |
| Buttons | `rounded-lg` (8px) | None |
| Inputs | `rounded-lg` (8px) | None (border only) |
| Nav buttons | `rounded-lg` (8px) | None |
| Alert banners | `rounded-lg` (8px) | None |

---

## 2. Layout & Navigation

### 2.1 Page Structure

```
┌─────────────────────────────────────────────────┐
│  HEADER (sticky)                                 │
│  ┌──────┐  ┌─────────┐ ┌─────────┐ ┌────────┐  │
│  │SkyLog│  │Dashboard│ │Logbook  │ │+ Flight│  │
│  └──────┘  └─────────┘ └─────────┘ └────────┘  │
├─────────────────────────────────────────────────┤
│                                                 │
│  MAIN CONTENT AREA                              │
│                                                 │
│  (Dashboard / Logbook / Entry Form)             │
│                                                 │
└─────────────────────────────────────────────────┘
```

- **Header** is a fixed top bar with the SkyLog logo/name on the left and navigation tabs on the right.
- **Active tab** is highlighted with `bg-blue-100 text-blue-700`.
- **No sidebar** — simple tab-based navigation keeps it mobile-friendly.

### 2.2 Responsive Behavior

| Breakpoint | Width | Layout Changes |
|-----------|-------|----------------|
| Default (mobile) | <640px | Single column, nav tabs stacked/compact, tables horizontally scrollable |
| `sm` | ≥640px | 2-column stat grid on dashboard, 2-column form fields |
| `md` | ≥768px | — |
| `lg` | ≥1024px | 3-column stat grid on dashboard |

---

## 3. Page Designs

### 3.1 Dashboard Page

**Purpose:** At-a-glance overview of pilot's flying statistics.

```
┌──────────────────────────────────────────────────┐
│  Dashboard                                        │
│                                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────┐   │
│  │ Total Flights│ │ Total Hours │ │Night Hours│   │
│  │     42      │ │   156.3h    │ │   28.5h   │   │
│  └─────────────┘ └─────────────┘ └───────────┘   │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────┐   │
│  │Last 30 Days │ │ Total Land. │ │ Unique AC │   │
│  │    8.2h     │ │     84      │ │     3     │   │
│  └─────────────┘ └─────────────┘ └───────────┘   │
│                                                   │
│  ┌──────────────────────────────────────────┐     │
│  │  Recent Flights (last 5)                 │     │
│  │  ┌──────┬────────┬────┬────┬──────┬────┐ │     │
│  │  │ Date │Aircraft│From│ To │Hours │ PIC│ │     │
│  │  ├──────┼────────┼────┼────┼──────┼────┤ │     │
│  │  │06/15 │ C172   │KLAX│KCRQ│ 1.2  │ J.D│ │     │
│  │  │06/12 │ PA28   │KCRQ│KBUR│ 0.8  │ J.D│ │     │
│  │  │...   │ ...    │... │ ...│ ...  │ ...│ │     │
│  │  └──────┴────────┴────┴────┴──────┴────┘ │     │
│  └──────────────────────────────────────────┘     │
└──────────────────────────────────────────────────┘
```

**Stat Cards:**
- White card with `rounded-xl`, `shadow-md`, `border border-gray-100`
- Label: uppercase, small, gray-500
- Value: large bold gray-900
- 3 columns on desktop, 2 on tablet, 1 on mobile

**Recent Flights Section:**
- A compact table below the stat cards showing the 5 most recent entries
- Same table styling as the Logbook page but only 5 rows
- "View All" link that navigates to the full Logbook

**States:**
- **Loading:** Centered spinner/message "Loading dashboard..."
- **Empty (no flights):** Show welcome message with call-to-action to add first flight
- **Error:** Red error banner with message text

---

### 3.2 Logbook Page

**Purpose:** Full searchable, sortable table of all flight entries.

```
┌──────────────────────────────────────────────────────┐
│  Logbook                                              │
│                                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Search flights...]                    [Sort ▼] │   │
│  └─────────────────────────────────────────────────┘   │
│                                                        │
│  ┌──────┬──────────┬──────┬──────┬───────┬─────┬───┐  │
│  │ Date │ Aircraft │ From │  To  │ Hours │ PIC │ ⚙ │  │
│  ├──────┼──────────┼──────┼──────┼───────┼─────┼───┤  │
│  │06/15 │ C172     │ KLAX │ KCRQ │ 1.2   │ J.D │ ✎🗑│  │
│  │06/12 │ PA28     │ KCRQ │ KBUR │ 0.8   │ J.D │ ✎🗑│  │
│  │06/10 │ C172     │ KCRQ │ KSNA │ 0.5   │ J.D │ ✎🗑│  │
│  │...   │ ...      │ ...  │ ...  │ ...   │ ... │    │  │
│  └──────┴──────────┴──────┴──────┴───────┴─────┴───┘  │
│                                                        │
│  Showing 1-10 of 42 flights                  [1] [2] ► │
└──────────────────────────────────────────────────────┘
```

**Table Columns:**
1. **Date** — Flight date (formatted)
2. **Aircraft** — Type + Registration (e.g., "C172 (N123AB)")
3. **From** — Departure ICAO
4. **To** — Arrival ICAO
5. **Duration** — Total time in hours (`1.2h`)
6. **PIC** — Pilot in Command name
7. **Actions** — Edit/Delete icons (appears on hover)

**Features (Phase 2 MVP → Phase 3):**
- **Sorting:** Click column header to sort ascending/descending
- **Search:** Free-text search box that filters by aircraft, airport, or remarks
- **Pagination:** Page navigation at the bottom (10-25 rows per page)
- **Row actions:** Edit (pencil icon) and Delete (trash icon) buttons on hover
- **Edit in place:** Clicking edit opens the EntryForm pre-populated with flight data

**States:**
- **Loading:** Full-width skeleton rows (3-4 grey bars)
- **Empty:** Illustration/icon + "No flights logged yet. Add your first flight to get started."
- **Error:** Red error banner
- **Search no results:** "No flights match your search." with clear search option

---

### 3.3 Entry Form Page

**Purpose:** Add new flight entries or edit existing ones.

```
┌────────────────────────────────────────────┐
│  Log New Flight       [Edit Mode: ✏ Edit] │
│                                             │
│  ┌─────────────────────────────────────────┐│
│  │ ✓ Flight logged successfully!           ││
│  └─────────────────────────────────────────┘│
│                                             │
│  ┌───────────────────┐ ┌──────────────────┐ │
│  │ Date*             │ │ Pilot in Command*│ │
│  │ [2026-06-18    ▼] │ │ [John Doe      ] │ │
│  └───────────────────┘ └──────────────────┘ │
│  ┌───────────────────┐ ┌──────────────────┐ │
│  │ Aircraft Type*    │ │ Registration*    │ │
│  │ [Cessna 172     ] │ │ [N123AB        ] │ │
│  └───────────────────┘ └──────────────────┘ │
│  ┌───────────────────┐ ┌──────────────────┐ │
│  │ Departure (ICAO)* │ │ Arrival (ICAO)*  │ │
│  │ [KLAX            ] │ │ [KCRQ           ] │ │
│  └───────────────────┘ └──────────────────┘ │
│  ┌───────────────────┐ ┌──────────────────┐ │
│  │ Departure Time    │ │ Arrival Time     │ │
│  │ [14:30           ] │ │ [15:45          ] │ │
│  └───────────────────┘ └──────────────────┘ │
│  ┌───────────────────┐ ┌──────────────────┐ │
│  │ Total Time (hrs)* │ │ Night Time (hrs) │ │
│  │ [1.2             ] │ │ [0.0            ] │ │
│  └───────────────────┘ └──────────────────┘ │
│  ┌───────────────────┐ ┌──────────────────┐ │
│  │ Day Landings      │ │ Night Landings   │ │
│  │ [3               ] │ │ [0              ] │ │
│  └───────────────────┘ └──────────────────┘ │
│                                             │
│  ☐ Cross Country                            │
│                                             │
│  Remarks:                                   │
│  ┌─────────────────────────────────────────┐│
│  │ VFR flight, smooth air, great visibility││
│  └─────────────────────────────────────────┘│
│                                             │
│  ┌─────────────────────────────────────────┐│
│  │          [ Log Flight ]                 ││
│  └─────────────────────────────────────────┘│
└────────────────────────────────────────────┘
```

**Layout:**
- Two-column grid on tablet/desktop, single column on mobile
- Required fields marked with red asterisk (`*`)
- ICAO airport codes auto-uppercased on input

**Form Fields:**
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Date | `date` | Yes | Must not be in the future (practical check) |
| Pilot in Command | `text` | Yes | Non-empty |
| Aircraft Type | `text` | Yes | Non-empty |
| Aircraft Registration | `text` | Yes | Non-empty |
| Departure (ICAO) | `text` | Yes | Auto-uppercase, 3-4 chars |
| Arrival (ICAO) | `text` | Yes | Auto-uppercase, 3-4 chars |
| Departure Time | `time` | No | — |
| Arrival Time | `time` | No | — |
| Total Time | `number` (step 0.1) | Yes | > 0 |
| Night Time | `number` (step 0.1) | No | ≥ 0, ≤ total_time |
| Day Landings | `number` | No | ≥ 0 |
| Night Landings | `number` | No | ≥ 0 |
| Cross Country | `checkbox` | No | — |
| Remarks | `textarea` | No | — |

**States:**
- **Create mode:** Empty form with today's date pre-filled
- **Edit mode:** Form pre-populated with existing flight data, button says "Update Flight"
- **Saving:** Button shows "Saving..." and is disabled
- **Success:** Green banner "Flight logged successfully!" with form reset
- **Error:** Red banner with error details
- **Validation:** Red border on invalid fields, inline error messages

---

## 4. Component Library

### 4.1 Shared Components

| Component | Props | Description |
|-----------|-------|-------------|
| `StatCard` | `label: string`, `value: number|string` | Dashboard stat display card |
| `NavButton` | `active: boolean`, `onClick: () => void`, `children` | Navigation tab button |
| `Field` | `label, name, type, value, onChange, required?, step?` | Form input with label |
| `FlightTable` | `flights: Flight[]`, `onEdit?, onDelete?` | Reusable table component |
| `Alert` | `type: 'success'|'error'`, `message: string` | Banner notification |
| `SearchBar` | `value: string`, `onChange` | Search input with icon |
| `Pagination` | `page, totalPages, onPageChange` | Page number navigation |

### 4.2 Future Components (Phase 3+)

- **ExportButton** — CSV/PDF export trigger
- **CurrencyBadge** — Shows currency status (current/expiring/expired)
- **AircraftSelector** — Dropdown with recently used aircraft
- **ConfirmDialog** — "Are you sure?" before delete
- **DateRangePicker** — Filter flights by date range

---

## 5. Interaction Design

### 5.1 Micro-interactions

| Element | Hover | Active/Focus | Transition |
|---------|-------|--------------|------------|
| Nav button | `bg-gray-100` | `bg-blue-100 text-blue-700` | `transition-colors` 150ms |
| Table row | `bg-gray-50` | — | 150ms ease |
| Primary button | `bg-blue-700` | scale(0.98) | `transition-colors` 150ms |
| Input field | — | `ring-2 ring-blue-500` | 150ms |
| Stat card | subtle lift (`translateY(-2px)`) | — | 200ms ease |

### 5.2 Loading States

- **Initial load:** Use skeleton/placeholder UI rather than full-page spinners
- **Data refresh:** Inline loading indicators (dimmed text)
- **Action feedback:** Button loading state with disabled interaction

### 5.3 Empty States

Each page needs a thoughtful empty state:

- **Dashboard (no data):** Welcome card with "Log your first flight to see your stats!"
- **Logbook (no data):** Centered illustration + "No flights yet. Ready for takeoff?"
- **Search (no results):** "No flights match your search. Try different terms."

---

## 6. Accessibility

- All form inputs must have associated `<label>` elements (already implemented via `htmlFor`)
- Color contrast: All text meets WCAG AA (already handled by Tailwind defaults)
- Focus indicators: Visible focus ring on all interactive elements
- Navigation: Logical tab order matching visual order
- Button text: Descriptive (not just icons without aria-labels)
- Click targets: Minimum 44×44px touch target on mobile

---

## 7. Page URLs (for future routing)

Once client-side routing is added:

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Redirect or the landing dashboard |
| `/logbook` | Logbook | Full flight table |
| `/logbook/new` | EntryForm (create) | Add new flight |
| `/logbook/:id/edit` | EntryForm (edit) | Edit existing flight |

---

## 8. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-18 | agent-designer | Initial design specification |
