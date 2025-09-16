import json
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

def build_response(data=None, status=200, message=""):
    return {"data": data, "status": status, "message": message}

class WrapResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths=()):
        super().__init__(app)
        self.exclude_paths = set(exclude_paths)
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        resp = await call_next(request)
        ct = (resp.headers.get("content-type") or "").split(";")[0]
        
        if ct != "application/json":
            return resp
        
        raw = b"".join([c async for c in resp.body_iterator])
        try:
            payload = json.loads(raw) if raw else None
        except:
            payload = (raw or b"").decode()

        # Handle standard FastAPI error responses
        if isinstance(payload, dict) and "detail" in payload:
            out, code = build_response(None, resp.status_code, str(payload["detail"])), resp.status_code
        elif isinstance(payload, dict) and {"data","status","message"} <= payload.keys():
            out, code = payload, payload.get("status", resp.status_code)
        else:
            out, code = build_response(payload, resp.status_code), resp.status_code
        
        filtered_headers = {}
        for key, value in resp.headers.items():
            if key.lower().startswith('access-control-') or key.lower() in ['server','date','vary','x-']:
                filtered_headers[key] = value
        
        return JSONResponse(out, status_code=code, headers=filtered_headers)
