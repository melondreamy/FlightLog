# SkyLog

A privacy-first, self-hosted digital flight logbook for pilots.

## Features

- **📊 Dashboard** — View total hours, recent flights, and key stats at a glance.
- **📖 Logbook** — Browse all flight entries in a clean table view.
- **✈️ Add Flights** — Log new flights with aircraft, route, times, and remarks.
- **🔒 Self-Hosted** — Full data ownership. Run it on your own server via Docker.

## Quick Start

### Using Docker (recommended)

```bash
docker compose up -d
```

Then open http://localhost:3000 in your browser.

### Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack

| Layer      | Technology        |
| ---------- | ----------------- |
| Backend    | Python / FastAPI  |
| Database   | SQLite            |
| Frontend   | React / TypeScript / Vite / Tailwind CSS |
| Container  | Docker / Compose  |

## License

MIT