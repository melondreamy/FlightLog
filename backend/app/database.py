"""Database configuration and connection for SkyLog."""

import sqlite3
import os
from pathlib import Path

# Default to a local SQLite file in the backend directory
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "skylog.db"


def get_db_path() -> str:
    """Get database path, allowing override via env var."""
    return os.environ.get("SKYLOG_DB_PATH", str(DEFAULT_DB_PATH))


def get_connection() -> sqlite3.Connection:
    """Create and return a new SQLite connection with row factory enabled."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db() -> None:
    """Initialize database tables and handle migrations."""
    conn = get_connection()
    try:
        # Create users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                username          TEXT    UNIQUE NOT NULL,
                email             TEXT    UNIQUE NOT NULL,
                hashed_password   TEXT    NOT NULL,
                is_admin          INTEGER DEFAULT 0,
                full_name         TEXT,
                settings          TEXT    DEFAULT '{}',
                created_at        TEXT    DEFAULT (datetime('now'))
            );
        """)
        
        # Create global welcome_config table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS global_config (
                key               TEXT PRIMARY KEY,
                value             TEXT
            );
        """)

        # Initialize global welcome config if not exists
        cursor = conn.execute("SELECT COUNT(*) as count FROM global_config WHERE key = 'welcome_page'")
        if cursor.fetchone()["count"] == 0:
            import json
            default_welcome = {
                "title": "Welcome to SkyLog",
                "description": "Your privacy-first, self-hosted digital flight logbook.",
                "features": ["Secure Data", "Customizable Columns", "FAA 8710-1 Reports"],
                "background_style": "default"
            }
            conn.execute("INSERT INTO global_config (key, value) VALUES (?, ?)", ("welcome_page", json.dumps(default_welcome)))

        # Create user welcome_config table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS welcome_config (
                user_id           INTEGER PRIMARY KEY,
                show_welcome      INTEGER DEFAULT 1,
                setup_complete    INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Create flights table if not exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                date              TEXT    NOT NULL,
                aircraft_type     TEXT    NOT NULL,
                aircraft_reg      TEXT    NOT NULL,
                departure         TEXT    NOT NULL,
                arrival           TEXT    NOT NULL,
                departure_time    TEXT,
                arrival_time      TEXT,
                total_time        REAL    NOT NULL CHECK(total_time > 0),
                night_time        REAL    DEFAULT 0 CHECK(night_time >= 0),
                pic_time          REAL    DEFAULT 0 CHECK(pic_time >= 0),
                sic_time          REAL    DEFAULT 0 CHECK(sic_time >= 0),
                dual_received     REAL    DEFAULT 0 CHECK(dual_received >= 0),
                dual_given        REAL    DEFAULT 0 CHECK(dual_given >= 0),
                actual_instrument REAL    DEFAULT 0 CHECK(actual_instrument >= 0),
                sim_instrument    REAL    DEFAULT 0 CHECK(sim_instrument >= 0),
                approaches        INTEGER DEFAULT 0 CHECK(approaches >= 0),
                pilot_in_command  TEXT    NOT NULL,
                remarks           TEXT,
                landings_day      INTEGER DEFAULT 0 CHECK(landings_day >= 0),
                landings_night    INTEGER DEFAULT 0 CHECK(landings_night >= 0),
                cross_country     INTEGER DEFAULT 0,
                created_at        TEXT    DEFAULT (datetime('now'))
            );
        """)

        # Migration: Check if columns exist in flights
        cursor = conn.execute("PRAGMA table_info(flights)")
        columns = [row['name'] for row in cursor.fetchall()]
        
        if 'user_id' not in columns:
            conn.execute("ALTER TABLE flights ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE")
        
        if 'custom_fields' not in columns:
            conn.execute("ALTER TABLE flights ADD COLUMN custom_fields TEXT")

        # Create endorsements table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS endorsements (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id           INTEGER NOT NULL,
                instructor_id     INTEGER,
                date              TEXT    NOT NULL,
                endorsement_type  TEXT    NOT NULL,
                text              TEXT    NOT NULL,
                created_at        TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE SET NULL
            );
        """)

        # Create certificates table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS certificates (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id           INTEGER NOT NULL,
                certificate_type  TEXT    NOT NULL,
                rating            TEXT    NOT NULL,
                date_issued       TEXT    NOT NULL,
                certificate_number TEXT,
                created_at        TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        conn.commit()
    finally:
        conn.close()
