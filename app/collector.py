"""Safe bounded adapter for the native collector executable."""
import json, subprocess
from datetime import datetime, timezone
from app.config import settings

class CollectorError(RuntimeError):
    pass

def collect():
    try:
        result=subprocess.run([settings.collector_binary], capture_output=True, text=True,
            timeout=settings.collection_timeout_seconds, check=False, close_fds=True)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CollectorError(f"collector unavailable: {type(exc).__name__}") from exc
    if result.returncode != 0:
        raise CollectorError(f"collector exited with code {result.returncode}")
    try:
        data=json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CollectorError("collector returned invalid JSON") from exc
    required={'protocol_version','collector_version','cpu','memory','uptime_seconds','load'}
    if not isinstance(data,dict) or not required.issubset(data):
        raise CollectorError("collector output does not match protocol")
    data['collected_at']=datetime.now(timezone.utc).isoformat()
    return data
