#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    # Roda em uma porta interna, escutando apenas localmente
    uvicorn.run(app, host="127.0.0.1", port=5001)