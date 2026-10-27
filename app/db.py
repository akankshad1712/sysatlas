"""SQLite persistence. Each operation owns a short-lived connection."""
import os, sqlite3
from pathlib import Path
from contextlib import contextmanager
from app.config import settings

SCHEMA_VERSION = 1

@contextmanager
def connection():
    path = Path(settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def migrate():
    with connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)")
        row = conn.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
        current = row[0] if row else 0
        if current < 1:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    collected_at TEXT NOT NULL,
                    collector_version TEXT NOT NULL,
                    cpu_user INTEGER NOT NULL CHECK(cpu_user >= 0),
                    cpu_nice INTEGER NOT NULL CHECK(cpu_nice >= 0),
                    cpu_system INTEGER NOT NULL CHECK(cpu_system >= 0),
                    cpu_idle INTEGER NOT NULL CHECK(cpu_idle >= 0),
                    memory_total_kib INTEGER NOT NULL CHECK(memory_total_kib >= 0),
                    memory_available_kib INTEGER NOT NULL CHECK(memory_available_kib >= 0),
                    uptime_seconds REAL NOT NULL CHECK(uptime_seconds >= 0),
                    load1 REAL NOT NULL CHECK(load1 >= 0),
                    load5 REAL NOT NULL CHECK(load5 >= 0),
                    load15 REAL NOT NULL CHECK(load15 >= 0)
                );
                CREATE INDEX IF NOT EXISTS idx_snapshots_collected_at ON snapshots(collected_at DESC);
                CREATE TABLE IF NOT EXISTS alert_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    metric TEXT NOT NULL CHECK(metric IN ('memory_used_percent')),
                    threshold REAL NOT NULL CHECK(threshold >= 0 AND threshold <= 100),
                    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0,1))
                );
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_id INTEGER NOT NULL REFERENCES alert_rules(id),
                    fingerprint TEXT NOT NULL UNIQUE,
                    state TEXT NOT NULL CHECK(state IN ('FIRING','ACKNOWLEDGED','RESOLVED')),
                    opened_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_value REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    occurred_at TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    detail TEXT NOT NULL
                );
            """)
            conn.execute("DELETE FROM schema_version")
            conn.execute("INSERT INTO schema_version(version) VALUES (1)")

def save_snapshot(m):
    with connection() as conn:
        cur = conn.execute("""INSERT INTO snapshots(collected_at,collector_version,cpu_user,cpu_nice,cpu_system,cpu_idle,
          memory_total_kib,memory_available_kib,uptime_seconds,load1,load5,load15) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
          (m['collected_at'],m['collector_version'],m['cpu']['user'],m['cpu']['nice'],m['cpu']['system'],m['cpu']['idle'],
           m['memory']['total_kib'],m['memory']['available_kib'],m['uptime_seconds'],*m['load']))
        conn.execute("INSERT INTO audit_events(occurred_at,event_type,detail) VALUES (?,?,?)",(m['collected_at'],'snapshot.created',f"snapshot_id={cur.lastrowid}"))
        return cur.lastrowid

def list_snapshots(limit: int):
    with connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM snapshots ORDER BY id DESC LIMIT ?", (limit,))]

def latest_snapshot():
    with connection() as conn:
        row=conn.execute("SELECT * FROM snapshots ORDER BY id DESC LIMIT 1").fetchone()
        return dict(row) if row else None

def create_rule(name, threshold):
    with connection() as conn:
        cur=conn.execute("INSERT INTO alert_rules(name,metric,threshold) VALUES (?, 'memory_used_percent', ?)",(name,threshold))
        conn.execute("INSERT INTO audit_events(occurred_at,event_type,detail) VALUES (datetime('now'), 'alert_rule.created', ?)",(f"rule_id={cur.lastrowid}",))
        return cur.lastrowid

def rules():
    with connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM alert_rules ORDER BY id")]

def incidents():
    with connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM incidents ORDER BY id DESC")]
