import os
from fastapi import FastAPI, Request, Response
import httpx
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Config
REAL_PROM_REMOTE_WRITE = os.getenv("REAL_PROM_REMOTE_WRITE", "http://real-prometheus:9090/api/v1/write")
PROXY_PORT = int(os.getenv("PROXY_PORT", 8080))

app = FastAPI()

@app.post("/api/v1/write")
async def proxy_prometheus_remote_write(request: Request):
    body = await request.body()
    headers = dict(request.headers)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            REAL_PROM_REMOTE_WRITE,
            headers=headers,
            content=body
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers)
    )

if __name__ == "__main__":
    uvicorn.run("proxy_prometheus:app", host="0.0.0.0", port=PROXY_PORT, reload=False)
