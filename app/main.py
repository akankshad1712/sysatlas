"""SysAtlas Omega API. Run with: uvicorn app.main:app --reload"""
import logging, uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.config import settings
from app.db import migrate, save_snapshot, list_snapshots, latest_snapshot, create_rule, rules, incidents
from app.collector import collect, CollectorError
from app.alerts import evaluate

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger=logging.getLogger('sysatlas')
@asynccontextmanager
async def lifespan(application):
    migrate()
    yield

app=FastAPI(title='SysAtlas Omega API', version='1.0.0', description='Linux observability and reliability control plane', lifespan=lifespan)

class RuleRequest(BaseModel):
    name: str = Field(min_length=1,max_length=80,pattern=r'^[A-Za-z0-9 _.-]+$')
    threshold: float = Field(ge=0,le=100)

@app.middleware('http')
async def correlation(request: Request, call_next):
    request_id=request.headers.get('X-Request-ID') or str(uuid.uuid4())
    response=await call_next(request)
    response.headers['X-Request-ID']=request_id
    logger.info('{"event":"http.request","request_id":"%s","method":"%s","path":"%s","status":%d}',request_id,request.method,request.url.path,response.status_code)
    return response

@app.exception_handler(Exception)
async def safe_error(request: Request, exc: Exception):
    logger.exception('unhandled application error')
    return JSONResponse(status_code=500,content={'error':{'code':'internal_error','message':'An internal error occurred.'}})

@app.get('/health/live', tags=['health'])
def liveness(): return {'status':'ok'}

@app.get('/health/ready', tags=['health'])
def readiness():
    try:
        from app.db import connection
        with connection() as conn: conn.execute('SELECT 1')
        return {'status':'ready','database':'ok'}
    except Exception:
        raise HTTPException(status_code=503,detail={'code':'database_unavailable','message':'Database is unavailable'})

@app.post('/api/v1/collect', tags=['collection'])
def collect_now():
    try: metrics=collect()
    except CollectorError as exc: raise HTTPException(status_code=503,detail={'code':'collector_failed','message':str(exc)})
    snapshot_id=save_snapshot(metrics)
    alert_changes=evaluate(metrics['memory']['total_kib'],metrics['memory']['available_kib'])
    return {'snapshot_id':snapshot_id,'metrics':metrics,'alert_changes':alert_changes}

@app.get('/api/v1/snapshots', tags=['metrics'])
def snapshots(limit: int=Query(default=20,ge=1,le=100)):
    return {'items':list_snapshots(min(limit,settings.max_page_size)),'limit':limit}

@app.get('/api/v1/snapshots/latest', tags=['metrics'])
def latest():
    row=latest_snapshot()
    if row is None: raise HTTPException(status_code=404,detail={'code':'no_snapshots','message':'No metrics have been collected yet'})
    return row

@app.post('/api/v1/alert-rules', status_code=201, tags=['alerts'])
def add_rule(body: RuleRequest):
    try: rule_id=create_rule(body.name,body.threshold)
    except Exception as exc:
        if 'UNIQUE constraint failed' in str(exc): raise HTTPException(status_code=409,detail={'code':'rule_exists','message':'A rule with this name already exists'})
        raise
    return {'id':rule_id,'name':body.name,'metric':'memory_used_percent','threshold':body.threshold,'enabled':True}

@app.get('/api/v1/alert-rules', tags=['alerts'])
def get_rules(): return {'items':rules()}

@app.get('/api/v1/incidents', tags=['alerts'])
def get_incidents(): return {'items':incidents()}

@app.get('/api/v1/diagnostics', tags=['operations'])
def diagnostics():
    row=latest_snapshot()
    return {'database':'configured','collector_binary':settings.collector_binary,'latest_snapshot_at':row['collected_at'] if row else None,
            'data_available':row is not None,'stale_after_seconds':settings.stale_after_seconds}
