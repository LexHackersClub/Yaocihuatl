from fastapi import FastAPI


app = FastAPI(title="Yaocihuatl Backend", version="0.1.0")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "yaocihuatl-backend",
        "status": "running",
        "phase": "scaffolding",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
