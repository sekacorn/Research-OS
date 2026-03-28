from fastapi import FastAPI

from api_fastapi.routers import stats, literature

app = FastAPI(title="Research OS API")

app.include_router(stats.router)
app.include_router(literature.router)

@app.get("/")
def root():
    return {"status": "ok"}
