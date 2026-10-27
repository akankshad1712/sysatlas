"""Deterministic memory-pressure alert evaluation."""
from datetime import datetime, timezone
from app.db import connection

def evaluate(memory_total_kib: int, memory_available_kib: int):
    if memory_total_kib <= 0:
        return []
    used=max(0.0,min(100.0,100.0*(memory_total_kib-memory_available_kib)/memory_total_kib))
    now=datetime.now(timezone.utc).isoformat()
    changed=[]
    with connection() as conn:
        rules=conn.execute("SELECT * FROM alert_rules WHERE enabled=1").fetchall()
        for rule in rules:
            fingerprint=f"rule:{rule['id']}"
            row=conn.execute("SELECT * FROM incidents WHERE fingerprint=?",(fingerprint,)).fetchone()
            if used >= rule['threshold']:
                if row is None or row['state']=='RESOLVED':
                    conn.execute("INSERT OR REPLACE INTO incidents(rule_id,fingerprint,state,opened_at,updated_at,last_value) VALUES (?,?, 'FIRING',?,?,?)",
                      (rule['id'],fingerprint,now,now,used))
                    changed.append({'rule':rule['name'],'state':'FIRING','value':round(used,2)})
                else:
                    conn.execute("UPDATE incidents SET updated_at=?,last_value=? WHERE id=?",(now,used,row['id']))
            elif row is not None and row['state']!='RESOLVED':
                conn.execute("UPDATE incidents SET state='RESOLVED',updated_at=?,last_value=? WHERE id=?",(now,used,row['id']))
                changed.append({'rule':rule['name'],'state':'RESOLVED','value':round(used,2)})
    return changed
