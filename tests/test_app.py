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
