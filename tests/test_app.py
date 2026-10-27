import os, tempfile
from fastapi.testclient import TestClient

_tmp=tempfile.TemporaryDirectory()
os.environ['SYSATLAS_DATABASE']=os.path.join(_tmp.name,'test.db')
from app import config
from app.main import app
from app.db import migrate
migrate()
client=TestClient(app)

def test_health():
    assert client.get('/health/live').json()=={'status':'ok'}
    assert client.get('/health/ready').status_code==200

def test_rule_create_and_duplicate():
    name='test-memory-pressure'
    r=client.post('/api/v1/alert-rules',json={'name':name,'threshold':80})
    assert r.status_code==201
    assert r.json()['threshold']==80
    assert client.post('/api/v1/alert-rules',json={'name':name,'threshold':80}).status_code==409

def test_rule_validation():
    assert client.post('/api/v1/alert-rules',json={'name':'bad','threshold':101}).status_code==422

def test_snapshots_empty():
    assert client.get('/api/v1/snapshots').json()['items']==[]

def test_collection_end_to_end():
    response=client.post('/api/v1/collect')
    assert response.status_code == 200, response.text
    assert response.json()['snapshot_id'] > 0
    assert client.get('/api/v1/snapshots/latest').status_code == 200


def test_alert_evaluate_ignores_invalid_memory_total():
    from app.alerts import evaluate

    assert evaluate(0, 0) == []
    assert evaluate(-1, 0) == []


def test_alert_fires_and_resolves():
    from app.alerts import evaluate

    name = "coverage-alert-lifecycle"
    response = client.post(
        "/api/v1/alert-rules",
        json={"name": name, "threshold": 80},
    )
    assert response.status_code == 201

    # 90% memory usage should trigger the rule.
    fired = evaluate(1000, 100)
    assert any(item["rule"] == name and item["state"] == "FIRING"
               for item in fired)

    # The existing firing incident should be updated, not fired again.
    repeated = evaluate(1000, 100)
    assert not any(item["rule"] == name for item in repeated)

    # Low memory usage should resolve the incident.
    resolved = evaluate(1000, 500)
    assert any(item["rule"] == name and item["state"] == "RESOLVED"
               for item in resolved)


def test_collector_unavailable(monkeypatch):
    import pytest
    from app.collector import collect, CollectorError

    def fake_run(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr("app.collector.subprocess.run", fake_run)

    with pytest.raises(CollectorError, match="FileNotFoundError"):
        collect()


def test_collector_nonzero_exit(monkeypatch):
    from types import SimpleNamespace
    import pytest
    from app.collector import collect, CollectorError

    monkeypatch.setattr(
        "app.collector.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=2, stdout=""),
    )

    with pytest.raises(CollectorError, match="exited with code 2"):
        collect()


def test_collector_invalid_json(monkeypatch):
    from types import SimpleNamespace
    import pytest
    from app.collector import collect, CollectorError

    monkeypatch.setattr(
        "app.collector.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="not-json"),
    )

    with pytest.raises(CollectorError, match="invalid JSON"):
        collect()


def test_collector_invalid_protocol(monkeypatch):
    from types import SimpleNamespace
    import pytest
    from app.collector import collect, CollectorError

    monkeypatch.setattr(
        "app.collector.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="{}"),
    )

    with pytest.raises(CollectorError, match="does not match protocol"):
        collect()
